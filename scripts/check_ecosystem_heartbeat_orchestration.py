#!/usr/bin/env python3
"""Validate the Site health-relative heartbeat and HIL priority contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "ecosystem-heartbeat-state.json"
DOC = ROOT / "docs" / "ECOSYSTEM_HEARTBEAT_ORCHESTRATION.md"


def main() -> int:
    failures: list[str] = []
    if not STATE.exists():
        failures.append("missing data/ecosystem-heartbeat-state.json")
    if not DOC.exists():
        failures.append("missing docs/ECOSYSTEM_HEARTBEAT_ORCHESTRATION.md")
    if failures:
        print("ECOSYSTEM_HEARTBEAT_ORCHESTRATION_FAIL")
        for failure in failures:
            print(failure)
        return 1

    state = json.loads(STATE.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    required_state = {
        "heartbeat_mode": "TRANSITION_DRIVEN",
        "time_role": "WATCHDOG_ONLY",
    }
    for key, expected in required_state.items():
        if state.get(key) != expected:
            failures.append(f"{key} must equal {expected}")

    if not isinstance(state.get("ecosystem_heartbeat"), int) or state["ecosystem_heartbeat"] < 0:
        failures.append("ecosystem_heartbeat must be a non-negative integer")
    if not isinstance(state.get("repository_heartbeat"), int) or state["repository_heartbeat"] < 0:
        failures.append("repository_heartbeat must be a non-negative integer")
    if not isinstance(state.get("task_sequence"), int) or state["task_sequence"] < 0:
        failures.append("task_sequence must be a non-negative integer")

    health = state.get("health_model", {})
    for marker in (
        "interpretation_is_relative_to_system_health",
        "missing_heartbeat_is_failure_only_when_progress_was_expected",
        "blocked_but_observed_is_not_equivalent_to_failed",
        "watchdog_does_not_imply_progress",
    ):
        if health.get(marker) is not True:
            failures.append(f"health_model.{marker} must be true")

    hil = state.get("hil_priority", {})
    if hil.get("goal") != "FIRST_SEAMLESS_HIL_USER_EXPERIENCE":
        failures.append("HIL goal is not the first seamless user experience")
    if hil.get("priority") != "HIGHEST_EXCLUSIVE_INTEGRATION_SEQUENCE":
        failures.append("HIL is not the highest exclusive integration sequence")
    if hil.get("heartbeat_must_not_delay_vertical_slice") is not True:
        failures.append("heartbeat must not delay the HIL vertical slice")

    if state.get("work_state") == "IDLE":
        expected = f"end of current work task sequence {state['task_sequence']:04d}, no tasks running"
        if state.get("task_sequence_label") != expected:
            failures.append("idle task_sequence_label is not canonical")
        if state.get("active_tasks"):
            failures.append("IDLE state cannot contain active tasks")

    required_doc_markers = (
        "The ecosystem heartbeat is a governed continuity signal",
        "The live working state is both a receiver and transmitter",
        "Time detects silence; it does not manufacture progress.",
        "The first seamless HIL user experience is the highest-priority exclusive integration sequence",
        "Heartbeat implementation observes and coordinates this vertical slice.",
    )
    for marker in required_doc_markers:
        if marker not in doc:
            failures.append(f"heartbeat contract missing marker: {marker}")

    if failures:
        print("ECOSYSTEM_HEARTBEAT_ORCHESTRATION_FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
