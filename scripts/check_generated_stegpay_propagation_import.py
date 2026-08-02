#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/generated-stegpay-propagations/latest/propagation.json"
RECEIPT = ROOT / "data/generated-stegpay-propagations/latest/import_receipt.json"
EXPECTED_PACKET_HASH = "aecfd09a016e1daaa32b66f0e7aa2bc2681edc70be14f25637fa95df2a1468e3"
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
    if receipt.get("event_id") != packet.get("event_id") or receipt.get("provider_id") != packet.get("provider_id"):
        fail("receipt identity mismatch")

    print("GENERATED_STEGPAY_SITE_IMPORT=PASS")
    print(f"packet_hash={packet_hash}")
    print(f"event_id={packet['event_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
