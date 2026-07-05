#!/usr/bin/env python3
"""Verify Site AI Entry adapter extension fixture."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ecosystem-chat-adapter-extension.schema.json"
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "adapter-extension.example.json"


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_ADAPTER_EXTENSION_FAIL: {message}")


def require_false(section: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if section.get(key) is not False:
            fail(f"{label}.{key} must be false")


def main() -> int:
    if not SCHEMA.exists():
        fail("missing adapter extension schema")
    if not FIXTURE.exists():
        fail("missing adapter extension fixture")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    status = fixture.get("adapter_status", {})
    require_false(status, ("provider_calls", "provider_authority", "test_secret_required"), "adapter_status")
    if status.get("capture_required_before_activation") is not True:
        fail("adapter_status.capture_required_before_activation must be true")

    preview = fixture.get("preview_marker", {})
    if preview.get("preview_only") is not True:
        fail("preview_marker.preview_only must be true")
    require_false(preview, ("capture_enabled", "record_saved", "authority_granted"), "preview_marker")
    if len(preview.get("input_hash", "")) != 64:
        fail("preview_marker.input_hash must be 64 chars")

    endpoint = fixture.get("endpoint_marker", {})
    require_false(endpoint, ("started", "calls_performed", "side_effects"), "endpoint_marker")

    service = fixture.get("service_marker", {})
    if service.get("wrapper_present") is not True:
        fail("service_marker.wrapper_present must be true")
    require_false(service, ("started_by_import", "calls_enabled", "side_effects_enabled"), "service_marker")

    print("ECOSYSTEM_CHAT_ADAPTER_EXTENSION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
