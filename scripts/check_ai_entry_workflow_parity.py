#!/usr/bin/env python3
"""Verify AI Entry workflow parity index and local Site workflow/mirror commands."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-workflow-parity.json"
SITE_CANONICAL = ROOT / ".github" / "workflows" / "validate.yml"
SITE_MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate.yml"
SITE_COMMAND = "python scripts/check_ecosystem_chat_application.py"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_WORKFLOW_PARITY_FAIL: {message}")


def main() -> int:
    if not INDEX.exists():
        fail("missing workflow parity index")
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.workflow_parity.v0.1":
        fail("bad schema version")
    repos = data.get("repos", {})
    if set(repos) != EXPECTED_REPOS:
        fail("repo set mismatch")
    for repo, spec in repos.items():
        if spec.get("parity_expected") is not True:
            fail(f"{repo} parity_expected must be true")
        if not spec.get("canonical") or not spec.get("mirror") or not spec.get("command"):
            fail(f"{repo} missing workflow parity fields")
    for path in (SITE_CANONICAL, SITE_MIRROR):
        text = path.read_text(encoding="utf-8")
        if SITE_COMMAND not in text:
            fail(f"{path.relative_to(ROOT)} missing Site application validation command")
        if "workflow_dispatch" not in text:
            fail(f"{path.relative_to(ROOT)} missing workflow_dispatch")
    boundary = data.get("current_boundary", {})
    for key in ("workflow_count_exceeds_two", "live_provider_calls_enabled", "live_sdk_calls_enabled", "execution_authority_issued"):
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_WORKFLOW_PARITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
