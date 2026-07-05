#!/usr/bin/env python3
"""Verify green-run visibility consolidation is explicit and non-manual."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-green-run-visibility-consolidation.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/StegVerse-SDK",
    "StegVerse-org/LLM-adapter",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_GREEN_RUN_VISIBILITY_CONSOLIDATION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.green_run_visibility_consolidation.v0.1":
        stop("bad schema version")
    if data.get("state") != "not_visible_through_connector":
        stop("state mismatch")
    repos = data.get("checked_repositories", {})
    if set(repos) != EXPECTED_REPOS:
        stop("repo set mismatch")
    for repo, item in repos.items():
        if not item.get("commit_sha"):
            stop(f"{repo} missing commit sha")
        if item.get("workflow_runs_visible") is not False:
            stop(f"{repo} visibility must be false")
        if not item.get("validation_command"):
            stop(f"{repo} missing validation command")
    if data.get("green_run_confirmed") is not False:
        stop("green run must not be claimed")
    if data.get("manual_screenshot_required") is not False:
        stop("manual screenshot must not be required")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "release-readiness lockfile":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_GREEN_RUN_VISIBILITY_CONSOLIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
