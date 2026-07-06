#!/usr/bin/env python3
"""Verify AI Entry loop checkpoint completion."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-loop-checkpoint-completion.json"
COMPLETED = (
    "loop_checkpoint_index",
    "loop_checkpoint_verifier",
    "site_validation_wired",
)


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_LOOP_CHECKPOINT_COMPLETION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.loop_checkpoint_completion.v0.1":
        stop("bad schema version")
    if data.get("state") != "complete":
        stop("state mismatch")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            stop(f"{key} must be true")
    outputs = data.get("outputs", {})
    for key in ("green_visible", "tag_ready", "runtime_ready"):
        if outputs.get(key) is not False:
            stop(f"{key} must be false")
    if outputs.get("manual_count") != 0:
        stop("manual count must be zero")
    if outputs.get("path") != "continue":
        stop("path mismatch")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "loop cycle record":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_LOOP_CHECKPOINT_COMPLETION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
