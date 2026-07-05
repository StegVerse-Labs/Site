#!/usr/bin/env python3
"""Verify AI Entry visibility recheck index is non-manual and non-claiming."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-visibility-recheck-index.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_VISIBILITY_RECHECK_INDEX_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.visibility_recheck_index.v0.1":
        stop("bad schema version")
    if data.get("state") != "recheck_plan_defined":
        stop("state mismatch")
    targets = data.get("recheck_targets", {})
    if set(targets) != EXPECTED_REPOS:
        stop("target repo set mismatch")
    for repo, target in targets.items():
        if not target.get("last_checked_commit"):
            stop(f"{repo} missing commit")
        if not target.get("command"):
            stop(f"{repo} missing command")
    rule = data.get("recheck_rule", {})
    if not rule.get("trigger"):
        stop("trigger missing")
    if rule.get("green_claim_allowed") is not False:
        stop("green claim must remain false")
    if rule.get("manual_screenshot_required") is not False:
        stop("manual screenshot must remain false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "live-activation architecture packet":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_VISIBILITY_RECHECK_INDEX_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
