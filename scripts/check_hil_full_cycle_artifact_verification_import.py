#!/usr/bin/env python3
"""Fail-closed validation for imported HIL full-cycle artifact verification evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "hil-full-cycle-artifact-verifications"
EXPECTED_FILES = {
    "gateway-first.log",
    "gateway-restart.log",
    "hil-automated-full-cycle-receipt-v1.json",
}
EXPECTED_CLAIMS = {
    "ephemeral_full_cycle_verified": True,
    "persistent_public_receiver_verified": False,
    "external_production_deployment_verified": False,
    "master_record_release_verified": False,
    "site_activation_authorized": False,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def is_hex(value: object, length: int) -> bool:
    return isinstance(value, str) and len(value) == length and all(ch in "0123456789abcdef" for ch in value)


def validate(path: Path) -> None:
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data.get("schema_version") == "HIL-FULL-CYCLE-ARTIFACT-VERIFICATION-IMPORT-v1", f"{path}: schema mismatch")
    require(data.get("source_repository") == "StegVerse-org/LLM-adapter", f"{path}: source repository mismatch")
    require(data.get("source_verifier_path") == "scripts/verify_hil_full_cycle_artifact.py", f"{path}: verifier path mismatch")
    require(is_hex(data.get("source_commit"), 40), f"{path}: source commit invalid")
    require(is_hex(data.get("source_verification_sha256"), 64), f"{path}: source verification hash invalid")
    require(is_hex(data.get("receipt_sha256"), 64), f"{path}: receipt hash invalid")
    require(data.get("artifact_purity_state") == "PURE_BOUNDED_HIL_EVIDENCE", f"{path}: artifact purity not proven")
    require(data.get("provider_specific_files_present") is False, f"{path}: provider-specific files present")
    require(data.get("observation_scope") == "GITHUB_HOSTED_EPHEMERAL_FULL_CYCLE_PROOF", f"{path}: observation scope mismatch")
    require(set(data.get("files", [])) == EXPECTED_FILES and len(data.get("files", [])) == 3, f"{path}: evidence file set mismatch")
    require(data.get("authority_effect") == "NONE", f"{path}: authority escalation")
    require(data.get("claims") == EXPECTED_CLAIMS, f"{path}: claim boundary mismatch")
    require(hashlib.sha256(raw).hexdigest() != data.get("source_verification_sha256"), f"{path}: import hash incorrectly claims to be source verification hash")


def main() -> None:
    if not IMPORT_DIR.exists():
        print("HIL_FULL_CYCLE_ARTIFACT_VERIFICATION_IMPORT=PASS pending_no_imports")
        return
    files = sorted(IMPORT_DIR.glob("*.json"))
    if not files:
        print("HIL_FULL_CYCLE_ARTIFACT_VERIFICATION_IMPORT=PASS pending_no_imports")
        return
    for path in files:
        validate(path)
    print(f"HIL_FULL_CYCLE_ARTIFACT_VERIFICATION_IMPORT=PASS imports={len(files)}")


if __name__ == "__main__":
    main()
