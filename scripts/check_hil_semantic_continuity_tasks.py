#!/usr/bin/env python3
"""Observe HIL semantic-continuity tasks and select the next repository-owned action."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data/hil-semantic-continuity-task-state.json"


def main() -> int:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    tasks = state["tasks"]
    by_id = {task["id"]: task for task in tasks}
    failures: list[str] = []

    for task in tasks:
        if task.get("external") is not False:
            failures.append(f"{task['id']}: external tasks are prohibited")
        location = task.get("task_location")
        if not location:
            failures.append(f"{task['id']}: missing task_location")
        for dependency in task.get("dependencies", []):
            if dependency not in by_id:
                failures.append(f"{task['id']}: unknown dependency {dependency}")

    completed = {
        task["id"]
        for task in tasks
        if task.get("task_location") and (ROOT / task["task_location"]).exists()
    }

    ready = []
    for task in tasks:
        if task["id"] in completed:
            continue
        if all(dependency in completed for dependency in task.get("dependencies", [])):
            ready.append(task)

    ready.sort(key=lambda task: (task.get("priority", 9999), task["id"]))
    report = {
        "workstream": state["workstream"],
        "state": "COMPLETE" if len(completed) == len(tasks) else "RUNNING",
        "completed": sorted(completed),
        "remaining": [task["id"] for task in tasks if task["id"] not in completed],
        "next_task": ready[0] if ready else None,
        "failures": failures,
        "halted": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    if failures:
        return 1
    if report["state"] != "COMPLETE" and report["next_task"] is None:
        print("No executable repository-owned task remains; dependency graph is blocked.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
