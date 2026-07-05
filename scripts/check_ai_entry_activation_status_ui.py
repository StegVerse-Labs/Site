#!/usr/bin/env python3
"""Verify browser adapter exposes governed-live activation status fail-closed."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "assets" / "ecosystem-ai-entry-adapter.js"
REQUIRED_MARKERS = (
    "var ACTIVATION_STATUS =",
    "current_mode: 'local_ready_live_disabled'",
    "readiness_state: 'not_ready_fail_closed'",
    "live_provider_calls_enabled: false",
    "live_sdk_calls_enabled: false",
    "credential_surface_enabled: false",
    "execution_authority_issued: false",
    "real_receipt_issued: false",
    "repo_mutation_from_chat_enabled: false",
    "function activationStatus()",
    "activation_status: activationStatus()",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_ACTIVATION_STATUS_UI_FAIL: {message}")


def main() -> int:
    text = ADAPTER.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            fail(f"missing marker: {marker}")
    if text.count("activation_status: activationStatus()") < 2:
        fail("activation status must appear in welcome and routed responses")
    print("AI_ENTRY_ACTIVATION_STATUS_UI_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
