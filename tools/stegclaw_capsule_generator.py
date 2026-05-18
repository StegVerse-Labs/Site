#!/usr/bin/env python3
"""
StegClaw Capsule Generator
===========================
Produces a StegEntity maintenance capsule, v0 authority token,
and v0 verified receipt for a given bundle zip.

These three files are what StegEntity validates and executes.
The zip_bundle adapter delivers the payload.

Phase 1 (v0): structural only. No cryptographic signing.
Phase 2: StegID mints receipts; TV/TVC issues authority tokens.

Usage:
    python tools/stegclaw_capsule_generator.py \
        --bundle incoming/ae-stage5-gcat-bcat-formal-v1.zip \
        --bundle-id ae-stage5-gcat-bcat-formal-v1 \
        --target StegVerse-Labs/Site \
        --adapter zip_bundle \
        --actor stegclaw \
        --out capsules/
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def expires_utc(hours: int = 1) -> str:
    dt = datetime.now(timezone.utc) + timedelta(hours=hours)
    return dt.replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# v0 Verified Receipt (StegID-style, structural only)
# ---------------------------------------------------------------------------

def make_verified_receipt(
    actor_class: str,
    scopes: list[str],
    bundle_hash: str,
    issuer: str = "stegclaw.v0",
    assurance_level: str = "v0_structural",
) -> dict:
    """
    Phase 1: structural receipt, no cryptographic signature.
    sig field is a deterministic hash of the payload for chain integrity.
    Phase 2: StegID replaces this with a real signed receipt.
    """
    receipt_id = f"RCPT-SE-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    issued_at = now_utc()
    expires_at = expires_utc(hours=24)

    payload = {
        "receipt_id": receipt_id,
        "actor_class": actor_class,
        "scopes": scopes,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "assurance_level": assurance_level,
        "issuer": issuer,
        "kid": f"{issuer}:v0:key1",
        "payload_hash": bundle_hash,
    }
    # Phase 1 sig: deterministic hash of payload (not a real signature)
    payload["sig"] = sha256_str(json.dumps(payload, sort_keys=True))
    payload["_phase"] = "v0_structural_no_crypto"
    payload["_note"] = (
        "Phase 1: structural integrity only. "
        "Phase 2: replace with StegID-signed receipt."
    )
    return payload


# ---------------------------------------------------------------------------
# v0 Authority Token (TVC-style, structural only)
# ---------------------------------------------------------------------------

def make_authority_token(
    adapter: str,
    target: str,
    scopes: list[str],
    capsule_hash: str,
    receipt_hash: str,
    token_ttl_hours: int = 1,
) -> dict:
    """
    Phase 1: structural token, reads from STEGTVC_GITHUB_TOKEN env var.
    Phase 2: TV/TVC issues this token via GitHub App with 1hr TTL.
    """
    token_id = f"TVC-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    return {
        "token_id": token_id,
        "status": "active",
        "adapter": adapter,
        "target": target,
        "scopes": scopes,
        "issued_at": now_utc(),
        "expires_at": expires_utc(hours=token_ttl_hours),
        "capsule_hash": capsule_hash,
        "receipt_hash": receipt_hash,
        "credential_source": "STEGTVC_GITHUB_TOKEN",
        "_phase": "v0_structural",
        "_note": (
            "Phase 1: credential read from env var. "
            "Phase 2: TV/TVC issues ephemeral GitHub App installation token."
        ),
    }


# ---------------------------------------------------------------------------
# Maintenance Capsule
# ---------------------------------------------------------------------------

def make_capsule(
    bundle_id: str,
    bundle_path: Path,
    bundle_hash: str,
    target: str,
    adapter: str,
    operations: list[dict],
    transition_id: str = "T-120",
    transition_name: str = "File Creation",
    transition_family: str = "Installation",
    actor: str = "stegclaw",
) -> dict:
    capsule_id = f"CAPSULE-{bundle_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"

    capsule = {
        "schema": "stegverse.maintenance_capsule.v1",
        "capsule_id": capsule_id,
        "created_at": now_utc(),
        "target": target,

        "transition": {
            "transition_id": transition_id,
            "transition_name": transition_name,
            "transition_family": transition_family,
            "actor": actor,
            "bundle_id": bundle_id,
            "bundle_path": str(bundle_path),
            "bundle_hash": bundle_hash,
        },

        "admissibility": {
            "decision": "PENDING",
            "basis": "Pending StegEntity admissibility check",
            "gcat_bcat_required": True,
            "boundary_coherence_required": True,
            "data_continuity_required": True,
            "failure_behavior": "fail-closed",
        },

        "operations": operations,

        "dependencies": {
            "adapter": adapter,
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
            "consequence_mass": 0.20,
            "recoverability_score": 0.90,
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


# ---------------------------------------------------------------------------
# Operations builder from bundle manifest
# ---------------------------------------------------------------------------

def operations_from_bundle(bundle_path: Path) -> list[dict]:
    """Extract operations list from bundle-manifest.json inside the zip."""
    import zipfile

    ops = []
    try:
        with zipfile.ZipFile(bundle_path) as zf:
            # Try bundle-manifest.json first (Site's format)
            for manifest_name in ["bundle-manifest.json", "ingestion-manifest.json"]:
                if manifest_name in zf.namelist():
                    manifest = json.loads(zf.read(manifest_name))
                    files = manifest.get("files", [])
                    for f in files:
                        ops.append({
                            "op": f.get("operation", "create_or_replace"),
                            "path": f.get("path", ""),
                            "sha256": f.get("sha256", ""),
                            "size_bytes": f.get("size_bytes", 0),
                            "role": f.get("role", "data"),
                        })
                    return ops

            # Fall back: list all zip members
            for name in sorted(zf.namelist()):
                if name.endswith("/") or name in ("README.md", "iosnoperiod.md"):
                    continue
                data = zf.read(name)
                ops.append({
                    "op": "create_or_replace",
                    "path": name,
                    "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
                    "size_bytes": len(data),
                    "role": "data",
                })
    except Exception as e:
        ops = [{"op": "create_or_replace", "path": "?", "error": str(e)}]

    return ops


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate(
    bundle_path: Path,
    bundle_id: str,
    target: str,
    adapter: str,
    actor: str,
    out_dir: Path,
    transition_id: str = "T-120",
    transition_name: str = "File Creation",
    transition_family: str = "Installation",
    scopes: list[str] | None = None,
) -> dict:
    if scopes is None:
        scopes = ["file:write", "receipt:emit", "bundle:install"]

    out_dir.mkdir(parents=True, exist_ok=True)
    bundle_hash = sha256_file(bundle_path)
    operations = operations_from_bundle(bundle_path)

    print(f"Bundle: {bundle_path.name}")
    print(f"Hash:   {bundle_hash[:48]}...")
    print(f"Ops:    {len(operations)} operations")
    print()

    # 1. Maintenance capsule
    capsule = make_capsule(
        bundle_id=bundle_id,
        bundle_path=bundle_path,
        bundle_hash=bundle_hash,
        target=target,
        adapter=adapter,
        operations=operations,
        transition_id=transition_id,
        transition_name=transition_name,
        transition_family=transition_family,
        actor=actor,
    )
    capsule_path = out_dir / f"{bundle_id}.capsule.json"
    capsule_path.write_text(json.dumps(capsule, indent=2), encoding="utf-8")
    print(f"Capsule: {capsule_path.name}")

    # 2. Verified receipt (StegID-style v0)
    receipt = make_verified_receipt(
        actor_class=actor,
        scopes=scopes,
        bundle_hash=bundle_hash,
    )
    receipt_path = out_dir / f"{bundle_id}.verified-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Receipt: {receipt_path.name}")

    # 3. Authority token (TVC-style v0)
    receipt_hash = sha256_str(json.dumps(receipt, sort_keys=True))
    token = make_authority_token(
        adapter=adapter,
        target=target,
        scopes=scopes,
        capsule_hash=capsule["capsule_hash"],
        receipt_hash=receipt_hash,
    )
    token_path = out_dir / f"{bundle_id}.authority-token.json"
    token_path.write_text(json.dumps(token, indent=2), encoding="utf-8")
    print(f"Token:   {token_path.name}")

    print()
    print(f"capsule_id:  {capsule['capsule_id']}")
    print(f"receipt_id:  {receipt['receipt_id']}")
    print(f"token_id:    {token['token_id']}")

    return {
        "bundle_id": bundle_id,
        "bundle_hash": bundle_hash,
        "capsule": capsule,
        "receipt": receipt,
        "token": token,
        "paths": {
            "capsule": str(capsule_path),
            "receipt": str(receipt_path),
            "token": str(token_path),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate StegEntity maintenance capsule + tokens for a bundle"
    )
    parser.add_argument("--bundle", required=True, help="Path to bundle zip")
    parser.add_argument("--bundle-id", required=True, help="Bundle ID")
    parser.add_argument("--target", default="StegVerse-Labs/Site")
    parser.add_argument("--adapter", default="zip_bundle")
    parser.add_argument("--actor", default="stegclaw")
    parser.add_argument("--transition-id", default="T-120")
    parser.add_argument("--transition-name", default="File Creation")
    parser.add_argument("--transition-family", default="Installation")
    parser.add_argument("--out", default="capsules/")
    args = parser.parse_args()

    generate(
        bundle_path=Path(args.bundle),
        bundle_id=args.bundle_id,
        target=args.target,
        adapter=args.adapter,
        actor=args.actor,
        out_dir=Path(args.out),
        transition_id=args.transition_id,
        transition_name=args.transition_name,
        transition_family=args.transition_family,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
