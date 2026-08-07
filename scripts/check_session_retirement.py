#!/usr/bin/env python3
"""Validate governed session retirement and archive dispositions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "session-orchestration-registry.json"
HANDOFF = ROOT / "docs" / "SESSION_ORCHESTRATION_MIRROR_HANDOFF.md"
SCHEMA = ROOT / "schemas" / "session-retirement.schema.json"
PROMPT = ROOT / "prompts" / "SESSION_SELF_AUDIT.md"
REPORT = ROOT / "session_retirement.report.json"
POSTURES = {"CURRENT", "SUPERSEDED", "MERGE_REQUIRED", "ARCHIVABLE"}
REGISTRY_SCHEMA_VERSIONS = {"1.0.0", "1.1.0", "1.3.0"}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def validate_receipt(receipt: dict[str, Any], index: int, failures: list[str]) -> None:
    prefix = f"sessions[{index}]"
    required = {
        "session_id",
        "repository",
        "task_id",
        "posture",
        "authority_checked",
        "active_task_ownership",
        "unique_unmerged_state",
        "safe_to_archive",
        "successor_execution_source",
        "reason",
    }
    missing = sorted(required - receipt.keys())
    if missing:
        fail(f"{prefix} missing required fields: {', '.join(missing)}", failures)
        return

    posture = receipt.get("posture")
    if posture not in POSTURES:
        fail(f"{prefix} invalid posture: {posture}", failures)

    authority = receipt.get("authority_checked")
    if not isinstance(authority, list) or not authority or not all(isinstance(x, str) and x for x in authority):
        fail(f"{prefix} authority_checked must be a non-empty string list", failures)

    if receipt.get("safe_to_archive"):
        if posture != "ARCHIVABLE":
            fail(f"{prefix} safe_to_archive requires ARCHIVABLE posture", failures)
        if receipt.get("active_task_ownership"):
            fail(f"{prefix} archivable session still owns active work", failures)
        if receipt.get("unique_unmerged_state"):
            fail(f"{prefix} archivable session contains unique unmerged state", failures)
        if receipt.get("conflicting_active_owner", False):
            fail(f"{prefix} archivable session has a conflicting active owner", failures)
        if receipt.get("required_before_archive", []):
            fail(f"{prefix} archivable session has unresolved required actions", failures)
        locations = receipt.get("material_state_locations")
        if not isinstance(locations, list) or not locations:
            fail(f"{prefix} archivable session lacks material_state_locations", failures)
        successor = receipt.get("successor_execution_source")
        if not isinstance(successor, str) or not successor:
            fail(f"{prefix} archivable session lacks successor execution source", failures)

    if posture == "MERGE_REQUIRED":
        if not receipt.get("unique_unmerged_state"):
            fail(f"{prefix} MERGE_REQUIRED must set unique_unmerged_state=true", failures)
        if receipt.get("safe_to_archive"):
            fail(f"{prefix} MERGE_REQUIRED cannot be safe to archive", failures)

    if posture == "CURRENT":
        if not receipt.get("active_task_ownership"):
            fail(f"{prefix} CURRENT must set active_task_ownership=true", failures)
        if receipt.get("safe_to_archive"):
            fail(f"{prefix} CURRENT cannot be safe to archive", failures)

    for path_value in receipt.get("material_state_locations", []):
        candidate = ROOT / path_value
        if not candidate.exists():
            fail(f"{prefix} material state location does not exist: {path_value}", failures)

    successor = receipt.get("successor_execution_source")
    if isinstance(successor, str) and successor and not (ROOT / successor).exists():
        fail(f"{prefix} successor execution source does not exist: {successor}", failures)


def duplicate_current_owner_failures(sessions: list[dict[str, Any]]) -> list[str]:
    current_owners: dict[tuple[str, str], list[str]] = {}
    for receipt in sessions:
        if receipt.get("posture") == "CURRENT" and receipt.get("active_task_ownership"):
            task_key = (str(receipt.get("repository")), str(receipt.get("task_id")))
            current_owners.setdefault(task_key, []).append(str(receipt.get("session_id")))

    failures: list[str] = []
    for task_key, owners in current_owners.items():
        if len(owners) > 1:
            failures.append(
                f"multiple CURRENT owners for {task_key[0]} {task_key[1]}: {', '.join(owners)}"
            )
    return failures


def main() -> int:
    failures: list[str] = []
    for path in (REGISTRY, HANDOFF, SCHEMA, PROMPT):
        if not path.exists():
            fail(f"missing required orchestration file: {path.relative_to(ROOT)}", failures)

    registry: dict[str, Any] = {}
    if REGISTRY.exists():
        try:
            registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"registry JSON invalid: {exc}", failures)

    if registry:
        if registry.get("schema_version") not in REGISTRY_SCHEMA_VERSIONS:
            fail(
                "registry schema_version must be one of: "
                + ", ".join(sorted(REGISTRY_SCHEMA_VERSIONS)),
                failures,
            )
        policy = registry.get("policy", {})
        required_policy = {
            "age_is_not_archive_authority": True,
            "compare_to_live_repository_state": True,
            "merge_unique_state_before_retirement": True,
            "one_active_owner_per_task": True,
            "archive_gate_fails_closed": True,
            "ui_archive_action_is_separate": True,
        }
        for key, expected in required_policy.items():
            if policy.get(key) is not expected:
                fail(f"registry policy {key} must be {expected}", failures)

        sessions = registry.get("sessions")
        if not isinstance(sessions, list) or not sessions:
            fail("registry sessions must be a non-empty list", failures)
            sessions = []

        seen_sessions: set[tuple[str, str]] = set()
        valid_sessions: list[dict[str, Any]] = []
        for index, receipt in enumerate(sessions):
            if not isinstance(receipt, dict):
                fail(f"sessions[{index}] must be an object", failures)
                continue
            validate_receipt(receipt, index, failures)
            valid_sessions.append(receipt)
            key = (str(receipt.get("session_id")), str(receipt.get("task_id")))
            if key in seen_sessions:
                fail(f"duplicate session/task receipt: {key[0]} / {key[1]}", failures)
            seen_sessions.add(key)

        failures.extend(duplicate_current_owner_failures(valid_sessions))

    report = {
        "schema_version": "1.0.0",
        "status_type": "session_retirement_validation_report",
        "status": "FAIL" if failures else "PASS",
        "registry": str(REGISTRY.relative_to(ROOT)),
        "session_count": len(registry.get("sessions", [])) if registry else 0,
        "failures": failures,
        "next_action": (
            "merge unique state, resolve ownership conflicts, and repair archive evidence"
            if failures
            else "use the registry disposition and archive only sessions marked ARCHIVABLE"
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"SESSION_RETIREMENT_{report['status']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
