#!/usr/bin/env python3
"""Verify AI Entry cross-repo release readiness index."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-release-readiness.json"
REQUIRED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RELEASE_READINESS_FAIL: {message}")


def main() -> int:
    if not INDEX.exists():
        fail("missing readiness index")
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.release_readiness.v0.1":
        fail("bad schema version")
    if set(data.get("repo_set_required_now", [])) != REQUIRED_REPOS:
        fail("repo set mismatch")
    if data.get("repo_set_sufficient_for_preview") is not True:
        fail("repo set must be sufficient for preview")
    if data.get("future_backend_repo_required_now") is not False:
        fail("future backend repo must not be required now")

    commands = data.get("canonical_commands", {})
    expected_commands = {
        "StegVerse-Labs/Site": "python scripts/check_ecosystem_chat_ai_entry.py",
        "StegVerse-org/LLM-adapter": "python scripts/verify_goal4.py",
        "StegVerse-org/StegVerse-SDK": "python scripts/verify_goal4.py",
    }
    if commands != expected_commands:
        fail("canonical commands mismatch")

    local_status = data.get("repo_local_status", {})
    for repo in REQUIRED_REPOS:
        status = local_status.get(repo, {})
        for key in ("workflow_wired", "ios_mirror_present", "manual_verification_gap_closed"):
            if status.get(key) is not True:
                fail(f"{repo}.{key} must be true")

    boundary = data.get("current_boundary", {})
    for key in (
        "live_provider_calls_enabled",
        "live_sdk_calls_enabled",
        "execution_authority_issued",
        "real_receipt_issued",
        "credential_surface_enabled",
    ):
        if boundary.get(key) is not False:
            fail(f"{key} must be false")

    print("AI_ENTRY_RELEASE_READINESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
