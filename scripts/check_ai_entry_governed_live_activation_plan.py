#!/usr/bin/env python3
"""Verify governed-live activation plan remains planned and fail-closed."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "ai-entry-governed-live-activation-plan.json"
FORBIDDEN = {
    "live_provider_calls",
    "live_sdk_calls",
    "credential_exposure",
    "real_receipt_issuance",
    "execution_authority_issuance",
    "repo_mutation_from_chat",
}
BOUNDARY_KEYS = (
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "credential_surface_enabled",
    "execution_authority_issued",
    "real_receipt_issued",
    "repo_mutation_from_chat_enabled",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_GOVERNED_LIVE_ACTIVATION_PLAN_FAIL: {message}")


def main() -> int:
    data = json.loads(PLAN.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.governed_live_activation_plan.v0.1":
        fail("bad schema version")
    if data.get("activation_state") != "planned_fail_closed":
        fail("activation state must remain planned_fail_closed")
    if data.get("current_mode") != "local_ready_live_disabled":
        fail("current mode must remain local_ready_live_disabled")
    preconditions = data.get("activation_preconditions", [])
    if len(preconditions) < 5:
        fail("missing activation preconditions")
    for item in preconditions:
        if item.get("required") is not True:
            fail(f"{item.get('name')} must be required")
        if item.get("complete") is not False:
            fail(f"{item.get('name')} must remain incomplete before activation")
    if set(data.get("activation_forbidden_until_preconditions_complete", [])) != FORBIDDEN:
        fail("forbidden activation set mismatch")
    boundary = data.get("current_boundary", {})
    for key in BOUNDARY_KEYS:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_GOVERNED_LIVE_ACTIVATION_PLAN_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
