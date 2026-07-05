#!/usr/bin/env python3
"""Verify governed backend activation routes stay preview-only and non-executing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "data" / "ai-entry-activation-routes.json"
EXPECTED_IDS = {
    "activation_guidance",
    "activation_request_preview",
    "activation_boundary_review",
}
FORBIDDEN = {
    "provider_call",
    "sdk_call",
    "credential_lookup",
    "receipt_issue",
    "execution_authority_issue",
    "repo_mutation",
}
BOUNDARY_FALSE = (
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "credential_surface_enabled",
    "execution_authority_issued",
    "real_receipt_issued",
    "repo_mutation_from_chat_enabled",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_ACTIVATION_ROUTES_FAIL: {message}")


def main() -> int:
    data = json.loads(ROUTES.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.activation_routes.v0.1":
        fail("bad schema version")
    routes = data.get("routes", [])
    if {route.get("id") for route in routes} != EXPECTED_IDS:
        fail("activation route set mismatch")
    for route in routes:
        if route.get("execution_allowed") is not False:
            fail(f"{route.get('id')} execution must be false")
        if route.get("live_calls_allowed") is not False:
            fail(f"{route.get('id')} live calls must be false")
        if not route.get("keywords"):
            fail(f"{route.get('id')} missing keywords")
    if set(data.get("forbidden_during_preview", [])) != FORBIDDEN:
        fail("forbidden preview set mismatch")
    boundary = data.get("current_boundary", {})
    for key in BOUNDARY_FALSE:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_ACTIVATION_ROUTES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
