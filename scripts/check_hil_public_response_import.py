#!/usr/bin/env python3
"""Validate the HIL v1.1 public-response index and any staged imports."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "hil-responses.json"
STAGED = ROOT / "data" / "hil-public-response-imports"
PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
HEX = set("0123456789abcdef")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def is_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def validate_import(record: dict, path: Path) -> None:
    require(record.get("schema_version") == "HIL-PUBLIC-RESPONSE-IMPORT-v1.1", f"{path}: schema")
    require(record.get("primary_sha256") == PRIMARY, f"{path}: primary chain")
    require(record.get("prompt_sha256") == PROMPT, f"{path}: prompt chain")
    response_hash = record.get("response_sha256")
    require(is_sha256(response_hash), f"{path}: response hash")
    receipt = record.get("receiver_receipt", {})
    require(receipt.get("submitted_file_sha256") == response_hash, f"{path}: receipt byte continuity")
    require(receipt.get("chain_validation_state") == "VERIFIED", f"{path}: receiver verification")
    acceptance = record.get("private_acceptance", {})
    require(acceptance.get("decision") == "ACCEPT_PRIVATE" and acceptance.get("authenticated") is True,
            f"{path}: authenticated private acceptance")
    publication = record.get("publication_receipt", {})
    require(publication.get("append_only") is True and publication.get("authenticated") is True,
            f"{path}: authenticated append-only publication")
    require(record.get("public_record", {}).get("publication_state") == "PUBLISHED", f"{path}: publication state")
    authority = record.get("authority", {})
    for key in ("custody", "endorsement", "scientific_proof", "master_record_append"):
        require(authority.get(key) is False, f"{path}: authority escalation {key}")


def main() -> None:
    index = json.loads(INDEX.read_text())
    primary = index.get("primary_document", {})
    require(primary.get("version") == "v1.1", "response index version")
    require(primary.get("sha256") == PRIMARY, "response index primary hash")
    require(primary.get("prompt_sha256") == PROMPT, "response index prompt hash")
    require(index.get("acquisition_state") == "CLOSED_PENDING_PROVEN_RECEIVER_AND_CONTROLLED_CYCLE",
            "acquisition must remain fail-closed")
    require(index.get("authority", {}).get("index_update_grants_publication_authority") is False,
            "index cannot grant publication authority")

    staged_by_id: dict[str, dict] = {}
    if STAGED.exists():
        for path in sorted(STAGED.glob("*.json")):
            record = json.loads(path.read_text())
            validate_import(record, path)
            response_id = record.get("response_id")
            require(isinstance(response_id, str) and response_id not in staged_by_id, f"{path}: duplicate response id")
            staged_by_id[response_id] = record

    for public in index.get("responses", []):
        response_id = public.get("response_id")
        require(response_id in staged_by_id, f"published response {response_id} lacks validated import evidence")
        require(public.get("response_sha256") == staged_by_id[response_id]["response_sha256"],
                f"published response {response_id} hash drift")

    digest = hashlib.sha256(INDEX.read_bytes()).hexdigest()
    print(f"PASS: HIL public response import boundary verified; index_sha256={digest}; staged={len(staged_by_id)}")


if __name__ == "__main__":
    main()
