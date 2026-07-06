#!/usr/bin/env python3
"""Verify AI Entry cross-repo promotion record remains non-green until visible runs exist."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "ai-entry-cross-repo-promotion-record.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/StegVerse-SDK",
    "StegVerse-org/LLM-adapter",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_CROSS_REPO_PROMOTION_RECORD_FAIL: {message}")


def main() -> int:
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.cross_repo_promotion_record.v0.1":
        stop("bad schema version")
    if data.get("state") != "promotion_recorded_not_green":
        stop("state mismatch")
    repos = data.get("repos", {})
    if set(repos) != EXPECTED_REPOS:
        stop("repo set mismatch")
    for repo, status in repos.items():
        if not status.get("status"):
            stop(f"{repo} status missing")
        if status.get("visible_run") is not False:
            stop(f"{repo} visible_run must be false")
        if status.get("promotion_ready") is not False:
            stop(f"{repo} promotion_ready must be false")
    for key in ("green_data_promotion", "tag_ready", "live_activation_ready"):
        if data.get(key) is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "cross-repo promotion verifier":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_CROSS_REPO_PROMOTION_RECORD_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
