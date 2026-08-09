#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "steggate-four-app-status.json"
HANDOFF = ROOT / "docs" / "STEGGATE_FOUR_APP_MIRROR_HANDOFF.md"
APPS = {"ecosystem_chat", "vacc", "math_solver", "hil"}
LABELS = {
    "ecosystem_chat": "Ecosystem Chat",
    "vacc": "VACC / VA Claims Chat",
    "math_solver": "Math Solver",
    "hil": "HIL experiment",
}
ORCH_BEGIN = "<!-- STEGGATE_FOUR_APP_ORCHESTRATION_BEGIN -->"
ORCH_END = "<!-- STEGGATE_FOUR_APP_ORCHESTRATION_END -->"
INTEGRATION_BEGIN = "<!-- STEGGATE_FOUR_APP_INTEGRATION_BEGIN -->"
INTEGRATION_END = "<!-- STEGGATE_FOUR_APP_INTEGRATION_END -->"
APP_BEGIN = "<!-- STEGGATE_FOUR_APP_APPLICATION_STATE_BEGIN -->"
APP_END = "<!-- STEGGATE_FOUR_APP_APPLICATION_STATE_END -->"
ORDER_BEGIN = "<!-- STEGGATE_FOUR_APP_EXECUTION_ORDER_BEGIN -->"
ORDER_END = "<!-- STEGGATE_FOUR_APP_EXECUTION_ORDER_END -->"


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
    expected_handoff_lines: list[str] = []
    expected_detail_markers: list[str] = [APP_BEGIN, APP_END]
    for name in ("ecosystem_chat", "vacc", "math_solver", "hil"):
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
        expected_handoff_lines.append(f"{LABELS[name]}: {percent}% ({completed}/{total})")
        expected_detail_markers.extend([
            f"### {LABELS[name]} — {percent}% execution-gate progress",
            f"Issue: `StegVerse-Labs/Site#{app.get('issue')}`.",
            f"Surface: `{app.get('surface')}`.",
            f"Machine state: `{app.get('state')}`.",
        ])
        for gate_name, gate_value in gates.items():
            expected_detail_markers.append(f"- `{gate_name}` — {'VERIFIED' if gate_value else 'NOT VERIFIED'}")
        for blocker in app.get("blockers") or []:
            expected_detail_markers.append(f"- {blocker}")

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

    orchestration = data.get("orchestration", {})
    if orchestration.get("state") != "COMPLETE":
        return fail("four-app progress orchestration must remain COMPLETE after observed validation")
    if orchestration.get("product_activation_effect") is not False:
        return fail("orchestration must not claim product activation effect")

    binding = data.get("common_runtime_binding")
    if not isinstance(binding, dict):
        return fail("missing common_runtime_binding")
    if binding.get("contract_version") != "stegverse.steggate.runtime-identity.v1":
        return fail("unexpected common runtime contract version")
    if binding.get("runtime_identity") != "stegverse:steggate:canonical:three-layer:v1":
        return fail("unexpected canonical runtime identity")
    if binding.get("canonical_owner") != "StegVerse-Labs/StegCore":
        return fail("unexpected canonical runtime owner")
    if binding.get("transport_identity_authoritative") is not False:
        return fail("transport identity must not be authoritative")
    if binding.get("activation_effect") is not False:
        return fail("common runtime integration cannot claim product activation effect")
    app_bindings = binding.get("application_bindings")
    if not isinstance(app_bindings, dict) or set(app_bindings) != APPS:
        return fail("common runtime application binding set mismatch")

    handoff = HANDOFF.read_text(encoding="utf-8")
    required_markers = [
        "Current execution progress",
        "Orchestration progress",
        "Common runtime identity integration",
        "Status-check contract",
        "Release / archive posture",
        ORCH_BEGIN,
        ORCH_END,
        INTEGRATION_BEGIN,
        INTEGRATION_END,
        APP_BEGIN,
        APP_END,
        ORDER_BEGIN,
        ORDER_END,
        f"Verified execution gates: {completed_sum} / {total_sum}",
        f"Aggregate execution progress: {aggregate_percent}%",
        f"Fully functional public applications: {functional} / 4",
        f"Goal complete: {str(goal_complete).lower()}",
        f"Archive ready: {str(goal_complete).lower()}",
        f"Last machine status timestamp: `{data.get('updated_at')}`",
        f"Runtime identity: `{binding.get('runtime_identity')}`.",
        f"Contract version: `{binding.get('contract_version')}`.",
        f"Public direct bindings: {binding.get('public_direct_bindings')} / {binding.get('required_public_direct_bindings')}.",
        *expected_handoff_lines,
        *expected_detail_markers,
    ]
    for key in ("ecosystem_chat", "vacc", "math_solver", "hil"):
        required_markers.append(f"- {LABELS[key]}: `{app_bindings.get(key)}`")
    for task in data.get("next_execution_order") or []:
        required_markers.append(task)
    for marker in required_markers:
        if marker not in handoff:
            return fail(f"handoff missing or stale marker: {marker}")

    print(
        "STEGGATE_FOUR_APP_STATUS_PASS "
        f"completed_gates={completed_sum}/{total_sum} "
        f"execution_progress_percent={aggregate_percent} "
        f"functional_apps={functional}/4 goal_complete={str(goal_complete).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
