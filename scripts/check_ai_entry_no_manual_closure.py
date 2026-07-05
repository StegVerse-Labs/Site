#!/usr/bin/env python3
"""Verify AI Entry no-manual closure is file-driven and archive-ready."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-no-manual-closure.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_NO_MANUAL_CLOSURE_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.no_manual_closure.v0.1":
        stop("bad schema version")
    if data.get("state") != "closed_file_driven":
        stop("state mismatch")
    if len(data.get("closed_goal_chain", [])) < 12:
        stop("closed goal chain incomplete")
    if len(data.get("continuation_sources", [])) < 4:
        stop("continuation sources incomplete")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    for key in ("visible_green_data", "ready_for_tag", "ready_for_live_activation"):
        if data.get(key) is not False:
            stop(f"{key} must be false")
    if data.get("archive_ready") is not True:
        stop("archive_ready must be true")
    if data.get("next_goal_candidate") != "monitor visible green data or open new activation design goal":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_NO_MANUAL_CLOSURE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
