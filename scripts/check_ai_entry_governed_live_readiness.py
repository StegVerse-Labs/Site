#!/usr/bin/env python3
"""Verify governed-live readiness status remains fail-closed until gates are complete."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "ai-entry-governed-live-readiness.json"
REQUIRED_FALSE_BOUNDARY = (
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "credential_surface_enabled",
    "execution_authority_issued",
    "real_receipt_issued",
    "repo_mutation_from_chat_enabled",
)
REQUIRED_PUBLIC_FIELDS = (
    "show_activation_status",
    "show_live_disabled_notice",
    "show_authority_not_issued",
    "show_provider_calls_disabled",
    "show_sdk_calls_disabled",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_GOVERNED_LIVE_READINESS_FAIL: {message}")


def main() -> int:
    data = json.loads(READINESS.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.governed_live_readiness.v0.1":
        fail("bad schema version")
    if data.get("current_mode") != "local_ready_live_disabled":
        fail("current mode must remain local_ready_live_disabled")
    if data.get("readiness_state") != "not_ready_fail_closed":
        fail("readiness state must remain not_ready_fail_closed")
    checks = {item.get("name"): item.get("ready") for item in data.get("readiness_checks", [])}
    for name in ("activation_plan_present", "activation_request_schema_present", "activation_request_fixture_present"):
        if checks.get(name) is not True:
            fail(f"{name} must be true")
    for name in ("provider_authority_gate_live", "sdk_authority_gate_live", "receipt_issuer_live", "execution_authority_live", "operator_recoverability_live"):
        if checks.get(name) is not False:
            fail(f"{name} must be false")
    public = data.get("public_surface_fields", {})
    for key in REQUIRED_PUBLIC_FIELDS:
        if public.get(key) is not True:
            fail(f"{key} must be true")
    boundary = data.get("current_boundary", {})
    for key in REQUIRED_FALSE_BOUNDARY:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_GOVERNED_LIVE_READINESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
