#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/generated-stegpay-propagations/latest/propagation.json"
RECEIPT = ROOT / "data/generated-stegpay-propagations/latest/import_receipt.json"
EXPECTED_PACKET_HASH = "e59e71bf31879f0bf29a8356f8027304a94a4dee59d3c0be35c3ecc505e7cec9"
EXPECTED_CONSUMER_RECEIPT_HASH = "b8084ecc9821eb7738e4dccffd239185a072e0bc630e71c72906098a830cf515"
EXPECTED_SOURCE_GENERATED_UTC = "2026-08-27T11:58:18Z"
EXPECTED_REASONS = {"signed_envelope_verified", "stegpay_verified_event"}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"object required: {path}")
    return value


def digest(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"GENERATED_STEGPAY_SITE_IMPORT=FAIL: {message}")


def main() -> int:
    for path in (PACKET, RECEIPT):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    packet = load(PACKET)
    receipt = load(RECEIPT)
    packet_hash = digest(packet)
    if packet_hash != EXPECTED_PACKET_HASH:
        fail(f"packet hash mismatch: {packet_hash}")
    if receipt.get("propagation_hash_sha256") != packet_hash:
        fail("receipt does not bind imported packet")
    if packet.get("generated_utc") != EXPECTED_SOURCE_GENERATED_UTC:
        fail("unexpected upstream generation")
    if receipt.get("source_generated_utc") != packet.get("generated_utc"):
        fail("receipt does not bind upstream generation")
    if packet.get("consumer_receipt_hash_sha256") != EXPECTED_CONSUMER_RECEIPT_HASH:
        fail("unexpected consumer receipt hash")
    if receipt.get("consumer_receipt_hash_sha256") != packet.get("consumer_receipt_hash_sha256"):
        fail("receipt does not bind consumer receipt")
    if packet.get("status") != "COMPLETE" or packet.get("blockers") != []:
        fail("source packet is not complete and blocker-free")
    if packet.get("consumer_state") != "deliverables_ready":
        fail("unexpected consumer state")
    if set(packet.get("verified_reasons") or []) != EXPECTED_REASONS:
        fail("verified reasons mismatch")
    for field in ("authority_effect", "activation_effect", "publication_effect", "release_effect"):
        if packet.get(field) is not False or receipt.get(field) is not False:
            fail(f"authority boundary violated: {field}")
    if packet.get("test_only") is not True or receipt.get("test_only") is not True:
        fail("test-only posture missing")
    if packet.get("transport_is_authority") is not False:
        fail("transport incorrectly treated as authority")
    if receipt.get("state") != "VALIDATED":
        fail("import receipt is not VALIDATED")
    if receipt.get("historical_task") != "SITE-0001-GENERATED-STEGPAY-PROPAGATION-IMPORT":
        fail("historical task identity drift")
    if receipt.get("historical_task_state") != "COMPLETE":
        fail("historical completed task was reopened")
    if receipt.get("event_id") != packet.get("event_id") or receipt.get("provider_id") != packet.get("provider_id"):
        fail("receipt identity mismatch")

    print("GENERATED_STEGPAY_SITE_IMPORT=PASS")
    print(f"packet_hash={packet_hash}")
    print(f"consumer_receipt_hash={EXPECTED_CONSUMER_RECEIPT_HASH}")
    print(f"generated_utc={EXPECTED_SOURCE_GENERATED_UTC}")
    print(f"event_id={packet['event_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
