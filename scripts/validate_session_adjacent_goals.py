#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "session-adjacent-goals.json"
OUTPUT = ROOT / "reports" / "session-adjacent-goals-validation.json"
ACTIVE = {"CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED"}
TERMINAL = {"COMPLETE", "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"}


def digest(value: dict) -> str:
    material = dict(value)
    material.pop("receipt_sha256", None)
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    errors: list[str] = []
    value = json.loads(SOURCE.read_text())
    if value.get("schema") != "stegverse.session_adjacent_goals.v1":
        errors.append("schema_invalid")
    goals = value.get("goals")
    if not isinstance(goals, list) or not goals:
        errors.append("goals_missing")
        goals = []
    seen: set[str] = set()
    boundaries: dict[str, str] = {}
    now = datetime.now(timezone.utc)
    stale: list[str] = []
    for goal in goals:
        task_id = str(goal.get("task_id", ""))
        if not task_id or task_id in seen:
            errors.append(f"duplicate_or_missing_task_id:{task_id}")
        seen.add(task_id)
        for field in ("originating_session_goal", "repository", "branch", "location", "owner", "claim_state", "claim_created_at", "claim_expires_at", "claim_release_condition", "expected_evidence", "completion_state", "validation_state", "integration_state", "blocker", "machine_observable_release_condition", "next_action", "next_task_after_release"):
            if not str(goal.get(field, "")).strip():
                errors.append(f"{task_id}:{field}_missing")
        if goal.get("archival_dependency") is not True:
            errors.append(f"{task_id}:archival_dependency_not_true")
        evidence = goal.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{task_id}:evidence_missing")
        collision = goal.get("collision_boundaries")
        if not isinstance(collision, list) or not collision:
            errors.append(f"{task_id}:collision_boundaries_missing")
        else:
            for boundary in collision:
                prior = boundaries.get(boundary)
                if prior and prior != task_id:
                    errors.append(f"collision:{prior}:{task_id}:{boundary}")
                boundaries[boundary] = task_id
        if goal.get("claim_state") in ACTIVE:
            try:
                expires = datetime.fromisoformat(str(goal["claim_expires_at"]).replace("Z", "+00:00"))
                if expires <= now:
                    stale.append(task_id)
                    errors.append(f"stale_claim:{task_id}")
            except Exception:
                errors.append(f"{task_id}:claim_expiration_invalid")
        if goal.get("claim_state") in TERMINAL and goal.get("completion_state") not in {"COMPLETE", "SUPERSEDED", "MERGED"}:
            errors.append(f"{task_id}:terminal_claim_without_terminal_completion")
    authority = value.get("authority_boundary")
    if not isinstance(authority, dict) or any(v is not False for v in authority.values()):
        errors.append("authority_boundary_invalid")
    receipt = {
        "schema": "stegverse.session_adjacent_goals_validation.v1",
        "source": str(SOURCE.relative_to(ROOT)),
        "validated_at": now.isoformat(),
        "result": "PASS" if not errors else "FAIL",
        "goal_count": len(goals),
        "observed_task_ids": sorted(seen),
        "stale_claims": sorted(stale),
        "errors": sorted(set(errors)),
        "archive_authorized": False,
        "authority_granted": False
    }
    receipt["receipt_sha256"] = digest(receipt)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(f"SESSION ADJACENT GOALS: {receipt['result']}")
    print(f"Errors: {', '.join(receipt['errors']) or 'none'}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
