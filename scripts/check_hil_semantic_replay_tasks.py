#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'data/hil-semantic-replay-task-state.json'


def main() -> int:
    state = json.loads(STATE.read_text(encoding='utf-8'))
    tasks = state['tasks']
    failures = []
    completed = []
    for task in tasks:
        if task.get('external') is not False:
            failures.append(f"{task['id']}: external tasks are prohibited")
        location = task.get('task_location')
        if not location:
            failures.append(f"{task['id']}: task_location missing")
        elif (ROOT / location).exists():
            completed.append(task['id'])
    remaining = [task['id'] for task in tasks if task['id'] not in completed]
    report = {
        'workstream': state.get('workstream','HIL_SEMANTIC_REPLAY'),
        'state': 'COMPLETE' if not remaining and not failures else 'RUNNING',
        'completed': completed,
        'remaining': remaining,
        'failures': failures,
        'halted': False,
        'next_task': None if not remaining else next(task for task in tasks if task['id'] == remaining[0])
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if failures:
        return 1
    if remaining:
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
