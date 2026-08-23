#!/usr/bin/env python3
"""Positive and negative tests for verify_hil_controlled_cycle.py."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts/verify_hil_controlled_cycle.py"
PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
TEST_CASE_ID = "HIL-E2E-001"


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def invoke(paths: list[Path]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), *map(str, paths)],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        original_path = base / "original.pdf"
        retrieved_path = base / "retrieved.pdf"
        provenance_path = base / "provenance.json"
        receipt_path = base / "receipt.json"
        status_path = base / "status.json"

        pdf = (
            b"%PDF-1.4\n"
            b"% HIL-E2E-001 controlled infrastructure validation fixture\n"
            b"% not a publication candidate\n"
            b"% no authority effect\n"
            b"%%EOF\n"
        )
        response_hash = hashlib.sha256(pdf).hexdigest()
        original_path.write_bytes(pdf)
        retrieved_path.write_bytes(pdf)

        provenance = {
            "schema_version": "HIL-RESPONSE-PROVENANCE-v1.1",
            "test_case_id": TEST_CASE_ID,
            "artifact_type": "HIL_TEST_RESPONSE_PACKET",
            "participant_type": "SYNTHETIC_VALIDATION_ACTOR",
            "participant_identifier": "CONTROLLED-INFRASTRUCTURE-CYCLE",
            "model": "SYNTHETIC-INFRASTRUCTURE-FIXTURE",
            "research_data": False,
            "authority_effect": False,
            "publication_consent": "NOT_APPLICABLE_SYNTHETIC",
            "primary_sha256": PRIMARY,
            "prompt_sha256": PROMPT,
            "response_sha256": response_hash,
        }
        unsigned_receipt = {
            "schema_version": "HIL-RECEIVER-RECEIPT-v2",
            "receipt_id": "HIL-RECEIPT-test",
            "submission_id": "HIL-SUBMISSION-test",
            "received_at": "2026-07-30T15:00:00.000Z",
            "submitted_file_sha256": response_hash,
            "primary_sha256": PRIMARY,
            "prompt_sha256": PROMPT,
            "chain_validation_state": "PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED",
            "custody_state": "EXACT_BYTES_PERSISTED",
            "custody_backend": "portable-sqlite-chunks-v1",
            "registry_state": "RECORDED",
            "review_state": "PENDING",
            "publication_state": "NOT_AUTHORIZED",
            "object_reference": "hil/v1.1/2026-07-30/HIL-SUBMISSION-test/response.pdf",
        }
        receipt = {
            **unsigned_receipt,
            "receipt_sha256": hashlib.sha256(canonical_json(unsigned_receipt)).hexdigest(),
        }
        status = {
            "submission_id": receipt["submission_id"],
            "submitted_file_sha256": response_hash,
            "size_bytes": len(pdf),
            "chunk_count": 1,
            "custody_backend": "portable-sqlite-chunks-v1",
            "state": "ACCEPTED",
            "created_at": receipt["received_at"],
            "receipt": receipt,
        }

        write_json(provenance_path, provenance)
        write_json(receipt_path, receipt)
        write_json(status_path, status)
        paths = [original_path, provenance_path, receipt_path, status_path, retrieved_path]

        positive = invoke(paths)
        if positive.returncode != 0 or "HIL_CONTROLLED_CYCLE=PASS" not in positive.stdout:
            print(positive.stdout, positive.stderr, file=sys.stderr)
            raise SystemExit("positive controlled-cycle fixture failed")

        tampered = bytearray(pdf)
        tampered[-2] ^= 1
        retrieved_path.write_bytes(tampered)
        negative = invoke(paths)
        negative_output = negative.stdout + negative.stderr
        if negative.returncode == 0 or "retrieved_bytes_not_identical" not in negative_output:
            print(negative.stdout, negative.stderr, file=sys.stderr)
            raise SystemExit("tampered retrieval was not rejected")

    print("HIL_CONTROLLED_CYCLE_TESTS=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
