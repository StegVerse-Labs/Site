#!/usr/bin/env python3
"""Verify StegVerse AI Entry API wrapper stays disabled by default."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))

from ecosystem_chat_api_wrapper import handle_request


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_API_WRAPPER_FAIL: {message}")


def main() -> int:
    default = handle_request("Compare SDK access with ChatGPT")
    activation = default.get("activation", {})
    if activation.get("live_provider_calls_enabled") is not False:
        fail("providers must be disabled by default")
    if activation.get("live_sdk_calls_enabled") is not False:
        fail("SDK must be disabled by default")
    if activation.get("provider_calls_performed") is not False:
        fail("provider calls must not be performed")
    if activation.get("sdk_calls_performed") is not False:
        fail("SDK calls must not be performed")
    if default.get("governance", {}).get("authority_issued") is not False:
        fail("wrapper must not issue authority")

    requested = handle_request("SDK integration", allow_live_providers=True, allow_live_sdk=True)
    requested_activation = requested.get("activation", {})
    if requested_activation.get("live_provider_calls_enabled") is not True:
        fail("provider request flag should be visible")
    if requested_activation.get("live_sdk_calls_enabled") is not True:
        fail("SDK request flag should be visible")
    if requested_activation.get("provider_calls_performed") is not False:
        fail("provider calls must still not be performed")
    if requested_activation.get("sdk_calls_performed") is not False:
        fail("SDK calls must still not be performed")
    if "Activation boundary" not in requested.get("route_guidance", ""):
        fail("requested live flags must add activation boundary guidance")

    print("ECOSYSTEM_CHAT_API_WRAPPER_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
