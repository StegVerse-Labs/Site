#!/usr/bin/env python3
"""Verify governed backend activation boundary is defined and remains non-executing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "data" / "ai-entry-backend-activation-boundary.json"
REQUIRED_FALSE = (
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "credential_surface_enabled",
    "execution_authority_issued",
    "real_receipt_issued",
    "repo_mutation_from_chat_enabled",
    "activation_request_executes",
)
REQUIRED_TARGETS = (
    "activation route model",
    "backend adapter request fixture",
    "backend adapter response fixture",
    "activation boundary verifier",
    "UI route to activation guidance",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_BACKEND_ACTIVATION_BOUNDARY_FAIL: {message}")


def main() -> int:
    data = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.backend_activation_boundary.v0.1":
        fail("bad schema version")
    if data.get("state") != "boundary_defined_live_disabled":
        fail("state must remain boundary_defined_live_disabled")
    activation_boundary = data.get("activation_boundary", {})
    for key in ("entry_surface", "browser_adapter", "backend_scaffold", "api_wrapper", "activation_request_schema"):
        if not activation_boundary.get(key):
            fail(f"missing activation boundary field: {key}")
    contract = data.get("non_executing_contract", {})
    for key in REQUIRED_FALSE:
        if contract.get(key) is not False:
            fail(f"{key} must be false")
    if tuple(data.get("next_build_targets", [])) != REQUIRED_TARGETS:
        fail("next build targets mismatch")
    print("AI_ENTRY_BACKEND_ACTIVATION_BOUNDARY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
