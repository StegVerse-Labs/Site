from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_DISPOSITIONS = {"SUPERSEDED", "ARCHIVABLE"}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate_packet(packet: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if packet.get("schema_version") != "1.0.0":
        failures.append("unsupported_packet_schema")
    if packet.get("packet_type") != "session_disposition_custody_packet":
        failures.append("invalid_packet_type")
    if packet.get("state") != "READY_FOR_CUSTODY_INTAKE":
        failures.append("packet_not_ready_for_intake")
    if packet.get("source_repository") != "StegVerse-Labs/Site":
        failures.append("invalid_source_repository")
    if packet.get("target_repository") != "master-records/orchestration":
        failures.append("invalid_target_repository")

    source = packet.get("source_receipt")
    if not isinstance(source, dict):
        failures.append("missing_source_receipt")
        source = {}

    disposition = packet.get("disposition")
    if disposition not in ALLOWED_DISPOSITIONS:
        failures.append("unsupported_disposition")

    expected_pairs = (
        ("receipt_sha256", receipt.get("receipt_sha256")),
        ("evidence_id", receipt.get("evidence_id")),
        ("session_id", receipt.get("session_id")),
        ("task_id", receipt.get("task_id")),
    )
    for key, expected in expected_pairs:
        if source.get(key) != expected:
            failures.append(f"source_receipt_mismatch:{key}")

    for key in ("baseline_registry_commit", "before_sha256", "after_sha256"):
        if packet.get(key) != receipt.get(key):
            failures.append(f"receipt_binding_mismatch:{key}")

    if packet.get("disposition") != receipt.get("disposition"):
        failures.append("receipt_binding_mismatch:disposition")
    if receipt.get("admission_status") != "ADMITTED":
        failures.append("source_receipt_not_admitted")
    if receipt.get("ui_archive_action_performed") is not False:
        failures.append("source_receipt_ui_archive_claim_invalid")

    if not SHA256_RE.fullmatch(str(source.get("receipt_sha256", ""))):
        failures.append("invalid_receipt_sha256")
    if not COMMIT_RE.fullmatch(str(packet.get("baseline_registry_commit", ""))):
        failures.append("invalid_baseline_registry_commit")
    for key in ("before_sha256", "after_sha256"):
        if not SHA256_RE.fullmatch(str(packet.get(key, ""))):
            failures.append(f"invalid_{key}")

    authority = packet.get("authority")
    if not isinstance(authority, dict):
        failures.append("missing_authority_boundary")
        authority = {}
    if authority.get("custody_requested") is not True:
        failures.append("custody_not_requested")
    for key in ("publication_authority", "release_authority", "activation_authority", "ui_archive_authority"):
        if authority.get(key) is not False:
            failures.append(f"authority_escalation:{key}")

    nonclaims = packet.get("nonclaims")
    if not isinstance(nonclaims, list) or len(nonclaims) < 3 or not all(isinstance(item, str) and item.strip() for item in nonclaims):
        failures.append("insufficient_nonclaims")

    return failures


def build_result(packet_path: Path) -> dict[str, Any]:
    packet = _load(packet_path)
    source = packet.get("source_receipt") if isinstance(packet.get("source_receipt"), dict) else {}
    source_path = source.get("path")
    if not isinstance(source_path, str) or not source_path:
        return {
            "schema": "stegverse.site.session_disposition_custody_validation.v1",
            "state": "BLOCKED",
            "failures": ["missing_source_receipt_path"],
            "custody_established": False,
            "reconstruction_verified": False,
            "authority_effect": "NONE",
        }

    root = Path(__file__).resolve().parents[1]
    receipt_path = root / source_path
    if not receipt_path.is_file():
        return {
            "schema": "stegverse.site.session_disposition_custody_validation.v1",
            "state": "BLOCKED",
            "failures": ["source_receipt_missing"],
            "custody_established": False,
            "reconstruction_verified": False,
            "authority_effect": "NONE",
        }

    receipt = _load(receipt_path)
    failures = validate_packet(packet, receipt)
    return {
        "schema": "stegverse.site.session_disposition_custody_validation.v1",
        "state": "PASS" if not failures else "BLOCKED",
        "failures": failures,
        "packet": str(packet_path),
        "source_receipt": source_path,
        "disposition": packet.get("disposition"),
        "custody_intake_ready": not failures,
        "custody_established": False,
        "reconstruction_verified": False,
        "publication_authority": False,
        "release_authority": False,
        "activation_authority": False,
        "ui_archive_authority": False,
        "authority_effect": "NONE",
        "next_action": "submit packet through the canonical Master Records custody lane and require an immutable sanitized return receipt" if not failures else "repair packet or receipt binding before custody intake",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Site session-disposition custody packet without claiming custody")
    parser.add_argument(
        "packet",
        nargs="?",
        default="data/session-custody-outbox/SESSION-ORCHESTRATION-DESIGN-SUPERSEDED-2026-08-07.custody.json",
    )
    args = parser.parse_args()
    result = build_result(Path(args.packet))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
