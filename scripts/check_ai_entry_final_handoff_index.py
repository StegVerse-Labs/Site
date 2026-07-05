#!/usr/bin/env python3
"""Verify AI Entry final handoff index is complete and archive-ready."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-final-handoff-index.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_FINAL_HANDOFF_INDEX_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.final_handoff_index.v0.1":
        stop("bad schema version")
    if data.get("state") != "handoff_index_complete":
        stop("state mismatch")
    for key in ("source_of_truth_files", "validation_files"):
        values = data.get(key, [])
        if len(values) < 6:
            stop(f"{key} is incomplete")
        for value in values:
            if not value:
                stop(f"{key} has blank entry")
    commands = data.get("cross_repo_commands", {})
    if set(commands) != EXPECTED_REPOS:
        stop("repo command set mismatch")
    if not all(commands.values()):
        stop("blank command found")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("archive_ready") is not True:
        stop("archive_ready must be true")
    if data.get("next_goal_candidate") != "visible-green-watch-or-live-activation-design":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_FINAL_HANDOFF_INDEX_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
