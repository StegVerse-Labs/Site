#!/usr/bin/env python3
"""Verify AI Entry stable archive checkpoint remains valid."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-stable-archive-checkpoint.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_STABLE_ARCHIVE_CHECKPOINT_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.stable_archive_checkpoint.v0.1":
        stop("bad schema version")
    if data.get("state") != "stable_checkpoint_recorded":
        stop("state mismatch")
    scope = data.get("checkpoint_scope", {})
    if not scope or any(value is not True for value in scope.values()):
        stop("checkpoint scope must all be true")
    if len(data.get("checkpoint_files", [])) < 3:
        stop("checkpoint files incomplete")
    flags = data.get("readiness_flags", {})
    for key in ("visible_green_data", "ready_for_tag", "ready_for_live_activation"):
        if flags.get(key) is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "post-archive green-data monitor":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_STABLE_ARCHIVE_CHECKPOINT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
