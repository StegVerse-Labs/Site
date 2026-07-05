#!/usr/bin/env python3
"""Verify Ecosystem Chat SDK access boundary remains disabled by default."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "ecosystem-chat-sdk-access.json"
SCHEMA = ROOT / "schemas" / "ecosystem-chat-sdk-access.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_SDK_ACCESS_FAIL: {message}")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if not MANIFEST.exists():
        fail("missing SDK access manifest")
    if not SCHEMA.exists():
        fail("missing SDK access schema")

    manifest = read_json(MANIFEST)
    if manifest.get("schema_version") != "stegverse.ecosystem_chat.sdk_access.v0.1":
        fail("bad schema_version")
    for key in ("enabled", "access_granted", "credential_surface", "intake_allowed", "execution_allowed"):
        if manifest.get(key) is not False:
            fail(f"{key} must be false by default")
    steps = manifest.get("required_steps")
    if not isinstance(steps, list) or len(steps) < 3:
        fail("required_steps must describe the activation path")
    required_phrases = ["without credentials", "receipt", "separate approval"]
    joined = "\n".join(steps).lower()
    for phrase in required_phrases:
        if phrase not in joined:
            fail(f"required_steps missing phrase: {phrase}")

    print("ECOSYSTEM_CHAT_SDK_ACCESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
