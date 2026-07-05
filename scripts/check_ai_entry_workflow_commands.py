#!/usr/bin/env python3
"""Verify declared AI Entry workflow commands match the current repo contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-workflow-parity.json"
EXPECTED = {
    "StegVerse-Labs/Site": "python scripts/check_ecosystem_chat_ai_entry_full.py",
    "StegVerse-org/LLM-adapter": "python scripts/verify_goal4_full.py",
    "StegVerse-org/StegVerse-SDK": "python scripts/verify_goal4.py",
}


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_WORKFLOW_COMMANDS_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    repos = data.get("repos", {})
    for repo, command in EXPECTED.items():
        spec = repos.get(repo)
        if not spec:
            fail(f"missing repo: {repo}")
        if spec.get("command") != command:
            fail(f"{repo} command mismatch")
    if set(repos) != set(EXPECTED):
        fail("unexpected repo set")
    print("AI_ENTRY_WORKFLOW_COMMANDS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
