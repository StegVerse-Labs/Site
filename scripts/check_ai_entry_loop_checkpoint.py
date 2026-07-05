#!/usr/bin/env python3
"""Verify AI Entry loop checkpoint remains file-driven."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-loop-checkpoint.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_LOOP_CHECKPOINT_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.loop_checkpoint.v0.1":
        stop("bad schema version")
    if data.get("state") != "recorded":
        stop("state mismatch")
    if len(data.get("inputs", [])) < 3:
        stop("inputs incomplete")
    outputs = data.get("outputs", {})
    for key in ("green_visible", "tag_ready", "runtime_ready"):
        if outputs.get(key) is not False:
            stop(f"{key} must be false")
    if outputs.get("manual_count") != 0:
        stop("manual count must be zero")
    if outputs.get("path") != "continue":
        stop("path mismatch")
    guards = data.get("guards", {})
    if not guards or any(value is not False for value in guards.values()):
        stop("guards must all be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "loop checkpoint completion":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_LOOP_CHECKPOINT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
