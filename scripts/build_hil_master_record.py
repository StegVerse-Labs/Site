#!/usr/bin/env python3
"""Build or append a deterministic HIL Master Record release from the public response index."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESPONSES = ROOT / "data" / "hil-responses.json"
MASTER_INDEX = ROOT / "data" / "hil-master-records.json"
EXPECTED_PRIMARY = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
HEX64 = re.compile(r"^[a-f0-9]{64}$")


def fail(message: str) -> None:
    raise SystemExit(f"HIL Master Record build failed: {message}")


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def response_projection(record: dict) -> dict:
    required_hashes = (
        "response_sha256",
        "provenance_manifest_sha256",
        "private_review_receipt_sha256",
        "publication_record_sha256",
    )
    for field in required_hashes:
        value = record.get(field)
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            fail(f"invalid {field} for {record.get('response_id', 'unknown response')}")
    artifact_path = record.get("artifact_path")
    if not isinstance(artifact_path, str) or not artifact_path.endswith(".pdf"):
        fail("invalid response artifact path")
    if artifact_path.startswith(("/", "http://", "https://")) or ".." in Path(artifact_path).parts:
        fail("response artifact path must be repository-relative")
    if record.get("primary_sha256") != EXPECTED_PRIMARY:
        fail("response Primary hash mismatch")
    return {
        "response_id": record["response_id"],
        "submission_id": record["submission_id"],
        "response_sha256": record["response_sha256"],
        "provenance_manifest_sha256": record["provenance_manifest_sha256"],
        "private_review_receipt_sha256": record["private_review_receipt_sha256"],
        "publication_record_sha256": record["publication_record_sha256"],
        "previous_record_sha256": record.get("previous_record_sha256"),
        "artifact_path": artifact_path,
        "published_at": record["published_at"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="append the release to data/hil-master-records.json")
    parser.add_argument("--release-id", help="explicit HIL-MR identifier; defaults to UTC timestamp")
    args = parser.parse_args()

    response_index = json.loads(RESPONSES.read_text(encoding="utf-8"))
    records = response_index.get("responses")
    if not isinstance(records, list):
        fail("response index has invalid shape")

    master_index = json.loads(MASTER_INDEX.read_text(encoding="utf-8"))
    releases = master_index.get("releases")
    if not isinstance(releases, list):
        fail("Master Record index has invalid shape")

    projections = [response_projection(record) for record in records]
    for previous, current in zip(projections, projections[1:]):
        if current["previous_record_sha256"] != previous["publication_record_sha256"]:
            fail("public response publication chain is discontinuous")
    if projections and projections[0]["previous_record_sha256"] is not None:
        fail("first public response must have null previous_record_sha256")

    created_at = datetime.now(timezone.utc).isoformat()
    release_id = args.release_id or f"HIL-MR-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    if not re.fullmatch(r"HIL-MR-[A-Z0-9-]+", release_id):
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
        "created_at": created_at,
        "primary_version": "v0.5",
        "primary_sha256": EXPECTED_PRIMARY,
        "response_count": len(projections),
        "response_records": projections,
        "previous_release_sha256": previous_release,
        "authority": {
            "custody_claimed": False,
            "execution": False,
            "endorsement": False,
            "publication_mutation": False,
        },
    }
    release["release_sha256"] = canonical_hash(release)
    print(json.dumps(release, indent=2, sort_keys=True))

    if not args.apply:
        print("HIL_MASTER_RECORD_BUILD=VALID_DRY_RUN")
        return

    releases.append(release)
    master_index["latest_release_sha256"] = release["release_sha256"]
    MASTER_INDEX.write_text(json.dumps(master_index, indent=2) + "\n", encoding="utf-8")
    print(f"HIL_MASTER_RECORD_BUILD=APPENDED:{release_id}")


if __name__ == "__main__":
    main()
