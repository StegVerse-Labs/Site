#!/usr/bin/env python3
"""Verify AI Entry recovery completion index remains live-disabled."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-recovery-completion.json"
COMPLETED = (
    "site_recoverability_boundary",
    "site_recoverability_boundary_verifier",
    "adapter_recovery_boundary_mirror",
    "adapter_recovery_boundary_verifier",
    "adapter_validation_wired",
)
FALSE_KEYS = (
    "recovery_confirmed",
    "activation_allowed",
    "execution_allowed",
    "live_provider_calls_allowed",
    "live_sdk_calls_allowed",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RECOVERY_COMPLETION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.site.ai_entry.recovery_completion.v0.1":
        fail("bad schema version")
    if data.get("state") != "preview_partial_live_disabled":
        fail("state mismatch")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            fail(f"{key} must be true")
    boundary = data.get("current_boundary", {})
    for key in FALSE_KEYS:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_RECOVERY_COMPLETION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
