#!/usr/bin/env python3
"""Live-compatible API wrapper for StegVerse AI Entry.

The wrapper intentionally defaults to disabled live behavior. It returns the
same backend response contract as the deterministic local scaffold while making
future activation boundaries explicit.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Any

from ecosystem_chat_backend import build_response

LIVE_PROVIDER_ENV = "STEGVERSE_AI_ENTRY_LIVE_PROVIDERS"
LIVE_SDK_ENV = "STEGVERSE_AI_ENTRY_LIVE_SDK"


def live_enabled(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def handle_request(message: str, *, allow_live_providers: bool = False, allow_live_sdk: bool = False) -> dict[str, Any]:
    response = build_response(message)
    response["activation"] = {
        "live_provider_calls_enabled": bool(allow_live_providers),
        "live_sdk_calls_enabled": bool(allow_live_sdk),
        "provider_calls_performed": False,
        "sdk_calls_performed": False,
        "activation_required_before_live_calls": True,
    }
    if allow_live_providers or allow_live_sdk:
        response["route_guidance"] += (
            "\n\nActivation boundary: live flags were requested, but this wrapper still performs no "
            "provider or SDK calls until governed adapter activation is installed."
        )
    return response


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message", nargs="*", help="Message to route")
    args = parser.parse_args()
    response = handle_request(
        " ".join(args.message),
        allow_live_providers=live_enabled(LIVE_PROVIDER_ENV),
        allow_live_sdk=live_enabled(LIVE_SDK_ENV),
    )
    print(json.dumps(response, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
