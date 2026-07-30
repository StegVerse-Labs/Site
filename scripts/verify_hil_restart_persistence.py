#!/usr/bin/env python3
"""Verify that a previously accepted HIL submission survives redeployment.

Inputs:
  receipt.json status-after-restart.json retrieved-after-restart.pdf

This verifier proves only post-redeployment status and exact-byte continuity for the
identified submission. It grants no review, publication, endorsement, execution,
or Master Record authority.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def main() -> None:
    require(len(sys.argv) == 4, "usage: verify_hil_restart_persistence.py RECEIPT.json STATUS.json RETRIEVED.pdf")
    receipt_path, status_path, retrieved_path = map(Path, sys.argv[1:])
    receipt = load_json(receipt_path)
    status = load_json(status_path)
    retrieved = retrieved_path.read_bytes()

    require(receipt.get("schema_version") == "HIL-RECEIVER-RECEIPT-v2", "receipt schema mismatch")
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    expected_receipt_hash = hashlib.sha256(canonical_json(unsigned)).hexdigest()
    require(receipt.get("receipt_sha256") == expected_receipt_hash, "receipt integrity mismatch")

    submission_id = receipt.get("submission_id")
    expected_hash = receipt.get("submitted_file_sha256")
    require(isinstance(submission_id, str) and submission_id, "receipt submission_id missing")
    require(isinstance(expected_hash, str) and len(expected_hash) == 64, "receipt response hash invalid")
    require(receipt.get("custody_state") == "EXACT_BYTES_PERSISTED", "receipt does not establish exact-byte custody")
    require(receipt.get("registry_state") == "RECORDED", "receipt registry state mismatch")
    require(receipt.get("review_state") == "PENDING", "review boundary drift")
    require(receipt.get("publication_state") == "NOT_AUTHORIZED", "publication boundary drift")

    require(status.get("submission_id") == submission_id, "status submission_id mismatch")
    require(status.get("submitted_file_sha256") == expected_hash, "status response hash mismatch")
    require(status.get("state") == "ACCEPTED", "submission is not accepted after restart")
    require(status.get("custody_backend") == receipt.get("custody_backend"), "custody backend mismatch")
    require(status.get("receipt") == receipt, "status receipt differs from original receipt")
    require(isinstance(status.get("chunk_count"), int) and status["chunk_count"] > 0, "chunk count missing after restart")

    require(retrieved.startswith(b"%PDF-"), "retrieved artifact is not a PDF")
    retrieved_hash = hashlib.sha256(retrieved).hexdigest()
    require(retrieved_hash == expected_hash, "retrieved bytes do not match accepted response hash")
    require(status.get("size_bytes") == len(retrieved), "retrieved byte length differs from status")

    print("HIL_RESTART_PERSISTENCE=PASS")
    print(f"submission_id={submission_id}")
    print(f"response_sha256={retrieved_hash}")
    print("durable_custody_after_restart=true")
    print("review_authority_granted=false")
    print("publication_authority_granted=false")
    print("master_record_authority_granted=false")


if __name__ == "__main__":
    main()
