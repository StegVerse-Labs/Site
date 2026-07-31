#!/usr/bin/env python3
"""Validate the HIL pilot ledger and its fail-closed semantic invariants."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/hil-pilot-ledger.json"
SCHEMA = ROOT / "data/schemas/hil-pilot-ledger.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"HIL pilot ledger validation failed: {message}")


def main() -> int:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        fail("jsonschema is required")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(ledger), key=lambda e: list(e.path))
    if errors:
        fail("; ".join(f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors))

    entries = ledger["entries"]
    if ledger["counts"]["model_requests_initiated"] != len(entries):
        fail("model_requests_initiated must equal entry count")
    if len({entry["submission_id"] for entry in entries}) != len(entries):
        fail("submission_id values must be unique")

    primary = ledger["canonical_primary"]
    prompt = ledger["canonical_prompt"]
    derived = {
        "completed_response_pdfs_confirmed": 0,
        "verified_return_packages": 0,
        "managed_receiving_acknowledgments": 0,
        "governed_receiver_receipts": 0,
    }
    for entry in entries:
        if (entry["canonical_paper_version"], entry["canonical_paper_sha256"]) != (primary["version"], primary["sha256"]):
            fail(f"{entry['submission_id']} canonical paper mismatch")
        if (entry["prompt_version"], entry["prompt_sha256"]) != (prompt["version"], prompt["sha256"]):
            fail(f"{entry['submission_id']} canonical prompt mismatch")
        pending = entry["verification_status"] == "MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED"
        response_fields = (entry["response_pdf_filename"], entry["response_pdf_sha256"], entry["response_pdf_size"])
        if pending and any(value is not None for value in response_fields):
            fail(f"{entry['submission_id']} pending entry claims response data")
        if not pending:
            if any(value is None for value in response_fields):
                fail(f"{entry['submission_id']} non-pending entry lacks complete response identity")
            derived["completed_response_pdfs_confirmed"] += 1
        if entry["verification_status"] in {"RETURN_PACKAGE_VERIFIED","MANAGED_RECEIVING_ACKNOWLEDGED","GOVERNED_RECEIVER_RECEIPT_VERIFIED"}:
            derived["verified_return_packages"] += 1
        if entry["verification_status"] in {"MANAGED_RECEIVING_ACKNOWLEDGED","GOVERNED_RECEIVER_RECEIPT_VERIFIED"}:
            derived["managed_receiving_acknowledgments"] += 1
        if entry["verification_status"] == "GOVERNED_RECEIVER_RECEIPT_VERIFIED":
            derived["governed_receiver_receipts"] += 1
        if entry["custody_status"] == "NO_CUSTODY" and entry["registry_status"] != "NOT_REGISTERED":
            fail(f"{entry['submission_id']} registry claim without custody")

    for key, value in derived.items():
        if ledger["counts"][key] != value:
            fail(f"counts.{key}={ledger['counts'][key]} but derived={value}")
    print(f"PASS: {LEDGER.relative_to(ROOT)} ({len(entries)} entries, fail-closed semantics verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
