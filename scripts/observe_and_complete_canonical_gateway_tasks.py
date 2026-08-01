#!/usr/bin/env python3
"""Observe canonical gateway activation tasks from repository evidence.

This script prevents development from halting at a prose status. It derives task
state from files and invariants, writes a durable receipt, and fails until every
locally completable task is complete. Merge and deployment remain explicit
repository/control-plane transitions rather than unnamed external tasks.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/development-tasks/canonical-gateway-activation.json"
BINDING = ROOT / "assets/ecosystem-node-gateway-binding.js"
LOADER = ROOT / "assets/conectrr-interop.js"
HTML = ROOT / "ecosystem-chat.html"
WORKFLOW = ROOT / ".github/workflows/observe-complete-canonical-gateway-tasks.yml"
REPORT = ROOT / "reports/canonical-gateway-task-status.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def inspect() -> dict:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    binding = BINDING.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    checks = {
        "CG-ACT-001": all(
            marker in loader
            for marker in (
                "assets/ecosystem-node-gateway-binding.js",
                "loadGatewayBinding",
                "canonicalGatewayBinding = 'active'",
            )
        ) and "assets/ecosystem-node-views.js" in html,
        "CG-ACT-002": all(
            marker in binding
            for marker in (
                "authority_effect: 'NONE'",
                "silent_repair_allowed: false",
                "rehash_allowed: false",
                "reorder_allowed: false",
                "importCanonicalEvents",
            )
        ),
        "CG-ACT-003": all(
            marker in workflow
            for marker in (
                "observe_and_complete_canonical_gateway_tasks.py",
                "canonical-gateway-task-status.json",
                "workflow_dispatch",
                "pull_request",
                "push",
            )
        ),
    }

    tasks = []
    for task in ledger["tasks"]:
        task = dict(task)
        if task["task_id"] in checks:
            task["state"] = "COMPLETE" if checks[task["task_id"]] else "BLOCKED_BY_REPOSITORY_EVIDENCE"
        tasks.append(task)

    local_complete = all(checks.values())
    receipt = {
        "schema": "stegverse.development-task-observation.v1",
        "goal_id": ledger["goal_id"],
        "repository": ledger["repository"],
        "branch": ledger["branch"],
        "locally_completable_tasks_complete": local_complete,
        "next_transition": "MERGE_PULL_REQUEST" if local_complete else "CONTINUE_IMPLEMENTATION",
        "tasks": tasks,
        "authority_effect": "NONE",
        "status_only_halt_permitted": False,
    }
    receipt["receipt_sha256"] = hashlib.sha256(canonical(receipt)).hexdigest()
    return receipt


def main() -> int:
    receipt = inspect()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["locally_completable_tasks_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
