#!/usr/bin/env python3
"""Verify Ecosystem Chat receipt preview stays non-authorizing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ecosystem-chat-receipt-preview.schema.json"
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "receipt-preview.example.json"


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_RECEIPT_PREVIEW_FAIL: {message}")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if not SCHEMA.exists():
        fail("missing receipt preview schema")
    if not FIXTURE.exists():
        fail("missing receipt preview fixture")

    fixture = read_json(FIXTURE)
    if fixture.get("schema_version") != "stegverse.ecosystem_chat.receipt_preview.v0.1":
        fail("bad schema_version")
    if fixture.get("preview_only") is not True:
        fail("receipt preview must be preview_only")
    for key in ("receipt_issued", "authority_issued", "reconstruction_available"):
        if fixture.get(key) is not False:
            fail(f"{key} must be false in preview")
    for key in ("input_hash", "route_id", "response_id"):
        if not fixture.get(key):
            fail(f"{key} required")

    print("ECOSYSTEM_CHAT_RECEIPT_PREVIEW_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
