#!/usr/bin/env python3
"""Validate the terminal AI Entry monitor-loop record."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "ai-entry-loop-cycle-record.json"


def main() -> int:
    value = json.loads(RECORD.read_text(encoding="utf-8"))
    failures: list[str] = []

    if value.get("schema_version") != "stegverse.ai_entry.loop_cycle_record.v0.1":
        failures.append("schema_version")
    if value.get("state") not in {"scheduled_monitor_active_green_absent", "green_visible_gates_recomputing"}:
        failures.append("state")

    observed = value.get("observed_posture") or {}
    continuation = value.get("continuation") or {}
    boundary = value.get("authority_boundary") or {}

    if observed.get("manual_task_count") != 0:
        failures.append("manual_task_count")
    if continuation.get("manual_user_action_required") is not False:
        failures.append("manual_user_action_required")
    if continuation.get("recursive_goal_expansion_allowed") is not False:
        failures.append("recursive_goal_expansion_allowed")
    if continuation.get("next_repository_local_goal") is not None:
        failures.append("next_repository_local_goal")
    if value.get("manual_tasks_remaining") != []:
        failures.append("manual_tasks_remaining")
    if value.get("archive_ready") is not True:
        failures.append("archive_ready")

    for key in (
        "record_is_ci_success",
        "record_is_tag_authority",
        "record_is_release_authority",
        "record_is_activation_authority",
        "record_is_execution_authority",
    ):
        if boundary.get(key) is not False:
            failures.append(f"authority_boundary:{key}")

    if failures:
        print("AI_ENTRY_LOOP_CYCLE_RECORD_FAIL: " + ", ".join(failures))
        return 1

    print("AI_ENTRY_LOOP_CYCLE_RECORD_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
