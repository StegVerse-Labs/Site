#!/usr/bin/env python3
"""Fail-closed validation for the HIL Master Record release index and builder contract."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "hil-master-records.json"
RESPONSES = ROOT / "data" / "hil-responses.json"
SCHEMA = ROOT / "data" / "schemas" / "hil-master-record-release.schema.json"
BUILDER = ROOT / "scripts" / "build_hil_master_record.py"
EXPECTED_PRIMARY = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
HEX64 = re.compile(r"^[a-f0-9]{64}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL Master Record verification failed: {message}")


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def main() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    responses = json.loads(RESPONSES.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    builder = BUILDER.read_text(encoding="utf-8")

    require(index.get("schema_version") == "HIL-MASTER-RECORD-INDEX-v1", "index schema mismatch")
    require(index.get("experiment_id") == "HIL-2026", "experiment mismatch")
    releases = index.get("releases")
    require(isinstance(releases, list), "releases must be an array")
    require(schema.get("$id") == "https://stegverse.org/schemas/hil-master-record-release-v1.json", "release schema ID mismatch")
    require(schema["properties"]["primary_sha256"]["const"] == EXPECTED_PRIMARY, "schema Primary hash mismatch")
    require(all(value is False for value in index["authority"].values()), "index authority must remain false")

    expected_previous = None
    seen_ids: set[str] = set()
    for release in releases:
        release_id = release.get("release_id")
        require(isinstance(release_id, str) and re.fullmatch(r"HIL-MR-[A-Z0-9-]+", release_id), "invalid release ID")
        require(release_id not in seen_ids, "duplicate release ID")
        seen_ids.add(release_id)
        require(release.get("previous_release_sha256") == expected_previous, f"release chain break at {release_id}")
        supplied = release.get("release_sha256")
        require(isinstance(supplied, str) and HEX64.fullmatch(supplied), "invalid release hash")
        unsigned = dict(release)
        unsigned.pop("release_sha256")
        require(canonical_hash(unsigned) == supplied, f"release hash mismatch at {release_id}")
        require(release.get("response_count") == len(release.get("response_records", [])), "response count mismatch")
        require(all(value is False for value in release["authority"].values()), "release authority must remain false")
        expected_previous = supplied

    require(index.get("latest_release_sha256") == expected_previous, "latest release pointer mismatch")
    public_records = responses.get("responses")
    require(isinstance(public_records, list), "public response index invalid")

    for marker in (
        "HIL-MASTER-RECORD-RELEASE-v1",
        "previous_release_sha256",
        "release_sha256",
        "HIL_MASTER_RECORD_BUILD=VALID_DRY_RUN",
        "--apply",
        "custody_claimed",
    ):
        require(marker in builder, f"builder missing marker: {marker}")

    print("HIL_MASTER_RECORD_VERIFICATION=PASS")
    print(f"HIL_MASTER_RECORD_RELEASE_COUNT={len(releases)}")
    print(f"HIL_PUBLIC_RESPONSE_COUNT={len(public_records)}")
    print("HIL_MASTER_RECORD_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
