#!/usr/bin/env python3
"""Persist bounded retry evidence from the latest autonomy runtime verification."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data/autonomy/runtime-verification-evidence.json"
POLICY = ROOT / "data/autonomy/freshness-policy.json"
OUT = ROOT / "data/autonomy/runtime-retry-state.json"
MAX_HISTORY = 24


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> None:
    evidence = load(EVIDENCE)
    policy = load(POLICY)
    prior: dict[str, Any] = {}
    if OUT.is_file():
        prior = load(OUT)

    failed = list(evidence.get("failed_required_check_ids", []))
    state = str(evidence.get("state", "FAIL"))
    history = list(prior.get("history", []))
    history.append({
        "observed_at": evidence.get("generated_at"),
        "state": state,
        "passed_required_checks": evidence.get("passed_required_checks"),
        "required_checks": evidence.get("required_checks"),
        "failed_required_check_ids": failed,
        "automatic_retry_required": state != "PASS",
    })
    history = history[-MAX_HISTORY:]

    consecutive_failures = 0
    for item in reversed(history):
        if item.get("state") == "PASS":
            break
        consecutive_failures += 1

    payload = {
        "schema_version": "1.0",
        "repository": "StegVerse-Labs/Site",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "latest_runtime_state": state,
        "latest_failed_required_check_ids": failed,
        "automatic_retry_required": state != "PASS",
        "next_retry_owner": "StegVerse-Labs/Site/.github/workflows/autonomy-telemetry.yml",
        "next_retry_schedule": "hourly and on relevant autonomy changes",
        "consecutive_failures": consecutive_failures,
        "freshness_policy_id": policy.get("policy_id"),
        "maximum_age_minutes": policy.get("maximum_age_minutes"),
        "history": history,
        "authority": {
            "retry_record_is_completion": False,
            "retry_record_is_release_authority": False,
            "manual_user_action_required": False,
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"state": state, "consecutive_failures": consecutive_failures, "retry_required": state != "PASS"}))


if __name__ == "__main__":
    main()
