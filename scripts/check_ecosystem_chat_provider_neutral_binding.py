#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "assets" / "ecosystem-chat-live-binding.js"

REQUIRED = (
    "verified_provider_neutral_stegverse_node",
    "query:gateway",
    "window.STEGVERSE_ECOSYSTEM_GATEWAY_URL",
    "localStorage",
    "same-origin",
    "loopback",
    "stegverse_ecosystem_gateway_base_url",
    "StegVerse-Labs/Site:ecosystem-chat.html",
    "fetchWithTimeout",
    "mode: 'cors'",
    "health.status !== 'ok'",
    "provider_output_is_authority: false",
    "repository_mutation_authority: false",
    "restricted_requests_execute: false",
)

FORBIDDEN = (
    "discovery: 'verified_loopback_stegverse_node'",
    "const NODE_CANDIDATES = [",
    "external_host_dependency: true",
    "hosting_provider_required: true",
)


def main() -> int:
    if not BINDING.exists():
        raise SystemExit("ECOSYSTEM CHAT PROVIDER-NEUTRAL BINDING: FAIL: missing binding")

    text = BINDING.read_text(encoding="utf-8")
    failures = [f"missing marker: {marker}" for marker in REQUIRED if marker not in text]
    failures.extend(f"forbidden marker present: {marker}" for marker in FORBIDDEN if marker in text)

    if failures:
        print("ECOSYSTEM CHAT PROVIDER-NEUTRAL BINDING: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("ECOSYSTEM CHAT PROVIDER-NEUTRAL BINDING: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
