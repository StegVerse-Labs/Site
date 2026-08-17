#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_STATE = ROOT / "data" / "marketplace-coinbase-activation-tasks.json"
SITE_STATUS = ROOT / "data" / "marketplace-coinbase-accessibility-status.json"
FORBIDDEN = ("STEGVERSE_CROSS_REPO_READ_TOKEN", "GH_TOKEN", "GITHUB_TOKEN", "GITHUB_PAT", "MARKETPLACE_COINBASE_EVIDENCE_TOKEN")
EXPECTED = {
    "MC-01-CRYPTO-ACCESSIBILITY": "PASS",
    "MC-02-MARKETPLACE-COLLECTION": "COLLECTED",
    "MC-03-PUBLISHER-VERIFY": "VERIFIED",
    "MC-04-SITE-PROJECTION": "PAPER_ACCESSIBLE",
}


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def main() -> int:
    failures: list[str] = []
    active = [name for name in FORBIDDEN if os.environ.get(name)]
    if active:
        failures.append("forbidden credential environment: " + ",".join(sorted(active)))

    state = read_json(TASK_STATE)
    if state.get("schema") != "stegverse.site.marketplace_coinbase_activation_tasks.v3":
        failures.append("unexpected task-state schema")
    if state.get("state") != "COMPLETE":
        failures.append("task-state not COMPLETE")

    access = state.get("controller_access") or {}
    checks = {
        "credential_authority": "TV/TVC",
        "non_tv_tvc_token_required": False,
        "github_token_authority": "NONE",
        "observation_mode": "DIRECT_REPOSITORY_EVIDENCE_RECONCILED",
        "network_reobservation_required": False,
    }
    for key, expected in checks.items():
        if access.get(key) != expected:
            failures.append(f"controller_access.{key} mismatch")

    authority = state.get("authority") or {}
    if any(authority.get(key) is not False for key in ("publication", "release", "execution", "live")):
        failures.append("authority escalation detected")

    tasks = {item.get("task_id"): item for item in state.get("tasks", []) if isinstance(item, dict)}
    if set(tasks) != set(EXPECTED):
        failures.append("task set mismatch")
    else:
        for task_id, expected_status in EXPECTED.items():
            task = tasks[task_id]
            if task.get("state") != "COMPLETE":
                failures.append(f"{task_id}: not COMPLETE")
            if task.get("observed_status") != expected_status:
                failures.append(f"{task_id}: status mismatch")
            if task.get("stop_condition_satisfied") is not True:
                failures.append(f"{task_id}: stop condition not satisfied")
            if task.get("credential_used") is not False:
                failures.append(f"{task_id}: credential_used must be false")

    site = read_json(SITE_STATUS)
    if site.get("state") != "PAPER_ACCESSIBLE" or site.get("paper_trading_accessible") is not True:
        failures.append("Site bounded projection not PAPER_ACCESSIBLE")
    if site.get("live_trading_accessible") is not False:
        failures.append("Site live accessibility boundary invalid")
    for key in ("publication_authority", "release_authority", "execution_authority", "live_authority"):
        if site.get(key) != "NOT_GRANTED":
            failures.append(f"Site authority boundary invalid: {key}")

    if failures:
        for failure in failures:
            print("MARKETPLACE_CONTROLLER_VALIDATION_FAIL:", failure)
        return 1

    print("MARKETPLACE_CONTROLLER_TERMINAL_VALIDATION_PASS")
    print("credential_authority=TV/TVC")
    print("github_token_authority=NONE")
    print("network_reobservation_required=false")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
