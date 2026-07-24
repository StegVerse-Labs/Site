#!/usr/bin/env python3
"""Validate and optionally append one HIL publication record to the Site projection."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "hil-responses.json"
EXPECTED_PRIMARY = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
EXPECTED_PROMPT = "0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922"
HEX64 = re.compile(r"^[a-f0-9]{64}$")
RESPONSE_ID = re.compile(r"^HIL-RESP-[A-Z0-9-]+$")


def fail(message: str) -> None:
    raise SystemExit(f"HIL publication import failed: {message}")


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def validate_publication(record: dict) -> None:
    if record.get("schema_version") != "HIL-PUBLICATION-RECORD-v1":
        fail("publication schema version mismatch")
    response_id = record.get("response_id")
    if not isinstance(response_id, str) or not RESPONSE_ID.fullmatch(response_id):
        fail("invalid response_id")
    if record.get("primary_sha256") != EXPECTED_PRIMARY:
        fail("Primary hash mismatch")
    for field in (
        "response_sha256",
        "provenance_manifest_sha256",
        "private_review_receipt_sha256",
        "publication_record_sha256",
    ):
        value = record.get(field)
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            fail(f"invalid {field}")
    previous = record.get("previous_publication_sha256")
    if previous is not None and (not isinstance(previous, str) or not HEX64.fullmatch(previous)):
        fail("invalid previous_publication_sha256")
    if record.get("publication_consent") not in {"public", "anonymous"}:
        fail("publication consent is not public or anonymous")
    if record.get("publication_consent") == "anonymous" and record.get("participant_display_name") is not None:
        fail("anonymous publication exposes participant_display_name")
    artifact_path = record.get("artifact_path")
    if not isinstance(artifact_path, str) or not artifact_path.endswith(".pdf"):
        fail("invalid artifact_path")
    if artifact_path.startswith(("/", "http://", "https://")):
        fail("artifact_path must be repository-relative")
    authority = record.get("authority")
    if authority != {
        "public_projection_authorized": True,
        "execution": False,
        "endorsement": False,
        "master_record_append": False,
    }:
        fail("publication authority boundary mismatch")

    supplied_hash = record["publication_record_sha256"]
    unsigned = dict(record)
    unsigned.pop("publication_record_sha256")
    if canonical_hash(unsigned) != supplied_hash:
        fail("publication_record_sha256 does not match canonical record")


def to_projection(record: dict) -> dict:
    return {
        "response_id": record["response_id"],
        "submission_id": record["submission_id"],
        "participant_display_name": record.get("participant_display_name"),
        "publication_consent": record["publication_consent"],
        "primary_document_version": "v0.5",
        "primary_sha256": record["primary_sha256"],
        "prompt_sha256": EXPECTED_PROMPT,
        "response_sha256": record["response_sha256"],
        "receiver_verified_file_sha256": record["response_sha256"],
        "provenance_manifest_sha256": record["provenance_manifest_sha256"],
        "chain_validation_state": record["chain_validation_state"],
        "private_review_id": record["private_review_id"],
        "private_review_receipt_sha256": record["private_review_receipt_sha256"],
        "publication_record_sha256": record["publication_record_sha256"],
        "previous_record_sha256": record.get("previous_publication_sha256"),
        "publication_state": "PUBLISHED",
        "published_at": record["published_at"],
        "artifact_path": record["artifact_path"],
        "master_record_release": record.get("master_record_release"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path, help="HIL-PUBLICATION-RECORD-v1 JSON file")
    parser.add_argument("--apply", action="store_true", help="append to data/hil-responses.json")
    args = parser.parse_args()

    record = json.loads(args.record.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        fail("publication record must be an object")
    validate_publication(record)

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    responses = index.get("responses")
    if not isinstance(responses, list):
        fail("Site response index has invalid shape")
    if any(item.get("response_id") == record["response_id"] for item in responses):
        fail("response_id already exists in Site index")
    if any(item.get("submission_id") == record["submission_id"] for item in responses):
        fail("submission_id already exists in Site index")

    expected_previous = responses[-1].get("publication_record_sha256") if responses else None
    if record.get("previous_publication_sha256") != expected_previous:
        fail("previous publication hash does not match Site append position")

    projection = to_projection(record)
    print(json.dumps(projection, indent=2, sort_keys=True))
    if not args.apply:
        print("HIL_PUBLICATION_IMPORT=VALID_DRY_RUN")
        return

    responses.append(projection)
    index["last_updated"] = datetime.now(timezone.utc).isoformat()
    INDEX.write_text(json.dumps(index, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"HIL_PUBLICATION_IMPORT=APPENDED:{record['response_id']}")


if __name__ == "__main__":
    main()
