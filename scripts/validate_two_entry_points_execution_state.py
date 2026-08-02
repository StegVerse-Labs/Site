#!/usr/bin/env python3
"""Fail-closed validation for the canonical two-entry-point execution registry."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "two-entry-points-execution-state.json"
RECEIPT_PATH = ROOT / "reports" / "two-entry-points-execution-state-validation.json"

CLAIM_STATES = {
    "UNCLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED", "BLOCKED", "COMPLETE",
    "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM",
}
COMPLETION_STATES = {
    "MISSING", "SCAFFOLDING", "PARTIALLY_IMPLEMENTED", "IMPLEMENTED_UNVALIDATED",
    "IN_PROGRESS", "BLOCKED", "COMPLETE", "SUPERSEDED", "MERGED",
}
ACTIVE_CLAIMS = {
    "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED",
}
TERMINAL_CLAIMS = {"COMPLETE", "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"}
REQUIRED_TASK_IDS = {"ECP-001", "ECP-002", "VACP-001", "CONS-001"}
REQUIRED_TASK_FIELDS = {
    "task_id", "originating_session_goal", "goal", "repository", "branch", "location",
    "owner", "execution_lane", "role", "claim_state", "claim_created_at",
    "claim_expires_at", "claim_release_condition", "expected_evidence",
    "collision_boundaries", "completion_state", "validation_state", "integration_state",
    "archival_dependency", "evidence", "blocker", "release_condition",
    "machine_observable_release_condition", "next_action", "next_task_after_release",
}


def canonical_sha(value: dict[str, Any]) -> str:
    material = dict(value)
    material.pop("receipt_sha256", None)
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def parse_time(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}:timestamp_missing")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label}:timestamp_invalid")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label}:timestamp_not_timezone_aware")
        return None
    return parsed.astimezone(timezone.utc)


def nonempty_string(task: dict[str, Any], field: str, errors: list[str]) -> None:
    if not isinstance(task.get(field), str) or not str(task[field]).strip():
        errors.append(f"{task.get('task_id', '<unknown>')}:{field}_missing")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    now = datetime.now(timezone.utc)

    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        state = {}
        errors.append("execution_state_missing")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        state = {}
        errors.append("execution_state_unreadable")

    if state.get("schema") != "stegverse.two_entry_points.execution_state.v1":
        errors.append("schema_invalid")
    if state.get("canonical_issue") != "StegVerse-Labs/Site#152":
        errors.append("canonical_issue_invalid")
    if not isinstance(state.get("originating_goal"), str) or not state["originating_goal"].strip():
        errors.append("originating_goal_missing")

    archive_state = state.get("archive_state")
    allowed_archive_states = {
        "ACTIVE_UNIQUE_WORK_REMAINS", "ACTIVE_DISTINCT_SUPPORT_WORK_REMAINS",
        "BLOCKED_UNIQUE_WORK_REMAINS", "MERGED_INTO_CANONICAL_WORKSTREAM",
        "COMPLETE_ARCHIVE",
    }
    if archive_state not in allowed_archive_states:
        errors.append("archive_state_invalid")

    policy = state.get("claim_policy")
    if not isinstance(policy, dict):
        errors.append("claim_policy_missing")
        policy = {}
    maximum_hours = policy.get("maximum_claim_hours_without_evidence")
    if not isinstance(maximum_hours, int) or maximum_hours < 1 or maximum_hours > 168:
        errors.append("claim_policy_maximum_hours_invalid")
    if policy.get("handoff_alone_is_transfer") is not False:
        errors.append("claim_policy_false_transfer_allowed")
    for field in ("stale_claim_action", "renewal_requires"):
        if not isinstance(policy.get(field), str) or not policy[field].strip():
            errors.append(f"claim_policy_{field}_missing")

    tasks = state.get("tasks")
    if not isinstance(tasks, list):
        tasks = []
        errors.append("tasks_not_list")

    seen_ids: set[str] = set()
    active_collision_claims: dict[str, str] = {}
    complete_or_transferred = 0
    stale_claims: list[str] = []

    for raw in tasks:
        if not isinstance(raw, dict):
            errors.append("task_not_object")
            continue
        task = raw
        task_id = str(task.get("task_id", "<unknown>"))
        missing = sorted(REQUIRED_TASK_FIELDS - set(task))
        if missing:
            errors.append(f"{task_id}:missing_fields:{','.join(missing)}")

        for field in (
            "task_id", "originating_session_goal", "goal", "repository", "branch", "location",
            "owner", "execution_lane", "role", "claim_release_condition", "expected_evidence",
            "validation_state", "integration_state", "release_condition",
            "machine_observable_release_condition", "next_action", "next_task_after_release",
        ):
            nonempty_string(task, field, errors)

        if task_id in seen_ids:
            errors.append(f"duplicate_task_id:{task_id}")
        seen_ids.add(task_id)

        claim_state = task.get("claim_state")
        completion_state = task.get("completion_state")
        if claim_state not in CLAIM_STATES:
            errors.append(f"{task_id}:claim_state_invalid:{claim_state}")
        if completion_state not in COMPLETION_STATES:
            errors.append(f"{task_id}:completion_state_invalid:{completion_state}")

        created = parse_time(task.get("claim_created_at"), f"{task_id}:claim_created_at", errors)
        expires = parse_time(task.get("claim_expires_at"), f"{task_id}:claim_expires_at", errors)
        if created and expires:
            if expires <= created:
                errors.append(f"{task_id}:claim_expiration_not_after_creation")
            if isinstance(maximum_hours, int) and (expires - created).total_seconds() > maximum_hours * 3600:
                errors.append(f"{task_id}:claim_duration_exceeds_policy")
            if claim_state in ACTIVE_CLAIMS and now >= expires:
                stale_claims.append(task_id)
                errors.append(f"{task_id}:active_claim_stale")

        evidence = task.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
            errors.append(f"{task_id}:evidence_missing")
        boundaries = task.get("collision_boundaries")
        if not isinstance(boundaries, list) or not boundaries or not all(isinstance(x, str) and x.strip() for x in boundaries):
            errors.append(f"{task_id}:collision_boundaries_missing")
            boundaries = []

        if task.get("archival_dependency") is not True:
            errors.append(f"{task_id}:archival_dependency_not_explicit")
        if completion_state not in {"COMPLETE", "SUPERSEDED", "MERGED"}:
            if not isinstance(task.get("blocker"), str) or not task["blocker"].strip():
                errors.append(f"{task_id}:blocker_missing_for_incomplete_task")

        if claim_state in ACTIVE_CLAIMS:
            for boundary in boundaries:
                prior = active_collision_claims.get(boundary)
                if prior and prior != task_id:
                    errors.append(f"active_claim_collision:{prior}:{task_id}:{boundary}")
                active_collision_claims[boundary] = task_id

        if claim_state in TERMINAL_CLAIMS or completion_state in {"COMPLETE", "SUPERSEDED", "MERGED"}:
            complete_or_transferred += 1

        if completion_state == "COMPLETE":
            validation = str(task.get("validation_state", ""))
            integration = str(task.get("integration_state", ""))
            if any(token in validation for token in ("PENDING", "UNVERIFIED", "UNOBSERVED")):
                errors.append(f"{task_id}:false_complete_validation")
            if any(token in integration for token in ("PENDING", "PARTIAL", "UNVERIFIED")):
                errors.append(f"{task_id}:false_complete_integration")

    missing_ids = sorted(REQUIRED_TASK_IDS - seen_ids)
    if missing_ids:
        errors.append(f"required_tasks_missing:{','.join(missing_ids)}")

    authority = state.get("authority_boundary")
    if not isinstance(authority, dict) or not authority:
        errors.append("authority_boundary_missing")
    elif any(value is not False for value in authority.values()):
        errors.append("authority_boundary_escalation")

    all_terminal = bool(tasks) and complete_or_transferred == len(tasks)
    if archive_state in {"COMPLETE_ARCHIVE", "MERGED_INTO_CANONICAL_WORKSTREAM"} and not all_terminal:
        errors.append("false_archive_or_merge_state_incomplete_tasks")
    if all_terminal and archive_state in {
        "ACTIVE_UNIQUE_WORK_REMAINS", "ACTIVE_DISTINCT_SUPPORT_WORK_REMAINS",
        "BLOCKED_UNIQUE_WORK_REMAINS",
    }:
        warnings.append("all_tasks_terminal_but_archive_state_active")

    result = "PASS" if not errors else "FAIL"
    receipt: dict[str, Any] = {
        "schema": "stegverse.two_entry_points.execution_state_validation.v1",
        "repository": "StegVerse-Labs/Site",
        "source": str(STATE_PATH.relative_to(ROOT)),
        "validated_at": now.isoformat(),
        "result": result,
        "task_count": len(tasks),
        "required_task_ids": sorted(REQUIRED_TASK_IDS),
        "observed_task_ids": sorted(seen_ids),
        "complete_or_transferred_tasks": complete_or_transferred,
        "active_claim_count": sum(1 for task in tasks if isinstance(task, dict) and task.get("claim_state") in ACTIVE_CLAIMS),
        "stale_claims": sorted(stale_claims),
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
    print(f"Stale claims: {', '.join(stale_claims) or 'none'}")
    print(f"Errors: {', '.join(receipt['errors']) or 'none'}")
    print(f"Receipt: {RECEIPT_PATH.relative_to(ROOT)}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
