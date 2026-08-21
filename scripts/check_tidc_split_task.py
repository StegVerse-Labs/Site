#!/usr/bin/env python3
"""Validate repository-owned TIDC aggregate split task outputs.

This checker validates only durable task/output structure. It does not create source
claims, infer missing chronology, adjudicate scientific reliability, or grant any
authority. Missing research outputs remain incomplete work owned by the TIDC lane.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "data" / "tasks"
SUPPORTED_TASKS = {"TIDC-SPLIT-NET-002", "TIDC-SPLIT-AI-001"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_task(task_id: str) -> tuple[Path, dict[str, Any]]:
    matches: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(TASK_DIR.glob("*.json")):
        try:
            value = load(path)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and value.get("task_id") == task_id:
            matches.append((path, value))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one task object for {task_id}; found {len(matches)}")
    return matches[0]


def contains_forbidden_seed_mutation(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("seed_ledger_changed") is True:
            return True
        return any(contains_forbidden_seed_mutation(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_forbidden_seed_mutation(item) for item in value)
    return False


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in SUPPORTED_TASKS:
        print("TIDC_SPLIT_TASK=FAIL")
        print("reason=usage: check_tidc_split_task.py <supported-task-id>")
        return 2

    task_id = sys.argv[1]
    failures: list[str] = []

    try:
        task_path, task = find_task(task_id)
    except ValueError as exc:
        print("TIDC_SPLIT_TASK=FAIL")
        print(f"reason={exc}")
        return 1

    if task.get("repository") != "StegVerse-Labs/Site":
        failures.append("repository mismatch")
    if task.get("external_dependencies") != []:
        failures.append("external_dependencies must be empty")
    if task.get("authority_effect") != "NONE":
        failures.append("task authority_effect must be NONE")

    outputs = task.get("required_outputs")
    if not isinstance(outputs, list) or len(outputs) != 4 or not all(isinstance(p, str) for p in outputs):
        failures.append("required_outputs must contain exactly four repository paths")
        outputs = []

    for relative in outputs:
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing output: {relative}")
            continue
        try:
            value = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid JSON output {relative}: {exc}")
            continue
        if contains_forbidden_seed_mutation(value):
            failures.append(f"seed ledger mutation claimed by {relative}")
        if isinstance(value, dict) and value.get("authority_effect") not in (None, "NONE", False):
            failures.append(f"authority escalation claimed by {relative}")

    if failures:
        print(f"TIDC_SPLIT_TASK=FAIL:{task_id}")
        print(f"task_location={task_path.relative_to(ROOT)}")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"TIDC_SPLIT_TASK=PASS:{task_id}")
    print(f"task_location={task_path.relative_to(ROOT)}")
    print("seed_ledger_changed=false")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
