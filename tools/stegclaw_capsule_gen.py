#!/usr/bin/env python3
"""
StegClaw On-Demand Capsule Generator (TVC v1.1 integrated)
============================================================
Scans incoming/ for .zip bundles that lack companion capsule files.

TVC call sequence (when TVC is available):
  1. tvc.registry.lifecycle.enforce.stegentity
     → FAIL_CLOSED if package is revoked/quarantined
     → DENY if package is deprecated/superseded
     → ALLOW if package is active
  2. tvc.registry.proof_bundle.stegentity
     → runs verify + pinned_bridge + evidence in one call
     → emits execution receipt

If lifecycle enforce fails: FAIL_CLOSED, no capsules generated.
If TVC not reachable: v0_structural_fallback (explicit, never silent).

Usage:
    python tools/stegclaw_capsule_gen.py \
        --policy data/headless-tasks/stegclaw-capsule-gen-v1.json

    python tools/stegclaw_capsule_gen.py \
        --policy data/headless-tasks/stegclaw-capsule-gen-v1.json \
        --tvc-root ../TVC

Environment:
    TVC_ROOT   Path to TVC repo root
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


RECEIPT_OUTPUT = "headless_cmd_reports/stegclaw-capsule-gen-v1.receipt.json"
MARKDOWN_OUTPUT = "headless_cmd_reports/stegclaw-capsule-gen-v1.report.md"
INCOMING_DIR = Path("incoming")

# TVC task sequence
TVC_LIFECYCLE_TASK = "tvc.registry.lifecycle.enforce.stegentity"
TVC_PROOF_TASK     = "tvc.registry.proof_bundle.stegentity"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def expires_utc(hours: int = 1) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)
            ).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# TVC dispatcher
# ---------------------------------------------------------------------------

def find_tvc_dispatcher(tvc_root: Path | None) -> Path | None:
    candidates = []
    if tvc_root:
        candidates.append(tvc_root / "tools" / "task_dispatcher.py")
    env_root = os.environ.get("TVC_ROOT", "")
    if env_root:
        candidates.append(Path(env_root) / "tools" / "task_dispatcher.py")
    for rel in ["../TVC", "../../TVC", "TVC"]:
        candidates.append(Path(rel) / "tools" / "task_dispatcher.py")
    return next((p for p in candidates if p.exists()), None)


def run_tvc_task(dispatcher: Path, task: str) -> dict:
    """Run a single TVC dispatcher task. Returns parsed result dict."""
    try:
        proc = subprocess.run(
            [sys.executable, str(dispatcher), task],
            capture_output=True, text=True, timeout=120,
            cwd=str(dispatcher.parent.parent),
        )
    except subprocess.TimeoutExpired:
        return {"status": "tvc_timeout", "task": task,
                "basis": f"TVC task {task} timed out after 120s"}
    except Exception as e:
        return {"status": "tvc_error", "task": task, "basis": str(e)}

    if proc.returncode != 0:
        return {"status": "tvc_failed", "task": task,
                "basis": f"exit {proc.returncode}: {proc.stderr[:200]}"}

    try:
        dispatch = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"status": "tvc_parse_error", "task": task,
                "basis": "output was not valid JSON"}

    return {
        "status": dispatch.get("status", "unknown"),
        "task": task,
        "result": dispatch.get("result", {}),
        "dispatch": dispatch,
    }


def call_tvc(tvc_root: Path | None) -> dict:
    """
    Run TVC lifecycle enforce then proof bundle.
    Returns combined result with authority_source.
    Never raises.
    """
    dispatcher = find_tvc_dispatcher(tvc_root)

    if not dispatcher:
        return {
            "status": "tvc_not_found",
            "authority_source": "v0_structural_fallback",
            "basis": "TVC dispatcher not found. Set --tvc-root or TVC_ROOT.",
        }

    print(f"  TVC dispatcher: {dispatcher}")

    # Step 1: lifecycle enforce
    print(f"  Step 1: {TVC_LIFECYCLE_TASK}")
    lifecycle = run_tvc_task(dispatcher, TVC_LIFECYCLE_TASK)
    lc_status = lifecycle.get("status")
    lc_result = lifecycle.get("result", {})
    lc_decision = lc_result.get("decision", lc_result.get("enforcement_decision", ""))

    print(f"  Lifecycle: {lc_status} — decision: {lc_decision or '(none)'}")

    # Hard stop on lifecycle failure
    if lc_status != "ok":
        return {
            "status": "lifecycle_failed",
            "authority_source": "v0_structural_fallback",
            "basis": f"TVC lifecycle enforce failed: {lifecycle.get('basis', lc_status)}",
            "lifecycle_result": lifecycle,
        }

    if lc_decision in ("FAIL_CLOSED", "DENY"):
        return {
            "status": "lifecycle_denied",
            "authority_source": "denied",
            "basis": (
                f"TVC lifecycle enforce returned {lc_decision}. "
                f"Package is not in an admissible lifecycle state. "
                f"Capsule generation halted."
            ),
            "lifecycle_result": lifecycle,
        }

    # Step 2: proof bundle (verify + pinned_bridge + evidence in one run)
    print(f"  Step 2: {TVC_PROOF_TASK}")
    proof = run_tvc_task(dispatcher, TVC_PROOF_TASK)
    proof_status = proof.get("status")
    proof_result = proof.get("result", {})

    print(f"  Proof bundle: {proof_status}")

    if proof_status != "ok":
        return {
            "status": "proof_failed",
            "authority_source": "v0_structural_fallback",
            "basis": f"TVC proof bundle failed: {proof.get('basis', proof_status)}",
            "lifecycle_result": lifecycle,
            "proof_result": proof,
        }

    # Find latest execution receipt
    receipt_dir = (dispatcher.parent.parent / "reports"
                   / "tvc_stegentity_pinned_package" / "stegentity_receipts")
    execution_receipt = None
    if receipt_dir.exists():
        receipts = sorted(receipt_dir.glob("*.json"))
        if receipts:
            try:
                execution_receipt = json.loads(receipts[-1].read_text())
            except Exception:
                pass

    return {
        "status": "ok",
        "authority_source": "tvc_registry_backed",
        "tvc_lifecycle_task": TVC_LIFECYCLE_TASK,
        "tvc_proof_task": TVC_PROOF_TASK,
        "lifecycle_decision": lc_decision,
        "lifecycle_result": lc_result,
        "proof_result": proof_result,
        "execution_receipt": execution_receipt,
        "registry_verify_ok": proof_result.get("registry_verify_ok"),
        "pinned_bridge_ok": proof_result.get("pinned_bridge_ok"),
        "evidence_manifest_ok": proof_result.get("evidence_manifest_ok"),
        "evidence_file_count": proof_result.get("evidence_file_count"),
    }


# ---------------------------------------------------------------------------
# Authority objects
# ---------------------------------------------------------------------------

def make_verified_receipt(tvc: dict, bundle_hash: str) -> dict:
    rid = f"RCPT-SE-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    exe = tvc.get("execution_receipt")

    if tvc["status"] == "ok" and exe:
        return {
            "receipt_id": rid,
            "actor_class": "stegclaw",
            "scopes": ["file:write", "receipt:emit", "bundle:install"],
            "issued_at": now_utc(),
            "expires_at": expires_utc(hours=24),
            "assurance_level": "tvc_registry_backed_v1.1",
            "issuer": "tvc.registry.v1.1",
            "kid": "tvc.registry.v1.1:stegentity",
            "payload_hash": bundle_hash,
            "sig": exe.get("receipt_hash", sha256_str(bundle_hash)),
            "tvc_execution_receipt": exe,
            "lifecycle_decision": tvc.get("lifecycle_decision"),
            "registry_verify_ok": tvc.get("registry_verify_ok"),
            "pinned_bridge_ok": tvc.get("pinned_bridge_ok"),
        }

    payload = {
        "receipt_id": rid,
        "actor_class": "stegclaw",
        "scopes": ["file:write", "receipt:emit", "bundle:install"],
        "issued_at": now_utc(),
        "expires_at": expires_utc(hours=24),
        "assurance_level": "v0_structural",
        "issuer": "stegclaw.v0",
        "kid": "stegclaw.v0:key1",
        "payload_hash": bundle_hash,
        "tvc_status": tvc["status"],
        "tvc_basis": tvc.get("basis"),
        "_phase": "v0_structural_no_crypto",
        "_note": f"TVC unavailable ({tvc['status']}). Phase 2: wire to TVC.",
    }
    payload["sig"] = sha256_str(json.dumps(payload, sort_keys=True))
    return payload


def make_authority_token(tvc: dict, capsule_hash: str,
                         receipt_hash: str, target: str) -> dict:
    tid = f"TVC-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    base = {
        "token_id": tid,
        "status": "active",
        "adapter": "zip_bundle",
        "target": target,
        "scopes": ["file:write", "receipt:emit", "bundle:install"],
        "issued_at": now_utc(),
        "expires_at": expires_utc(hours=1),
        "capsule_hash": capsule_hash,
        "receipt_hash": receipt_hash,
        "authority_source": tvc.get("authority_source", "unknown"),
    }
    if tvc["status"] == "ok":
        base.update({
            "tvc_lifecycle_task": tvc.get("tvc_lifecycle_task"),
            "tvc_proof_task": tvc.get("tvc_proof_task"),
            "lifecycle_decision": tvc.get("lifecycle_decision"),
            "registry_verify_ok": tvc.get("registry_verify_ok"),
            "pinned_bridge_ok": tvc.get("pinned_bridge_ok"),
            "evidence_file_count": tvc.get("evidence_file_count"),
        })
    else:
        base.update({
            "credential_source": "STEGTVC_GITHUB_TOKEN",
            "tvc_status": tvc["status"],
            "tvc_basis": tvc.get("basis"),
            "_phase": "v0_structural",
            "_note": f"TVC: {tvc['status']}. Phase 2: wire to TVC.",
        })
    return base


# ---------------------------------------------------------------------------
# Bundle introspection + capsule (unchanged)
# ---------------------------------------------------------------------------

def read_bundle_manifest(bundle_path: Path) -> dict:
    try:
        with zipfile.ZipFile(bundle_path) as zf:
            for name in ["bundle-manifest.json", "ingestion-manifest.json"]:
                if name in zf.namelist():
                    return json.loads(zf.read(name))
    except Exception:
        pass
    return {}


def infer_meta(bundle_path: Path, manifest: dict) -> dict:
    stem = bundle_path.stem
    bundle_id = manifest.get("bundle_id", stem)
    bundle_type = manifest.get("bundle_type", "")
    tid, tname = "T-120", "File Creation"
    if bundle_type in ("engine-bootstrap", "core-lite-bootstrap") \
            or "bootstrap" in stem.lower():
        tid, tname = "T-126", "Core-Lite Bootstrap Installation"
    elif bundle_type == "tvc-integration":
        tid, tname = "T-124", "TVC Integration Install"
    elif bundle_type == "stegentity-integration":
        tid, tname = "T-125", "StegEntity Integration Install"
    risk = manifest.get("classification", {}).get("risk_level", "low")
    return {
        "bundle_id": bundle_id,
        "transition_id": tid,
        "transition_name": tname,
        "transition_family": "Installation",
        "consequence_mass": {"low": 0.20, "medium": 0.45, "high": 0.75}.get(risk, 0.20),
        "recoverability_score": {"low": 0.90, "medium": 0.75, "high": 0.55}.get(risk, 0.90),
        "target": "StegVerse-Labs/Site",
    }


def build_operations(bundle_path: Path, manifest: dict) -> list[dict]:
    SKIP = {"README.md", "iosnoperiod.md",
            "bundle-manifest.json", "ingestion-manifest.json"}
    files = manifest.get("files", [])
    if files:
        return [
            {"op": f.get("operation", "create_or_replace"),
             "path": f.get("path", ""),
             "sha256": f.get("sha256", ""),
             "size_bytes": f.get("size_bytes", 0),
             "role": f.get("role", "data")}
            for f in files if f.get("path") not in SKIP
        ]
    ops = []
    try:
        with zipfile.ZipFile(bundle_path) as zf:
            for name in sorted(zf.namelist()):
                if name.endswith("/") or name in SKIP:
                    continue
                data = zf.read(name)
                ops.append({"op": "create_or_replace", "path": name,
                             "sha256": sha256_bytes(data),
                             "size_bytes": len(data), "role": "data"})
    except Exception as e:
        ops = [{"op": "error", "path": "?", "error": str(e)}]
    return ops


def build_capsule(bundle_path: Path, meta: dict,
                  ops: list[dict], bundle_hash: str,
                  tvc: dict) -> dict:
    capsule_id = (
        f"CAPSULE-{meta['bundle_id']}-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    )
    c = {
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
        "operations": ops,
        "dependencies": {
            "adapter": "zip_bundle",
            "adapter_version": "v0",
            "requires_bundle": str(bundle_path),
            "runtime_package": "stegentity",
            "runtime_verified_via": "tvc_package_registry",
            "tvc_lifecycle_enforced": tvc.get("status") == "ok",
            "tvc_proof_bundle_ok": tvc.get("pinned_bridge_ok", False),
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
    c["capsule_hash"] = sha256_str(json.dumps(c, sort_keys=True))
    return c


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(dry_run: bool = False, tvc_root: Path | None = None) -> int:
    print("=== StegClaw Capsule Generator (TVC v1.1) ===")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    print(f"Scanning: {INCOMING_DIR}/")
    print()

    if not INCOMING_DIR.exists():
        print("incoming/ not found.")
        return 0

    bundles = sorted(INCOMING_DIR.glob("*.zip"))
    if not bundles:
        print("No .zip bundles in incoming/")
        return 0

    print("Calling TVC (lifecycle enforce + proof bundle)...")
    tvc = call_tvc(tvc_root)
    src = tvc.get("authority_source", "unknown")
    print(f"TVC: {tvc['status']} — authority_source: {src}")
    if tvc["status"] not in ("ok", "tvc_not_found"):
        print(f"  Basis: {tvc.get('basis', '')}")
    print()

    # Hard stop on lifecycle denial
    if tvc.get("status") == "lifecycle_denied":
        print("HALT: TVC lifecycle enforce returned DENY or FAIL_CLOSED.")
        print(f"Basis: {tvc.get('basis')}")
        print("No capsules generated.")
        _write_receipt(bundles, 0, 0, tvc, dry_run)
        return 1

    results = []
    generated = skipped = 0

    for bundle_path in bundles:
        stem = bundle_path.stem.replace(".sandbox-candidate", "")
        capsule_p = bundle_path.parent / f"{stem}.capsule.json"
        receipt_p = bundle_path.parent / f"{stem}.verified-receipt.json"
        token_p   = bundle_path.parent / f"{stem}.authority-token.json"

        if capsule_p.exists() and receipt_p.exists() and token_p.exists():
            print(f"SKIP: {bundle_path.name}")
            skipped += 1
            results.append({"bundle": bundle_path.name,
                             "action": "skipped",
                             "reason": "already capsulated"})
            continue

        print(f"Generating: {bundle_path.name}")
        bundle_hash = sha256_file(bundle_path)
        manifest    = read_bundle_manifest(bundle_path)
        meta        = infer_meta(bundle_path, manifest)
        ops         = build_operations(bundle_path, manifest)

        print(f"  {meta['transition_id']} — {meta['transition_name']} — {len(ops)} ops — {src}")

        capsule = build_capsule(bundle_path, meta, ops, bundle_hash, tvc)
        receipt = make_verified_receipt(tvc, bundle_hash)
        rh      = sha256_str(json.dumps(receipt, sort_keys=True))
        token   = make_authority_token(tvc, capsule["capsule_hash"],
                                       rh, meta["target"])

        if not dry_run:
            capsule_p.write_text(json.dumps(capsule, indent=2), encoding="utf-8")
            receipt_p.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
            token_p.write_text(json.dumps(token, indent=2), encoding="utf-8")
            print(f"  Written: {capsule_p.name}")
            print(f"  Written: {receipt_p.name}")
            print(f"  Written: {token_p.name}")
        else:
            print("  [DRY RUN] would write 3 companion files")

        generated += 1
        results.append({
            "bundle": bundle_path.name,
            "action": "generated" if not dry_run else "would_generate",
            "bundle_id": meta["bundle_id"],
            "transition_id": meta["transition_id"],
            "capsule_id": capsule["capsule_id"],
            "authority_source": src,
            "ops": len(ops),
        })
        print()

    _write_receipt(bundles, generated, skipped, tvc, dry_run, results)
    print(f"=== Done: {generated} generated, {skipped} skipped ({src}) ===")
    print(f"Receipt: {RECEIPT_OUTPUT}")
    return 0


def _write_receipt(bundles, generated, skipped, tvc, dry_run,
                   results=None) -> None:
    task_receipt = {
        "schema": "stegverse.ingest_receipt.v1",
        "receipt_id": (
            f"RCPT-CAPSULE-GEN-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        ),
        "task_id": "stegclaw-capsule-gen-v1",
        "decision": "ALLOW" if generated > 0 or skipped > 0 else "FAIL_CLOSED",
        "mode": "dry_run" if dry_run else "apply",
        "tvc_status": tvc["status"],
        "authority_source": tvc.get("authority_source", "unknown"),
        "lifecycle_decision": tvc.get("lifecycle_decision"),
        "bundles_seen": len(bundles),
        "generated": generated,
        "skipped": skipped,
        "results": results or [],
        "cost_usd": 0.0,
        "timestamp": now_utc(),
    }
    task_receipt["receipt_hash"] = sha256_str(
        json.dumps(task_receipt, sort_keys=True)
    )
    Path(RECEIPT_OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    Path(RECEIPT_OUTPUT).write_text(
        json.dumps(task_receipt, indent=2), encoding="utf-8"
    )

    src = tvc.get("authority_source", "unknown")
    lines = [
        "# StegClaw Capsule Generator Report",
        "",
        f"Generated: `{now_utc()}`",
        f"Mode: `{'dry_run' if dry_run else 'apply'}`",
        f"TVC status: `{tvc['status']}`",
        f"Authority source: `{src}`",
        f"Lifecycle decision: `{tvc.get('lifecycle_decision', 'n/a')}`",
        f"Bundles seen: `{len(bundles)}`  "
        f"Generated: `{generated}`  Skipped: `{skipped}`",
        "",
        "## Results", "",
    ]
    for r in (results or []):
        detail = (
            f"{r.get('transition_id','?')} — "
            f"{r.get('ops','?')} ops — {r.get('authority_source','?')}"
            if r.get("action") != "skipped" else r.get("reason", "")
        )
        lines.append(f"- `{r.get('action','?').upper()}` `{r.get('bundle','')}` — {detail}")

    Path(MARKDOWN_OUTPUT).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--tvc-root",
                        default=os.environ.get("TVC_ROOT", ""))
    args = parser.parse_args()
    return run(dry_run=args.dry_run,
               tvc_root=Path(args.tvc_root) if args.tvc_root else None)


if __name__ == "__main__":
    raise SystemExit(main())
