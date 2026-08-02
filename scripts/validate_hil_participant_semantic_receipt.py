#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data/fixtures/hil-semantic-transformation/participant-record-with-receipt.json"
DISPUTE = ROOT / "data/fixtures/hil-semantic-transformation/participant-record-dispute.json"


def validate_primary(data: dict) -> list[str]:
    failures: list[str] = []
    participant = data["participant_record"]
    transformed = data["transformed_record"]
    receipt = data["semantic_receipt"]
    continuity = participant["semantic_continuity"]

    if not participant.get("immutable"):
        failures.append("participant source is not immutable")
    if not continuity.get("source_record_preserved"):
        failures.append("source preservation is false")
    if receipt["source_record_id"] != participant["record_id"]:
        failures.append("source_record_id does not resolve")
    if receipt["output_record_id"] != transformed["record_id"]:
        failures.append("output_record_id does not resolve")
    if receipt["receipt_id"] not in continuity.get("receipt_refs", []):
        failures.append("receipt is not linked from participant record")
    if participant["record_id"] not in receipt.get("evidence_refs", []):
        failures.append("source evidence reference missing")
    if transformed["record_id"] not in receipt.get("evidence_refs", []):
        failures.append("output evidence reference missing")
    if receipt.get("authority_effect") is not False:
        failures.append("semantic receipt grants authority")
    if continuity.get("authority_effect") is not False:
        failures.append("participant continuity grants authority")
    if continuity.get("latest_receipt_state") != "PASS":
        failures.append("participant receipt state is not PASS")
    return failures


def validate_dispute(data: dict) -> list[str]:
    failures: list[str] = []
    source = data["participant_record"]
    receipts = data["competing_receipts"]
    dispute = data["dispute_record"]
    ids = [receipt["receipt_id"] for receipt in receipts]

    if not source.get("immutable") or not source["semantic_continuity"].get("source_record_preserved"):
        failures.append("dispute source is not preserved")
    if len(ids) != len(set(ids)):
        failures.append("competing receipts overwrite identity")
    if set(ids) != set(source["semantic_continuity"].get("receipt_refs", [])):
        failures.append("participant record does not link every competing receipt")
    if dispute.get("state") != "DISPUTED":
        failures.append("dispute state is not DISPUTED")
    if set(dispute.get("receipt_refs", [])) != set(ids):
        failures.append("dispute does not reference competing receipts")
    if any(receipt.get("authority_effect") is not False for receipt in receipts):
        failures.append("competing receipt grants authority")
    if dispute.get("authority_effect") is not False:
        failures.append("dispute grants authority")
    return failures


def main() -> int:
    failures = validate_primary(json.loads(FIXTURE.read_text(encoding="utf-8")))
    if DISPUTE.exists():
        failures.extend(validate_dispute(json.loads(DISPUTE.read_text(encoding="utf-8"))))
    result = {
        "validator": "validate_hil_participant_semantic_receipt.py",
        "validation": "PASS" if not failures else "FAIL",
        "failures": failures,
        "authority_effect": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
