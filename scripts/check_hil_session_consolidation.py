#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data/session-goal-inventories/HIL-RUNTIME-SESSION-2026-08-02.json"
HANDOFF = ROOT / "docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md"
REQUIRED_TASKS = {f"HIL-SESSION-{i:03d}" for i in range(1, 9)}
ALLOWED_CLAIMS = {
    "UNCLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED", "BLOCKED", "COMPLETE",
    "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


if not INVENTORY.is_file():
    fail(f"missing inventory: {INVENTORY.relative_to(ROOT)}")
if not HANDOFF.is_file():
    fail(f"missing handoff: {HANDOFF.relative_to(ROOT)}")

data = json.loads(INVENTORY.read_text())
if data.get("inventory_id") != "HIL-RUNTIME-SESSION-2026-08-02":
    fail("unexpected inventory_id")
if data.get("canonical_handoff") != "docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md":
    fail("canonical handoff mismatch")

tasks = data.get("tasks")
if not isinstance(tasks, list):
    fail("tasks must be a list")
ids = [task.get("task_id") for task in tasks]
if set(ids) != REQUIRED_TASKS or len(ids) != len(REQUIRED_TASKS):
    fail(f"task inventory must contain exactly {sorted(REQUIRED_TASKS)}")

for task in tasks:
    task_id = task["task_id"]
    for field in (
        "goal", "destination", "branch", "locations", "owner", "claim_state",
        "completion_state", "validation_state", "integration_state",
        "archival_dependency", "evidence", "next_action"
    ):
        if field not in task or task[field] in (None, "", []):
            fail(f"{task_id}: missing {field}")
    if task["claim_state"] not in ALLOWED_CLAIMS:
        fail(f"{task_id}: unsupported claim_state {task['claim_state']}")

archive_conditions = data.get("archive_conditions")
if not isinstance(archive_conditions, list) or len(archive_conditions) < 4:
    fail("archive_conditions incomplete")
if data.get("authority_effect") != "none":
    fail("inventory must not grant authority")

handoff = HANDOFF.read_text()
for marker in (
    "## Active goal", "## Canonical owners and claims", "## Incomplete operational work",
    "## Exact next tasks", "## Machine-owned automation", "## Validation commands",
    "## Integration and propagation obligations", "## Archive conditions",
    "MERGED INTO:"
):
    if marker not in handoff:
        fail(f"handoff missing marker: {marker}")
inventory_text = INVENTORY.read_text()
for task_id in sorted(REQUIRED_TASKS):
    if task_id not in inventory_text:
        fail(f"inventory does not preserve {task_id}")

print("PASS: HIL session inventory and canonical consolidation handoff are complete and fail-closed")
