#!/usr/bin/env python3
"""Fail-closed validator for the StegVerse live baseline readiness contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data/framework-evaluations/stegverse-live-baseline-readiness.json"
REQUIRED_TRUE = {
    "frozen_test_case",
    "self_declaration_record",
    "public_baseline_jsonl",
    "artifact_receipt_generator",
    "artifact_receipt_verifier",
}
RUNTIME_GATES = {
    "authorized_real_provider",
    "persistent_endpoint",
    "provider_usage_persistence",
    "master_records_custody",
    "transition_custody",
    "immutable_adapter_receipt",
    "post_execution_reconstruction",
    "public_endpoint_verification",
}
NO_AUTHORITY = {
    "comparison": False,
    "admissibility": False,
    "certification": False,
    "execution": False,
    "custody": False,
    "parentage": False,
}


def require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> int:
    if not READINESS.is_file():
        raise AssertionError("missing StegVerse live baseline readiness contract")
    payload = json.loads(READINESS.read_text(encoding="utf-8"))
    require(payload.get("schema_version") == "1.0.0", "unsupported schema_version")
    require(payload.get("framework_id") == "stegverse", "framework_id mismatch")
    require(payload.get("test_case_id") == "stegverse-public-baseline-v1", "test_case_id mismatch")
    require(payload.get("phase") == "STEGVERSE_LIVE_BASELINE_EXECUTION", "phase mismatch")

    inputs = payload.get("required_inputs") or {}
    require(REQUIRED_TRUE <= set(inputs), "missing developed baseline inputs")
    require(all(inputs.get(key) is True for key in REQUIRED_TRUE), "developed baseline input regressed")
    require(RUNTIME_GATES <= set(inputs), "missing runtime gate")

    all_runtime_ready = all(inputs.get(key) is True for key in RUNTIME_GATES)
    state = payload.get("state")
    if all_runtime_ready:
        require(state in {"READY", "EXECUTION_PENDING_OBSERVATION", "EXECUTION_COMPLETE"}, "ready runtime gates cannot remain BLOCKED")
    else:
        require(state == "BLOCKED", "incomplete runtime gates must fail closed as BLOCKED")
        require(payload.get("blocking_conditions"), "BLOCKED state requires blocking_conditions")
        require(payload.get("execution_authorized") is False, "BLOCKED state cannot authorize execution")
        require(payload.get("promotion_authorized") is False, "BLOCKED state cannot authorize promotion")
        require(payload.get("publication_authorized") is False, "BLOCKED state cannot authorize publication")

    require(payload.get("authority") == NO_AUTHORITY, "readiness contract authority boundary changed")
    transition = payload.get("next_transition") or {}
    require(transition.get("name") == "RUN_STEGVERSE_LIVE_BASELINE", "unexpected next transition")
    require(transition.get("resulting_state") == "EXECUTION_PENDING_OBSERVATION", "unexpected resulting state")
    require(len(transition.get("allowed_when") or []) >= 6, "next transition gate is incomplete")

    print(f"STEGVERSE LIVE BASELINE READINESS: {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
