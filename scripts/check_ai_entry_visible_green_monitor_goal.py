#!/usr/bin/env python3
"""Verify AI Entry visible-green monitor goal remains file-driven."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-visible-green-monitor-goal.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_VISIBLE_GREEN_MONITOR_GOAL_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.visible_green_monitor_goal.v0.1":
        stop("bad schema version")
    if data.get("state") != "monitor_goal_defined":
        stop("state mismatch")
    if len(data.get("source_files", [])) < 4:
        stop("source files incomplete")
    if set(data.get("monitor_targets", {})) != EXPECTED_REPOS:
        stop("monitor target repo set mismatch")
    current = data.get("current_state", {})
    for key in ("visible_green_data", "ready_for_tag", "ready_for_live_activation"):
        if current.get(key) is not False:
            stop(f"{key} must be false")
    if current.get("manual_tasks_remaining") != 0:
        stop("manual task count must be zero")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if not data.get("next_allowed_goal_when_green_visible"):
        stop("green-visible next goal missing")
    if not data.get("next_allowed_goal_without_green"):
        stop("without-green next goal missing")
    print("AI_ENTRY_VISIBLE_GREEN_MONITOR_GOAL_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
