#!/usr/bin/env python3
"""Validate a HIL pilot ledger and its fail-closed semantic invariants."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "data/hil-pilot-ledger.json"
DEFAULT_SCHEMA = ROOT / "data/schemas/hil-pilot-ledger.schema.json"


def validate_ledger(ledger_path: Path, schema_path: Path) -> tuple[int, str]:
    from stegverse_jsonschema import Draft202012Validator, FormatChecker

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(ledger),
        key=lambda error: list(error.path),
    )
    if errors:
        raise ValueError(
            "; ".join(
                f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
                for error in errors
            )
        )

    entries = ledger["entries"]
    if ledger["counts"]["model_requests_initiated"] != len(entries):
        raise ValueError("model_requests_initiated must equal entry count")
    if len({entry["submission_id"] for entry in entries}) != len(entries):
        raise ValueError("submission_id values must be unique")

    primary = ledger["canonical_primary"]
    prompt = ledger["canonical_prompt"]
    derived = {
        "completed_response_pdfs_confirmed": 0,
        "verified_return_packages": 0,
        "managed_receiving_acknowledgments": 0,
        "governed_receiver_receipts": 0,
    }
    for entry in entries:
        submission_id = entry["submission_id"]
        if (entry["canonical_paper_version"], entry["canonical_paper_sha256"]) != (
            primary["version"],
            primary["sha256"],
        ):
            raise ValueError(f"{submission_id} canonical paper mismatch")
        if (entry["prompt_version"], entry["prompt_sha256"]) != (
            prompt["version"],
            prompt["sha256"],
        ):
            raise ValueError(f"{submission_id} canonical prompt mismatch")

        status = entry["verification_status"]
        pending = status == "MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED"
        response_fields = (
            entry["response_pdf_filename"],
            entry["response_pdf_sha256"],
            entry["response_pdf_size"],
        )
        package_fields = (entry["package_id"], entry["package_sha256"])

        if pending:
            if any(value is not None for value in response_fields + package_fields):
                raise ValueError(f"{submission_id} pending entry claims response or package data")
            if entry["return_mode"] != "not_yet_returned":
                raise ValueError(f"{submission_id} pending entry claims a return mode")
            if entry["custody_status"] != "NO_CUSTODY" or entry["registry_status"] != "NOT_REGISTERED":
                raise ValueError(f"{submission_id} pending entry escalates custody or registry state")
        else:
            if any(value is None for value in response_fields):
                raise ValueError(f"{submission_id} non-pending entry lacks complete response identity")
            derived["completed_response_pdfs_confirmed"] += 1

        package_verified = status in {
            "RETURN_PACKAGE_VERIFIED",
            "MANAGED_RECEIVING_ACKNOWLEDGED",
            "GOVERNED_RECEIVER_RECEIPT_VERIFIED",
        }
        if package_verified:
            if any(value is None for value in package_fields):
                raise ValueError(f"{submission_id} verified package status lacks package identity")
            derived["verified_return_packages"] += 1

        managed_ack = status in {
            "MANAGED_RECEIVING_ACKNOWLEDGED",
            "GOVERNED_RECEIVER_RECEIPT_VERIFIED",
        }
        if managed_ack:
            derived["managed_receiving_acknowledgments"] += 1

        governed_receipt = status == "GOVERNED_RECEIVER_RECEIPT_VERIFIED"
        if governed_receipt:
            derived["governed_receiver_receipts"] += 1
            if entry["custody_status"] != "GOVERNED_RECEIVER_CUSTODY":
                raise ValueError(f"{submission_id} governed receipt lacks governed receiver custody")
            if entry["registry_status"] != "REGISTERED":
                raise ValueError(f"{submission_id} governed receipt lacks registry commitment")

        if entry["custody_status"] == "NO_CUSTODY" and entry["registry_status"] != "NOT_REGISTERED":
            raise ValueError(f"{submission_id} registry claim without custody")
        if entry["review_status"] != "NOT_REVIEWED" and not governed_receipt:
            raise ValueError(f"{submission_id} review claim without governed receiver receipt")

    for key, value in derived.items():
        if ledger["counts"][key] != value:
            raise ValueError(f"counts.{key}={ledger['counts'][key]} but derived={value}")
    return len(entries), str(ledger_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()
    try:
        count, ledger_path = validate_ledger(args.ledger, args.schema)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"HIL pilot ledger validation failed: {exc}") from exc
    try:
        display = Path(ledger_path).resolve().relative_to(ROOT)
    except ValueError:
        display = Path(ledger_path)
    print(f"PASS: {display} ({count} entries, fail-closed semantics verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
