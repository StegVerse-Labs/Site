#!/usr/bin/env python3
"""Validate Site workload-health orchestration without redefining the HB32 protocol heartbeat."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "ecosystem-heartbeat-state.json"
DOC = ROOT / "docs" / "ECOSYSTEM_HEARTBEAT_ORCHESTRATION.md"

def main() -> int:
    failures=[]
    if not STATE.exists(): failures.append("missing data/ecosystem-heartbeat-state.json")
    if not DOC.exists(): failures.append("missing docs/ECOSYSTEM_HEARTBEAT_ORCHESTRATION.md")
    if failures:
        print("ECOSYSTEM_HEARTBEAT_ORCHESTRATION_FAIL"); [print(x) for x in failures]; return 1
    state=json.loads(STATE.read_text(encoding="utf-8")); doc=DOC.read_text(encoding="utf-8")
    if state.get("heartbeat_mode") != "TRANSITION_DRIVEN": failures.append("heartbeat_mode must remain TRANSITION_DRIVEN for workload health")
    if state.get("heartbeat_semantics") != "REPOSITORY_WORKLOAD_HEALTH_ONLY_NOT_HB_PROTOCOL_TIMING": failures.append("transition heartbeat must be explicitly workload-health only")
    if state.get("time_role") != "WATCHDOG_ONLY": failures.append("time_role must equal WATCHDOG_ONLY")
    protocol=state.get("canonical_protocol_heartbeat",{})
    expected={"anchor_epoch":32,"anchor_time_utc":"2026-08-23T19:00:00.000Z","period_ms":10,"reference_rate_hz":100,"progression_dependency":"OSCILLATOR_ONLY","continuous_process_required":False,"resident_sampler_required_for_progression":False,"observation_is_causal":False,"live_proof_state":"COMPLETED","live_proof_transition":"INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED","authority_effect":"NONE","github_runtime_authority":"NONE"}
    for key,value in expected.items():
        if protocol.get(key) != value: failures.append(f"canonical_protocol_heartbeat.{key} must equal {value!r}")
    for key in ("ecosystem_heartbeat","repository_heartbeat","task_sequence"):
        if not isinstance(state.get(key),int) or state[key] < 0: failures.append(f"{key} must be a non-negative integer")
    health=state.get("health_model",{})
    for marker in ("interpretation_is_relative_to_system_health","missing_heartbeat_is_failure_only_when_progress_was_expected","blocked_but_observed_is_not_equivalent_to_failed","watchdog_does_not_imply_progress"):
        if health.get(marker) is not True: failures.append(f"health_model.{marker} must be true")
    if health.get("workload_health_is_protocol_heartbeat") is not False: failures.append("workload health must not equal protocol heartbeat")
    if health.get("protocol_heartbeat_grants_execution_authority") is not False: failures.append("protocol heartbeat must not grant execution authority")
    if state.get("authority",{}).get("heartbeat_timing") is not False: failures.append("Site must not claim heartbeat timing authority")
    hil=state.get("hil_priority",{})
    if hil.get("goal") != "FIRST_SEAMLESS_HIL_USER_EXPERIENCE": failures.append("HIL goal is not the first seamless user experience")
    if hil.get("priority") != "HIGHEST_EXCLUSIVE_INTEGRATION_SEQUENCE": failures.append("HIL is not the highest exclusive integration sequence")
    if hil.get("heartbeat_must_not_delay_vertical_slice") is not True: failures.append("heartbeat must not delay the HIL vertical slice")
    if state.get("work_state") == "IDLE":
        expected_idle=f"end of current work task sequence {state['task_sequence']:04d}, no tasks running"
        if state.get("task_sequence_label") != expected_idle: failures.append("idle task_sequence_label is not canonical")
        if state.get("active_tasks"): failures.append("IDLE state cannot contain active tasks")
    for marker in ("The ecosystem heartbeat is a governed continuity signal","The live working state is both a receiver and transmitter","Time detects silence; it does not manufacture progress.","The first seamless HIL user experience is the highest-priority exclusive integration sequence","Heartbeat implementation observes and coordinates this vertical slice."):
        if marker not in doc: failures.append(f"heartbeat contract missing marker: {marker}")
    if failures:
        print("ECOSYSTEM_HEARTBEAT_ORCHESTRATION_FAIL"); [print(x) for x in failures]; return 1
    print("ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS:WORKLOAD_HEALTH_SEPARATE_FROM_HB32_PROTOCOL")
    return 0
if __name__ == "__main__": raise SystemExit(main())
