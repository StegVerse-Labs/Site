#!/usr/bin/env python3
"""Reconcile TIDC source-expansion task state from committed evidence records.

Normal reconciliation derives progress and materializes exactly one repository-owned
successor task for the first missing source record. ``--check EVENT_ID`` is read-only
acceptance for that task. Neither mode invents source evidence or silently recodes the
seed ledger.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/tidc/source-expansion/seed-source-expansion-plan.json"
QUEUE = ROOT / "data/tidc/work-queue.json"
LEDGER = ROOT / "data/tidc/pilot-events-v0.1.json"
TASK_DIR = ROOT / "data/tasks"
RECEIPT = ROOT / "brain_reports/tidc_source_expansion_reconciliation.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def valid_record(path: Path, event_id: str) -> tuple[bool, list[str]]:
    problems: list[str] = []
    if not path.is_file():
        return False, ["record_missing"]
    try:
        record = load(path)
    except Exception as exc:
        return False, [f"invalid_json:{exc}"]
    if record.get("event_id") != event_id:
        problems.append("event_id_mismatch")
    if not record.get("sources"):
        problems.append("sources_missing")
    if "field_evidence" not in record:
        problems.append("field_evidence_missing")
    if record.get("seed_ledger_changed") is not False:
        problems.append("seed_ledger_boundary_missing")
    if record.get("authority_effect") != "NONE":
        problems.append("authority_boundary_invalid")
    return not problems, problems


def task_id(event_id: str) -> str:
    return f"TIDC-SRC-{event_id}"


def task_path(event_id: str) -> Path:
    return TASK_DIR / f"tidc-source-expansion-{event_id.lower()}.json"


def materialize_next_task(event_id: str, location: str) -> Path:
    path = task_path(event_id)
    task = {
        "schema_version": "1.1.0",
        "task_id": task_id(event_id),
        "repository": "StegVerse-Labs/Site",
        "workstream": "TIDC",
        "task": f"Reconstruct primary-source evidence for {event_id} without silently recoding the seed ledger.",
        "task_location": location,
        "implementation_locations": [location],
        "verification_locations": [
            "scripts/reconcile_tidc_source_expansion.py",
            "data/tidc/source-expansion/seed-source-expansion-plan.json",
            "data/tidc/pilot-events-v0.1.json",
        ],
        "acceptance": {
            "required_files_exist": True,
            "validator_command": f"python scripts/reconcile_tidc_source_expansion.py --check {event_id}",
            "success_marker": f"TIDC_SOURCE_RECORD_VALID={event_id}",
        },
        "auto_admit": True,
        "external_dependencies": [],
        "state": "READY_FOR_MACHINE_COMPLETION_CHECK",
        "completion_boundary": "A valid record must contain source evidence and field evidence, preserve seed_ledger_changed=false, and retain authority_effect=NONE. Missing evidence remains incomplete; do not synthesize it for task completion.",
        "authority_effect": "NONE",
    }
    if path.is_file():
        existing = load(path)
        if existing.get("task_id") != task["task_id"]:
            raise SystemExit(f"TIDC_SOURCE_TASK_ID_COLLISION:{path.relative_to(ROOT)}")
        if existing.get("state") == "COMPLETE":
            return path
    write(path, task)
    return path


def check_event(event_id: str) -> int:
    plan = load(PLAN)
    by_id = {item.get("event_id"): item for item in plan.get("items", [])}
    item = by_id.get(event_id)
    if not item:
        print("TIDC_SOURCE_RECORD_INVALID")
        print(f"event_id={event_id}")
        print("- event_not_in_source_expansion_plan")
        return 2

    path = ROOT / item["task_location"]
    valid, problems = valid_record(path, event_id)
    if not valid:
        print("TIDC_SOURCE_RECORD_INVALID")
        print(f"event_id={event_id}")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"TIDC_SOURCE_RECORD_VALID={event_id}")
    print(f"record={item['task_location']}")
    print("seed_ledger_changed=false")
    print("authority_effect=NONE")
    return 0


def reconcile() -> None:
    plan = load(PLAN)
    statuses: list[dict[str, Any]] = []
    completed = 0
    next_ready: str | None = None
    next_location: str | None = None

    for item in plan.get("items", []):
        event_id = item["event_id"]
        record_path = ROOT / item["task_location"]
        valid, problems = valid_record(record_path, event_id)
        if valid:
            item["status"] = "PRIMARY_SOURCE_RECORD_PRESENT_PENDING_REVIEW"
            completed += 1
        else:
            item["status"] = "READY_FOR_PRIMARY_SOURCE_RECONSTRUCTION"
            if next_ready is None:
                next_ready = event_id
                next_location = item["task_location"]
        statuses.append({
            "event_id": event_id,
            "location": item["task_location"],
            "valid_record_present": valid,
            "problems": problems,
        })

    plan["completed_record_count"] = completed
    plan["remaining_record_count"] = len(statuses) - completed
    plan["next_repository_owned_task"] = None if next_ready is None else {
        "task_id": task_id(next_ready),
        "event_id": next_ready,
        "location": next_location,
        "task_object": task_path(next_ready).relative_to(ROOT).as_posix(),
    }
    plan["development_halted"] = False
    write(PLAN, plan)

    queue = load(QUEUE)
    for task in queue.get("tasks", []):
        if task.get("id") == "TIDC-IW-001":
            task["status"] = "COMPLETE" if completed == len(statuses) else "ACTIVE"
            task["completed_units"] = completed
            task["total_units"] = len(statuses)
            task["next_location"] = next_location
            task["next_task_id"] = None if next_ready is None else task_id(next_ready)
    queue["development_halted"] = False
    write(QUEUE, queue)

    next_task_object: str | None = None
    if next_ready is not None and next_location is not None:
        next_task_object = materialize_next_task(next_ready, next_location).relative_to(ROOT).as_posix()

    receipt = {
        "schema": "stegverse.site.tidc.source_expansion_reconciliation.v0.2",
        "plan": PLAN.relative_to(ROOT).as_posix(),
        "completed_record_count": completed,
        "remaining_record_count": len(statuses) - completed,
        "next_repository_owned_task": plan["next_repository_owned_task"],
        "next_task_object": next_task_object,
        "records": statuses,
        "development_halted": False,
        "authority_effect": "NONE",
    }
    write(RECEIPT, receipt)
    print(f"TIDC_SOURCE_EXPANSION_RECONCILED completed={completed} remaining={len(statuses)-completed}")
    print(f"next={next_ready}")
    print(f"next_task_object={next_task_object}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", metavar="EVENT_ID")
    args = parser.parse_args()
    if args.check:
        raise SystemExit(check_event(args.check))
    reconcile()


if __name__ == "__main__":
    main()
