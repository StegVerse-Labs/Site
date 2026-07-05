#!/usr/bin/env python3
"""Verify governed backend activation path progress remains live-disabled."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "data" / "ai-entry-backend-activation-progress.json"
COMPLETED = (
    "activation_boundary_contract",
    "activation_route_model",
    "backend_activation_request_fixture",
    "backend_activation_response_fixture",
    "ui_activation_guidance_routes",
)
REMAINING = (
    "handoff_sync",
    "final_green_run_confirmation",
    "governed_live_authority_service",
    "receipt_issuer_boundary",
    "provider_capture_boundary",
    "sdk_access_decision_boundary",
    "operator_recoverability_boundary",
)
BOUNDARY_FALSE = (
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "credential_surface_enabled",
    "execution_authority_issued",
    "real_receipt_issued",
    "repo_mutation_from_chat_enabled",
    "activation_request_executes",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_BACKEND_ACTIVATION_PROGRESS_FAIL: {message}")


def main() -> int:
    data = json.loads(PROGRESS.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.backend_activation_progress.v0.1":
        fail("bad schema version")
    if data.get("state") != "preview_path_partial_live_disabled":
        fail("state must remain preview_path_partial_live_disabled")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            fail(f"{key} must be complete")
    remaining = data.get("remaining_components", {})
    for key in REMAINING:
        if remaining.get(key) is not True:
            fail(f"{key} must remain listed")
    boundary = data.get("current_boundary", {})
    for key in BOUNDARY_FALSE:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_BACKEND_ACTIVATION_PROGRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
