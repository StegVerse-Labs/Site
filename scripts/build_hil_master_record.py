#!/usr/bin/env python3
"""Build or append a deterministic HIL v1.1 Master Record release."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESPONSES = ROOT / "data" / "hil-responses.json"
MASTER_INDEX = ROOT / "data" / "hil-master-records.json"
RELEASE_DIR = ROOT / "data" / "hil-master-record-releases"
PRIMARY_SHA = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT_SHA = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
HEX64 = re.compile(r"^[a-f0-9]{64}$")


def fail(message: str) -> None:
    raise SystemExit(f"HIL Master Record build failed: {message}")


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def canonical_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def response_projection(record: dict[str, Any]) -> dict[str, Any]:
    response_sha = record.get("response_sha256")
    if not isinstance(response_sha, str) or not HEX64.fullmatch(response_sha):
        fail(f"invalid response_sha256 for {record.get('response_id', 'unknown response')}")

    if record.get("primary_sha256") != PRIMARY_SHA:
        fail("response Primary hash mismatch")
    if record.get("prompt_sha256") != PROMPT_SHA:
        fail("response prompt hash mismatch")

    receipt = record.get("receiver_receipt")
    review = record.get("private_review")
    publication = record.get("publication")
    if not isinstance(receipt, dict) or receipt.get("submitted_file_sha256") != response_sha:
        fail("receiver receipt does not preserve response-byte continuity")
    if receipt.get("chain_validation_state") != "VERIFIED":
        fail("receiver receipt is not VERIFIED")
    if not isinstance(review, dict) or review.get("decision") != "ACCEPT_PRIVATE" or review.get("authenticated") is not True:
        fail("authenticated ACCEPT_PRIVATE review is required")
    if not isinstance(publication, dict) or publication.get("append_only") is not True or publication.get("authenticated") is not True:
        fail("authenticated append-only publication is required")

    return {
        "response_id": record["response_id"],
        "sha256": response_sha,
        "public_index_path": "data/hil-responses.json",
        "receiver_receipt": {
            "receipt_id": receipt["receipt_id"],
            "submitted_file_sha256": response_sha,
            "chain_validation_state": "VERIFIED",
        },
        "private_review": {
            "decision": "ACCEPT_PRIVATE",
            "decision_receipt_id": review["decision_receipt_id"],
            "authenticated": True,
        },
        "publication": {
            "publication_receipt_id": publication["publication_receipt_id"],
            "append_only": True,
            "authenticated": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the release file and append its index entry")
    parser.add_argument("--release-id", help="explicit HIL-MR identifier; defaults to UTC timestamp")
    parser.add_argument("--response-id", help="response to release; defaults to the latest published response")
    args = parser.parse_args()

    response_index = json.loads(RESPONSES.read_text(encoding="utf-8"))
    records = response_index.get("responses")
    if not isinstance(records, list) or not records:
        fail("at least one governed public response is required")

    selected = None
    if args.response_id:
        selected = next((record for record in records if record.get("response_id") == args.response_id), None)
        if selected is None:
            fail("requested response_id was not found")
    else:
        selected = records[-1]

    projection = response_projection(selected)
    master_index = json.loads(MASTER_INDEX.read_text(encoding="utf-8"))
    releases = master_index.get("releases")
    if not isinstance(releases, list):
        fail("Master Record index has invalid shape")

    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    release_id = args.release_id or f"HIL-MR-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    if not re.fullmatch(r"HIL-MR-[A-Z0-9._-]+", release_id):
        fail("invalid release_id")
    if any(release.get("release_id") == release_id for release in releases):
        fail("release_id already exists")

    previous_release = master_index.get("latest_release_sha256")
    if previous_release is not None and (not isinstance(previous_release, str) or not HEX64.fullmatch(previous_release)):
        fail("invalid latest_release_sha256")

    release = {
        "schema_version": "HIL-MASTER-RECORD-RELEASE-v1",
        "release_id": release_id,
        "experiment_id": "HIL-2026",
        "primary": {
            "version": "v1.1",
            "sha256": PRIMARY_SHA,
            "prompt_sha256": PROMPT_SHA,
        },
        "response": {
            "response_id": projection["response_id"],
            "sha256": projection["sha256"],
            "public_index_path": projection["public_index_path"],
        },
        "receiver_receipt": projection["receiver_receipt"],
        "private_review": projection["private_review"],
        "publication": projection["publication"],
        "previous_release_sha256": previous_release,
        "created_at": created_at,
        "authority": {
            "custody": False,
            "execution": False,
            "publication_mutation": False,
            "endorsement": False,
            "scientific_proof": False,
        },
    }
    release["release_payload_sha256"] = canonical_hash(release)
    print(json.dumps(release, indent=2, sort_keys=True))

    if not args.apply:
        print("HIL_MASTER_RECORD_BUILD=VALID_DRY_RUN")
        return

    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    release_path = RELEASE_DIR / f"{release_id}.json"
    if release_path.exists():
        fail("release file already exists")
    release_path.write_text(json.dumps(release, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    releases.append({
        "release_id": release_id,
        "path": str(release_path.relative_to(ROOT)),
        "release_payload_sha256": release["release_payload_sha256"],
    })
    master_index["latest_release_sha256"] = release["release_payload_sha256"]
    MASTER_INDEX.write_text(json.dumps(master_index, indent=2) + "\n", encoding="utf-8")
    print(f"HIL_MASTER_RECORD_BUILD=APPENDED:{release_id}")


if __name__ == "__main__":
    main()
