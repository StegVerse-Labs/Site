#!/usr/bin/env python3
"""Validate Conectrr minimum interoperable handoff fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "conectrr-minimum-handoff.fixture.json"
EXPECTED_SCHEMA = "stegverse.conectrr.minimum-handoff.v0.1"

REQUIRED_TOP_LEVEL = {
    "handoff_id",
    "schema",
    "source",
    "intent",
    "recommendation",
    "unresolved_dependencies",
    "boundary",
}

REQUIRED_BOUNDARY_FALSE = {
    "consent_established",
    "authority_established",
    "admissibility_determined",
    "commitment_created",
    "execution_authorized",
}


def failure(record: dict[str, Any]) -> str | None:
    missing = REQUIRED_TOP_LEVEL - record.keys()
    if missing:
        return f"MISSING_FIELDS:{','.join(sorted(missing))}"

    handoff_id = record.get("handoff_id")
    if not isinstance(handoff_id, str) or not handoff_id.strip() or ":" not in handoff_id:
        return "UNSTABLE_HANDOFF_ID"

    if record.get("schema") != EXPECTED_SCHEMA:
        return "INVALID_SCHEMA"

    intent = record.get("intent") or {}
    if not isinstance(intent.get("summary"), str) or not intent["summary"].strip():
        return "UNDER_SPECIFIED_INTENT"

    recommendation = record.get("recommendation") or {}
    reasoning = recommendation.get("reasoning") or []
    evidence_refs = recommendation.get("evidence_refs") or []
    if not reasoning and not evidence_refs:
        return "UNDER_SPECIFIED_REASONING"

    boundary = record.get("boundary") or {}
    for key in REQUIRED_BOUNDARY_FALSE:
        if boundary.get(key) is True:
            return {
                "consent_established": "OVERREACH_CONSENT",
                "authority_established": "OVERREACH_AUTHORITY",
                "admissibility_determined": "OVERREACH_ADMISSIBILITY",
                "commitment_created": "OVERREACH_COMMITMENT",
                "execution_authorized": "OVERREACH_EXECUTION",
            }[key]

    if boundary.get("recommendation_only") is not True:
        return "OVERREACH_EXECUTION"

    unresolved = record.get("unresolved_dependencies")
    uncertainties = recommendation.get("uncertainties") or []
    if not isinstance(unresolved, list):
        return "UNRESOLVED_DEPENDENCY_HIDDEN"
    if not unresolved and not uncertainties:
        return "UNDER_SPECIFIED_UNCERTAINTY"

    return None


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    errors: list[str] = []

    for case in cases:
        case_id = case.get("case_id", "unknown")
        expected = case.get("expected")
        observed_failure = failure(case.get("record") or {})
        observed = "PASS" if observed_failure is None else "FAIL"

        if observed != expected:
            errors.append(f"{case_id}: expected {expected}, observed {observed} ({observed_failure})")
            continue

        expected_failure = case.get("expected_failure")
        if expected_failure and observed_failure != expected_failure:
            errors.append(
                f"{case_id}: expected failure {expected_failure}, observed {observed_failure}"
            )

    if errors:
        print("CONECTRR_MINIMUM_HANDOFF_CHECK=FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("CONECTRR_MINIMUM_HANDOFF_CHECK=PASS")
    print(f"cases={len(cases)}")
    print("boundary_failures=bidirectional")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
