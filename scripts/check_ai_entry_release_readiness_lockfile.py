#!/usr/bin/env python3
"""Verify AI Entry release-readiness lockfile remains preview locked."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCKFILE = ROOT / "data" / "ai-entry-release-readiness-lockfile.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RELEASE_READINESS_LOCKFILE_FAIL: {message}")


def main() -> int:
    data = json.loads(LOCKFILE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.release_readiness_lockfile.v0.1":
        stop("bad schema version")
    if data.get("state") != "preview_locked_live_disabled":
        stop("state mismatch")
    scope = data.get("locked_scope", {})
    if not scope or any(value is not True for value in scope.values()):
        stop("all locked scope values must be true")
    commands = data.get("validation_commands", {})
    if set(commands) != EXPECTED_REPOS:
        stop("validation command repo set mismatch")
    if not all(commands.values()):
        stop("validation command missing")
    live_state = data.get("live_state", {})
    if not live_state:
        stop("live state missing")
    for key, value in live_state.items():
        if value is not False:
            stop(f"{key} must be false")
    if data.get("green_run_confirmed") is not False:
        stop("green run must not be claimed")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("release_tag_ready") is not False:
        stop("release tag must not be ready before green confirmation")
    if data.get("next_goal_candidate") != "tag-readiness gate":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_RELEASE_READINESS_LOCKFILE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
