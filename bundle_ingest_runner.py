#!/usr/bin/env python3
"""
StegVerse Bundle Ingest Runner (TVC-integrated)
================================================
All credential resolution goes through stegtvc_resolve_credential().
No direct env var reads for tokens.
TV/TVC is the authority gate before any credential is issued.

Phase 1: TVC reads STEGTVC_GITHUB_TOKEN from env.
Phase 2: TVC calls GitHub App API for ephemeral installation token.

Usage:
    python tools/bundle_ingest_runner.py \
        --policy data/headless-tasks/bundle-ingest-v1.json

    python tools/bundle_ingest_runner.py \
        --policy data/headless-tasks/bundle-ingest-v1.json \
        --apply
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# TVC resolver — all credentials flow through here
sys.path.insert(0, str(Path(__file__).parent.parent))
from stegtvc_client import resolve as stegtvc_resolve
try:
    from app.resolver import stegtvc_resolve_credential, stegtvc_emit_resolution_receipt
except ImportError:
    stegtvc_resolve_credential = None
    stegtvc_emit_resolution_receipt = None


MANIFEST_FILENAME = "ingestion-manifest.json"
RECEIPT_OUTPUT = "headless_cmd_reports/bundle-ingest-v1.receipt.json"
MARKDOWN_OUTPUT = "headless_cmd_reports/bundle-ingest-v1.report.md"
INCOMING_DIR = Path("incoming")
REVIEWED_DIR = Path("sandbox_reviewed")
FAILED_DIR = Path("failed_bundles")
INSTALLED_DIR = Path("installed_bundles")
TRUST_COLLAPSE_THRESHOLD = 0.10


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return "sha256:" + h.hexdigest()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# TVC credential resolution with receipt
# ---------------------------------------------------------------------------

def resolve_github_token(apply: bool) -> tuple[str, dict]:
    """
    Resolve GitHub token via TVC.
    Returns (token, resolution_receipt).
    In dry-run mode: returns empty token without calling TVC credential backend.
    """
    # Always resolve the config (validates the use_case is registered)
    try:
        resolved_config = stegtvc_resolve(
            use_case="github-push",
            module="bundle-ingest"
        )
    except Exception as e:
        return "", {
            "resolution": "FAIL_CLOSED",
            "basis": f"TVC config resolution failed: {e}"
        }

    if not apply:
        receipt = {
            "resolution": "DRY_RUN",
            "basis": "Dry run mode — no credential requested from TVC",
            "use_case": "github-push",
            "module": "bundle-ingest",
            "provider": resolved_config.get("provider"),
        }
        return "", receipt

    # Live mode — request credential from TVC
    if stegtvc_resolve_credential is None:
        return "", {
            "resolution": "FAIL_CLOSED",
            "basis": "stegtvc_resolve_credential not available; check app/resolver.py"
        }

    try:
        token = stegtvc_resolve_credential(
            use_case="github-push",
            module="bundle-ingest"
        )
        receipt = stegtvc_emit_resolution_receipt(
            use_case="github-push",
            module="bundle-ingest",
            resolved=resolved_config,
            credential_resolved=True,
            gcat_decision="ALLOW",
        ) if stegtvc_emit_resolution_receipt else {
            "resolution": "ALLOW",
            "basis": "TVC credential resolved"
        }
        return token, receipt

    except Exception as e:
        return "", {
            "resolution": "FAIL_CLOSED",
            "basis": f"TVC credential resolution failed: {e}. "
                     f"Phase 1: set STEGTVC_GITHUB_TOKEN. "
                     f"Phase 2: register GitHub App in stegtvc_config.json."
        }


# ---------------------------------------------------------------------------
# GCAT-BCAT gate
# ---------------------------------------------------------------------------

def gcat_bcat_gate(manifest: dict) -> tuple[str, str]:
    admissibility = manifest.get("admissibility", {})
    decision = admissibility.get("decision")
    if decision and decision != "PENDING":
        return decision, f"Pre-evaluated: {decision}"

    if not admissibility:
        return "FAIL_CLOSED", "No admissibility section"

    classification = manifest.get("classification", {})
    if classification.get("contains_secrets"):
        return "DENY", "Bundle declares contains_secrets=true"

    risk = _estimate_bundle_risk(manifest)
    if risk > 0.80:
        return "DENY", f"Bundle risk {risk:.2f} exceeds gate threshold"
    if risk > 0.60:
        return "FAIL_CLOSED", f"Bundle risk {risk:.2f} in uncertain range"

    return "ALLOW", "GCAT-BCAT gate passed"


def _estimate_bundle_risk(manifest: dict) -> float:
    risk = 0.0
    c = manifest.get("classification", {})
    if c.get("contains_executable_code"):
        risk += 0.30
    if c.get("contains_workflows"):
        risk += 0.40
    if c.get("risk_level") == "high":
        risk += 0.30
    elif c.get("risk_level") == "medium":
        risk += 0.15
    dest = manifest.get("destination", {})
    if dest.get("install_mode") in ("replace_files", "merge_files"):
        risk += 0.10
    if dest.get("allowed_to_overwrite"):
        risk += 0.10
    return min(risk, 1.0)


# ---------------------------------------------------------------------------
# Manifest validation
# ---------------------------------------------------------------------------

def validate_manifest(manifest: dict, bundle_path: Path,
                       extracted_dir: Path) -> tuple[bool, list[str]]:
    errors = []

    schema = manifest.get("schema", {})
    if schema.get("name") != "stegverse.ingestion.manifest":
        errors.append(f"Unknown schema: {schema.get('name')}")

    for section in ["bundle", "origin", "destination", "classification",
                    "admissibility", "files", "receipts", "custody",
                    "routing", "retention", "master_records", "outcome"]:
        if section not in manifest:
            errors.append(f"Missing section: {section}")

    for file_entry in manifest.get("files", []):
        path = file_entry.get("path", "")
        if path.startswith(".git/") or path.startswith(".github/workflows/"):
            errors.append(f"Forbidden path: {path}")

        expected_hash = file_entry.get("sha256", "")
        if not expected_hash:
            continue
        candidates = [extracted_dir / path, extracted_dir / path.lstrip(".")]
        found = next((c for c in candidates if c.exists()), None)
        if not found:
            if file_entry.get("required", False):
                errors.append(f"Required file missing: {path}")
            continue
        actual_hash = sha256_file(found)
        if actual_hash != expected_hash:
            errors.append(f"Hash mismatch: {path}")

    iosnoperiod = manifest.get("iosnoperiod", {})
    if iosnoperiod.get("required"):
        for mapping in iosnoperiod.get("mappings", []):
            ios_path = mapping.get("ios_safe_path", "")
            if ios_path and not (extracted_dir / ios_path).exists():
                errors.append(f"Missing iOS mirror: {ios_path}")

    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------

def install_files(manifest: dict, extracted_dir: Path,
                  token: str, dry_run: bool) -> tuple[bool, list[str]]:
    notes = []
    dest = manifest.get("destination", {})
    org = dest.get("org", "")
    repo = dest.get("repo", "")
    branch = dest.get("branch", "main")

    if dry_run or not token:
        mode = "DRY RUN" if dry_run else "NO TOKEN"
        notes.append(f"[{mode}] would install to {org}/{repo} branch={branch}")
        for f in manifest.get("files", []):
            notes.append(f"  {f.get('operation','copy')} → {f.get('path')}")
        return True, notes

    repo_url = f"https://x-access-token:{token}@github.com/{org}/{repo}.git"

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            subprocess.run(
                ["git", "clone", "--depth=1", "--branch", branch,
                 repo_url, tmpdir],
                check=True, capture_output=True, timeout=60
            )
            installed_count = 0
            for file_entry in manifest.get("files", []):
                src_path = file_entry.get("path", "")
                operation = file_entry.get("operation", "create_or_replace")
                src = extracted_dir / src_path
                if not src.exists():
                    src = extracted_dir / src_path.lstrip(".")
                if not src.exists():
                    notes.append(f"SKIP (not found): {src_path}")
                    continue
                dest_file = Path(tmpdir) / src_path
                if operation == "create_only" and dest_file.exists():
                    notes.append(f"SKIP (exists): {src_path}")
                    continue
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest_file)
                installed_count += 1
                notes.append(f"INSTALLED: {src_path}")

            if installed_count == 0:
                return False, notes + ["No files installed"]

            bundle_id = manifest.get("bundle", {}).get("bundle_id", "unknown")
            for cmd in [
                ["git", "-C", tmpdir, "config", "user.email",
                 "stegclaw@stegverse"],
                ["git", "-C", tmpdir, "config", "user.name", "StegClaw"],
                ["git", "-C", tmpdir, "add", "-A"],
                ["git", "-C", tmpdir, "commit", "-m",
                 f"ingest: {bundle_id} [{installed_count} files]"],
                ["git", "-C", tmpdir, "push", "origin", branch],
            ]:
                subprocess.run(cmd, check=True, capture_output=True,
                                timeout=60)

            notes.append(f"PUSHED: {installed_count} files to {org}/{repo}")
            return True, notes

        except subprocess.CalledProcessError as e:
            err = e.stderr.decode()[:200] if e.stderr else str(e)
            return False, notes + [f"Git error: {err}"]
        except Exception as e:
            return False, notes + [f"Install error: {str(e)}"]


# ---------------------------------------------------------------------------
# Receipt + report
# ---------------------------------------------------------------------------

def emit_receipt(bundle_path: Path, manifest: dict, decision: str,
                 basis: str, install_notes: list[str],
                 validation_errors: list[str],
                 tvc_receipt: dict,
                 prev_hash: str | None) -> dict:
    bundle_id = manifest.get("bundle", {}).get("bundle_id",
                                                bundle_path.stem)
    content = {
        "schema": "stegverse.ingest_receipt.v1",
        "receipt_id": (
            f"RCPT-INGEST-{bundle_id}-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        ),
        "bundle_id": bundle_id,
        "bundle_hash": (sha256_file(bundle_path)
                        if bundle_path.exists() else None),
        "decision": decision,
        "basis": basis,
        "validation_errors": validation_errors,
        "install_notes": install_notes,
        "tvc_resolution": tvc_receipt.get("resolution"),
        "tvc_receipt_hash": tvc_receipt.get("receipt_hash"),
        "destination": manifest.get("destination", {}),
        "task_identity_preserved": True,
        "sandbox_ephemeral": True,
        "cost_usd": 0.0,
        "prev_receipt_hash": prev_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    content["receipt_hash"] = sha256_str(
        json.dumps(content, sort_keys=True)
    )
    return content


def write_report(results: list[dict], dry_run: bool) -> str:
    mode = "DRY RUN" if dry_run else "APPLIED"
    lines = [
        f"# Bundle Ingest Report [{mode}]",
        f"",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"",
        "| Bundle | Decision | TVC | Notes |",
        "|---|---|---|---|",
    ]
    for r in results:
        bundle = r.get("bundle_id", "unknown")
        decision = r.get("decision", "UNKNOWN")
        tvc = r.get("tvc_resolution", "n/a")
        errors = "; ".join(r.get("validation_errors", [])[:1])
        lines.append(f"| {bundle} | {decision} | {tvc} | {errors or 'OK'} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(policy_path: Path, apply: bool) -> int:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    budget_ceiling = policy.get("budget_ceiling_usd", 1.00)

    print(f"=== Bundle Ingest Runner (TVC-integrated) ===")
    print(f"Mode: {'APPLY' if apply else 'DRY RUN'}")
    print(f"Budget ceiling: ${budget_ceiling:.2f}")
    print()

    # Resolve GitHub token via TVC before processing any bundles
    token, tvc_receipt = resolve_github_token(apply)
    tvc_resolution = tvc_receipt.get("resolution", "UNKNOWN")
    print(f"TVC resolution: {tvc_resolution}")
    if tvc_resolution == "FAIL_CLOSED" and apply:
        print(f"HALT: TVC credential resolution failed — {tvc_receipt.get('basis')}")
        print("Cannot apply without a valid token from TVC.")
        return 1

    bundles = (sorted(INCOMING_DIR.glob("*.zip"))
               if INCOMING_DIR.exists() else [])
    if not bundles:
        print("No bundles in incoming/")
        return 0

    print(f"Found {len(bundles)} bundle(s)")

    results = []
    prev_hash = None

    for bundle_path in bundles:
        print(f"\n--- {bundle_path.name} ---")

        with tempfile.TemporaryDirectory() as tmpdir:
            extracted_dir = Path(tmpdir)

            try:
                with zipfile.ZipFile(bundle_path) as zf:
                    zf.extractall(extracted_dir)
            except Exception as e:
                print(f"  FAIL_CLOSED: extraction failed: {e}")
                r = emit_receipt(bundle_path, {}, "FAIL_CLOSED",
                                 str(e), [], [str(e)], tvc_receipt, prev_hash)
                results.append(r)
                prev_hash = r["receipt_hash"]
                _move_bundle(bundle_path, FAILED_DIR)
                continue

            manifest_candidates = list(
                extracted_dir.rglob(MANIFEST_FILENAME)
            )
            if not manifest_candidates:
                print(f"  FAIL_CLOSED: no {MANIFEST_FILENAME}")
                r = emit_receipt(bundle_path, {}, "FAIL_CLOSED",
                                 "No manifest found", [], ["missing manifest"],
                                 tvc_receipt, prev_hash)
                results.append(r)
                prev_hash = r["receipt_hash"]
                _move_bundle(bundle_path, FAILED_DIR)
                continue

            manifest_path = manifest_candidates[0]
            extracted_dir = manifest_path.parent
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            bundle_id = manifest.get("bundle", {}).get(
                "bundle_id", bundle_path.stem
            )
            print(f"  Bundle ID: {bundle_id}")

            valid, errors = validate_manifest(
                manifest, bundle_path, extracted_dir
            )
            if not valid:
                print(f"  FAIL_CLOSED: {len(errors)} validation error(s)")
                decision, basis = "FAIL_CLOSED", f"Validation: {errors[0]}"
                install_notes = []
            else:
                decision, basis = gcat_bcat_gate(manifest)
                print(f"  GCAT-BCAT: {decision}")
                install_notes = []
                if decision == "ALLOW":
                    success, install_notes = install_files(
                        manifest, extracted_dir, token, dry_run=not apply
                    )
                    if not success:
                        decision = "FAIL_CLOSED"
                        basis = install_notes[-1] if install_notes else "install failed"

            r = emit_receipt(bundle_path, manifest, decision, basis,
                             install_notes, errors, tvc_receipt, prev_hash)
            results.append(r)
            prev_hash = r["receipt_hash"]
            print(f"  Decision: {decision}")

            target = (INSTALLED_DIR if decision == "ALLOW"
                      else FAILED_DIR if decision in ("FAIL_CLOSED", "DENY")
                      else REVIEWED_DIR)
            _move_bundle(bundle_path, target)

    Path(RECEIPT_OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    Path(RECEIPT_OUTPUT).write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    Path(MARKDOWN_OUTPUT).write_text(
        write_report(results, dry_run=not apply), encoding="utf-8"
    )

    allow_count = sum(1 for r in results if r.get("decision") == "ALLOW")
    fail_count = len(results) - allow_count
    print(f"\n=== {allow_count} ALLOW, {fail_count} non-ALLOW ===")
    print(f"Receipt: {RECEIPT_OUTPUT}")

    return 0 if fail_count == 0 else 1


def _move_bundle(bundle_path: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / bundle_path.name
    if not dest.exists():
        shutil.move(str(bundle_path), str(dest))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return run(Path(args.policy), args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
