#!/usr/bin/env python3
"""Advance repository-owned TIDC work without waiting on a serial evidence artifact.

This executor creates and refreshes planning artifacts derived from the committed
pilot ledger. It does not invent sources, recode events, or claim validation.
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


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(value: Any) -> str:
    material = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(material).hexdigest()


def main() -> None:
    ledger = load(LEDGER)
    events = ledger.get("events", [])
    if len(events) != 10:
        raise SystemExit("TIDC_INTERNAL_ADVANCEMENT_INVALID: expected 10 pilot events")

    source_items = []
    for event in events:
        source_items.append({
            "event_id": event["event_id"],
            "event_name": event["event_name"],
            "source_id": event["source_id"],
            "open_questions": event.get("open_questions", []),
            "task_location": f"data/tidc/source-expansion/{event['event_id']}.json",
            "status": "READY_FOR_PRIMARY_SOURCE_RECONSTRUCTION",
            "completion_rule": "Preserve exact source metadata, retrieval date, immutable URL or archive reference, and field-level evidence without silently recoding the seed ledger.",
        })

    source_plan = {
        "schema": "stegverse.site.tidc.source_expansion_plan.v0.1",
        "posture": "RESEARCH_NOTE_NOT_CONFIRMATORY",
        "source_ledger": LEDGER.relative_to(ROOT).as_posix(),
        "items": source_items,
        "authority_effect": "NONE",
    }

    negative_plan = {
        "schema": "stegverse.site.tidc.negative_control_design.v0.1",
        "posture": "DESIGN_ONLY_NOT_CODED_EVENTS",
        "control_classes": [
            {
                "id": "NC-CLASS-001",
                "class": "technology-present-without-discovery-output",
                "location": "data/tidc/negative-controls/technology-present-no-output/",
                "purpose": "Test whether mere technology availability is incorrectly treated as a discovery event.",
                "status": "READY_FOR_CANDIDATE_COLLECTION",
            },
            {
                "id": "NC-CLASS-002",
                "class": "publication-before-effective-access-placebo",
                "location": "data/tidc/negative-controls/pre-access-placebos/",
                "purpose": "Detect timelines that appear to peak before effective access or exposure.",
                "status": "READY_FOR_CANDIDATE_COLLECTION",
            },
            {
                "id": "NC-CLASS-003",
                "class": "supportive-technology-misattributed-as-necessary",
                "location": "data/tidc/negative-controls/supportive-not-necessary/",
                "purpose": "Test dependency-class inflation.",
                "status": "READY_FOR_CANDIDATE_COLLECTION",
            },
        ],
        "selection_boundary": "Candidate controls must be preserved even when they weaken the clustering hypothesis.",
        "authority_effect": "NONE",
    }

    aggregate_ids = ["NET-002", "AI-001", "AI-003"]
    split_items = []
    by_id = {event["event_id"]: event for event in events}
    for event_id in aggregate_ids:
        event = by_id[event_id]
        split_items.append({
            "parent_event_id": event_id,
            "parent_event_name": event["event_name"],
            "location": f"data/tidc/tranche-02/splits/{event_id}/",
            "status": "READY_FOR_SOURCE_BOUND_SPLIT",
            "required_outputs": [
                "split-manifest.json",
                "source-map.json",
                "date-evidence.json",
                "coding-delta.json",
            ],
            "rule": "Do not alter tranche 01; create child candidate records and identify every inherited or changed field.",
        })

    split_plan = {
        "schema": "stegverse.site.tidc.aggregate_event_split_plan.v0.1",
        "posture": "TRANCHE_02_PREPARATION",
        "items": split_items,
        "authority_effect": "NONE",
    }

    queue = {
        "schema": "stegverse.site.tidc.internal_work_queue.v0.1",
        "development_halted": False,
        "serial_dependency_policy": "A missing serial artifact cannot block repository-owned source, control, split, validation, or publication-preparation work.",
        "tasks": [
            {"id": "TIDC-IW-001", "owner_repo": "StegVerse-Labs/Site", "location": SOURCE_PLAN.relative_to(ROOT).as_posix(), "status": "ACTIVE", "task": "Expand seed-event primary-source records."},
            {"id": "TIDC-IW-002", "owner_repo": "StegVerse-Labs/Site", "location": NEGATIVE_PLAN.relative_to(ROOT).as_posix(), "status": "ACTIVE", "task": "Collect and code negative controls and placebo candidates."},
            {"id": "TIDC-IW-003", "owner_repo": "StegVerse-Labs/Site", "location": SPLIT_PLAN.relative_to(ROOT).as_posix(), "status": "ACTIVE", "task": "Split aggregate pilot events into source-bound tranche-02 candidates."},
            {"id": "TIDC-IW-004", "owner_repo": "StegVerse-Labs/Site", "location": "data/tidc/blinded-coding/returns/", "status": "OBSERVED_NOT_HALTING", "task": "Process any return that appears through the existing validator, receipt, and comparison chain."},
        ],
        "authority_effect": "NONE",
    }

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
        "schema": "stegverse.site.tidc.internal_advancement_receipt.v0.1",
        "executor": "scripts/advance_tidc_internal_work.py",
        "source_ledger_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        "outputs": outputs,
        "tasks_activated": ["TIDC-IW-001", "TIDC-IW-002", "TIDC-IW-003", "TIDC-IW-004"],
        "development_halted": False,
        "research_claim_effect": "NONE",
        "authority_effect": "NONE",
    }
    write(RECEIPT, receipt)
    print("TIDC_INTERNAL_ADVANCEMENT=PASS")
    print("development_halted=false")
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
