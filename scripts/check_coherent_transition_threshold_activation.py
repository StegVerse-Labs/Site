#!/usr/bin/env python3
"""Fail closed unless the coherent-transition threshold is evidenced."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "coherent-transition-threshold-state.json"
REQUIRED = (
    "transition_cluster_declared",
    "coherence_reference_observed",
    "required_transitions_jointly_ready",
    "continuation_conditions_preserved",
    "coherence_reference_regenerated_or_maintained",
    "next_cycle_admissible",
    "evidence_reconstructable",
)


def fail(message: str) -> None:
    raise SystemExit(f"COHERENT_TRANSITION_THRESHOLD_ACTIVATION=BLOCKED\n{message}")


def main() -> None:
    if not STATE_PATH.is_file():
        fail("state is missing")
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    conditions = state.get("conditions", {})
    missing = [name for name in REQUIRED if conditions.get(name) is not True]
    if state.get("threshold_state") != "THRESHOLD_ESTABLISHED":
        fail(f"threshold_state={state.get('threshold_state')}; missing={missing}")
    if missing:
        fail(f"required predicates not satisfied: {missing}")
    if state.get("non_manufacture_rule_satisfied") is not True:
        fail("non-manufacture rule is not satisfied")
    refs = state.get("evidence_refs", [])
    unresolved = [ref for ref in refs if not isinstance(ref, str) or not (ROOT / ref).is_file()]
    if unresolved:
        fail(f"unresolved evidence refs: {unresolved}")
    print("COHERENT_TRANSITION_THRESHOLD_ACTIVATION=PASS")
    print("THRESHOLD_ESTABLISHED=true")
    print("EXTERNAL_TASKS_ALLOWED=false")
    print("AUTHORITY_EFFECT=false")


if __name__ == "__main__":
    main()
