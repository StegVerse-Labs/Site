#!/usr/bin/env python3
"""Verify governed backend activation progress remains repository-complete and live-disabled."""
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
    "handoff_sync",
    "governed_live_authority_service_preview",
    "receipt_issuer_boundary_preview",
    "provider_capture_boundary_preview",
    "sdk_access_decision_boundary_preview",
    "operator_recoverability_boundary",
    "cross_repo_handoff_consolidation",
    "automated_green_visibility_monitor",
    "terminal_loop_cycle_record",
)
EXTERNAL_EVIDENCE_FALSE = (
    "connector_visible_green_run",
    "live_provider_observation",
    "live_sdk_observation",
    "live_custody_and_reconstruction",
    "release_authority_receipt",
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
    if data.get("schema_version") != "stegverse.ai_entry.backend_activation_progress.v0.2":
        fail("bad schema version")
    if data.get("state") != "repository_boundaries_complete_live_evidence_pending":
        fail("state must remain repository_boundaries_complete_live_evidence_pending")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            fail(f"{key} must be complete")
    if data.get("remaining_repository_components") != {}:
        fail("remaining_repository_components must be empty")
    evidence = data.get("external_evidence_gates", {})
    for key in EXTERNAL_EVIDENCE_FALSE:
        if evidence.get(key) is not False:
            fail(f"{key} must remain false until observed")
    boundary = data.get("current_boundary", {})
    for key in BOUNDARY_FALSE:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        fail("manual_tasks_remaining must be empty")
    if data.get("archive_ready") is not True:
        fail("archive_ready must remain true")
    print("AI_ENTRY_BACKEND_ACTIVATION_PROGRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
