#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "steggate-four-app-status.json"
HANDOFF = ROOT / "docs" / "STEGGATE_FOUR_APP_MIRROR_HANDOFF.md"
UNIFIED = ROOT / "data" / "unified-conversational-capabilities.json"
APPS = {"ecosystem_chat", "vacc", "math_solver", "hil"}
LABELS = {"ecosystem_chat":"Ecosystem Chat","vacc":"VACC / VA Claims Chat","math_solver":"Math Solver","hil":"HIL experiment"}
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
    if not STATUS.is_file() or not HANDOFF.is_file() or not UNIFIED.is_file(): return fail("missing machine status, handoff, or unified capability contract")
    data = json.loads(STATUS.read_text(encoding="utf-8")); unified = json.loads(UNIFIED.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.steggate.four_app_status.v1": return fail("unexpected schema_version")
    if data.get("goal_id") != "STEGGATE-FOUR-PUBLIC-APPS-001": return fail("unexpected goal_id")
    if unified.get("schema") != "stegverse.site.unified-conversational-capability.v1": return fail("unified capability contract schema mismatch")
    topology = data.get("topology_semantics") or {}
    expected = {
        "primary_public_conversational_surface":"ecosystem-chat.html",
        "legacy_four_app_name_is_accounting_only":True,
        "applications_object_represents_capability_family_gate_projections":True,
        "competing_primary_chat_applications":False,
        "specialty_capabilities_share_conversational_surface":True,
        "shared_runtime_owner":"StegVerse-org/LLM-adapter",
        "duplicate_provider_runtime_authority_allowed":False,
    }
    for key,value in expected.items():
        if topology.get(key) != value: return fail(f"legacy four-app topology not reconciled: {key}")
    if unified.get("primary_surface") != topology.get("primary_public_conversational_surface"): return fail("primary surface mismatch")
    if unified.get("shared_runtime_owner") != topology.get("shared_runtime_owner"): return fail("runtime owner mismatch")
    apps = data.get("applications")
    if not isinstance(apps,dict) or set(apps) != APPS: return fail("application accounting set mismatch")
    completed_sum=0; total_sum=0; functional=0; expected_lines=[]; markers=[APP_BEGIN,APP_END]
    for name in ("ecosystem_chat","vacc","math_solver","hil"):
        app=apps[name]; gates=app.get("gates")
        if not isinstance(gates,dict) or not gates or any(not isinstance(v,bool) for v in gates.values()): return fail(f"{name}: invalid gates")
        completed=sum(1 for v in gates.values() if v); total=len(gates); percent=round(completed*100/total)
        if app.get("completed_gates")!=completed or app.get("total_gates")!=total or app.get("progress_percent")!=percent: return fail(f"{name}: progress mismatch")
        completed_sum+=completed; total_sum+=total; functional += 1 if percent==100 else 0
        expected_lines.append(f"{LABELS[name]}: {percent}% ({completed}/{total})")
        markers += [f"### {LABELS[name]} — {percent}% execution-gate progress",f"Issue: `StegVerse-Labs/Site#{app.get('issue')}`.",f"Surface: `{app.get('surface')}`.",f"Machine state: `{app.get('state')}`."]
        markers += [f"- `{g}` — {'VERIFIED' if v else 'NOT VERIFIED'}" for g,v in gates.items()]
        markers += [f"- {b}" for b in (app.get("blockers") or [])]
    if not str(apps["vacc"].get("surface","")).startswith("ecosystem-chat.html -> VACC specialty"): return fail("VACC not shared-surface specialty")
    if not str(apps["math_solver"].get("surface","")).startswith("ecosystem-chat.html -> mathematics educator specialty"): return fail("math not shared-surface specialty")
    if not str(apps["hil"].get("surface","")).startswith("ecosystem-chat.html discovery/routing"): return fail("HIL not shared-surface discoverable")
    aggregate=data.get("aggregate",{}); aggregate_percent=round(completed_sum*100/total_sum); goal_complete=functional==4
    if aggregate.get("completed_gates")!=completed_sum or aggregate.get("total_gates")!=total_sum or aggregate.get("execution_progress_percent")!=aggregate_percent: return fail("aggregate mismatch")
    if aggregate.get("fully_functional_public_apps")!=functional or aggregate.get("required_fully_functional_public_apps")!=4 or aggregate.get("goal_complete") is not goal_complete: return fail("functional capability aggregate mismatch")
    if data.get("orchestration",{}).get("state")!="COMPLETE" or data.get("orchestration",{}).get("product_activation_effect") is not False: return fail("orchestration boundary invalid")
    binding=data.get("common_runtime_binding") or {}; app_bindings=binding.get("application_bindings") or {}
    if binding.get("contract_version")!="stegverse.steggate.runtime-identity.v1" or binding.get("runtime_identity")!="stegverse:steggate:canonical:three-layer:v1" or binding.get("canonical_owner")!="StegVerse-Labs/StegCore" or binding.get("transport_identity_authoritative") is not False or binding.get("activation_effect") is not False: return fail("runtime binding invalid")
    if set(app_bindings)!=APPS: return fail("runtime binding capability set mismatch")
    handoff=HANDOFF.read_text(encoding="utf-8")
    required=["legacy accounting name only","one primary public conversational surface","Current execution progress","Orchestration progress","Common runtime identity integration","Status-check contract","Release / archive posture",ORCH_BEGIN,ORCH_END,INTEGRATION_BEGIN,INTEGRATION_END,APP_BEGIN,APP_END,ORDER_BEGIN,ORDER_END,f"Verified execution gates: {completed_sum} / {total_sum}",f"Aggregate execution progress: {aggregate_percent}%",f"Fully functional public applications: {functional} / 4",f"Goal complete: {str(goal_complete).lower()}",f"Archive ready: {str(goal_complete).lower()}",f"Last machine status timestamp: `{data.get('updated_at')}`",f"Runtime identity: `{binding.get('runtime_identity')}`.",f"Contract version: `{binding.get('contract_version')}`.",f"Public direct bindings: {binding.get('public_direct_bindings')} / {binding.get('required_public_direct_bindings')}.",*expected_lines,*markers]
    required += [f"- {LABELS[k]}: `{app_bindings.get(k)}`" for k in ("ecosystem_chat","vacc","math_solver","hil")]
    required += list(data.get("next_execution_order") or [])
    for marker in required:
        if marker not in handoff: return fail(f"handoff missing or stale marker: {marker}")
    print(f"STEGGATE_FOUR_APP_STATUS_PASS completed_gates={completed_sum}/{total_sum} execution_progress_percent={aggregate_percent} functional_capabilities={functional}/4 goal_complete={str(goal_complete).lower()}")
    return 0


if __name__ == "__main__": raise SystemExit(main())
