#!/usr/bin/env python3
"""Validate the archived chat-session launcher goal inventory and merge record."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "session-consolidation" / "chat-session-launcher-session-inventory.json"

REQUIRED_TASKS = {
    "SESSION-CSL-001",
    "SESSION-CSL-002",
    "SESSION-CSL-003",
    "SESSION-ACT-001",
    "SESSION-ACT-002",
    "SESSION-DEP-001",
    "SESSION-CUSTODY-001",
    "SESSION-PROP-001",
    "SESSION-CONSOLIDATION-001",
}

ALLOWED_CLAIM_STATES = {
    "UNCLAIMED",
    "CLAIMED_FOR_IMPLEMENTATION",
    "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION",
    "MACHINE_OWNED",
    "BLOCKED",
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}


def fail(message: str) -> int:
    print(f"CHAT_SESSION_CONSOLIDATION_FAIL: {message}")
    return 1


def main() -> int:
    if not INVENTORY.is_file():
        return fail(f"missing {INVENTORY.relative_to(ROOT)}")

    try:
        payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"inventory is not valid JSON: {type(exc).__name__}")

    if payload.get("record_type") != "session_goal_inventory_and_consolidation":
        return fail("unexpected record_type")
    if payload.get("session_role") != "CONSOLIDATION_ONLY":
        return fail("session role must remain consolidation-only")
    if payload.get("new_implementation_claim_created") is not False:
        return fail("consolidation must not create an implementation claim")

    continuation = payload.get("canonical_continuation")
    if not isinstance(continuation, list) or len(continuation) < 6:
        return fail("canonical continuation locations are incomplete")

    items = payload.get("inventory")
    if not isinstance(items, list):
        return fail("inventory must be a list")
    by_id = {item.get("task_id"): item for item in items if isinstance(item, dict)}
    missing = sorted(REQUIRED_TASKS - set(by_id))
    if missing:
        return fail(f"missing task IDs: {', '.join(missing)}")

    for task_id in REQUIRED_TASKS:
        item = by_id[task_id]
        for field in (
            "originating_goal",
            "destination_repository",
            "branch",
            "location",
            "owner",
            "claim_state",
            "completion_state",
            "validation_state",
            "integration_state",
            "archival_dependency",
            "evidence",
            "next_executable_action",
        ):
            if field not in item:
                return fail(f"{task_id} missing {field}")
        if item["claim_state"] not in ALLOWED_CLAIM_STATES:
            return fail(f"{task_id} has unsupported claim state")
        if item["archival_dependency"] is not False:
            return fail(f"{task_id} still depends on this conversation")

    merge = payload.get("merge_record") or {}
    if merge.get("state") != "MERGED_INTO_CANONICAL_WORKSTREAM":
        return fail("merge record is not canonical-workstream merged")
    if merge.get("archive_safe") is not True:
        return fail("merge record is not archive safe")
    for field in ("transferred", "already_complete", "remaining", "continuation_owner"):
        value = merge.get(field)
        if not isinstance(value, list) or not value:
            return fail(f"merge record missing {field}")

    unresolved = payload.get("unresolved_dependencies")
    if not isinstance(unresolved, list) or not unresolved:
        return fail("unresolved dependencies must remain explicitly assigned")
    for dependency in unresolved:
        if not dependency.get("owner"):
            return fail("unresolved dependency lacks owner")
        if not dependency.get("machine_observable_release_condition"):
            return fail("unresolved dependency lacks release condition")
        if dependency.get("session_unique_information_required") is not False:
            return fail("unresolved dependency still requires conversation state")

    authority = payload.get("authority") or {}
    if any(authority.get(key) is not False for key in ("execution", "activation", "publication", "release")):
        return fail("consolidation record must grant no authority")

    print("CHAT_SESSION_CONSOLIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
