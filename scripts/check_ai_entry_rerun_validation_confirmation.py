#!/usr/bin/env python3
"""Verify rerun validation confirmation state distinguishes visibility from code failure."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-rerun-validation-confirmation.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RERUN_VALIDATION_CONFIRMATION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.rerun_validation_confirmation.v0.1":
        stop("bad schema version")
    if data.get("state") != "workflow_run_not_connector_visible":
        stop("state mismatch")
    if not data.get("checked_commit"):
        stop("checked commit missing")
    if data.get("workflow_runs_visible") is not False:
        stop("workflow visibility must be false")
    if data.get("known_false_negative_fixed") is not True:
        stop("false negative fix must be recorded")
    if data.get("supported_command_registry_present") is not True:
        stop("supported command registry must be present")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "workflow visibility refresh":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_RERUN_VALIDATION_CONFIRMATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
