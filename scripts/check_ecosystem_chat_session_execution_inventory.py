#!/usr/bin/env python3
"""Validate the canonical Ecosystem Chat session execution inventory."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "ecosystem-chat-session-execution-inventory.json"
REQUIRED_HANDOFFS = {
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/ECOSYSTEM_CHAT_VALUE_MIRROR_HANDOFF.md",
    "docs/ECOSYSTEM_CHAT_ASPECTS_MIRROR_HANDOFF.md",
    "docs/ECOSYSTEM_CHAT_SESSION_CONSOLIDATION.md",
}
VALID_CLAIM_STATES = {
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
ACTIVE_STATES = {"CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION"}
TERMINAL_STATES = {"COMPLETE", "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_time(value: Any, label: str) -> datetime:
    require(isinstance(value, str) and value, f"{label} required")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, f"{label} must include timezone")
    return parsed.astimezone(timezone.utc)


def main() -> int:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    require(payload.get("schema") == "stegverse.session-execution-inventory.v0.1", "unsupported inventory schema")
    require(payload.get("canonical_repository") == "StegVerse-Labs/Site", "canonical repository mismatch")
    require(payload.get("canonical_branch") == "feature/ecosystem-node-dual-view", "canonical branch mismatch")
    require(set(payload.get("canonical_handoffs", [])) == REQUIRED_HANDOFFS, "canonical handoff set mismatch")

    claim_policy = payload.get("claim_policy")
    require(isinstance(claim_policy, dict), "claim_policy required")
    require(set(claim_policy.get("statuses", [])) == VALID_CLAIM_STATES, "claim policy statuses mismatch")
    require(isinstance(claim_policy.get("stale_after_hours"), int) and claim_policy["stale_after_hours"] > 0, "stale_after_hours invalid")

    tasks = payload.get("tasks")
    require(isinstance(tasks, list) and tasks, "tasks required")
    seen_ids: set[str] = set()
    collision_owners: dict[str, str] = {}
    active_claims = 0
    blocked = 0
    complete = 0
    archival_dependencies = 0
    now = datetime.now(timezone.utc)

    for task in tasks:
        require(isinstance(task, dict), "task must be object")
        task_id = task.get("task_id")
        require(isinstance(task_id, str) and task_id, "task_id required")
        require(task_id not in seen_ids, f"duplicate task_id: {task_id}")
        seen_ids.add(task_id)

        for field in [
            "originating_goal",
            "destination_repository",
            "branch",
            "location",
            "owner",
            "claim_state",
            "completion_state",
            "validation_state",
            "integration_state",
            "next_action",
        ]:
            require(isinstance(task.get(field), str) and task[field], f"{task_id}: {field} required")
        require(task["claim_state"] in VALID_CLAIM_STATES, f"{task_id}: invalid claim_state")
        require(isinstance(task.get("archival_dependency"), bool), f"{task_id}: archival_dependency must be bool")
        require(isinstance(task.get("evidence_refs"), list), f"{task_id}: evidence_refs must be list")

        if task["archival_dependency"]:
            archival_dependencies += 1

        if task["claim_state"] in ACTIVE_STATES:
            active_claims += 1
            created = parse_time(task.get("claim_created_at"), f"{task_id}.claim_created_at")
            expires = parse_time(task.get("claim_expires_at"), f"{task_id}.claim_expires_at")
            require(created <= expires, f"{task_id}: claim expires before creation")
            require(isinstance(task.get("claim_release_condition"), str) and task["claim_release_condition"], f"{task_id}: release condition required")
            require(isinstance(task.get("collision_boundaries"), list) and task["collision_boundaries"], f"{task_id}: collision boundaries required")
            for boundary in task["collision_boundaries"]:
                require(isinstance(boundary, str) and boundary, f"{task_id}: invalid collision boundary")
                existing = collision_owners.get(boundary)
                require(existing is None or existing == task_id, f"claim collision: {boundary} owned by {existing} and {task_id}")
                collision_owners[boundary] = task_id
            if expires < now:
                require(task.get("claim_state") == "BLOCKED", f"{task_id}: stale active claim must be released or blocked")

        if task["claim_state"] == "BLOCKED":
            blocked += 1
            require(isinstance(task.get("blocker"), str) and task["blocker"], f"{task_id}: blocker required")
            require(isinstance(task.get("release_condition"), str) and task["release_condition"], f"{task_id}: release_condition required")

        if task["claim_state"] in TERMINAL_STATES:
            complete += 1
            require(task["evidence_refs"], f"{task_id}: terminal task requires evidence")
            require(task["next_action"] == "none" or task["claim_state"] != "COMPLETE", f"{task_id}: completed task should have next_action none")

        if task["completion_state"] == "missing":
            require(task["claim_state"] in {"UNCLAIMED", "BLOCKED"}, f"{task_id}: missing task cannot be claimed complete")

    print("ECOSYSTEM_CHAT_SESSION_EXECUTION_INVENTORY_CHECK=PASS")
    print(f"tasks={len(tasks)}")
    print(f"complete_or_merged={complete}")
    print(f"active_claims={active_claims}")
    print(f"blocked={blocked}")
    print(f"archival_dependencies={archival_dependencies}")
    print("claim_collisions=0")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
