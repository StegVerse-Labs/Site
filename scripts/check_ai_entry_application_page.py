#!/usr/bin/env python3
"""Verify the cohesive AI Entry page exposes all required user-facing panes."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegverse-llm-console.html"

REQUIRED_MARKERS = (
    "One StegVerse AI window",
    "StegVerse AI response",
    "Route / ecosystem essentials",
    "SDK / access guidance",
    "Governed-live activation status",
    "ChatGPT comparison",
    "Claude comparison",
    "Other LLM comparison",
    "id=\"activationOutput\"",
    "id=\"activationChips\"",
    "renderActivation(response.activation_status)",
    "window.StegVerseAIEntryAdapter.buildResponse('')",
)

FORBIDDEN_MARKERS = (
    "fetch(\"https://",
    "fetch('https://",
    "localStorage.setItem",
    "navigator.sendBeacon",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_APPLICATION_PAGE_FAIL: {message}")


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            fail(f"page missing marker: {marker}")
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            fail(f"page contains forbidden live/side-effect marker: {marker}")
    print("AI_ENTRY_APPLICATION_PAGE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
