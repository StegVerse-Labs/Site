#!/usr/bin/env python3
"""Verify browser adapter carries the same route-priority contract as backend."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "assets" / "ecosystem-ai-entry-adapter.js"
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "route-precedence-cases.json"

REQUIRED_MARKERS = (
    "var ROUTE_PRIORITY =",
    "restricted_admin: 100",
    "sdk_intake_candidate: 90",
    "sdk_access_guidance: 80",
    "runtime_status: 70",
    "llm_comparison: 60",
    "governance_review: 50",
    "documentation_route: 40",
    "ecosystem_explanation: 30",
    "chat_answer: 10",
    "function routeScore",
    "score.matches > bestScore.matches",
    "score.priority > bestScore.priority",
)


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_UI_ROUTE_PRIORITY_FAIL: {message}")


def main() -> int:
    if not ADAPTER.exists():
        fail("missing browser adapter")
    if not FIXTURE.exists():
        fail("missing route precedence fixture")
    text = ADAPTER.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            fail(f"browser adapter missing marker: {marker}")
    print("ECOSYSTEM_CHAT_UI_ROUTE_PRIORITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
