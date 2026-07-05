#!/usr/bin/env python3
"""Verify AI Entry no-manual-task automation closure index."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-automation-closure.json"
EXPECTED_ITEMS = {
    "route_precedence",
    "site_full_wrapper",
    "adapter_dependency_isolation",
    "sdk_import_and_pytest_compatibility",
}


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_AUTOMATION_CLOSURE_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.automation_closure.v0.1":
        fail("bad schema version")
    items = data.get("closure_items", [])
    names = {item.get("name") for item in items}
    if names != EXPECTED_ITEMS:
        fail("closure item mismatch")
    for item in items:
        if item.get("status") != "self_verified":
            fail(f"{item.get('name')} is not self_verified")
        if not item.get("repo") or not item.get("checks"):
            fail(f"{item.get('name')} missing repo/checks")
    if data.get("manual_tasks_remaining") != []:
        fail("manual tasks remain")
    boundary = data.get("current_boundary", {})
    for key in ("live_provider_calls_enabled", "live_sdk_calls_enabled", "execution_authority_issued", "real_receipt_issued", "workflow_count_exceeds_two"):
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_AUTOMATION_CLOSURE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
