#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "steggate-four-app-status.json"
HANDOFF = ROOT / "docs" / "STEGGATE_FOUR_APP_MIRROR_HANDOFF.md"
APPS = {"ecosystem_chat", "vacc", "math_solver", "hil"}


def fail(message: str) -> int:
    print(f"STEGGATE_FOUR_APP_STATUS_FAIL: {message}")
    return 1


def main() -> int:
    if not STATUS.is_file():
        return fail("missing machine status")
    if not HANDOFF.is_file():
        return fail("missing mirror handoff")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.steggate.four_app_status.v1":
        return fail("unexpected schema_version")
    if data.get("goal_id") != "STEGGATE-FOUR-PUBLIC-APPS-001":
        return fail("unexpected goal_id")

    apps = data.get("applications")
    if not isinstance(apps, dict) or set(apps) != APPS:
        return fail("application set must be exactly ecosystem_chat,vacc,math_solver,hil")

    completed_sum = 0
    total_sum = 0
    functional = 0
    for name in sorted(APPS):
        app = apps[name]
        gates = app.get("gates")
        if not isinstance(gates, dict) or not gates:
            return fail(f"{name}: missing gates")
        if any(not isinstance(value, bool) for value in gates.values()):
            return fail(f"{name}: every gate must be boolean")
        completed = sum(1 for value in gates.values() if value)
        total = len(gates)
        percent = round(completed * 100 / total)
        if app.get("completed_gates") != completed:
            return fail(f"{name}: completed_gates mismatch")
        if app.get("total_gates") != total:
            return fail(f"{name}: total_gates mismatch")
        if app.get("progress_percent") != percent:
            return fail(f"{name}: progress_percent mismatch")
        if percent == 100:
            functional += 1
        completed_sum += completed
        total_sum += total

    aggregate = data.get("aggregate", {})
    aggregate_percent = round(completed_sum * 100 / total_sum)
    if aggregate.get("completed_gates") != completed_sum:
        return fail("aggregate completed_gates mismatch")
    if aggregate.get("total_gates") != total_sum:
        return fail("aggregate total_gates mismatch")
    if aggregate.get("execution_progress_percent") != aggregate_percent:
        return fail("aggregate execution_progress_percent mismatch")
    if aggregate.get("fully_functional_public_apps") != functional:
        return fail("fully_functional_public_apps mismatch")
    if aggregate.get("required_fully_functional_public_apps") != 4:
        return fail("required app count must remain 4")
    goal_complete = functional == 4
    if aggregate.get("goal_complete") is not goal_complete:
        return fail("goal_complete mismatch")
    if goal_complete and data.get("state") != "COMPLETE":
        return fail("complete goal must set state COMPLETE")
    if not goal_complete and data.get("state") == "COMPLETE":
        return fail("incomplete goal cannot set state COMPLETE")

    handoff = HANDOFF.read_text(encoding="utf-8")
    required_markers = [
        "Current execution progress",
        "Status-check contract",
        "Archive posture",
        "0/4" if not goal_complete else "4/4",
    ]
    for marker in required_markers:
        if marker not in handoff:
            return fail(f"handoff missing marker: {marker}")

    print(
        "STEGGATE_FOUR_APP_STATUS_PASS "
        f"completed_gates={completed_sum}/{total_sum} "
        f"execution_progress_percent={aggregate_percent} "
        f"functional_apps={functional}/4 goal_complete={str(goal_complete).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
