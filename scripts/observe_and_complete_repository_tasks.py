#!/usr/bin/env python3
"""Observe, reconcile, and complete repository-local tasks.

Every active task must resolve to a committed task object with exact implementation
locations, verification locations, and an executable acceptance command. Session
names and external-task placeholders are never treated as ownership or progress.

Repository-local tasks in READY_FOR_MACHINE_COMPLETION_CHECK are discovered
automatically. This prevents development from halting merely because a new task was
not copied into a central status array. The committed task object, its implementation
locations, and its executable acceptance command are the machine-owned work queue.

Task identity is carried by the committed object's ``task_id`` field. Historical task
files are not required to rename themselves to match that identifier; filename-only
lookup would make valid repository-owned work appear unaddressable. Duplicate objects
for one task_id remain fail-closed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "site-orchestration-state.json"
TASK_DIR = ROOT / "data" / "tasks"
REPORT_PATH = ROOT / "repository-task-observation.report.json"
DISCOVERABLE_STATES = {"READY_FOR_MACHINE_COMPLETION_CHECK", "RUNNING"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def run_validator(command: str) -> tuple[bool, str]:
    result = subprocess.run(
        command.split(), cwd=ROOT, text=True, capture_output=True, check=False
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def task_candidates(task_id: str) -> list[Path]:
    """Return committed task objects whose durable internal identity is task_id."""
    exact = TASK_DIR / f"{task_id}.json"
    matches: list[Path] = []
    if exact.is_file():
        try:
            if load(exact).get("task_id") == task_id:
                matches.append(exact)
        except (OSError, json.JSONDecodeError, AttributeError):
            pass

    if not TASK_DIR.is_dir():
        return matches
    for path in sorted(TASK_DIR.glob("*.json")):
        if path == exact:
            continue
        try:
            task = load(path)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(task, dict) and task.get("task_id") == task_id:
            matches.append(path)
    return matches


def resolve_task_path(task_id: str) -> tuple[Path | None, list[Path]]:
    matches = task_candidates(task_id)
    return (matches[0] if len(matches) == 1 else None), matches


def discover_repository_tasks() -> list[str]:
    discovered: list[str] = []
    if not TASK_DIR.is_dir():
        return discovered
    for path in sorted(TASK_DIR.glob("*.json")):
        try:
            task = load(path)
        except (OSError, json.JSONDecodeError):
            continue
        task_id = task.get("task_id") if isinstance(task, dict) else None
        if (
            isinstance(task_id, str)
            and task.get("repository") == "StegVerse-Labs/Site"
            and task.get("state") in DISCOVERABLE_STATES
        ):
            discovered.append(task_id)
    return list(dict.fromkeys(discovered))


def observe_task(task_id: str) -> dict[str, Any]:
    path, candidates = resolve_task_path(task_id)
    if not candidates:
        expected = TASK_DIR / f"{task_id}.json"
        return {
            "task_id": task_id,
            "state": "BLOCKED_UNADDRESSABLE_TASK",
            "task_location": str(expected.relative_to(ROOT)),
            "reason": "active task has no committed repository-local task object",
        }
    if path is None:
        return {
            "task_id": task_id,
            "state": "BLOCKED_DUPLICATE_TASK_OBJECTS",
            "task_locations": [str(item.relative_to(ROOT)) for item in candidates],
            "reason": "multiple committed task objects declare the same task_id",
        }

    relative = str(path.relative_to(ROOT))
    task = load(path)
    external = task.get("external_dependencies", [])
    implementation = task.get("implementation_locations", [])
    verification = task.get("verification_locations", [])
    missing = [p for p in implementation + verification if not (ROOT / p).is_file()]
    command = task.get("acceptance", {}).get("validator_command")
    marker = task.get("acceptance", {}).get("success_marker", "")

    if task.get("repository") != "StegVerse-Labs/Site":
        return {
            "task_id": task_id,
            "state": "BLOCKED_REPOSITORY_MISMATCH",
            "task_location": relative,
        }
    if external:
        return {
            "task_id": task_id,
            "state": "BLOCKED_EXTERNAL_DEPENDENCY_PROHIBITED",
            "task_location": relative,
            "external_dependencies": external,
        }
    if not implementation:
        return {
            "task_id": task_id,
            "state": "BLOCKED_NO_IMPLEMENTATION_LOCATIONS",
            "task_location": relative,
        }
    if not verification:
        return {
            "task_id": task_id,
            "state": "BLOCKED_NO_VERIFICATION_LOCATIONS",
            "task_location": relative,
        }
    if missing:
        return {
            "task_id": task_id,
            "state": "INCOMPLETE",
            "task_location": relative,
            "missing_locations": sorted(set(missing)),
        }
    if not command:
        return {
            "task_id": task_id,
            "state": "BLOCKED_NO_EXECUTABLE_ACCEPTANCE",
            "task_location": relative,
        }

    passed, output = run_validator(command)
    marker_seen = marker in output if marker else passed
    return {
        "task_id": task_id,
        "state": "COMPLETE" if passed and marker_seen else "VALIDATION_FAILED",
        "task_location": relative,
        "validator_command": command,
        "success_marker": marker,
        "success_marker_seen": marker_seen,
        "output": output,
    }


def reconcile_ownership(state: dict[str, Any], active: list[str]) -> list[dict[str, str]]:
    """Replace session-shaped ownership with committed task-object pointers."""
    ownership = state.setdefault("ownership", {})
    changes: list[dict[str, str]] = []
    mappings = {
        "SITE-0001-UPLOAD": "hil_upload_surface",
        "SITE-0001-COHERENT-TRANSITION-THRESHOLD": "coherent_transition_threshold",
    }
    for task_id in active:
        key = mappings.get(task_id)
        path, candidates = resolve_task_path(task_id)
        if not key or path is None or len(candidates) != 1:
            continue
        expected = str(path.relative_to(ROOT))
        actual = ownership.get(key)
        if actual != expected:
            ownership[key] = expected
            changes.append({"task_id": task_id, "from": str(actual), "to": expected})
    return changes


def mark_task_complete(task_id: str, observation: dict[str, Any]) -> None:
    location = observation.get("task_location")
    if not isinstance(location, str):
        raise ValueError(f"completed task {task_id} has no unique task_location")
    path = ROOT / location
    task = load(path)
    if task.get("task_id") != task_id:
        raise ValueError(f"task identity mismatch at {location}")
    task["state"] = "COMPLETE"
    task["completion_observation"] = {
        "controller": "scripts/observe_and_complete_repository_tasks.py",
        "validator_command": observation.get("validator_command"),
        "success_marker": observation.get("success_marker"),
        "success_marker_seen": observation.get("success_marker_seen", False),
        "external_dependencies": [],
    }
    write(path, task)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Return non-zero after writing the durable report.",
    )
    args = parser.parse_args()

    state = load(STATE_PATH)
    active_sequence = state["active_sequence"]
    declared_active = list(active_sequence.get("parallel_safe_tasks", []))
    discovered = discover_repository_tasks()
    active = list(dict.fromkeys(declared_active + discovered))
    ownership_changes = reconcile_ownership(state, active)
    observations = [observe_task(task_id) for task_id in active]
    completed = [o["task_id"] for o in observations if o["state"] == "COMPLETE"]
    blockers = [o for o in observations if o["state"] != "COMPLETE"]

    state_updated = bool(ownership_changes)
    if args.apply and completed:
        active_sequence["parallel_safe_tasks"] = [
            task_id for task_id in declared_active if task_id not in completed
        ]
        completed_list = active_sequence.setdefault("completed_parallel_safe_tasks", [])
        for observation in observations:
            completed_id = observation["task_id"]
            if completed_id not in completed:
                continue
            if completed_id not in completed_list:
                completed_list.append(completed_id)
            mark_task_complete(completed_id, observation)
        state_updated = True

    remaining = [task_id for task_id in active if task_id not in completed]
    active_sequence["machine_observation"] = {
        "controller": "scripts/observe_and_complete_repository_tasks.py",
        "task_directory": "data/tasks",
        "active_task_count": len(remaining),
        "blocker_count": len(blockers),
        "auto_discovery_enabled": True,
        "discoverable_task_states": sorted(DISCOVERABLE_STATES),
        "external_session_ownership_allowed": False,
    }
    if not remaining:
        active_sequence["state"] = "IDLE"
        active_sequence["terminal_statement"] = active_sequence.get(
            "idle_terminal_statement", "end of current work task sequence, no tasks running"
        )
    elif blockers:
        active_sequence["state"] = "OBSERVED_BLOCKED"
    else:
        active_sequence["state"] = "RUNNING"
    state_updated = True

    report = {
        "schema_version": "2.2.0",
        "repository": "StegVerse-Labs/Site",
        "controller": "scripts/observe_and_complete_repository_tasks.py",
        "declared_active_tasks": declared_active,
        "auto_discovered_tasks": discovered,
        "active_tasks_observed": active,
        "ownership_reconciliations": ownership_changes,
        "observations": observations,
        "completed_tasks": completed,
        "remaining_tasks": remaining,
        "blockers": blockers,
        "state_updated": state_updated,
        "policy": {
            "external_session_ownership_allowed": False,
            "external_tasks_allowed": False,
            "unaddressable_task_allowed": False,
            "implementation_locations_required": True,
            "verification_locations_required": True,
            "validator_required_for_completion": True,
            "observation_must_be_durable": True,
            "repository_task_auto_discovery": True,
            "central_status_registration_required": False,
            "task_identity_source": "task_id_field",
            "duplicate_task_ids_fail_closed": True,
        },
    }

    if args.apply:
        write(STATE_PATH, state)
    write(REPORT_PATH, report)
    print(json.dumps(report, indent=2))

    if blockers and args.fail_on_blockers:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
