#!/usr/bin/env python3
"""Advance repository-owned TIDC work without erasing observed task state.

This executor refreshes planning surfaces from the committed pilot ledger while
preserving or deriving evidence-backed completion state. It must never regress a
completed source record or aggregate split to READY merely because the planning
worker ran after a reconciler/observer.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/tidc/pilot-events-v0.1.json"
QUEUE = ROOT / "data/tidc/work-queue.json"
SOURCE_PLAN = ROOT / "data/tidc/source-expansion/seed-source-expansion-plan.json"
NEGATIVE_PLAN = ROOT / "data/tidc/negative-controls/negative-control-design-v0.1.json"
SPLIT_PLAN = ROOT / "data/tidc/tranche-02/aggregate-event-split-plan.json"
RECEIPT = ROOT / "brain_reports/tidc_internal_advancement_receipt.json"


def load(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(value: Any) -> str:
    material = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(material).hexdigest()


def source_record_valid(path: Path, event_id: str) -> bool:
    record = load(path)
    if not isinstance(record, dict):
        return False
    return (
        record.get("event_id") == event_id
        and bool(record.get("sources"))
        and "field_evidence" in record
        and record.get("seed_ledger_changed") is False
        and record.get("authority_effect") == "NONE"
    )


def merge_item(seed: dict[str, Any], existing: dict[str, Any] | None) -> dict[str, Any]:
    """Keep durable fields written by downstream reconcilers, then refresh seed fields."""
    merged = dict(existing or {})
    merged.update(seed)
    return merged


def split_task_state(event_id: str) -> str | None:
    path = ROOT / "data/tasks" / f"tidc-split-{event_id.lower()}.json"
    task = load(path)
    if isinstance(task, dict):
        return task.get("state")
    return None


def negative_control_candidate_valid(path: Path, class_id: str) -> bool:
    row = load(path)
    return (
        isinstance(row, dict)
        and row.get("schema") == "stegverse.site.tidc.negative_control_candidate.v0.1"
        and row.get("control_class_id") == class_id
        and row.get("seed_ledger_changed") is False
        and row.get("discovery_event_added") is False
        and row.get("authority_effect") == "NONE"
        and bool(row.get("control_statement"))
        and bool(row.get("falsification_use"))
    )


def negative_control_completion() -> tuple[bool, int]:
    task = load(ROOT / "data/tasks/tidc-negative-controls-001.json")
    if not isinstance(task, dict) or task.get("state") != "COMPLETE":
        return False, 0
    expected = {
        "NC-CLASS-001": ROOT / "data/tidc/negative-controls/technology-present-no-output/QAI-2025-JP-OSAKA.json",
        "NC-CLASS-002": ROOT / "data/tidc/negative-controls/pre-access-placebos/QNT-001-vs-QAI-2025-JP-OSAKA.json",
        "NC-CLASS-003": ROOT / "data/tidc/negative-controls/supportive-not-necessary/AI-002-LLVM-integration.json",
    }
    completed = sum(1 for class_id, path in expected.items() if negative_control_candidate_valid(path, class_id))
    return completed == len(expected), completed


def main() -> None:
    ledger = load(LEDGER)
    events = ledger.get("events", [])
    if len(events) != 10:
        raise SystemExit("TIDC_INTERNAL_ADVANCEMENT_INVALID: expected 10 pilot events")

    old_source = load(SOURCE_PLAN, {}) or {}
    old_source_by_id = {item.get("event_id"): item for item in old_source.get("items", [])}

    source_items: list[dict[str, Any]] = []
    source_completed = 0
    first_missing: dict[str, str] | None = None
    for event in events:
        event_id = event["event_id"]
        location = f"data/tidc/source-expansion/{event_id}.json"
        valid = source_record_valid(ROOT / location, event_id)
        if valid:
            source_completed += 1
        elif first_missing is None:
            first_missing = {
                "task_id": f"TIDC-SRC-{event_id}",
                "event_id": event_id,
                "location": location,
                "task_object": f"data/tasks/tidc-source-expansion-{event_id.lower()}.json",
            }
        seed = {
            "event_id": event_id,
            "event_name": event["event_name"],
            "source_id": event["source_id"],
            "open_questions": event.get("open_questions", []),
            "task_location": location,
            "status": "PRIMARY_SOURCE_RECORD_PRESENT_PENDING_REVIEW" if valid else "READY_FOR_PRIMARY_SOURCE_RECONSTRUCTION",
            "completion_rule": "Preserve exact source metadata, retrieval date, immutable URL or archive reference, and field-level evidence without silently recoding the seed ledger.",
        }
        source_items.append(merge_item(seed, old_source_by_id.get(event_id)))

    source_plan = {
        **{k: v for k, v in old_source.items() if k not in {"items", "completed_record_count", "remaining_record_count", "next_repository_owned_task", "development_halted"}},
        "schema": "stegverse.site.tidc.source_expansion_plan.v0.1",
        "posture": "RESEARCH_NOTE_NOT_CONFIRMATORY",
        "source_ledger": LEDGER.relative_to(ROOT).as_posix(),
        "items": source_items,
        "authority_effect": "NONE",
        "completed_record_count": source_completed,
        "remaining_record_count": len(events) - source_completed,
        "next_repository_owned_task": first_missing,
        "development_halted": False,
    }

    old_negative = load(NEGATIVE_PLAN, {}) or {}
    old_negative_by_id = {item.get("id"): item for item in old_negative.get("control_classes", [])}
    negative_seed = [
        {
            "id": "NC-CLASS-001",
            "class": "technology-present-without-discovery-output",
            "location": "data/tidc/negative-controls/technology-present-no-output/",
            "purpose": "Test whether mere technology availability is incorrectly treated as a discovery event.",
        },
        {
            "id": "NC-CLASS-002",
            "class": "publication-before-effective-access-placebo",
            "location": "data/tidc/negative-controls/pre-access-placebos/",
            "purpose": "Detect timelines that appear to peak before effective access or exposure.",
        },
        {
            "id": "NC-CLASS-003",
            "class": "supportive-technology-misattributed-as-necessary",
            "location": "data/tidc/negative-controls/supportive-not-necessary/",
            "purpose": "Test dependency-class inflation.",
        },
    ]
    negative_complete, negative_completed = negative_control_completion()
    negative_classes = []
    for seed in negative_seed:
        existing = old_negative_by_id.get(seed["id"], {})
        location = ROOT / seed["location"]
        coded_files = sorted(p for p in location.glob("*.json") if p.is_file()) if location.is_dir() else []
        if negative_complete:
            status = "COMPLETE"
        else:
            status = existing.get("status", "READY_FOR_CANDIDATE_COLLECTION")
            if coded_files and status == "READY_FOR_CANDIDATE_COLLECTION":
                status = "CANDIDATES_PRESENT_PENDING_REVIEW"
        negative_classes.append(merge_item({**seed, "status": status}, existing))

    negative_plan = {
        **{k: v for k, v in old_negative.items() if k not in {"control_classes", "posture", "completed_control_classes"}},
        "schema": "stegverse.site.tidc.negative_control_design.v0.1",
        "posture": "CANDIDATES_CODED_VALIDATED" if negative_complete else old_negative.get("posture", "DESIGN_ONLY_NOT_CODED_EVENTS"),
        "control_classes": negative_classes,
        "completed_control_classes": negative_completed,
        "coded_candidate_count": max(old_negative.get("coded_candidate_count", 0), negative_completed),
        "selection_boundary": "Candidate controls must be preserved even when they weaken the clustering hypothesis.",
        "authority_effect": "NONE",
    }

    aggregate_ids = ["NET-002", "AI-001", "AI-003"]
    by_id = {event["event_id"]: event for event in events}
    old_split = load(SPLIT_PLAN, {}) or {}
    old_split_by_id = {item.get("parent_event_id"): item for item in old_split.get("items", [])}
    split_items = []
    completed_splits = 0
    for event_id in aggregate_ids:
        event = by_id[event_id]
        location = f"data/tidc/tranche-02/splits/{event_id}/"
        required_outputs = ["split-manifest.json", "source-map.json", "date-evidence.json", "coding-delta.json"]
        outputs_present = all((ROOT / location / name).is_file() for name in required_outputs)
        task_state = split_task_state(event_id)
        complete = outputs_present and task_state == "COMPLETE"
        if complete:
            completed_splits += 1
        status = "COMPLETE" if complete else (
            "OUTPUTS_PRESENT_PENDING_REVIEW" if outputs_present else "READY_FOR_SOURCE_BOUND_SPLIT"
        )
        seed = {
            "parent_event_id": event_id,
            "parent_event_name": event["event_name"],
            "location": location,
            "status": status,
            "required_outputs": required_outputs,
            "rule": "Do not alter tranche 01; create child candidate records and identify every inherited or changed field.",
        }
        split_items.append(merge_item(seed, old_split_by_id.get(event_id)))

    split_plan = {
        **{k: v for k, v in old_split.items() if k not in {"items", "completed_split_count", "remaining_split_count"}},
        "schema": "stegverse.site.tidc.aggregate_event_split_plan.v0.1",
        "posture": "TRANCHE_02_PREPARATION",
        "items": split_items,
        "completed_split_count": completed_splits,
        "remaining_split_count": len(aggregate_ids) - completed_splits,
        "authority_effect": "NONE",
    }

    old_queue = load(QUEUE, {}) or {}
    old_queue_by_id = {item.get("id"): item for item in old_queue.get("tasks", [])}
    queue_seed = [
        {
            "id": "TIDC-IW-001",
            "owner_repo": "StegVerse-Labs/Site",
            "location": SOURCE_PLAN.relative_to(ROOT).as_posix(),
            "status": "COMPLETE" if source_completed == len(events) else "ACTIVE",
            "task": "Expand seed-event primary-source records.",
            "completed_units": source_completed,
            "total_units": len(events),
            "next_location": None if first_missing is None else first_missing["location"],
            "next_task_id": None if first_missing is None else first_missing["task_id"],
        },
        {
            "id": "TIDC-IW-002",
            "owner_repo": "StegVerse-Labs/Site",
            "location": NEGATIVE_PLAN.relative_to(ROOT).as_posix(),
            "status": "COMPLETE" if negative_complete else old_queue_by_id.get("TIDC-IW-002", {}).get("status", "ACTIVE"),
            "task": "Collect and code negative controls and placebo candidates.",
            "completed_units": negative_completed,
            "total_units": 3,
        },
        {
            "id": "TIDC-IW-003",
            "owner_repo": "StegVerse-Labs/Site",
            "location": SPLIT_PLAN.relative_to(ROOT).as_posix(),
            "status": "COMPLETE" if completed_splits == len(aggregate_ids) else "ACTIVE",
            "task": "Split aggregate pilot events into source-bound tranche-02 candidates.",
            "completed_units": completed_splits,
            "total_units": len(aggregate_ids),
        },
        {
            "id": "TIDC-IW-004",
            "owner_repo": "StegVerse-Labs/Site",
            "location": "data/tidc/blinded-coding/returns/",
            "status": old_queue_by_id.get("TIDC-IW-004", {}).get("status", "OBSERVED_NOT_HALTING"),
            "task": "Process any return that appears through the existing validator, receipt, and comparison chain.",
        },
    ]
    queue = {
        **{k: v for k, v in old_queue.items() if k not in {"tasks", "development_halted"}},
        "schema": "stegverse.site.tidc.internal_work_queue.v0.1",
        "development_halted": False,
        "serial_dependency_policy": "A missing serial artifact cannot block repository-owned source, control, split, validation, or publication-preparation work.",
        "tasks": [merge_item(seed, old_queue_by_id.get(seed["id"])) for seed in queue_seed],
        "authority_effect": "NONE",
    }
    # Derived state is authoritative over stale queue state for source/control/split lanes.
    for task in queue["tasks"]:
        if task["id"] == "TIDC-IW-001":
            task.update(queue_seed[0])
        elif task["id"] == "TIDC-IW-002":
            task.update(queue_seed[1])
        elif task["id"] == "TIDC-IW-003":
            task.update(queue_seed[2])

    write(SOURCE_PLAN, source_plan)
    write(NEGATIVE_PLAN, negative_plan)
    write(SPLIT_PLAN, split_plan)
    write(QUEUE, queue)

    outputs = {
        SOURCE_PLAN.relative_to(ROOT).as_posix(): digest(source_plan),
        NEGATIVE_PLAN.relative_to(ROOT).as_posix(): digest(negative_plan),
        SPLIT_PLAN.relative_to(ROOT).as_posix(): digest(split_plan),
        QUEUE.relative_to(ROOT).as_posix(): digest(queue),
    }
    receipt = {
        "schema": "stegverse.site.tidc.internal_advancement_receipt.v0.2",
        "executor": "scripts/advance_tidc_internal_work.py",
        "source_ledger_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        "outputs": outputs,
        "tasks_activated": [task["id"] for task in queue["tasks"] if task["status"] != "COMPLETE"],
        "source_expansion_completed": source_completed,
        "source_expansion_total": len(events),
        "aggregate_splits_completed": completed_splits,
        "aggregate_splits_total": len(aggregate_ids),
        "negative_controls_completed": negative_completed,
        "negative_controls_total": 3,
        "development_halted": False,
        "research_claim_effect": "NONE",
        "authority_effect": "NONE",
    }
    write(RECEIPT, receipt)
    print("TIDC_INTERNAL_ADVANCEMENT=PASS")
    print(f"source_expansion={source_completed}/{len(events)}")
    print(f"aggregate_splits={completed_splits}/{len(aggregate_ids)}")
    print(f"negative_controls={negative_completed}/3")
    print("development_halted=false")
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
