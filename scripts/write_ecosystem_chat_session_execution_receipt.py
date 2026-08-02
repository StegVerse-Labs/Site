#!/usr/bin/env python3
"""Write a deterministic receipt for the Ecosystem Chat session execution inventory."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "ecosystem-chat-session-execution-inventory.json"
OUTPUT = ROOT / "evidence" / "ecosystem-chat" / "session-execution-receipt.json"
ACTIVE = {"CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION"}
TERMINAL = {"COMPLETE", "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def determine_state(tasks: list[dict[str, Any]]) -> str:
    if any(task.get("claim_state") == "FAILED" for task in tasks):
        return "FAILED"
    if any(task.get("claim_state") == "BLOCKED" and task.get("archival_dependency") for task in tasks):
        return "BLOCKED"
    if any(task.get("claim_state") in ACTIVE for task in tasks):
        return "CLAIMED"
    if any(task.get("claim_state") == "UNCLAIMED" and task.get("archival_dependency") for task in tasks):
        return "REVIEW_REQUIRED"
    if all(task.get("claim_state") in TERMINAL or not task.get("archival_dependency") for task in tasks):
        return "COMPLETE"
    return "RETRY"


def next_task(tasks: list[dict[str, Any]]) -> dict[str, Any] | None:
    priority = ["UNCLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "BLOCKED"]
    for state in priority:
        for task in tasks:
            if task.get("claim_state") == state and task.get("next_action") != "none":
                return {
                    "task_id": task.get("task_id"),
                    "owner": task.get("owner"),
                    "repository": task.get("destination_repository"),
                    "location": task.get("location"),
                    "action": task.get("next_action"),
                    "release_condition": task.get("release_condition") or task.get("claim_release_condition"),
                }
    return None


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    tasks = inventory["tasks"]
    inventory_sha256 = hashlib.sha256(canonical_bytes(inventory)).hexdigest()
    state = determine_state(tasks)
    receipt = {
        "schema": "stegverse.session-execution-receipt.v0.1",
        "inventory_id": inventory["inventory_id"],
        "canonical_repository": inventory["canonical_repository"],
        "canonical_branch": inventory["canonical_branch"],
        "inventory_sha256": inventory_sha256,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": state,
        "authority_effect": "NONE",
        "counts": {
            "tasks": len(tasks),
            "complete": sum(task.get("claim_state") == "COMPLETE" for task in tasks),
            "active_claims": sum(task.get("claim_state") in ACTIVE for task in tasks),
            "blocked": sum(task.get("claim_state") == "BLOCKED" for task in tasks),
            "unclaimed": sum(task.get("claim_state") == "UNCLAIMED" for task in tasks),
            "archival_dependencies": sum(bool(task.get("archival_dependency")) for task in tasks),
            "unresolved_archival_dependencies": sum(bool(task.get("archival_dependency")) and task.get("claim_state") not in TERMINAL for task in tasks),
        },
        "active_claims": [
            {
                "task_id": task["task_id"],
                "claim_state": task["claim_state"],
                "owner": task["owner"],
                "location": task["location"],
                "expires_at": task.get("claim_expires_at"),
                "release_condition": task.get("claim_release_condition"),
            }
            for task in tasks if task.get("claim_state") in ACTIVE
        ],
        "blocked_tasks": [
            {
                "task_id": task["task_id"],
                "owner": task["owner"],
                "repository": task["destination_repository"],
                "location": task["location"],
                "blocker": task.get("blocker"),
                "release_condition": task.get("release_condition"),
            }
            for task in tasks if task.get("claim_state") == "BLOCKED"
        ],
        "next_executable_task": next_task(tasks),
        "archive_ready": state == "COMPLETE",
        "archive_reason": "All session goals are complete, superseded, or merged and no unresolved archival dependencies remain." if state == "COMPLETE" else "Durable continuation exists, but one or more inventory items remain active, blocked, or unclaimed.",
    }
    receipt["receipt_sha256"] = hashlib.sha256(canonical_bytes(receipt)).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"SESSION_EXECUTION_RECEIPT={OUTPUT.relative_to(ROOT)}")
    print(f"STATE={state}")
    print(f"ARCHIVE_READY={str(receipt['archive_ready']).lower()}")
    print(f"RECEIPT_SHA256={receipt['receipt_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
