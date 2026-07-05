#!/usr/bin/env python3
"""Verify AI Entry cross-repo handoff index remains preview-only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-cross-repo-handoff.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_CROSS_REPO_HANDOFF_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.cross_repo_handoff.v0.1":
        stop("bad schema version")
    if data.get("state") != "preview_consolidated":
        stop("state mismatch")
    repos = data.get("repos", {})
    if set(repos) != EXPECTED_REPOS:
        stop("repo set mismatch")
    for repo, config in repos.items():
        if not config.get("command"):
            stop(f"{repo} missing command")
        if not config.get("ready_items"):
            stop(f"{repo} missing ready items")
    boundary = data.get("boundary", {})
    if not boundary:
        stop("boundary missing")
    for key, value in boundary.items():
        if value is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "green run visibility consolidation":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_CROSS_REPO_HANDOFF_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
