#!/usr/bin/env python3
"""Validate HIL Master Record release files without granting release authority."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "hil-master-records.json"
RELEASE_DIR = ROOT / "data" / "hil-master-record-releases"
PRIMARY_SHA = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT_SHA = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")


def canonical_payload(record: dict[str, Any]) -> bytes:
    payload = {key: value for key, value in record.items() if key != "release_payload_sha256"}
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def validate_release(record: dict[str, Any], expected_previous: str | None) -> str:
    if record.get("schema_version") != "HIL-MASTER-RECORD-RELEASE-v1":
        fail("invalid release schema_version")
    if record.get("experiment_id") != "HIL-2026":
        fail("invalid experiment_id")

    primary = record.get("primary", {})
    if primary.get("version") != "v1.1" or primary.get("sha256") != PRIMARY_SHA:
        fail("release does not bind the exact canonical v1.1 Primary")
    if primary.get("prompt_sha256") != PROMPT_SHA:
        fail("release does not bind the exact canonical v1.1 prompt")

    response = record.get("response", {})
    receipt = record.get("receiver_receipt", {})
    response_sha = response.get("sha256")
    if not isinstance(response_sha, str) or len(response_sha) != 64:
        fail("invalid response sha256")
    if receipt.get("submitted_file_sha256") != response_sha:
        fail("response and receiver receipt byte hashes differ")
    if receipt.get("chain_validation_state") != "VERIFIED":
        fail("receiver receipt is not VERIFIED")

    review = record.get("private_review", {})
    if review.get("decision") != "ACCEPT_PRIVATE" or review.get("authenticated") is not True:
        fail("authenticated ACCEPT_PRIVATE review is required")

    publication = record.get("publication", {})
    if publication.get("append_only") is not True or publication.get("authenticated") is not True:
        fail("authenticated append-only publication is required")

    if record.get("previous_release_sha256") != expected_previous:
        fail("previous_release_sha256 does not match the release chain")

    authority = record.get("authority", {})
    required_false = ("custody", "execution", "publication_mutation", "endorsement", "scientific_proof")
    if any(authority.get(key) is not False for key in required_false):
        fail("release attempts authority escalation")

    actual = hashlib.sha256(canonical_payload(record)).hexdigest()
    if record.get("release_payload_sha256") != actual:
        fail(f"release_payload_sha256 mismatch: expected {actual}")
    return actual


def main() -> int:
    index = load_json(INDEX_PATH)
    if index.get("schema_version") != "HIL-MASTER-RECORD-INDEX-v1":
        fail("invalid HIL Master Record index schema")

    releases = index.get("releases")
    if not isinstance(releases, list):
        fail("index releases must be a list")

    expected_previous: str | None = None
    observed: list[str] = []
    for entry in releases:
        if not isinstance(entry, dict):
            fail("index release entries must be objects")
        path_value = entry.get("path")
        if not isinstance(path_value, str) or not path_value.startswith("data/hil-master-record-releases/"):
            fail("release path is outside the governed release directory")
        path = ROOT / path_value
        record = load_json(path)
        digest = validate_release(record, expected_previous)
        if entry.get("release_id") != record.get("release_id"):
            fail("index and release_id differ")
        if entry.get("release_payload_sha256") != digest:
            fail("index and release payload hashes differ")
        observed.append(digest)
        expected_previous = digest

    latest = index.get("latest_release_sha256")
    if latest != (observed[-1] if observed else None):
        fail("latest_release_sha256 does not match the chain tip")

    authority = index.get("authority", {})
    if any(authority.get(key) is not False for key in (
        "site_index_is_custody",
        "site_index_is_execution_authority",
        "site_index_is_endorsement",
        "site_index_is_publication_mutation_authority",
    )):
        fail("index attempts authority escalation")

    print(f"PASS: validated {len(observed)} HIL Master Record release(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
