#!/usr/bin/env python3
"""Project deterministic successor packets and archive queue from governed session state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "session-orchestration-registry.json"
CROSS_REPO = ROOT / "data" / "session-orchestration-cross-repository.report.json"
SUCCESSORS = ROOT / "data" / "session-orchestration-successor-packets.json"
QUEUE = ROOT / "data" / "session-orchestration-archive-queue.json"

QUEUE_STATE = {
    "CURRENT": "CLAIMED",
    "SUPERSEDED": "SUPERSEDED",
    "MERGE_REQUIRED": "REVIEW_REQUIRED",
    "ARCHIVABLE": "COMPLETE",
}


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("sessions"), list):
        raise ValueError("registry must be an object with sessions[]")
    return value


def load_cross_repository(path: Path = CROSS_REPO) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("state_type") != "session_orchestration_cross_repository_report":
        raise ValueError("cross-repository report is missing or has the wrong state_type")
    return value


def resolve_local_source(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and (ROOT / value).exists()


def projection_failures(registry: dict[str, Any], cross_repository: dict[str, Any] | None = None) -> list[str]:
    failures: list[str] = []
    if cross_repository is not None:
        if cross_repository.get("status") != "PASS":
            failures.append("cross-repository authority comparison is not PASS")
        summary = cross_repository.get("summary", {})
        if not isinstance(summary, dict):
            failures.append("cross-repository comparison summary is malformed")
        else:
            if summary.get("owner_collision_count", 0) != 0:
                failures.append("cross-repository comparison reports owner collisions")
            if summary.get("stale_handoff_count", 0) != 0:
                failures.append("cross-repository comparison reports stale handoffs")
            if summary.get("unresolved_successor_count", 0) != 0:
                failures.append("cross-repository comparison reports unresolved successors")

    seen: set[tuple[str, str]] = set()
    current_owners: dict[tuple[str, str], list[str]] = {}
    for index, session in enumerate(registry.get("sessions", [])):
        if not isinstance(session, dict):
            failures.append(f"sessions[{index}] is not an object")
            continue
        session_id = session.get("session_id")
        task_id = session.get("task_id")
        repository = session.get("repository")
        posture = session.get("posture")
        key = (str(session_id), str(task_id))
        if key in seen:
            failures.append(f"duplicate session/task: {key[0]} / {key[1]}")
        seen.add(key)
        if posture not in QUEUE_STATE:
            failures.append(f"sessions[{index}] unsupported posture: {posture}")
        if not resolve_local_source(session.get("successor_execution_source")):
            failures.append(f"sessions[{index}] unresolved successor execution source")
        if posture == "ARCHIVABLE" and not session.get("safe_to_archive"):
            failures.append(f"sessions[{index}] ARCHIVABLE is not safe_to_archive=true")
        if session.get("safe_to_archive") and posture != "ARCHIVABLE":
            failures.append(f"sessions[{index}] safe_to_archive requires ARCHIVABLE posture")
        if posture == "CURRENT" and session.get("active_task_ownership"):
            task_key = (str(repository), str(task_id))
            current_owners.setdefault(task_key, []).append(str(session_id))
    for task_key, owners in current_owners.items():
        if len(owners) > 1:
            failures.append(
                f"multiple CURRENT owners for {task_key[0]} {task_key[1]}: {', '.join(owners)}"
            )
    return failures


def cross_repository_binding(cross_repository: dict[str, Any] | None) -> dict[str, Any]:
    if cross_repository is None:
        return {
            "status": "NOT_EVALUATED",
            "source": "data/session-orchestration-cross-repository.report.json",
            "summary": {},
            "delegated_dependencies": [],
        }
    return {
        "status": cross_repository.get("status"),
        "source": "data/session-orchestration-cross-repository.report.json",
        "summary": cross_repository.get("summary", {}),
        "delegated_dependencies": cross_repository.get("delegated_dependencies", []),
    }


def successor_packet(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": session.get("session_id"),
        "originating_goal": session.get("originating_goals", session.get("reason")),
        "repository": session.get("repository"),
        "branch": session.get("branch", "main"),
        "task_id": session.get("task_id"),
        "commit": session.get("current_commit"),
        "authority_source": session.get("authority_checked", []),
        "claimant": session.get("claimant", "repository registry"),
        "posture": session.get("posture"),
        "release_condition": session.get("claim_release_condition", session.get("required_before_archive", [])),
        "collision_boundaries": session.get("collision_boundaries", []),
        "expected_evidence": session.get("material_state_locations", []),
        "completion_conditions": session.get("required_before_archive", []),
        "successor_execution_source": session.get("successor_execution_source"),
        "nonclaims": [
            "packet does not grant execution authority",
            "packet does not perform ChatGPT UI archive or deletion",
            "missing evidence must not be converted to completion",
        ],
    }


def archive_row(session: dict[str, Any]) -> dict[str, Any]:
    posture = str(session.get("posture"))
    archive_candidate = posture == "ARCHIVABLE" and session.get("safe_to_archive") is True
    return {
        "session_id": session.get("session_id"),
        "task_id": session.get("task_id"),
        "repository": session.get("repository"),
        "posture": posture,
        "queue_state": QUEUE_STATE.get(posture, "FAILED"),
        "archive_candidate": archive_candidate,
        "ui_archive_action_performed": False,
        "active_task_ownership": session.get("active_task_ownership"),
        "unique_unmerged_state": session.get("unique_unmerged_state"),
        "conflicting_active_owner": session.get("conflicting_active_owner", False),
        "successor_execution_source": session.get("successor_execution_source"),
        "required_before_archive": session.get("required_before_archive", []),
        "evidence": session.get("material_state_locations", []),
        "reason": session.get("reason"),
    }


def build(
    registry: dict[str, Any],
    cross_repository: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    failures = projection_failures(registry, cross_repository)
    sessions = [row for row in registry.get("sessions", []) if isinstance(row, dict)]
    successor_rows = [successor_packet(row) for row in sessions if row.get("posture") != "ARCHIVABLE"]
    queue_rows = [archive_row(row) for row in sessions]
    next_executable = [
        row
        for row in successor_rows
        if row.get("posture") == "CURRENT" and row.get("successor_execution_source")
    ]
    cross_binding = cross_repository_binding(cross_repository)
    successors = {
        "schema_version": "1.1.0",
        "state_type": "session_orchestration_successor_packets",
        "status": "FAIL" if failures else "PASS",
        "repository": registry.get("repository"),
        "source_registry": "data/session-orchestration-registry.json",
        "cross_repository_authority": cross_binding,
        "packets": successor_rows,
        "next_executable": next_executable[0] if len(next_executable) == 1 else None,
        "frontier_state": (
            "READY" if len(next_executable) == 1 and not failures else
            "REVIEW_REQUIRED" if len(next_executable) > 1 or failures else
            "EMPTY"
        ),
        "frontier_reason": (
            "exactly one CURRENT session owner has a resolvable successor source and cross-repository authority comparison passes"
            if len(next_executable) == 1 and not failures else
            "cross-repository or ownership evidence requires review before continuation"
            if failures else
            "multiple CURRENT candidates require owner reconciliation"
            if len(next_executable) > 1 else
            "no CURRENT session candidate is executable from the registry"
        ),
        "failures": failures,
    }
    queue = {
        "schema_version": "1.1.0",
        "state_type": "session_orchestration_archive_queue",
        "status": "FAIL" if failures else "PASS",
        "repository": registry.get("repository"),
        "source_registry": "data/session-orchestration-registry.json",
        "cross_repository_authority": cross_binding,
        "ui_action_supported": False,
        "entries": queue_rows,
        "archive_candidate_count": sum(1 for row in queue_rows if row["archive_candidate"]),
        "failures": failures,
    }
    return successors, queue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail when generated files differ from committed projections")
    args = parser.parse_args()
    registry = load_registry()
    try:
        cross_repository = load_cross_repository()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        cross_repository = {
            "state_type": "session_orchestration_cross_repository_report",
            "status": "FAIL",
            "summary": {},
            "delegated_dependencies": [],
            "failures": [f"cross-repository report unavailable: {exc}"],
        }
    successors, queue = build(registry, cross_repository)
    rendered_successors = json.dumps(successors, indent=2) + "\n"
    rendered_queue = json.dumps(queue, indent=2) + "\n"
    if args.check:
        stale = []
        if not SUCCESSORS.exists() or SUCCESSORS.read_text(encoding="utf-8") != rendered_successors:
            stale.append(str(SUCCESSORS.relative_to(ROOT)))
        if not QUEUE.exists() or QUEUE.read_text(encoding="utf-8") != rendered_queue:
            stale.append(str(QUEUE.relative_to(ROOT)))
        if stale:
            print("SESSION_ORCHESTRATION_PROJECTION_STALE:" + ",".join(stale))
            return 1
    else:
        SUCCESSORS.write_text(rendered_successors, encoding="utf-8")
        QUEUE.write_text(rendered_queue, encoding="utf-8")
    status = successors["status"]
    print(f"SESSION_ORCHESTRATION_PROJECTION_{status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
