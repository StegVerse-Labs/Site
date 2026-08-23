#!/usr/bin/env python3
"""Validate canonical TIDC session consolidation and continuation state."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data/tidc/session-consolidation-inventory.json"
HANDOFF = ROOT / "docs/TIDC_MIRROR_HANDOFF.md"
OPEN_HANDOFF = ROOT / "docs/TIDC_OPEN_RESEARCH_HANDOFF.md"
QUEUE = ROOT / "data/tidc/work-queue.json"
REQUIRED_PATHS = [
    "docs/TIDC_MIRROR_HANDOFF.md",
    "docs/TIDC_OPEN_RESEARCH_HANDOFF.md",
    "data/tidc/session-consolidation-inventory.json",
    "data/tidc/work-queue.json",
    "scripts/advance_tidc_internal_work.py",
    "scripts/reconcile_tidc_source_expansion.py",
    ".github/workflows/advance-tidc-internal-work.yml",
    ".github/workflows/reconcile-tidc-source-expansion.yml",
    ".github/workflows/check-tidc-research.yml",
]
ALLOWED_STATES = {
    "UNCLAIMED",
    "CLAIMED_FOR_IMPLEMENTATION",
    "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION",
    "MACHINE_OWNED",
    "BLOCKED",
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}


def fail(message: str) -> None:
    raise SystemExit(f"TIDC_SESSION_CONSOLIDATION_INVALID: {message}")


def load(path: Path):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).is_file():
            fail(f"required path missing: {relative}")

    inventory = load(INVENTORY)
    queue = load(QUEUE)
    handoff = HANDOFF.read_text(encoding="utf-8")
    open_handoff = OPEN_HANDOFF.read_text(encoding="utf-8")

    if inventory.get("schema") != "stegverse.site.tidc.session_consolidation_inventory.v1":
        fail("unexpected inventory schema")
    if inventory.get("repository") != "StegVerse-Labs/Site" or inventory.get("branch") != "main":
        fail("repository or branch mismatch")
    if inventory.get("development_halted") is not False:
        fail("development_halted must be false")
    if inventory.get("unspecified_external_tasks") != 0:
        fail("unspecified external tasks must be zero")
    if inventory.get("session_state") != "MERGED_INTO_CANONICAL_WORKSTREAM":
        fail("session state must be merged into canonical workstream")

    items = inventory.get("items")
    if not isinstance(items, list) or len(items) != 10:
        fail("inventory must contain exactly 10 session-goal items")

    seen = set()
    for item in items:
        task_id = item.get("task_id")
        if not task_id or task_id in seen:
            fail("task IDs must be nonempty and unique")
        seen.add(task_id)
        if item.get("claim_state") not in ALLOWED_STATES:
            fail(f"invalid claim state for {task_id}")
        for field in (
            "goal",
            "destination",
            "location",
            "owner",
            "completion_state",
            "validation_state",
            "integration_state",
            "evidence",
            "next_action",
        ):
            if not item.get(field):
                fail(f"{task_id} missing {field}")

    counts = inventory.get("counts", {})
    if counts.get("total_session_goals") != len(items):
        fail("total_session_goals mismatch")
    if counts.get("transferred_or_complete") != len(items):
        fail("not all session goals are transferred or complete")
    if counts.get("unassigned_tasks") != 0 or counts.get("external_tasks") != 0:
        fail("unassigned or external tasks remain")

    continuation = inventory.get("canonical_continuation", {})
    if continuation.get("site_handoff") != "docs/TIDC_MIRROR_HANDOFF.md":
        fail("canonical Site handoff mismatch")
    next_task = continuation.get("next_task")
    if next_task != "data/tidc/source-expansion/AI-002.json":
        fail("next task is not the expected AI-002 source record")

    if queue.get("development_halted") is not False:
        fail("work queue reports development halted")
    for task in queue.get("tasks", []):
        if not task.get("owner_repo") or not task.get("location"):
            fail("work queue task lacks owner or location")

    required_handoff_terms = [
        "MERGED INTO: StegVerse-Labs/Site/docs/TIDC_MIRROR_HANDOFF.md",
        "data/tidc/source-expansion/AI-002.json",
        "unspecified external tasks",
        "StegVerse-Labs/StegCore/docs/TIDC_EVIDENCE_CHAIN_MIRROR_HANDOFF.md",
        "Active TIDC research may remain incomplete while the originating conversation becomes archive-safe",
    ]
    for term in required_handoff_terms:
        if term not in handoff:
            fail(f"canonical handoff missing term: {term}")

    if "posture: RESEARCH_NOTE" not in open_handoff or "research_state: PILOT_NOT_CONFIRMATORY" not in open_handoff:
        fail("scientific authority boundary missing")

    print("TIDC_SESSION_CONSOLIDATION=PASS")
    print(f"goals={len(items)} transferred_or_complete={counts['transferred_or_complete']}")
    print(f"next_task={next_task}")
    print("development_halted=false external_tasks=0")


if __name__ == "__main__":
    main()
