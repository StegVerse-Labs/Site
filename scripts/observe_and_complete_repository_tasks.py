#!/usr/bin/env python3
"""Observe repository-local tasks and fail closed on unaddressable ownership.

The controller does not invent external sessions. Every active task must point to a
committed task object containing exact implementation and verification locations.
With --apply it advances tasks whose validators pass and updates orchestration state.
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


def observe_task(task_id: str) -> dict[str, Any]:
    task_path = TASK_DIR / f"{task_id}.json"
    if not task_path.is_file():
        return {
            "task_id": task_id,
            "state": "BLOCKED_UNADDRESSABLE_TASK",
            "task_location": str(task_path.relative_to(ROOT)),
            "reason": "active task has no committed repository-local task object",
        }

    task = load(task_path)
    external = task.get("external_dependencies", [])
    missing = [p for p in task.get("implementation_locations", []) if not (ROOT / p).is_file()]
    missing += [p for p in task.get("verification_locations", []) if not (ROOT / p).is_file()]
    command = task.get("acceptance", {}).get("validator_command")
    marker = task.get("acceptance", {}).get("success_marker", "")

    if external:
        return {
            "task_id": task_id,
            "state": "BLOCKED_EXTERNAL_DEPENDENCY_PROHIBITED",
            "task_location": str(task_path.relative_to(ROOT)),
            "external_dependencies": external,
        }
    if missing:
        return {
            "task_id": task_id,
            "state": "INCOMPLETE",
            "task_location": str(task_path.relative_to(ROOT)),
            "missing_locations": sorted(set(missing)),
        }
    if not command:
        return {
            "task_id": task_id,
            "state": "BLOCKED_NO_EXECUTABLE_ACCEPTANCE",
            "task_location": str(task_path.relative_to(ROOT)),
        }

    passed, output = run_validator(command)
    marker_seen = marker in output if marker else passed
    return {
        "task_id": task_id,
        "state": "COMPLETE" if passed and marker_seen else "VALIDATION_FAILED",
        "task_location": str(task_path.relative_to(ROOT)),
        "validator_command": command,
        "success_marker": marker,
        "success_marker_seen": marker_seen,
        "output": output,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    state = load(STATE_PATH)
    active = list(state["active_sequence"].get("parallel_safe_tasks", []))
    observations = [observe_task(task_id) for task_id in active]

    completed = [o["task_id"] for o in observations if o["state"] == "COMPLETE"]
    blockers = [o for o in observations if o["state"] != "COMPLETE"]

    changed = False
    if args.apply and completed:
        remaining = [task_id for task_id in active if task_id not in completed]
        completed_list = state["active_sequence"].setdefault("completed_parallel_safe_tasks", [])
        for task_id in completed:
            if task_id not in completed_list:
                completed_list.append(task_id)
        state["active_sequence"]["parallel_safe_tasks"] = remaining
        ownership = state.setdefault("ownership", {})
        for task_id in completed:
            if task_id == "SITE-0001-UPLOAD":
                ownership["hil_upload_surface"] = "data/tasks/SITE-0001-UPLOAD.json"
        write(STATE_PATH, state)
        changed = True

    report = {
        "schema_version": "1.0.0",
        "repository": "StegVerse-Labs/Site",
        "controller": "scripts/observe_and_complete_repository_tasks.py",
        "active_tasks_observed": active,
        "observations": observations,
        "completed_tasks": completed,
        "blockers": blockers,
        "state_updated": changed,
        "policy": {
            "external_session_ownership_allowed": False,
            "unaddressable_task_allowed": False,
            "validator_required_for_completion": True,
        },
    }
    write(REPORT_PATH, report)

    print(json.dumps(report, indent=2))
    if blockers:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
