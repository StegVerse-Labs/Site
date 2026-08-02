#!/usr/bin/env python3
"""Validate the canonical two-entry-point execution registry.

The validator is intentionally fail-closed. It rejects duplicate task identifiers,
indefinite or conflicting claims, incomplete ownership metadata, false completion,
and archive states that are not supported by completed or actually transferred work.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "two-entry-points-execution-state.json"
RECEIPT_PATH = ROOT / "reports" / "two-entry-points-execution-state-validation.json"

CLAIM_STATES = {
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
COMPLETION_STATES = {
    "MISSING",
    "SCAFFOLDING",
    "PARTIALLY_IMPLEMENTED",
    "IMPLEMENTED_UNVALIDATED",
    "IN_PROGRESS",
    "BLOCKED",
    "COMPLETE",
    "SUPERSEDED",
    "MERGED",
}
TERMINAL_CLAIMS = {"COMPLETE", "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"}
ACTIVE_CLAIMS = {
    "CLAIMED_FOR_IMPLEMENTATION",
    "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION",
    "MACHINE_OWNED",
}
REQUIRED_TASK_FIELDS = {
    "task_id",
    "goal",
    "repository",
    "branch",
    "location",
    "owner",
    "claim_state",
    "completion_state",
    "validation_state",
    "integration_state",
    "evidence",
    "blocker",
    "release_condition",
    "next_action",
}
REQUIRED_TASK_IDS = {"ECP-001", "ECP-002", "VACP-001", "CONS-001"}


def canonical_sha(value: dict[str, Any]) -> str:
    material = dict(value)
    material.pop("receipt_sha256", None)
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require_nonempty(task: dict[str, Any], field: str, errors: list[str]) -> None:
    value = task.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(errors, f"{task.get('task_id', '<unknown>')}:{field}_missing")


def collision_key(task: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(task.get("repository", "")).strip(),
        str(task.get("branch", "")).strip(),
        str(task.get("location", "")).strip().lower(),
    )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        state = {}
        fail(errors, "execution_state_missing")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        state = {}
        fail(errors, "execution_state_unreadable")

    if state.get("schema") != "stegverse.two_entry_points.execution_state.v1":
        fail(errors, "schema_invalid")
    if state.get("canonical_issue") != "StegVerse-Labs/Site#152":
        fail(errors, "canonical_issue_invalid")
    if not isinstance(state.get("originating_goal"), str) or not state["originating_goal"].strip():
        fail(errors, "originating_goal_missing")

    archive_state = state.get("archive_state")
    if archive_state not in {
        "ACTIVE_UNIQUE_WORK_REMAINS",
        "ACTIVE_DISTINCT_SUPPORT_WORK_REMAINS",
        "BLOCKED_UNIQUE_WORK_REMAINS",
        "MERGED_INTO_CANONICAL_WORKSTREAM",
        "COMPLETE_ARCHIVE",
    }:
        fail(errors, "archive_state_invalid")

    tasks = state.get("tasks")
    if not isinstance(tasks, list):
        tasks = []
        fail(errors, "tasks_not_list")

    seen_ids: set[str] = set()
    active_locations: dict[tuple[str, str, str], str] = {}
    complete_or_transferred = 0

    for raw in tasks:
        if not isinstance(raw, dict):
            fail(errors, "task_not_object")
            continue
        task = raw
        missing_fields = sorted(REQUIRED_TASK_FIELDS - set(task))
        if missing_fields:
            fail(errors, f"{task.get('task_id', '<unknown>')}:missing_fields:{','.join(missing_fields)}")

        for field in (
            "task_id",
            "goal",
            "repository",
            "branch",
            "location",
            "owner",
            "validation_state",
            "integration_state",
            "release_condition",
            "next_action",
        ):
            require_nonempty(task, field, errors)

        task_id = str(task.get("task_id", ""))
        if task_id in seen_ids:
            fail(errors, f"duplicate_task_id:{task_id}")
        seen_ids.add(task_id)

        claim_state = task.get("claim_state")
        completion_state = task.get("completion_state")
        if claim_state not in CLAIM_STATES:
            fail(errors, f"{task_id}:claim_state_invalid:{claim_state}")
        if completion_state not in COMPLETION_STATES:
            fail(errors, f"{task_id}:completion_state_invalid:{completion_state}")

        evidence = task.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
            fail(errors, f"{task_id}:evidence_missing")

        blocker = task.get("blocker")
        if completion_state not in {"COMPLETE", "SUPERSEDED", "MERGED"}:
            if not isinstance(blocker, str) or not blocker.strip():
                fail(errors, f"{task_id}:blocker_missing_for_incomplete_task")

        if claim_state in ACTIVE_CLAIMS:
            owner = str(task.get("owner", "")).strip()
            if not owner:
                fail(errors, f"{task_id}:active_claim_without_owner")
            key = collision_key(task)
            prior = active_locations.get(key)
            if prior and prior != task_id:
                fail(errors, f"active_claim_collision:{prior}:{task_id}")
            active_locations[key] = task_id

        if claim_state in TERMINAL_CLAIMS or completion_state in {"COMPLETE", "SUPERSEDED", "MERGED"}:
            complete_or_transferred += 1

        if completion_state == "COMPLETE":
            validation_state = str(task.get("validation_state", ""))
            integration_state = str(task.get("integration_state", ""))
            if "PENDING" in validation_state or "UNVERIFIED" in validation_state:
                fail(errors, f"{task_id}:false_complete_validation")
            if "PENDING" in integration_state or "PARTIAL" in integration_state:
                fail(errors, f"{task_id}:false_complete_integration")

    missing_ids = sorted(REQUIRED_TASK_IDS - seen_ids)
    if missing_ids:
        fail(errors, f"required_tasks_missing:{','.join(missing_ids)}")

    authority = state.get("authority_boundary")
    if not isinstance(authority, dict) or not authority:
        fail(errors, "authority_boundary_missing")
    elif any(value is not False for value in authority.values()):
        fail(errors, "authority_boundary_escalation")

    all_terminal = bool(tasks) and complete_or_transferred == len(tasks)
    if archive_state == "COMPLETE_ARCHIVE" and not all_terminal:
        fail(errors, "false_archive_state_incomplete_tasks")
    if archive_state == "MERGED_INTO_CANONICAL_WORKSTREAM" and not all_terminal:
        fail(errors, "false_merged_state_incomplete_tasks")
    if all_terminal and archive_state in {
        "ACTIVE_UNIQUE_WORK_REMAINS",
        "ACTIVE_DISTINCT_SUPPORT_WORK_REMAINS",
        "BLOCKED_UNIQUE_WORK_REMAINS",
    }:
        warnings.append("all_tasks_terminal_but_archive_state_active")

    result = "PASS" if not errors else "FAIL"
    receipt: dict[str, Any] = {
        "schema": "stegverse.two_entry_points.execution_state_validation.v1",
        "repository": "StegVerse-Labs/Site",
        "source": str(STATE_PATH.relative_to(ROOT)),
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "result": result,
        "task_count": len(tasks),
        "required_task_ids": sorted(REQUIRED_TASK_IDS),
        "observed_task_ids": sorted(seen_ids),
        "complete_or_transferred_tasks": complete_or_transferred,
        "archive_state": archive_state,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "authority_granted": False,
        "release_authorized": False,
        "archive_authorized": result == "PASS" and archive_state == "COMPLETE_ARCHIVE" and all_terminal,
    }
    receipt["receipt_sha256"] = canonical_sha(receipt)
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"TWO ENTRY POINTS EXECUTION STATE: {result}")
    print(f"Tasks: {len(tasks)}")
    print(f"Errors: {', '.join(receipt['errors']) or 'none'}")
    print(f"Receipt: {RECEIPT_PATH.relative_to(ROOT)}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
