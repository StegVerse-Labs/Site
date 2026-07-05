#!/usr/bin/env python3
"""Verify AI Entry next-path gate keeps live paths disabled until visible green exists."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data" / "ai-entry-next-path-gate.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_NEXT_PATH_GATE_FAIL: {message}")


def main() -> int:
    data = json.loads(GATE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.next_path_gate.v0.1":
        stop("bad schema version")
    if data.get("state") != "watch_mode_green_not_visible":
        stop("state mismatch")
    paths = data.get("available_paths", {})
    if paths.get("visible_green_watch", {}).get("selected") is not True:
        stop("visible green watch must be selected")
    if paths.get("live_activation_design", {}).get("selected") is not False:
        stop("live activation design must not be selected")
    boundary = data.get("current_boundary", {})
    if not boundary:
        stop("boundary missing")
    for key, value in boundary.items():
        if value is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "scheduled visibility recheck index":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_NEXT_PATH_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
