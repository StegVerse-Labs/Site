#!/usr/bin/env python3
"""Verify governed-live activation request fixture remains fail-closed."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ai-entry-governed-live-activation-request.schema.json"
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "governed-live-activation-request.example.json"


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_GOVERNED_LIVE_ACTIVATION_REQUEST_FAIL: {message}")


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if schema.get("properties", {}).get("schema_version", {}).get("const") != fixture.get("schema_version"):
        fail("schema version mismatch")
    scope = fixture.get("scope", {})
    if scope.get("live_calls_requested") is not False:
        fail("live calls must not be requested by preview fixture")
    for item in fixture.get("preconditions", []):
        if item.get("satisfied") is not False:
            fail(f"precondition must remain unsatisfied: {item.get('name')}")
    authority = fixture.get("authority_boundary", {})
    for key in ("authority_issued", "execution_allowed", "credential_access_allowed"):
        if authority.get(key) is not False:
            fail(f"{key} must be false")
    fail_closed = fixture.get("fail_closed_boundary", {})
    if fail_closed.get("default_decision") != "DENY":
        fail("default decision must be DENY")
    if fail_closed.get("recovery_required") is not True:
        fail("recovery must be required")
    if fail_closed.get("manual_override_allowed") is not False:
        fail("manual override must be false")
    print("AI_ENTRY_GOVERNED_LIVE_ACTIVATION_REQUEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
