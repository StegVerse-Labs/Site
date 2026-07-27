#!/usr/bin/env python3
"""Create a deterministic receipt for a validated TIDC blinded-coder return."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKET_ID = "BCP-2026-07-27-01"
PACKET_SHA256 = "eb393cc621c532951e1712c744a739ea202a7b003fd66d71a7d5155a282299cc"


def fail(message: str) -> None:
    raise SystemExit(f"TIDC_BLINDED_RECEIPT_INVALID: {message}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing return file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    if not isinstance(value, dict):
        fail("top-level return must be an object")
    if value.get("packet_id") != PACKET_ID:
        fail("packet_id mismatch")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("return_json", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--received-at", help="RFC3339 timestamp; defaults to current UTC time")
    args = parser.parse_args()

    returned = load_json(args.return_json)
    canonical = canonical_bytes(returned)
    raw = args.return_json.read_bytes()
    received_at = args.received_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    receipt = {
        "schema": "stegverse.site.tidc.blinded_return_receipt.v0.1",
        "packet_id": PACKET_ID,
        "receipt_posture": "RECEIVED_NOT_ADJUDICATED",
        "coder_type": "blinded AI",
        "human_replication": False,
        "received_at": received_at,
        "source_file": args.return_json.as_posix(),
        "packet_sha256": PACKET_SHA256,
        "return_raw_sha256": sha256_hex(raw),
        "return_canonical_sha256": sha256_hex(canonical),
        "record_count": len(returned.get("records", [])),
        "independence_statement": returned.get("coder_independence_statement"),
        "authority_effect": "NONE",
        "adjudication_status": "PENDING",
        "interpretation_boundary": [
            "Receipt generation establishes file integrity and intake chronology only.",
            "The receipt does not establish coder independence beyond the supplied statement.",
            "The receipt does not establish reliability, validity, replication, or confirmation.",
            "The original return must be preserved without silent repair or normalization.",
        ],
    }
    receipt["receipt_sha256"] = sha256_hex(canonical_bytes(receipt))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("TIDC_BLINDED_RETURN_RECEIPT_CREATED")
    print(f"receipt={args.out} return_sha256={receipt['return_raw_sha256']}")


if __name__ == "__main__":
    main()
