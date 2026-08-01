#!/usr/bin/env python3
"""Observe and continue the StegVerse Marketplace-Coinbase accessibility layer.

Every task is represented with an exact repository or issue location. The controller
executes the importer, validates the resulting status digest and authority boundaries,
and writes a durable task state. It never waits on an unnamed external task.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "marketplace-coinbase-first-accessibility-status.json"
TASK_STATE = ROOT / "data" / "marketplace-coinbase-first-accessibility-task-state.json"
IMPORTER = ROOT / "scripts" / "import_marketplace_coinbase_first_accessibility.py"
ISSUE = "StegVerse-Labs/Site#130"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def validate_status(status: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    body = {key: value for key, value in status.items() if key != "status_digest"}
    if status.get("status_digest") != digest(body):
        failures.append("status_digest_mismatch")
    if status.get("schema") != "stegverse.site.marketplace_coinbase_first_accessibility.v1":
        failures.append("unsupported_status_schema")
    for field in (
        "publication_authority",
        "release_authority",
        "execution_authority",
        "live_authority",
        "custody_authority",
        "withdrawal_authority",
    ):
        if status.get(field) != "NOT_GRANTED":
            failures.append(f"{field}_boundary_invalid")
    if status.get("authority_effect") is not False:
        failures.append("authority_effect_invalid")
    if status.get("activation_effect") is not False:
        failures.append("activation_effect_invalid")
    if status.get("status") == "ACCESSIBLE":
        if status.get("paper_trading_accessible") is not True:
            failures.append("accessible_without_paper_trading_accessible")
        if not status.get("source_commit_sha"):
            failures.append("accessible_without_source_commit")
        if not status.get("source_workflow_run_id"):
            failures.append("accessible_without_source_workflow_run")
        if not status.get("source_receipt_digest"):
            failures.append("accessible_without_source_receipt_digest")
    return failures


def task(task_id: str, state: str, location: str, evidence: list[str], stop_condition: str) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "state": state,
        "location": location,
        "evidence": evidence,
        "stop_condition": stop_condition,
    }


def main() -> int:
    run = subprocess.run(["python", str(IMPORTER)], cwd=ROOT, text=True, capture_output=True, check=False)
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    failures = validate_status(status)

    accessible = status.get("status") == "ACCESSIBLE" and not failures and run.returncode == 0
    source_state = "COMPLETED" if accessible else "RUNNING"
    activation_state = "COMPLETED" if accessible else "BLOCKED_BY_MACHINE_EVIDENCE"

    tasks = [
        task(
            "SITE-MCFA-001",
            "COMPLETED",
            "StegVerse-Labs/Site/data/marketplace-coinbase-first-accessibility-source-observation.json",
            [
                "StegVerse-Labs/crypto-bot run 30681165495",
                "StegVerse-Labs/crypto-bot job 91318313997",
                "StegVerse-Labs/crypto-bot artifact 8812256423",
            ],
            "immutable observed source validates",
        ),
        task(
            "SITE-MCFA-002",
            source_state,
            "StegVerse-Labs/Site/scripts/import_marketplace_coinbase_first_accessibility.py",
            ["StegVerse-Labs/Site/data/marketplace-coinbase-first-accessibility-status.json"],
            "status is ACCESSIBLE with valid status_digest",
        ),
        task(
            "SITE-MCFA-003",
            source_state,
            "StegVerse-Labs/Site/.github/workflows/import-marketplace-coinbase-first-accessibility.yml",
            ["Site workflow run, job, logs, and artifact"],
            "authoritative workflow conclusion is success",
        ),
        task(
            "SITE-MCFA-004",
            activation_state,
            ISSUE,
            ["data/marketplace-coinbase-first-accessibility-task-state.json"],
            "issue closes only after SITE-MCFA-001 through SITE-MCFA-003 are completed",
        ),
    ]

    body = {
        "schema": "stegverse.site.marketplace_coinbase_first_accessibility_task_state.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "controller": "scripts/continue_marketplace_coinbase_first_accessibility.py",
        "controller_workflow": ".github/workflows/continue-marketplace-coinbase-first-accessibility.yml",
        "issue": ISSUE,
        "state": "ACTIVE" if accessible else "BUILDING",
        "activation_ready": accessible,
        "importer_exit_code": run.returncode,
        "importer_stdout_tail": run.stdout[-2000:],
        "importer_stderr_tail": run.stderr[-2000:],
        "status": status.get("status"),
        "status_digest": status.get("status_digest"),
        "validation_failures": failures,
        "tasks": tasks,
        "external_tasks": [],
        "continuation_policy": {
            "unnamed_external_tasks_forbidden": True,
            "pending_status_must_map_to_repository_task": True,
            "controller_reexecutes_until_terminal": True,
            "terminal_success": "ACCESSIBLE",
            "terminal_failure": "REJECTED_WITH_EXACT_REPOSITORY_FAILURE",
        },
        "publication_authority": "NOT_GRANTED",
        "release_authority": "NOT_GRANTED",
        "execution_authority": "NOT_GRANTED",
        "live_authority": "NOT_GRANTED",
        "custody_authority": "NOT_GRANTED",
        "withdrawal_authority": "NOT_GRANTED",
    }
    payload = {**body, "task_state_digest": digest(body)}
    TASK_STATE.parent.mkdir(parents=True, exist_ok=True)
    TASK_STATE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"state": payload["state"], "activation_ready": accessible, "status": status.get("status")}, sort_keys=True))
    return 0 if accessible else 2


if __name__ == "__main__":
    raise SystemExit(main())
