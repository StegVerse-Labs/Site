#!/usr/bin/env python3
"""Verify browser AI Entry adapter exposes governed backend activation guidance routes only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "assets" / "ecosystem-ai-entry-adapter.js"
REQUIRED_MARKERS = (
    "activation_request_preview",
    "activation_boundary_review",
    "activation_guidance",
    "live_calls_enabled: false",
    "live_sdk_calls_enabled: false",
    "credential_surface_enabled: false",
    "execution_authority_issued: false",
    "real_receipt_issued: false",
    "repo_mutation_from_chat_enabled: false",
    "execution_allowed: false",
)
FORBIDDEN_MARKERS = (
    "fetch(",
    "XMLHttpRequest",
    "localStorage.setItem",
    "navigator.sendBeacon",
    "provider_calls: true",
    "authority_issued: true",
    "execution_allowed: true",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_UI_ACTIVATION_ROUTES_FAIL: {message}")


def main() -> int:
    text = ADAPTER.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            fail(f"adapter missing marker: {marker}")
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            fail(f"adapter contains forbidden marker: {marker}")
    print("AI_ENTRY_UI_ACTIVATION_ROUTES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
