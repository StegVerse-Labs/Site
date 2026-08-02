#!/usr/bin/env python3
"""Validate the repository-local coherent transition threshold posture."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "coherent-transition-threshold-state.json"
SCHEMA_PATH = ROOT / "data" / "coherent-transition-threshold.schema.json"

REQUIRED_CONDITIONS = (
    "transition_cluster_declared",
    "coherence_reference_observed",
    "required_transitions_jointly_ready",
    "continuation_conditions_preserved",
    "coherence_reference_regenerated_or_maintained",
    "next_cycle_admissible",
    "evidence_reconstructable",
)

VALID_STATES = {
    "UNDECLARED",
    "CLUSTER_DECLARED",
    "SYNCHRONY_OBSERVED",
    "THRESHOLD_CANDIDATE",
    "THRESHOLD_ESTABLISHED",
    "CONTINUITY_DEGRADED",
    "FAILED_CLOSED",
}


def fail(message: str) -> None:
    raise SystemExit(f"COHERENT_TRANSITION_THRESHOLD=FAIL\n{message}")


def main() -> None:
    if not STATE_PATH.is_file() or not SCHEMA_PATH.is_file():
        fail("state or schema is missing")

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("schema_version") != "1.0.0":
        fail("unsupported schema_version")
    if state.get("state_type") != "coherent_transition_threshold_state":
        fail("invalid state_type")
    if state.get("repository") != "StegVerse-Labs/Site":
        fail("repository mismatch")
    if state.get("threshold_state") not in VALID_STATES:
        fail("invalid threshold_state")

    conditions = state.get("conditions")
    if not isinstance(conditions, dict):
        fail("conditions must be an object")
    missing = [key for key in REQUIRED_CONDITIONS if key not in conditions]
    if missing:
        fail(f"missing conditions: {', '.join(missing)}")
    if any(not isinstance(conditions[key], bool) for key in REQUIRED_CONDITIONS):
        fail("all conditions must be boolean")

    refs = state.get("evidence_refs")
    if not isinstance(refs, list) or not refs:
        fail("evidence_refs must be a non-empty list")
    unresolved = [ref for ref in refs if not isinstance(ref, str) or not (ROOT / ref).is_file()]
    if unresolved:
        fail(f"unresolved evidence refs: {unresolved}")

    authority = state.get("authority", {})
    if any(authority.get(key) is not False for key in (
        "execution", "activation", "publication", "scientific_claim", "biological_classification"
    )):
        fail("authority flags must remain false")

    established = state["threshold_state"] == "THRESHOLD_ESTABLISHED"
    all_conditions = all(conditions[key] for key in REQUIRED_CONDITIONS)
    non_manufacture = state.get("non_manufacture_rule_satisfied") is True

    if established and not (all_conditions and non_manufacture):
        fail("THRESHOLD_ESTABLISHED requires all conditions and the non-manufacture rule")
    if all_conditions and non_manufacture and not established:
        fail("all threshold conditions are satisfied but threshold_state is not THRESHOLD_ESTABLISHED")

    print("COHERENT_TRANSITION_THRESHOLD=PASS")
    print(f"THRESHOLD_STATE={state['threshold_state']}")
    print(f"THRESHOLD_ESTABLISHED={'true' if established else 'false'}")
    print("EXTERNAL_TASKS_ALLOWED=false")
    print("AUTHORITY_EFFECT=false")


if __name__ == "__main__":
    main()
