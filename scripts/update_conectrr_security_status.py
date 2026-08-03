#!/usr/bin/env python3
"""Persist Conectrr security-overlay workflow state and release its finite claim.

This script is intended for GitHub Actions after both deterministic validators
run. It records evidence without granting certification, admissibility, or
execution authority, and updates the durable session inventory atomically.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "data" / "conectrr-security-overlay.json"
INVENTORY = ROOT / "data" / "conectrr-session-goal-inventory.json"
STATUS = ROOT / "data" / "conectrr-security-overlay-status.json"
SECURITY_LOG = ROOT / "reports" / "conectrr-security-overlay-validation.txt"
RUNTIME_LOG = ROOT / "reports" / "conectrr-runtime-projection-validation.txt"
TASK_ID = "SV-SITE-CONECTRR-SEC-001"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    security_output = read_text(SECURITY_LOG)
    runtime_output = read_text(RUNTIME_LOG)
    security_pass = "CONECTRR_SECURITY_OVERLAY_CHECK=PASS" in security_output
    runtime_pass = "CONECTRR_RUNTIME_PROJECTION_CHECK=PASS" in runtime_output
    passed = security_pass and runtime_pass
    checked_at = datetime.now(timezone.utc).isoformat()
    overlay_sha256 = hashlib.sha256(OVERLAY.read_bytes()).hexdigest()

    payload = {
        "schema": "stegverse.conectrr.security-overlay.status.v1",
        "goal_id": TASK_ID,
        "state": "COMPLETE" if passed else "FAILED",
        "monitoring_state": "MACHINE_OWNED",
        "checked_at": checked_at,
        "repository": os.environ.get("GITHUB_REPOSITORY", "StegVerse-Labs/Site"),
        "commit": os.environ.get("GITHUB_SHA"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "security_validator_passed": security_pass,
        "runtime_integration_passed": runtime_pass,
        "overlay_sha256": overlay_sha256,
        "authority_effect": "none",
        "claims_not_created": [
            "certification",
            "authorization_to_operate",
            "agency_approval",
            "admissibility",
            "execution_authority",
        ],
        "next_executable_action": (
            "scheduled_monitoring_of_current_applicable_baselines"
            if passed
            else "inspect_failed_workflow_logs_and_retry_after_correction"
        ),
        "release_condition_satisfied": passed,
    }
    STATUS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    claim = next((item for item in inventory["claims"] if item["task_id"] == TASK_ID), None)
    if claim is None:
        raise SystemExit(f"missing inventory claim: {TASK_ID}")
    claim["state"] = "COMPLETE" if passed else "FAILED"
    claim["monitoring_state"] = "MACHINE_OWNED"
    claim["last_checked_at"] = checked_at
    claim["evidence"] = "data/conectrr-security-overlay-status.json"
    claim["release_condition_satisfied"] = passed
    claim["next_task_after_release"] = payload["next_executable_action"]
    inventory["updated_at"] = checked_at
    blockers = inventory["session_consolidation"].setdefault("archive_blockers", [])
    hosted_blocker = "first hosted security-overlay workflow execution has not yet been inspected"
    if passed:
        blockers[:] = [item for item in blockers if item != hosted_blocker]
    elif hosted_blocker not in blockers:
        blockers.insert(0, hosted_blocker)
    INVENTORY.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")

    print("CONECTRR_SECURITY_STATUS_UPDATE=PASS" if passed else "CONECTRR_SECURITY_STATUS_UPDATE=FAIL")
    print(f"state={payload['state']}")
    print("monitoring_state=MACHINE_OWNED")
    print("authority_effect=none")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
