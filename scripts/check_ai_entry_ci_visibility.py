#!/usr/bin/env python3
"""Verify CI visibility state is explicit and does not imply green when connector-visible runs are absent."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISIBILITY = ROOT / "data" / "ai-entry-ci-visibility.json"
BOUNDARY_FALSE = (
    "treat_ci_as_green",
    "live_provider_calls_enabled",
    "live_sdk_calls_enabled",
    "execution_authority_issued",
    "activation_request_executes",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_CI_VISIBILITY_FAIL: {message}")


def main() -> int:
    data = json.loads(VISIBILITY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.ci_visibility.v0.1":
        fail("bad schema version")
    if data.get("ci_visibility_state") != "not_visible_through_connector":
        fail("visibility state mismatch")
    if data.get("green_run_confirmed") is not False:
        fail("green run must not be confirmed without visible run data")
    if data.get("manual_screenshot_required") is not False:
        fail("manual screenshot must not be required")
    if data.get("local_validator_command") != "python scripts/check_ecosystem_chat_application.py":
        fail("local validator command mismatch")
    checked = data.get("checked_commits", [])
    if len(checked) < 3:
        fail("expected at least three checked commits")
    for item in checked:
        if item.get("combined_status_visible") is not False:
            fail("combined status should be false for recorded connector checks")
        if item.get("workflow_runs_visible") is not False:
            fail("workflow runs should be false for recorded connector checks")
    boundary = data.get("current_boundary", {})
    for key in BOUNDARY_FALSE:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_CI_VISIBILITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
