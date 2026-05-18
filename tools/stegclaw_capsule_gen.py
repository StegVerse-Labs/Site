#!/usr/bin/env python3
"""
StegClaw On-Demand Capsule Generator
======================================
Scans incoming/ for .zip bundles that lack companion files.
For each unmatched bundle, generates:
  - <bundle-id>.capsule.json
  - <bundle-id>.authority-token.json
  - <bundle-id>.verified-receipt.json

Written to incoming/ alongside the bundle.
Idempotent: skips bundles that already have all three files.

This enables the one-file drop flow:
  User drops bundle.zip → incoming/
  This task runs → three companion files generated
  bundle_ingest.py runs → ALLOW → installed
  StegEntity runtime → capsule + token + receipt → governed execution

Usage:
    python tools/stegclaw_capsule_gen.py \
        --policy data/headless-tasks/stegclaw-capsule-gen-v1.json

    python tools/stegclaw_capsule_gen.py \
        --policy data/headless-tasks/stegclaw-capsule-gen-v1.json \
        --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


RECEIPT_OUTPUT = "headless_cmd_reports/stegclaw-capsule-gen-v1.receipt.json"
MARKDOWN_OUTPUT = "headless_cmd_reports/stegclaw-capsule-gen-v1.report.md"
INCOMING_DIR = Path("incoming")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def expires_utc(hours: int = 1) -> str:
    dt = datetime.now(timezone.utc) + timedelta(hours=hours)
    return dt.replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Bundle introspection
# ---------------------------------------------------------------------------

def read_bundle_manifest(bundle_path: Path) -> dict:
    """Read bundle-manifest.json or ingestion-manifest.json from zip."""
    try:
        with zipfile.ZipFile(bundle_path) as zf:
            for name in ["bundle-manifest.json", "ingestion-manifest.json"]:
                if name in zf.namelist():
                    return json.loads(zf.read(name))
    except Exception:
        pass
    return {}


def infer_bundle_metadata(bundle_path: Path, manifest: dict) -> dict:
    """
    Infer transition metadata from bundle manifest.
    Falls back to filename-based inference if manifest is minimal.
    """
    stem = bundle_path.stem  # e.g. ae-stage5-gcat-bcat-formal-v1

    # From manifest
    bundle_id = manifest.get("bundle_id", stem)
    bundle_type = manifest.get("bundle_type", "")

    # Infer transition from bundle type or name
    transition_id = "T-120"
    transition_name = "File Creation"
    transition_family = "Installation"

    if bundle_type in ("engine-bootstrap", "core-lite-bootstrap"):
        transition_id = "T-126"
        transition_name = "Core-Lite Bootstrap Installation"
    elif bundle_type == "tvc-integration":
        transition_id = "T-124"
        transition_name = "TVC Integration Install"
    elif bundle_type == "stegentity-integration":
        transition_id = "T-125"
        transition_name = "StegEntity Integration Install"
    elif bundle_type in ("formalism-proof-stage", "papers"):
        transition_id = "T-120"
        transition_name = "File Creation"
    elif "bootstrap" in stem.lower():
        transition_id = "T-126"
        transition_name = "Core-Lite Bootstrap Installation"

    # Infer consequence mass from risk level
    risk = manifest.get("classification", {}).get("risk_level", "low")
    consequence_mass = {"low": 0.20, "medium": 0.45, "high": 0.75}.get(risk, 0.20)
    recoverability = {"low": 0.90, "medium": 0.75, "high": 0.55}.get(risk, 0.90)

    return {
        "bundle_id": bundle_id,
        "transition_id": transition_id,
        "transition_name": transition_name,
        "transition_family": transition_family,
        "consequence_mass": consequence_mass,
        "recoverability_score": recoverability,
        "target": "StegVerse-Labs/Site",
    }


def build_operations(bundle_path: Path, manifest: dict) -> list[dict]:
    """Build operations list from manifest files or zip contents."""
    # Try manifest files list first
    files = manifest.get("files", [])
    if files:
        return [
            {
                "op": f.get("operation", "create_or_replace"),
                "path": f.get("path", ""),
                "sha256": f.get("sha256", ""),
                "size_bytes": f.get("size_bytes", 0),
                "role": f.get("role", "data"),
            }
            for f in files
            if f.get("path") not in ("README.md", "iosnoperiod.md", "")
        ]

    # Fall back to zip contents
    ops = []
    try:
        with zipfile.ZipFile(bundle_path) as zf:
            for name in sorted(zf.namelist()):
                if name.endswith("/"):
                    continue
                if name in ("README.md", "iosnoperiod.md",
                            "bundle-manifest.json", "ingestion-manifest.json"):
                    continue
                data = zf.read(name)
                ops.append({
                    "op": "create_or_replace",
                    "path": name,
                    "sha256": sha256_bytes(data),
                    "size_bytes": len(data),
                    "role": "data",
                })
    except Exception as e:
        ops = [{"op": "error", "path": "?", "error": str(e)}]

    return ops


# ---------------------------------------------------------------------------
# Capsule generation
# ---------------------------------------------------------------------------

def generate_capsule(bundle_path: Path, meta: dict,
                     operations: list[dict], bundle_hash: str) -> dict:
    capsule_id = (
        f"CAPSULE-{meta['bundle_id']}-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    )
    capsule = {
        "schema": "stegverse.maintenance_capsule.v1",
        "capsule_id": capsule_id,
        "created_at": now_utc(),
        "target": meta["target"],
        "transition": {
            "transition_id": meta["transition_id"],
            "transition_name": meta["transition_name"],
            "transition_family": meta["transition_family"],
            "actor": "stegclaw",
            "bundle_id": meta["bundle_id"],
            "bundle_path": str(bundle_path),
            "bundle_hash": bundle_hash,
        },
        "admissibility": {
            "decision": "PENDING",
            "basis": "Pending StegEntity admissibility evaluation",
            "gcat_bcat_required": True,
            "boundary_coherence_required": True,
            "data_continuity_required": True,
            "failure_behavior": "fail-closed",
        },
        "operations": operations,
        "dependencies": {
            "adapter": "zip_bundle",
            "adapter_version": "v0",
            "requires_bundle": str(bundle_path),
            "requires_token": "STEGTVC_GITHUB_TOKEN",
            "requires_receipt": True,
        },
        "consequences": {
            "scope": "file_installation",
            "reversible": True,
            "rollback_window_hours": 24,
            "downstream_effects": [
                "target repo files updated",
                "bundle fingerprint index updated",
                "latest-bundle-ingestion-receipt updated",
            ],
            "consequence_mass": meta["consequence_mass"],
            "recoverability_score": meta["recoverability_score"],
        },
        "rollback_plan": {
            "strategy": "git_revert",
            "steps": [
                "identify commit hash from execution receipt",
                "git revert --no-commit <commit>",
                "verify pre-state hashes restored",
                "emit rollback receipt",
            ],
            "rollback_receipt_required": True,
        },
        "verification": {
            "checks": [
                {"name": "bundle_hash_matches", "required": True},
                {"name": "all_files_present_post_install", "required": True},
                {"name": "no_forbidden_paths", "required": True},
                {"name": "receipt_emitted", "required": True},
                {"name": "outcome_report_written", "required": True},
            ],
            "state_reconstructable": True,
        },
    }
    capsule["capsule_hash"] = sha256_str(json.dumps(capsule, sort_keys=True))
    return capsule


def generate_verified_receipt(bundle_hash: str) -> dict:
    receipt_id = (
        f"RCPT-SE-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    )
    payload = {
        "receipt_id": receipt_id,
        "actor_class": "stegclaw",
        "scopes": ["file:write", "receipt:emit", "bundle:install"],
        "issued_at": now_utc(),
        "expires_at": expires_utc(hours=24),
        "assurance_level": "v0_structural",
        "issuer": "stegclaw.v0",
        "kid": "stegclaw.v0:key1",
        "payload_hash": bundle_hash,
        "_phase": "v0_structural_no_crypto",
        "_note": (
            "Phase 1: structural integrity only. "
            "Phase 2: replace with StegID-signed receipt."
        ),
    }
    payload["sig"] = sha256_str(json.dumps(payload, sort_keys=True))
    return payload


def generate_authority_token(capsule_hash: str, receipt_hash: str,
                             target: str) -> dict:
    token_id = (
        f"TVC-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    )
    return {
        "token_id": token_id,
        "status": "active",
        "adapter": "zip_bundle",
        "target": target,
        "scopes": ["file:write", "receipt:emit", "bundle:install"],
        "issued_at": now_utc(),
        "expires_at": expires_utc(hours=1),
        "capsule_hash": capsule_hash,
        "receipt_hash": receipt_hash,
        "credential_source": "STEGTVC_GITHUB_TOKEN",
        "_phase": "v0_structural",
        "_note": (
            "Phase 1: credential from env var. "
            "Phase 2: TV/TVC issues ephemeral GitHub App token."
        ),
    }


# ---------------------------------------------------------------------------
# Main scan + generate loop
# ---------------------------------------------------------------------------

def run(dry_run: bool = False) -> int:
    print(f"=== StegClaw On-Demand Capsule Generator ===")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    print(f"Scanning: {INCOMING_DIR}/")
    print()

    if not INCOMING_DIR.exists():
        print("incoming/ not found — nothing to do.")
        return 0

    bundles = sorted(INCOMING_DIR.glob("*.zip"))
    if not bundles:
        print("No .zip bundles found in incoming/")
        return 0

    results = []
    generated_count = 0
    skipped_count = 0

    for bundle_path in bundles:
        stem = bundle_path.stem.replace(".sandbox-candidate", "")
        capsule_path = bundle_path.parent / f"{stem}.capsule.json"
        receipt_path = bundle_path.parent / f"{stem}.verified-receipt.json"
        token_path   = bundle_path.parent / f"{stem}.authority-token.json"

        # Idempotency check — skip if all three already exist
        if capsule_path.exists() and receipt_path.exists() and token_path.exists():
            print(f"SKIP (already capsulated): {bundle_path.name}")
            skipped_count += 1
            results.append({
                "bundle": bundle_path.name,
                "action": "skipped",
                "reason": "capsule files already present"
            })
            continue

        print(f"Generating: {bundle_path.name}")

        bundle_hash = sha256_file(bundle_path)
        manifest = read_bundle_manifest(bundle_path)
        meta = infer_bundle_metadata(bundle_path, manifest)
        operations = build_operations(bundle_path, manifest)

        print(f"  bundle_id:   {meta['bundle_id']}")
        print(f"  transition:  {meta['transition_id']} — {meta['transition_name']}")
        print(f"  operations:  {len(operations)}")

        capsule = generate_capsule(bundle_path, meta, operations, bundle_hash)
        receipt = generate_verified_receipt(bundle_hash)
        receipt_hash = sha256_str(json.dumps(receipt, sort_keys=True))
        token = generate_authority_token(
            capsule["capsule_hash"], receipt_hash, meta["target"]
        )

        if not dry_run:
            capsule_path.write_text(json.dumps(capsule, indent=2),
                                    encoding="utf-8")
            receipt_path.write_text(json.dumps(receipt, indent=2),
                                    encoding="utf-8")
            token_path.write_text(json.dumps(token, indent=2),
                                  encoding="utf-8")
            print(f"  Written: {capsule_path.name}")
            print(f"  Written: {receipt_path.name}")
            print(f"  Written: {token_path.name}")
        else:
            print(f"  [DRY RUN] would write: {capsule_path.name}")
            print(f"  [DRY RUN] would write: {receipt_path.name}")
            print(f"  [DRY RUN] would write: {token_path.name}")

        generated_count += 1
        results.append({
            "bundle": bundle_path.name,
            "action": "generated" if not dry_run else "would_generate",
            "bundle_id": meta["bundle_id"],
            "transition_id": meta["transition_id"],
            "capsule_id": capsule["capsule_id"],
            "ops": len(operations),
        })
        print()

    # Write receipt
    receipt_obj = {
        "schema": "stegverse.ingest_receipt.v1",
        "receipt_id": (
            f"RCPT-CAPSULE-GEN-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        ),
        "task_id": "stegclaw-capsule-gen-v1",
        "decision": "ALLOW",
        "mode": "dry_run" if dry_run else "apply",
        "bundles_seen": len(bundles),
        "generated": generated_count,
        "skipped": skipped_count,
        "results": results,
        "cost_usd": 0.0,
        "timestamp": now_utc(),
    }
    receipt_obj["receipt_hash"] = sha256_str(
        json.dumps(receipt_obj, sort_keys=True)
    )

    Path(RECEIPT_OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    Path(RECEIPT_OUTPUT).write_text(
        json.dumps(receipt_obj, indent=2), encoding="utf-8"
    )

    # Write markdown report
    lines = [
        "# StegClaw Capsule Generator Report",
        "",
        f"Generated: `{now_utc()}`",
        f"Mode: `{'dry_run' if dry_run else 'apply'}`",
        f"Bundles seen: `{len(bundles)}`",
        f"Generated: `{generated_count}`",
        f"Skipped: `{skipped_count}`",
        "",
        "## Results",
        "",
    ]
    for r in results:
        status = r["action"].upper()
        name = r["bundle"]
        detail = (
            f"{r.get('transition_id','?')} — {r.get('ops','?')} ops"
            if r["action"] != "skipped" else r["reason"]
        )
        lines.append(f"- `{status}` `{name}` — {detail}")

    Path(MARKDOWN_OUTPUT).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"=== Done: {generated_count} generated, {skipped_count} skipped ===")
    print(f"Receipt: {RECEIPT_OUTPUT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="On-demand capsule generator for incoming/ bundles"
    )
    parser.add_argument("--policy", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
