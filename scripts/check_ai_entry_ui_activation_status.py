#!/usr/bin/env python3
"""Verify browser AI Entry adapter exposes fail-closed governed-live activation status."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "assets" / "ecosystem-ai-entry-adapter.js"

REQUIRED_MARKERS = (
    "activation_status",
    "current_mode: 'local_ready_live_disabled'",
    "readiness_state: 'not_ready_fail_closed'",
    "live_provider_calls_enabled: false",
    "live_sdk_calls_enabled: false",
    "credential_surface_enabled: false",
    "execution_authority_issued: false",
    "real_receipt_issued: false",
    "repo_mutation_from_chat_enabled: false",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_UI_ACTIVATION_STATUS_FAIL: {message}")


def main() -> int:
    text = ADAPTER.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            fail(f"browser adapter missing marker: {marker}")
    print("AI_ENTRY_UI_ACTIVATION_STATUS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
