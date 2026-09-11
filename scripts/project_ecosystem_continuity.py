#!/usr/bin/env python3
"""Create a public/private-safe Site projection from a canonical ECE evaluation.

This consumer does not evaluate continuity and must not infer health beyond the
canonical retained evaluation. Invalid input fails closed to INDETERMINATE.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EVALUATION_SCHEMA = "stegverse.ecosystem-continuity-evaluation.v1"
PROJECTION_SCHEMA = "stegverse.site-ecosystem-continuity-projection.v1"
AUTHORITY_EFFECT = "NONE_READ_ONLY_PROJECTION"
CONTINUITY_STATES = {
    "CONTINUOUS", "CONTINUOUS_WITH_DEGRADATION", "AT_RISK", "INTERRUPTED", "INDETERMINATE"
}
OBSERVATION_STATES = {
    "PASS", "FAIL", "DEGRADED", "UNKNOWN", "NOT_OBSERVED", "STALE", "UNREACHABLE", "PROBE_REQUIRED"
}
SAFE_FINDING_FIELDS = {
    "finding_id", "component_id", "predicate_id", "observation_state", "severity",
    "continuity_critical", "evidence_age_seconds", "authority_owner", "remediation_state"
}


def _indeterminate(reason: str) -> dict:
    return {
        "schema": PROJECTION_SCHEMA,
        "source_evaluation_id": None,
        "evaluated_at": None,
        "evaluator_version": None,
        "continuity_state": "INDETERMINATE",
        "source_available": False,
        "projection_error": reason,
        "completeness": None,
        "findings": [],
        "authority_effect": AUTHORITY_EFFECT,
    }


def project(evaluation: dict) -> dict:
    if evaluation.get("schema") != EVALUATION_SCHEMA:
        return _indeterminate("INVALID_EVALUATION_SCHEMA")
    if evaluation.get("authority_effect") != "NONE_DIAGNOSTIC_ONLY":
        return _indeterminate("INVALID_EVALUATION_AUTHORITY_EFFECT")
    continuity = evaluation.get("continuity_state")
    if continuity not in CONTINUITY_STATES:
        return _indeterminate("INVALID_CONTINUITY_STATE")

    safe_findings = []
    for finding in evaluation.get("findings", []):
        state = finding.get("observation_state")
        if state not in OBSERVATION_STATES:
            return _indeterminate("INVALID_OBSERVATION_STATE")
        safe = {key: finding.get(key) for key in SAFE_FINDING_FIELDS}
        # Evidence locators and free-form detail are intentionally not projected by v1.
        safe_findings.append(safe)

    return {
        "schema": PROJECTION_SCHEMA,
        "source_evaluation_id": evaluation.get("evaluation_id"),
        "evaluated_at": evaluation.get("evaluated_at"),
        "evaluator_version": evaluation.get("evaluator_version"),
        "continuity_state": continuity,
        "source_available": True,
        "projection_error": None,
        "completeness": evaluation.get("completeness"),
        "findings": safe_findings,
        "authority_effect": AUTHORITY_EFFECT,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        evaluation = json.loads(Path(args.input).read_text())
        result = project(evaluation)
    except (OSError, json.JSONDecodeError) as exc:
        result = _indeterminate(f"SOURCE_UNAVAILABLE:{type(exc).__name__}")
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
