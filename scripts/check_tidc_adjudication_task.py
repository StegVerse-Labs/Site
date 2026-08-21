#!/usr/bin/env python3
"""Validate completed TIDC adjudication task outputs without rewriting research history."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "data" / "tasks"

SUPPORTED = {
    "TIDC-ADJ-COMP-002-PUBLICATION-DATE": {
        "task_file": "data/tasks/tidc-adjudicate-comp-002-publication-date.json",
        "outputs": ["data/tidc/adjudication/COMP-002-publication-date.json"],
        "expected": {
            "data/tidc/adjudication/COMP-002-publication-date.json": {
                "event_id": "COMP-002",
                "field": "publication_date",
                "seed_value": "1991-04",
                "source_supported_value": "1989-12-01",
                "disposition": "SUPERSEDE_IN_FUTURE_VERSION_PRESERVE_SEED_HISTORY",
            }
        },
    },
    "TIDC-ADJ-NET-001-DATES": {
        "task_file": "data/tasks/tidc-adjudicate-net-001-dates.json",
        "outputs": [
            "data/tidc/adjudication/NET-001-candidate-generation-date.json",
            "data/tidc/adjudication/NET-001-verification-date.json",
        ],
        "expected": {
            "data/tidc/adjudication/NET-001-candidate-generation-date.json": {
                "event_id": "NET-001",
                "field": "candidate_generation_date",
                "seed_value": "2010-02-18",
                "source_supported_value": "2009-02-01",
                "disposition": "SUPERSEDE_IN_FUTURE_VERSION",
            },
            "data/tidc/adjudication/NET-001-verification-date.json": {
                "event_id": "NET-001",
                "field": "verification_date",
                "seed_value": "2011-07-02",
                "source_supported_value": None,
                "disposition": "SET_NULL_IN_FUTURE_VERSION_PENDING_DISTINCT_EVIDENCE",
            },
        },
    },
}


def load_object(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} must contain an object")
    return value


def fail(task_id: str, reasons: list[str]) -> int:
    print(f"TIDC_ADJUDICATION_TASK_ACCEPTANCE=FAIL task_id={task_id}")
    for reason in reasons:
        print(f"- {reason}")
    return 1


def validate(task_id: str) -> int:
    spec = SUPPORTED.get(task_id)
    if spec is None:
        return fail(task_id, ["unsupported adjudication task id"])

    reasons: list[str] = []
    try:
        task = load_object(spec["task_file"])
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(task_id, [f"task object unreadable: {exc}"])

    if task.get("task_id") != task_id:
        reasons.append("task_id does not match canonical task object")
    if task.get("repository") != "StegVerse-Labs/Site":
        reasons.append("repository binding is not StegVerse-Labs/Site")
    if task.get("external_dependencies") != []:
        reasons.append("external_dependencies must remain empty")
    if task.get("authority_effect") != "NONE":
        reasons.append("task authority_effect must remain NONE")

    for relative in spec["outputs"]:
        path = ROOT / relative
        if not path.is_file():
            reasons.append(f"required output missing: {relative}")
            continue
        try:
            record = load_object(relative)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            reasons.append(f"invalid output {relative}: {exc}")
            continue
        for key, expected in spec["expected"][relative].items():
            if record.get(key) != expected:
                reasons.append(
                    f"{relative} {key} mismatch: {record.get(key)!r} != {expected!r}"
                )
        if record.get("seed_ledger_changed") is not False:
            reasons.append(f"{relative} must preserve seed_ledger_changed=false")
        if record.get("authority_effect") != "NONE":
            reasons.append(f"{relative} authority_effect must remain NONE")

    if reasons:
        return fail(task_id, reasons)

    print(f"TIDC_ADJUDICATION_TASK_ACCEPTANCE=PASS task_id={task_id}")
    print("seed_history_preserved=true")
    print("external_dependencies=0")
    print("authority_effect=NONE")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_tidc_adjudication_task.py <task-id>", file=sys.stderr)
        return 2
    return validate(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
