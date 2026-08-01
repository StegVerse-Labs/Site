#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data/site-orchestration-state.json"
TASK_DIR = ROOT / "data/tasks"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    state = load(STATE_PATH)
    sequence = state["active_sequence"]
    active = list(sequence.get("parallel_safe_tasks", []))
    completed = set(sequence.get("completed_parallel_safe_tasks", []))
    admitted: list[str] = []

    for path in sorted(TASK_DIR.glob("*.json")):
        task = load(path)
        task_id = task.get("task_id")
        if not task_id or task.get("auto_admit") is not True:
            continue
        if task.get("repository") != "StegVerse-Labs/Site":
            continue
        if task.get("external_dependencies"):
            continue
        if task_id in completed or task_id in active:
            continue
        if task.get("state") != "READY_FOR_MACHINE_COMPLETION_CHECK":
            continue
        active.append(task_id)
        admitted.append(task_id)

    sequence["parallel_safe_tasks"] = active
    if active:
        sequence["state"] = "RUNNING"
    sequence["machine_admission"] = {
        "controller": "scripts/admit_repository_tasks.py",
        "task_directory": "data/tasks",
        "admitted_tasks": admitted,
        "external_tasks_allowed": False,
        "external_session_ownership_allowed": False
    }
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(sequence["machine_admission"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
