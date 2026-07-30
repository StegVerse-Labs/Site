#!/usr/bin/env python3
"""Verify one preserved HIL production-path participant-readiness cycle.

Passing proves upload, receipt, exact-byte custody, retrieval, and authority-boundary
continuity within the supplied evidence package. It does not grant review,
publication, endorsement, execution, or Master Record authority.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
PROVENANCE_SCHEMA = "HIL-RESPONSE-PROVENANCE-v1.1"
RECEIPT_SCHEMA = "HIL-RECEIVER-RECEIPT-v2"
CUSTODY_BACKEND = "portable-sqlite-chunks-v1"
TEST_CASE_ID = "HIL-E2E-001"


def fail(message: str) -> None:
    raise SystemExit(f"HIL_CONTROLLED_CYCLE=FAIL\nreason={message}")


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid_json:{path}:{exc}")
    if not isinstance(value, dict):
        fail(f"json_object_required:{path}")
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(
            "usage: verify_hil_controlled_cycle.py ORIGINAL.pdf provenance.json "
            "receipt.json status.json RETRIEVED.pdf",
            file=sys.stderr,
        )
        return 2

    original_path, provenance_path, receipt_path, status_path, retrieved_path = map(Path, argv[1:])
    original = original_path.read_bytes()
    retrieved = retrieved_path.read_bytes()
    provenance = load_json(provenance_path)
    receipt = load_json(receipt_path)
    status = load_json(status_path)

    require(original.startswith(b"%PDF-"), "original_pdf_signature_invalid")
    require(retrieved.startswith(b"%PDF-"), "retrieved_pdf_signature_invalid")
    require(b"HIL-E2E-001" in original, "canonical_test_case_marker_missing")
    require(b"not a publication candidate" in original.lower(), "publication_boundary_marker_missing")
    require(b"no authority effect" in original.lower(), "authority_boundary_marker_missing")

    original_hash = sha256_bytes(original)
    retrieved_hash = sha256_bytes(retrieved)
    require(original == retrieved, "retrieved_bytes_not_identical")
    require(len(original) == len(retrieved), "retrieved_size_mismatch")
    require(original_hash == retrieved_hash, "retrieved_hash_mismatch")

    require(provenance.get("schema_version") == PROVENANCE_SCHEMA, "provenance_schema_mismatch")
    require(provenance.get("test_case_id") == TEST_CASE_ID, "test_case_id_mismatch")
    require(provenance.get("artifact_type") == "HIL_TEST_RESPONSE_PACKET", "artifact_type_mismatch")
    require(provenance.get("participant_type") == "SYNTHETIC_VALIDATION_ACTOR", "participant_type_mismatch")
    require(provenance.get("participant_identifier") == "CONTROLLED-INFRASTRUCTURE-CYCLE", "participant_identifier_mismatch")
    require(provenance.get("model") == "SYNTHETIC-INFRASTRUCTURE-FIXTURE", "synthetic_model_marker_mismatch")
    require(provenance.get("research_data") is False, "research_data_must_be_false")
    require(provenance.get("authority_effect") is False, "authority_effect_must_be_false")
    require(provenance.get("publication_consent") == "NOT_APPLICABLE_SYNTHETIC", "publication_consent_boundary_invalid")
    require(provenance.get("primary_sha256") == PRIMARY, "provenance_primary_hash_mismatch")
    require(provenance.get("prompt_sha256") == PROMPT, "provenance_prompt_hash_mismatch")
    require(provenance.get("response_sha256") == original_hash, "provenance_response_hash_mismatch")

    require(receipt.get("schema_version") == RECEIPT_SCHEMA, "receipt_schema_mismatch")
    require(isinstance(receipt.get("receipt_id"), str) and receipt["receipt_id"], "receipt_id_missing")
    require(isinstance(receipt.get("submission_id"), str) and receipt["submission_id"], "submission_id_missing")
    require(receipt.get("submitted_file_sha256") == original_hash, "receipt_response_hash_mismatch")
    require(receipt.get("primary_sha256") == PRIMARY, "receipt_primary_hash_mismatch")
    require(receipt.get("prompt_sha256") == PROMPT, "receipt_prompt_hash_mismatch")
    require(receipt.get("chain_validation_state") == "PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED", "receipt_chain_state_invalid")
    require(receipt.get("custody_state") == "EXACT_BYTES_PERSISTED", "receipt_custody_state_invalid")
    require(receipt.get("custody_backend") == CUSTODY_BACKEND, "receipt_custody_backend_invalid")
    require(receipt.get("registry_state") == "RECORDED", "receipt_registry_state_invalid")
    require(receipt.get("review_state") == "PENDING", "receipt_review_state_invalid")
    require(receipt.get("publication_state") == "NOT_AUTHORIZED", "receipt_publication_state_invalid")

    unsigned_receipt = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    expected_receipt_hash = sha256_bytes(canonical_json(unsigned_receipt))
    require(receipt.get("receipt_sha256") == expected_receipt_hash, "receipt_integrity_hash_invalid")

    require(status.get("submission_id") == receipt.get("submission_id"), "status_submission_id_mismatch")
    require(status.get("submitted_file_sha256") == original_hash, "status_response_hash_mismatch")
    require(status.get("size_bytes") == len(original), "status_size_mismatch")
    require(isinstance(status.get("chunk_count"), int) and status["chunk_count"] > 0, "status_chunk_count_invalid")
    require(status.get("custody_backend") == CUSTODY_BACKEND, "status_custody_backend_invalid")
    require(status.get("state") == "ACCEPTED", "status_state_invalid")
    require(status.get("receipt") == receipt, "status_embedded_receipt_mismatch")

    print("HIL_CONTROLLED_CYCLE=PASS")
    print(f"test_case_id={TEST_CASE_ID}")
    print(f"submission_id={receipt['submission_id']}")
    print(f"receipt_id={receipt['receipt_id']}")
    print(f"response_sha256={original_hash}")
    print(f"retrieved_sha256={retrieved_hash}")
    print(f"size_bytes={len(original)}")
    print(f"chunk_count={status['chunk_count']}")
    print("exact_bytes_retrieved=true")
    print("authority_granted=false")
    print("review_completed=false")
    print("publication_authorized=false")
    print("master_record_released=false")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
