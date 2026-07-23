#!/usr/bin/env python3
"""Validate fixture-only Conectrr adapter conformance without semantic normalization."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "conectrr-adapter-conformance.fixture.json"
BOUNDARY_KEYS = {
    "consent_established",
    "authority_established",
    "admissibility_determined",
    "commitment_created",
    "execution_authorized",
}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    adapter = payload["adapter"]
    raw = payload["raw_source_payload"]
    output = payload["adapter_output"]
    embedded = output["source_payload"]
    assertions = output["adapter_assertions"]
    errors: list[str] = []

    raw_bytes = canonical_bytes(raw)
    embedded_bytes = canonical_bytes(embedded)
    if raw_bytes != embedded_bytes:
        errors.append("adapter changed canonical source bytes")
    if hashlib.sha256(raw_bytes).hexdigest() != hashlib.sha256(embedded_bytes).hexdigest():
        errors.append("adapter changed source digest")
    if adapter.get("semantic_normalization_permitted") is not False:
        errors.append("semantic normalization boundary is not fail-closed")
    if output.get("source_payload_embedded_unmodified") is not True:
        errors.append("adapter did not declare unmodified source embedding")
    boundary = embedded.get("boundary") or {}
    for key in BOUNDARY_KEYS:
        if boundary.get(key) is not False:
            errors.append(f"adapter boundary overreach: {key}")
    if assertions.get("authority_effect") != "none":
        errors.append("adapter grants authority")
    if assertions.get("live_output_verified") is not False:
        errors.append("fixture improperly claims live output verification")
    if adapter.get("authorized") is not False or adapter.get("mode") != "fixture_only":
        errors.append("fixture must remain non-authorized and fixture-only")

    if errors:
        print("CONECTRR_ADAPTER_CONFORMANCE_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONECTRR_ADAPTER_CONFORMANCE_CHECK=PASS")
    print("source_bytes=preserved")
    print("source_digest=preserved")
    print("semantic_normalization=false")
    print("live_output_verified=false")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
