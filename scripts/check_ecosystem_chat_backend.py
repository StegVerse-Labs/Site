#!/usr/bin/env python3
"""Verify deterministic Ecosystem Chat backend scaffold behavior."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.ecosystem_chat_backend import build_response

PRECEDENCE_FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "route-precedence-cases.json"

BASE_CASES = [
    ("", "chat_answer", False),
    ("Delete a workflow secret", "restricted_admin", True),
]


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_BACKEND_FAIL: {message}")


def precedence_cases() -> list[tuple[str, str, bool]]:
    payload = json.loads(PRECEDENCE_FIXTURE.read_text(encoding="utf-8"))
    cases: list[tuple[str, str, bool]] = []
    for item in payload.get("cases", []):
        cases.append((str(item["message"]), str(item["expected_route"]), True))
    return cases


def assert_response(message: str, expected_route: str, expected_candidate: bool) -> None:
    response = build_response(message)
    if response.get("primary_route") != expected_route:
        fail(f"{message!r} route {response.get('primary_route')} != {expected_route}")
    governance = response.get("governance", {})
    if governance.get("governed_candidate") is not expected_candidate:
        fail(f"{message!r} governed_candidate mismatch")
    if governance.get("authority_issued") is not False:
        fail(f"{message!r} must not issue authority")
    if governance.get("receipt_id") is not None:
        fail(f"{message!r} preview receipt_id must be null")
    comparisons = response.get("comparison_outputs", [])
    if len(comparisons) != 3:
        fail(f"{message!r} expected three comparison outputs")
    if any(item.get("authority") is not False for item in comparisons):
        fail(f"{message!r} comparison authority must remain false")
    if not response.get("response_id"):
        fail(f"{message!r} missing response_id")
    if not response.get("stegverse_response"):
        fail(f"{message!r} missing StegVerse response")


def main() -> int:
    if not PRECEDENCE_FIXTURE.exists():
        fail("missing route precedence fixture")
    for message, expected_route, expected_candidate in BASE_CASES + precedence_cases():
        assert_response(message, expected_route, expected_candidate)
    print("ECOSYSTEM_CHAT_BACKEND_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
