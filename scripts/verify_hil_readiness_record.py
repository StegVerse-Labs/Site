#!/usr/bin/env python3
"""Validate a preserved HIL receiver readiness record against v1.1.

Usage:
    python scripts/verify_hil_readiness_record.py path/to/readiness.json

The validator is intentionally offline. Fetching the public endpoint and
preserving its bytes, headers, timestamp, and transport evidence are separate
observation steps. This script determines only whether the supplied JSON body
conforms to the exact Site activation contract.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "state": "READY",
    "primary_version": "v1.1",
    "primary_sha256": "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462",
    "protocol_version": "HIL-PROTOCOL-v1.1",
    "prompt_version": "HIL-PROMPT-v1.1",
    "prompt_sha256": "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c",
    "provenance_manifest_required": True,
    "provenance_manifest_schema": "HIL-RESPONSE-PROVENANCE-v1.1",
    "participant_metadata_required": False,
}


def fail(message: str) -> None:
    raise SystemExit(f"HIL_READINESS_RECORD=FAIL: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("provide exactly one readiness JSON path")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"file not found: {path}")

    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"invalid JSON: {error}")

    if not isinstance(record, dict):
        fail("readiness body must be a JSON object")

    mismatches = []
    for key, expected in EXPECTED.items():
        actual = record.get(key)
        if actual != expected:
            mismatches.append(f"{key}: expected {expected!r}, got {actual!r}")

    if mismatches:
        fail("; ".join(mismatches))

    print("HIL_READINESS_RECORD=PASS")
    print(f"validated_fields={len(EXPECTED)}")
    print("authority_granted=false")
    print("durable_custody_proven=false")
    print("publication_ready_proven=false")


if __name__ == "__main__":
    main()
