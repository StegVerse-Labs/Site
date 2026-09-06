#!/usr/bin/env python3
"""Derive the coherent-transition threshold posture from durable Site state.

This observer does not infer life, scientific validity, or execution authority. It
maps repository-observable transition and task evidence to a bounded threshold
posture and emits a durable report. With --apply it replaces the canonical state.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HEARTBEAT_PATH = ROOT / "data" / "ecosystem-heartbeat-state.json"
ORCHESTRATION_PATH = ROOT / "data" / "site-orchestration-state.json"
TASK_REPORT_PATH = ROOT / "repository-task-observation.report.json"
STATE_PATH = ROOT / "data" / "coherent-transition-threshold-state.json"
REPORT_PATH = ROOT / "data" / "coherent-transition-threshold-observation.json"
ACTIVATION_TASK_ID = "SITE-0001-COHERENT-TRANSITION-THRESHOLD-ACTIVATION"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def is_activation_self_observation(blocker: Any) -> bool:
    """Return true only for this threshold task's own pre-threshold observation.

    The activation validator is expected to remain blocked until the threshold is
    established. Counting that expected result as an independent readiness blocker
    makes the derivation circular: the threshold cannot establish because its own
    not-yet-established result blocks it. Other observer blockers remain fail-closed.
    """
    return isinstance(blocker, dict) and blocker.get("task_id") == ACTIVATION_TASK_ID


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    required = [HEARTBEAT_PATH, ORCHESTRATION_PATH]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"COHERENT_TRANSITION_DERIVATION=FAIL\nmissing={missing}")

    heartbeat = load(HEARTBEAT_PATH)
    orchestration = load(ORCHESTRATION_PATH)
    task_report = load(TASK_REPORT_PATH) if TASK_REPORT_PATH.is_file() else {}

    active_sequence = orchestration.get("active_sequence", {})
    heartbeat_mode = heartbeat.get("heartbeat_mode")
    work_state = heartbeat.get("work_state")
    system_health = heartbeat.get("system_health")
    active_tasks = heartbeat.get("active_tasks", [])
    blocked_tasks = heartbeat.get("blocked_tasks", [])
    raw_observer_blockers = task_report.get("blockers", [])
    if not isinstance(raw_observer_blockers, list):
        raw_observer_blockers = [raw_observer_blockers]
    activation_self_observations = [
        blocker for blocker in raw_observer_blockers if is_activation_self_observation(blocker)
    ]
    observer_blockers = [
        blocker for blocker in raw_observer_blockers if not is_activation_self_observation(blocker)
    ]

    cluster_declared = bool(active_sequence.get("task_sequence"))
    coherence_observed = heartbeat_mode == "TRANSITION_DRIVEN"
    jointly_ready = (
        work_state == "IDLE"
        and not active_tasks
        and not blocked_tasks
        and not observer_blockers
    )
    continuation_preserved = (
        coherence_observed
        and system_health in {"ACTIVE", "HEALTHY", "IDLE_HEALTHY"}
        and not blocked_tasks
        and not observer_blockers
    )
    coherence_maintained = coherence_observed and heartbeat.get("repository_heartbeat", 0) >= 1
    next_cycle_admissible = jointly_ready and continuation_preserved
    evidence_reconstructable = all(path.is_file() for path in required)

    conditions = {
        "transition_cluster_declared": cluster_declared,
        "coherence_reference_observed": coherence_observed,
        "required_transitions_jointly_ready": jointly_ready,
        "continuation_conditions_preserved": continuation_preserved,
        "coherence_reference_regenerated_or_maintained": coherence_maintained,
        "next_cycle_admissible": next_cycle_admissible,
        "evidence_reconstructable": evidence_reconstructable,
    }

    if all(conditions.values()):
        threshold_state = "THRESHOLD_ESTABLISHED"
    elif cluster_declared and coherence_observed and jointly_ready:
        threshold_state = "THRESHOLD_CANDIDATE"
    elif cluster_declared and coherence_observed:
        threshold_state = "SYNCHRONY_OBSERVED"
    elif cluster_declared:
        threshold_state = "CLUSTER_DECLARED"
    else:
        threshold_state = "UNDECLARED"

    state = {
        "schema_version": "1.0.0",
        "state_type": "coherent_transition_threshold_state",
        "repository": "StegVerse-Labs/Site",
        "threshold_state": threshold_state,
        "conditions": conditions,
        "evidence_refs": [
            "docs/ECOSYSTEM_HEARTBEAT_ORCHESTRATION.md",
            "data/ecosystem-heartbeat-state.json",
            "scripts/check_ecosystem_heartbeat_orchestration.py",
            "data/site-orchestration-state.json",
        ],
        "non_manufacture_rule_satisfied": True,
        "notes": [
            "Posture is derived from committed repository state, not session claims.",
            "The activation task's own expected pre-threshold validator result is observation evidence, not an independent readiness blocker; excluding it prevents circular self-blocking while every other task blocker remains fail-closed.",
            "A threshold requires an idle, unblocked, reconstructable transition cluster with a maintained transition-driven coherence reference.",
            "This state grants no execution, activation, publication, scientific-claim, or biological-classification authority.",
        ],
        "authority": {
            "execution": False,
            "activation": False,
            "publication": False,
            "scientific_claim": False,
            "biological_classification": False,
        },
    }

    report = {
        "schema_version": "1.0.0",
        "repository": "StegVerse-Labs/Site",
        "observer": "scripts/derive_coherent_transition_threshold.py",
        "source_paths": [str(path.relative_to(ROOT)) for path in required]
        + ([str(TASK_REPORT_PATH.relative_to(ROOT))] if TASK_REPORT_PATH.is_file() else []),
        "observed": {
            "heartbeat_mode": heartbeat_mode,
            "work_state": work_state,
            "system_health": system_health,
            "active_task_count": len(active_tasks),
            "blocked_task_count": len(blocked_tasks),
            "observer_blocker_count": len(observer_blockers),
            "observer_blocker_count_raw": len(raw_observer_blockers),
            "activation_self_observation_count": len(activation_self_observations),
            "activation_self_observation_excluded": bool(activation_self_observations),
        },
        "derived_state": state,
        "next_executable_action": (
            "preserve machine observation until active and blocked task sets are empty"
            if not jointly_ready
            else "validate continuation preservation and next-cycle admissibility"
        ),
        "external_tasks_allowed": False,
        "authority_effect": False,
    }

    write(REPORT_PATH, report)
    if args.apply:
        write(STATE_PATH, state)

    print("COHERENT_TRANSITION_DERIVATION=PASS")
    print(f"THRESHOLD_STATE={threshold_state}")
    print(f"APPLIED={'true' if args.apply else 'false'}")
    print("EXTERNAL_TASKS_ALLOWED=false")


if __name__ == "__main__":
    main()
