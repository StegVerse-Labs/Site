#!/usr/bin/env python3
"""Verify AI Entry design-only refinement remains blocked on visible green data."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-design-only-refinement.json"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_DESIGN_ONLY_REFINEMENT_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.design_only_refinement.v0.1":
        stop("bad schema version")
    if data.get("state") != "design_only_green_absent":
        stop("state mismatch")
    if len(data.get("source_files", [])) < 3:
        stop("source files incomplete")
    scope = data.get("refinement_scope", {})
    if not scope or any(value is not True for value in scope.values()):
        stop("refinement scope must all be true")
    flags = data.get("readiness_flags", {})
    for key in ("visible_green_data", "ready_for_tag", "ready_for_live_activation"):
        if flags.get(key) is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "design-only refinement completion":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_DESIGN_ONLY_REFINEMENT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
