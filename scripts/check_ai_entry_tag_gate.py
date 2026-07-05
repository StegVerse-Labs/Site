#!/usr/bin/env python3
"""Verify AI Entry tag gate waits for visible green data."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data" / "ai-entry-tag-gate.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_TAG_GATE_FAIL: {message}")


def main() -> int:
    data = json.loads(GATE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.tag_gate.v0.1":
        stop("bad schema version")
    if data.get("state") != "waiting_for_visible_green":
        stop("state mismatch")
    inputs = data.get("inputs", {})
    for key in ("release_lockfile", "cross_repo_index", "visibility_index"):
        if inputs.get(key) is not True:
            stop(f"{key} must be true")
    if inputs.get("visible_green") is not False:
        stop("visible green must be false")
    candidate = data.get("candidate", {})
    if candidate.get("ready") is not False:
        stop("candidate must not be ready")
    if not candidate.get("name"):
        stop("candidate name missing")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "site handoff final consolidation":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_TAG_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
