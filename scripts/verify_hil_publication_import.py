#!/usr/bin/env python3
"""Fail-closed validator for published HIL response imports and Master Record linkage."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
HEX64 = set("0123456789abcdef")


def load_json(path: str) -> dict:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def is_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX64


def canonical_hash(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def verify_response(record: dict, seen_ids: set[str]) -> None:
    response_id = record.get("response_id")
    require(isinstance(response_id, str) and response_id.startswith("HIL-RESP-"), "invalid response_id")
    require(response_id not in seen_ids, f"duplicate response_id: {response_id}")
    seen_ids.add(response_id)
    require(record.get("primary_sha256") == PRIMARY, f"{response_id}: Primary hash mismatch")
    require(record.get("prompt_sha256") == PROMPT, f"{response_id}: prompt hash mismatch")
    require(is_sha256(record.get("response_sha256")), f"{response_id}: invalid response hash")
    require(is_sha256(record.get("provenance_manifest_sha256")), f"{response_id}: invalid provenance hash")
    require(is_sha256(record.get("receiver_receipt_sha256")), f"{response_id}: invalid receiver receipt hash")
    require(is_sha256(record.get("private_review_receipt_sha256")), f"{response_id}: invalid private review hash")
    require(is_sha256(record.get("publication_record_sha256")), f"{response_id}: invalid publication hash")
    require(record.get("private_review_decision") == "ACCEPT_PRIVATE", f"{response_id}: private acceptance missing")
    require(record.get("publication_state") == "PUBLISHED_APPEND_ONLY", f"{response_id}: publication state invalid")
    require(record.get("authority_effect") == "NONE", f"{response_id}: import grants authority")
    artifact_path = record.get("artifact_public_path")
    require(isinstance(artifact_path, str) and artifact_path.startswith("data/hil-responses/"), f"{response_id}: invalid artifact path")


def main() -> None:
    index = load_json("data/hil-responses.json")
    masters = load_json("data/hil-master-records.json")
    require(index.get("schema_version") == "HIL-RESPONSES-INDEX-v1.1", "response index schema drift")
    primary = index.get("primary_document") or {}
    require(primary.get("sha256") == PRIMARY and primary.get("prompt_sha256") == PROMPT, "response index chain drift")
    responses = index.get("responses")
    require(isinstance(responses, list), "responses must be a list")
    seen_ids: set[str] = set()
    for record in responses:
        require(isinstance(record, dict), "response entry must be an object")
        verify_response(record, seen_ids)

    releases = masters.get("releases")
    require(isinstance(releases, list), "Master Record releases must be a list")
    previous = None
    for release in releases:
        require(isinstance(release, dict), "Master Record release must be an object")
        require(release.get("previous_release_sha256") == previous, "Master Record chain discontinuity")
        unsigned = dict(release)
        declared = unsigned.pop("release_sha256", None)
        require(is_sha256(declared), "invalid Master Record release hash")
        require(canonical_hash(unsigned) == declared, "Master Record release hash mismatch")
        linked = release.get("response_ids")
        require(isinstance(linked, list) and all(item in seen_ids for item in linked), "Master Record references unknown response")
        require(release.get("authority_effect") == "NONE", "Master Record release grants authority")
        previous = declared
    require(masters.get("latest_release_sha256") == previous, "latest Master Record hash mismatch")
    print("HIL_PUBLICATION_IMPORT_CONTRACT=PASS")


if __name__ == "__main__":
    main()
