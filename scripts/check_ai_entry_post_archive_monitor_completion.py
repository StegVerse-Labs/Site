#!/usr/bin/env python3
"""Verify AI Entry post-archive monitor completion remains green-absent."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-post-archive-monitor-completion.json"
COMPLETED = (
    "post_archive_monitor_index",
    "post_archive_monitor_verifier",
    "site_validation_wired",
)


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_POST_ARCHIVE_MONITOR_COMPLETION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.post_archive_monitor_completion.v0.1":
        stop("bad schema version")
    if data.get("state") != "monitor_complete_green_absent":
        stop("state mismatch")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            stop(f"{key} must be true")
    outputs = data.get("monitor_outputs", {})
    for key in ("visible_green_data", "ready_for_tag", "ready_for_live_activation"):
        if outputs.get(key) is not False:
            stop(f"{key} must be false")
    if outputs.get("manual_task_count") != 0:
        stop("manual task count must be zero")
    decision = data.get("continuation_decision", {})
    if decision.get("selected_path") != "continue monitor loop":
        stop("selected path mismatch")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "monitor loop checkpoint":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_POST_ARCHIVE_MONITOR_COMPLETION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
