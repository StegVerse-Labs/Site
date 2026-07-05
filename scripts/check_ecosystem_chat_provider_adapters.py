#!/usr/bin/env python3
"""Verify Ecosystem Chat provider adapters remain disabled and comparison-only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "ecosystem-chat-provider-adapters.json"
SCHEMA = ROOT / "schemas" / "ecosystem-chat-provider-adapter.schema.json"
REQUIRED_PROVIDERS = {"ChatGPT", "Claude", "Other LLM"}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_PROVIDER_ADAPTERS_FAIL: {message}")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if not MANIFEST.exists():
        fail("missing provider adapter manifest")
    if not SCHEMA.exists():
        fail("missing provider adapter schema")

    manifest = read_json(MANIFEST)
    providers = manifest.get("providers")
    if not isinstance(providers, list) or not providers:
        fail("providers must be a non-empty list")

    names = {provider.get("provider") for provider in providers if isinstance(provider, dict)}
    if names != REQUIRED_PROVIDERS:
        fail(f"provider set mismatch: {sorted(names)}")

    for provider in providers:
        name = provider.get("provider")
        if provider.get("schema_version") != "stegverse.ecosystem_chat.provider_adapter.v0.1":
            fail(f"{name} bad schema_version")
        if provider.get("enabled") is not False:
            fail(f"{name} must be disabled")
        if provider.get("authority") is not False:
            fail(f"{name} must not have authority")
        if provider.get("live_call_allowed") is not False:
            fail(f"{name} live calls must be disallowed")
        if provider.get("comparison_only") is not True:
            fail(f"{name} must remain comparison-only")
        if not provider.get("output_label"):
            fail(f"{name} missing output_label")
        requirements = provider.get("activation_requirements")
        if not isinstance(requirements, list) or not requirements:
            fail(f"{name} missing activation requirements")
        if "comparison-only label retained" not in requirements:
            fail(f"{name} must retain comparison-only label")

    print("ECOSYSTEM_CHAT_PROVIDER_ADAPTERS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
