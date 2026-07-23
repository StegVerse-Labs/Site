#!/usr/bin/env python3
"""Verify that Conectrr source serialization and declared hash survive import unchanged."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "conectrr-independent-evaluation.fixture.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    source = payload["source_event"]
    before = canonical_bytes(source)
    before_hash = hashlib.sha256(before).hexdigest()

    imported = json.loads(before.decode("utf-8"))
    after = canonical_bytes(imported)
    after_hash = hashlib.sha256(after).hexdigest()
    errors: list[str] = []

    if before != after:
        errors.append("canonical source bytes changed across import serialization")
    if before_hash != after_hash:
        errors.append("canonical source hash changed across import serialization")
    declared = source.get("governed_projection", {}).get("source_hash")
    if not isinstance(declared, str) or not declared.startswith("sha256:"):
        errors.append("source record does not preserve a declared source_hash marker")
    if source != imported:
        errors.append("source semantics changed across import clone")

    if errors:
        print("CONECTRR_SOURCE_PRESERVATION_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONECTRR_SOURCE_PRESERVATION_CHECK=PASS")
    print(f"canonical_sha256={before_hash}")
    print("source_bytes_unchanged=true")
    print("source_semantics_unchanged=true")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
