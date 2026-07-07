#!/usr/bin/env python3
"""Verify AI Entry visibility refresh index does not promote without visible runs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-visibility-refresh-index.json"
EXPECTED = {"StegVerse-Labs/Site", "StegVerse-org/StegVerse-SDK", "StegVerse-org/LLM-adapter"}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_VISIBILITY_REFRESH_INDEX_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.visibility_refresh_index.v0.1":
        stop("bad schema version")
    if data.get("state") != "refresh_index_recorded_not_green":
        stop("state mismatch")
    repos = data.get("tracked_repos", {})
    if set(repos) != EXPECTED:
        stop("tracked repo set mismatch")
    for repo, value in repos.items():
        if not value.get("latest_known_state"):
            stop(f"{repo} state missing")
        if value.get("visible_run") is not False:
            stop(f"{repo} visible_run must be false")
    if data.get("promotion_allowed") is not False:
        stop("promotion must remain false")
    if data.get("tag_allowed") is not False:
        stop("tag must remain false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    print("AI_ENTRY_VISIBILITY_REFRESH_INDEX_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
