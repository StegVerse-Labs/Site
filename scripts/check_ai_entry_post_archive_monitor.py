#!/usr/bin/env python3
"""Verify AI Entry post-archive monitor remains green-absent and non-manual."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-post-archive-monitor.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_POST_ARCHIVE_MONITOR_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.post_archive_monitor.v0.1":
        stop("bad schema version")
    if data.get("state") != "monitor_active_green_absent":
        stop("state mismatch")
    if data.get("source_checkpoint") != "data/ai-entry-stable-archive-checkpoint.json":
        stop("source checkpoint mismatch")
    if len(data.get("tracked_files", [])) < 4:
        stop("tracked files incomplete")
    outputs = data.get("monitor_outputs", {})
    for key in ("visible_green_data", "ready_for_tag", "ready_for_live_activation"):
        if outputs.get(key) is not False:
            stop(f"{key} must be false")
    if outputs.get("manual_task_count") != 0:
        stop("manual task count must be zero")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if not data.get("next_action_when_green_visible"):
        stop("green-visible action missing")
    if data.get("next_action_when_green_absent") != "continue post archive monitor":
        stop("green-absent action mismatch")
    print("AI_ENTRY_POST_ARCHIVE_MONITOR_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
