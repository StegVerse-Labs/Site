#!/usr/bin/env python3
"""Fail-closed validation for imported Master Records persistent-service evidence."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "master-records-persistent-service-evidence"
HEX40 = re.compile(r"^[a-f0-9]{40}$")
HEX64 = re.compile(r"^[a-f0-9]{64}$")
FALSE_AUTHORITY = {
    "configuration_is_custody_evidence": False,
    "health_is_custody_authority": False,
    "write_receipt_is_publication_authority": False,
    "reconstruction_is_release_authority": False,
    "execution_authorized": False,
    "publication_authorized": False,
    "release_authorized": False,
    "site_activation_authorized": False,
    "authority_effect": "NONE",
}
PENDING = "AWAITING_VERIFIED_EXTERNAL_SERVICE_EVIDENCE"
VERIFIED = "VERIFIED_PERSISTENT_CUSTODY_AND_RECONSTRUCTION"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def valid_hash(value: object) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def validate_pending(path: Path, data: dict) -> None:
    require(data["state"] == PENDING, f"{path}: invalid pending state")
    config = data["configuration_observation"]
    service = data["service"]
    custody = data["custody_cycle"]
    reconstruction = data["reconstruction"]
    require(not config["endpoint_configured"], f"{path}: pending import claims endpoint configured")
    require(not config["endpoint_public_https_verified"], f"{path}: pending import claims endpoint verified")
    require(not config["token_configured"], f"{path}: pending import claims token configured")
    require(config["observation_sha256"] is None, f"{path}: pending import includes configuration hash")
    require(not any((service["persistent_service_observed"], service["health_verified"], service["restart_observed"])), f"{path}: pending import claims service evidence")
    require(not any((custody["write_verified"], custody["readback_verified"], custody["payload_hash_matches"], custody["post_restart_readback_verified"])), f"{path}: pending import claims custody evidence")
    require(not any((reconstruction["reconstruction_verified"], reconstruction["reconstructed_payload_matches_source"])), f"{path}: pending import claims reconstruction evidence")
    require(data["evidence_refs"] == [], f"{path}: pending import must not contain evidence references")


def validate_verified(path: Path, data: dict) -> None:
    require(data["state"] == VERIFIED, f"{path}: invalid verified state")
    config = data["configuration_observation"]
    service = data["service"]
    custody = data["custody_cycle"]
    reconstruction = data["reconstruction"]
    require(config["endpoint_configured"] is True, f"{path}: endpoint not configured")
    require(config["endpoint_public_https_verified"] is True, f"{path}: endpoint not public HTTPS verified")
    require(config["token_configured"] is True, f"{path}: token not configured")
    require(valid_hash(config["observation_sha256"]), f"{path}: configuration observation hash invalid")
    require(service["persistent_service_observed"] is True, f"{path}: persistent service not observed")
    require(service["health_verified"] is True, f"{path}: health not verified")
    require(valid_hash(service["health_receipt_sha256"]), f"{path}: health receipt hash invalid")
    require(service["restart_observed"] is True, f"{path}: restart not observed")
    require(valid_hash(service["restart_receipt_sha256"]), f"{path}: restart receipt hash invalid")
    require(isinstance(service["service_instance_before_restart"], str) and service["service_instance_before_restart"], f"{path}: pre-restart instance missing")
    require(isinstance(service["service_instance_after_restart"], str) and service["service_instance_after_restart"], f"{path}: post-restart instance missing")
    require(service["service_instance_before_restart"] != service["service_instance_after_restart"], f"{path}: restart did not change instance identity")
    for key in ("source_payload_sha256", "write_receipt_sha256", "readback_payload_sha256", "readback_receipt_sha256"):
        require(valid_hash(custody[key]), f"{path}: invalid custody hash: {key}")
    require(isinstance(custody["record_id"], str) and custody["record_id"], f"{path}: custody record ID missing")
    require(custody["write_verified"] is True, f"{path}: write not verified")
    require(custody["readback_verified"] is True, f"{path}: readback not verified")
    require(custody["payload_hash_matches"] is True, f"{path}: payload hash mismatch")
    require(custody["post_restart_readback_verified"] is True, f"{path}: post-restart readback not verified")
    require(custody["source_payload_sha256"] == custody["readback_payload_sha256"], f"{path}: readback hash differs from source")
    require(valid_hash(reconstruction["reconstruction_receipt_sha256"]), f"{path}: reconstruction receipt hash invalid")
    require(valid_hash(reconstruction["reconstructed_payload_sha256"]), f"{path}: reconstructed payload hash invalid")
    require(reconstruction["reconstruction_verified"] is True, f"{path}: reconstruction not verified")
    require(reconstruction["reconstructed_payload_matches_source"] is True, f"{path}: reconstructed payload mismatch")
    require(reconstruction["reconstructed_payload_sha256"] == custody["source_payload_sha256"], f"{path}: reconstructed hash differs from source")
    require(isinstance(data["evidence_refs"], list) and data["evidence_refs"], f"{path}: supporting evidence references missing")


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "MASTER-RECORDS-PERSISTENT-SERVICE-EVIDENCE-IMPORT-v1", f"{path}: schema mismatch")
    require(data.get("source_repository") == "master-records/orchestration", f"{path}: source repository mismatch")
    require(data.get("source_path") == "data/master-records-persistent-service-evidence.json", f"{path}: source path mismatch")
    require(bool(HEX40.fullmatch(str(data.get("source_commit", "")))), f"{path}: source commit invalid")
    require(bool(HEX40.fullmatch(str(data.get("source_validation_commit", "")))), f"{path}: source validation commit invalid")
    require(valid_hash(data.get("source_sha256")), f"{path}: source hash invalid")
    require(data.get("authority") == FALSE_AUTHORITY, f"{path}: authority escalation")
    state = data.get("state")
    require(state in {PENDING, VERIFIED}, f"{path}: state invalid")
    if state == PENDING:
        validate_pending(path, data)
    else:
        validate_verified(path, data)


def main() -> None:
    if not IMPORT_DIR.exists():
        print("MASTER_RECORDS_PERSISTENT_SERVICE_EVIDENCE_IMPORT=PASS pending_no_imports")
        return
    files = sorted(IMPORT_DIR.glob("*.json"))
    if not files:
        print("MASTER_RECORDS_PERSISTENT_SERVICE_EVIDENCE_IMPORT=PASS pending_no_imports")
        return
    for path in files:
        validate(path)
    print(f"MASTER_RECORDS_PERSISTENT_SERVICE_EVIDENCE_IMPORT=PASS imports={len(files)}")


if __name__ == "__main__":
    main()
