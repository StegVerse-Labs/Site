#!/usr/bin/env python3
"""Reconcile TIDC source-expansion task state from committed evidence records."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/tidc/source-expansion/seed-source-expansion-plan.json"
QUEUE = ROOT / "data/tidc/work-queue.json"
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


def main() -> None:
    plan = load(PLAN)
    statuses: list[dict[str, Any]] = []
    completed = 0
    next_ready: str | None = None

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
        statuses.append({
            "event_id": event_id,
            "location": item["task_location"],
            "valid_record_present": valid,
            "problems": problems,
        })

    plan["completed_record_count"] = completed
    plan["remaining_record_count"] = len(statuses) - completed
    plan["next_repository_owned_task"] = None if next_ready is None else {
        "event_id": next_ready,
        "location": f"data/tidc/source-expansion/{next_ready}.json",
    }
    plan["development_halted"] = False
    write(PLAN, plan)

    queue = load(QUEUE)
    for task in queue.get("tasks", []):
        if task.get("id") == "TIDC-IW-001":
            task["status"] = "COMPLETE" if completed == len(statuses) else "ACTIVE"
            task["completed_units"] = completed
            task["total_units"] = len(statuses)
            task["next_location"] = None if next_ready is None else f"data/tidc/source-expansion/{next_ready}.json"
    queue["development_halted"] = False
    write(QUEUE, queue)

    receipt = {
        "schema": "stegverse.site.tidc.source_expansion_reconciliation.v0.1",
        "plan": PLAN.relative_to(ROOT).as_posix(),
        "completed_record_count": completed,
        "remaining_record_count": len(statuses) - completed,
        "next_repository_owned_task": plan["next_repository_owned_task"],
        "records": statuses,
        "development_halted": False,
        "authority_effect": "NONE",
    }
    write(RECEIPT, receipt)
    print(f"TIDC_SOURCE_EXPANSION_RECONCILED completed={completed} remaining={len(statuses)-completed}")
    print(f"next={next_ready}")


if __name__ == "__main__":
    main()
