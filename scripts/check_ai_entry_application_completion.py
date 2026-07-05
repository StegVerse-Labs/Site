#!/usr/bin/env python3
"""Verify cohesive AI Entry application preview completion remains live-disabled."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-application-completion.json"
REQUIRED_SURFACE = (
    "one_window_entry",
    "stegverse_response_panel",
    "route_essentials_panel",
    "sdk_guidance_panel",
    "governed_live_activation_status_panel",
    "external_llm_comparison_panes",
)
REQUIRED_BOUNDARY_FALSE = (
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "credential_surface_enabled",
    "execution_authority_issued",
    "real_receipt_issued",
    "repo_mutation_from_chat_enabled",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_APPLICATION_COMPLETION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.application_completion.v0.1":
        fail("bad schema version")
    if data.get("state") != "preview_complete_live_disabled":
        fail("state must be preview_complete_live_disabled")
    surface = data.get("application_surface", {})
    for key in REQUIRED_SURFACE:
        if surface.get(key) is not True:
            fail(f"{key} must be true")
    validation = data.get("validation_surface", {})
    if validation.get("application_validator") != "scripts/check_ecosystem_chat_application.py":
        fail("application validator mismatch")
    if validation.get("workflow_command") != "python scripts/check_ecosystem_chat_application.py":
        fail("workflow command mismatch")
    if data.get("remaining_manual_tasks") != []:
        fail("manual tasks remain")
    boundary = data.get("current_boundary", {})
    for key in REQUIRED_BOUNDARY_FALSE:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_APPLICATION_COMPLETION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
