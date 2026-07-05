#!/usr/bin/env python3
"""Verify AI Entry operator recoverability boundary remains preview-only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "data" / "ai-entry-operator-recoverability-boundary.json"
FALSE_KEYS = (
    "recoverability_confirmed",
    "operator_override_allowed",
    "activation_allowed",
    "execution_allowed",
    "live_provider_calls_allowed",
    "live_sdk_calls_allowed",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_OPERATOR_RECOVERABILITY_BOUNDARY_FAIL: {message}")


def main() -> int:
    data = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.site.ai_entry.operator_recoverability_boundary.v0.1":
        fail("bad schema version")
    if data.get("state") != "boundary_defined_preview_only":
        fail("state must remain boundary_defined_preview_only")
    recoverability = data.get("recoverability_boundary", {})
    if recoverability.get("mode") != "preview_only":
        fail("mode must be preview_only")
    if recoverability.get("default_decision") != "DENY":
        fail("default decision must be DENY")
    contract = data.get("non_executing_contract", {})
    for key in FALSE_KEYS:
        if contract.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_OPERATOR_RECOVERABILITY_BOUNDARY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
