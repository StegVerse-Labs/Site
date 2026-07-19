#!/usr/bin/env python3
"""Generate fail-closed autonomy roadmap state from current Site telemetry."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data/autonomy/live-status.json"
RUNTIME = ROOT / "data/autonomy/runtime-verification-evidence.json"
OUT = ROOT / "data/autonomy/roadmap-status.json"


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def node_map(live: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes = live.get("task_graph", {}).get("nodes", [])
    return {str(node.get("id")): node for node in nodes if isinstance(node, dict) and node.get("id")}


def status_is(nodes: dict[str, dict[str, Any]], node_id: str, expected: str) -> bool:
    return str(nodes.get(node_id, {}).get("status", "")).upper() == expected


def main() -> None:
    live = load(LIVE)
    runtime = load(RUNTIME) if RUNTIME.exists() else {}
    nodes = node_map(live)
    summary = live.get("summary", {})
    repositories = int(summary.get("repositories", 0) or 0)
    valid_evidence = int(summary.get("valid_completion_evidence", 0) or 0)
    next_actions = int(summary.get("next_actions", 0) or 0)
    corrective = live.get("corrective_actions", [])
    reasons = [str(item.get("reason", "")) for item in corrective if isinstance(item, dict)]
    enumeration_error = next((reason for reason in reasons if "HTTP 404" in reason), "")
    authority_block = next((reason for reason in reasons if "repository-scoped token" in reason), "")

    runtime_pass = runtime.get("state") == "PASS" and int(runtime.get("required_checks", 0)) > 0 and runtime.get("required_checks") == runtime.get("passed_required_checks")
    truth_complete = valid_evidence > 0 and not enumeration_error
    execution_complete = status_is(nodes, "public-execution-runners", "COMPLETE") and not authority_block
    governance_complete = execution_complete and valid_evidence > 0
    continuity_complete = all((truth_complete, execution_complete, runtime_pass, governance_complete))

    phases = [
        {
            "id": "truth-layer", "title": "Phase 1 — Truth layer",
            "implementation": "ADVANCED" if repositories else "PARTIAL",
            "operation": "COMPLETE" if truth_complete else "PARTIAL",
            "evidence": "SUFFICIENT" if valid_evidence else "INSUFFICIENT",
            "exit_gate": "COMPLETE" if truth_complete else "INCOMPLETE",
            "progress_percent": 100 if truth_complete else (67 if repositories else 20),
            "completed": ["public ecosystem inventory", "objective contract", "implementation and operational classification", "strict evidence inspection", "completion gate", "machine-owned action generation"],
            "remaining": [] if truth_complete else ["valid operational completion evidence for at least one repository", "successful enumeration of every configured organization", "successor freeze evidence"],
            "blockers": [item for item in [enumeration_error, f"{valid_evidence} of {repositories} repositories satisfy strict completion evidence"] if item],
        },
        {
            "id": "execution-layer", "title": "Phase 2 — Execution layer",
            "implementation": "ADVANCED" if next_actions else "PARTIAL",
            "operation": "COMPLETE" if execution_complete else "PARTIAL",
            "evidence": "SUFFICIENT" if execution_complete else "PARTIAL",
            "exit_gate": "COMPLETE" if execution_complete else "INCOMPLETE",
            "progress_percent": 100 if execution_complete else (46 if next_actions else 20),
            "completed": ["next-action planning", "bounded Site-owned dispatch", "deny-by-default cross-repository routing"],
            "remaining": [] if execution_complete else ["repository-owned bounded runners", "persistent retry and remediation evidence", "dependency-complete external execution"],
            "blockers": [authority_block] if authority_block else [],
        },
        {
            "id": "runtime-verification-layer", "title": "Phase 3 — Runtime verification layer",
            "implementation": "COMPLETE" if RUNTIME.exists() else "SPECIFIED",
            "operation": "COMPLETE" if runtime_pass else "FAILED_OR_NOT_OBSERVED",
            "evidence": "SUFFICIENT" if runtime_pass else ("RECORDED_FAILURE" if RUNTIME.exists() else "MISSING"),
            "exit_gate": "COMPLETE" if runtime_pass else "INCOMPLETE",
            "progress_percent": 100 if runtime_pass else (55 if RUNTIME.exists() else 25),
            "completed": ["endpoint, freshness, machine-mode, and mobile-browser check specification"] + (["executed endpoint and mobile browser verification", "durable runtime evidence"] if RUNTIME.exists() else []),
            "remaining": [] if runtime_pass else ["repair failed runtime checks and obtain a complete PASS receipt"],
            "blockers": [] if runtime_pass else [f"runtime verification state: {runtime.get('state', 'NOT_OBSERVED')}; {runtime.get('passed_required_checks', 0)} of {runtime.get('required_checks', 0)} required checks passed"],
        },
        {
            "id": "governance-layer", "title": "Phase 4 — Governance layer",
            "implementation": "ADVANCED", "operation": "COMPLETE" if governance_complete else "PARTIAL",
            "evidence": "SUFFICIENT" if governance_complete else "PARTIAL",
            "exit_gate": "COMPLETE" if governance_complete else "INCOMPLETE",
            "progress_percent": 100 if governance_complete else 42,
            "completed": ["authority checks", "fail-closed completion classification", "cross-repository mutation refusal"],
            "remaining": [] if governance_complete else ["successor eligibility", "audit downgrade evidence", "cross-repository admissibility completion"],
            "blockers": [] if governance_complete else ["destination-owned admissibility evidence remains incomplete"],
        },
        {
            "id": "continuity-layer", "title": "Phase 5 — Continuity layer",
            "implementation": "PARTIAL", "operation": "COMPLETE" if continuity_complete else "PARTIAL",
            "evidence": "SUFFICIENT" if continuity_complete else "PARTIAL",
            "exit_gate": "COMPLETE" if continuity_complete else "INCOMPLETE",
            "progress_percent": 100 if continuity_complete else 34,
            "completed": ["Site mirror handoff", "machine-owned continuation sequence", "repository history and generated state preservation"],
            "remaining": [] if continuity_complete else ["human-readable ecosystem map", "operational inheritance packet", "debt and service inventory", "transfer and shutdown procedures", "durable ecosystem master record"],
            "blockers": [] if continuity_complete else ["ecosystem-wide continuity packet is not yet complete"],
        },
    ]

    payload = {
        "schema_version": "1.2", "generated_from": str(LIVE.relative_to(ROOT)),
        "runtime_evidence_source": str(RUNTIME.relative_to(ROOT)),
        "source_generated_at": live.get("generated_at"),
        "overall_state": "COMPLETE" if all(p["exit_gate"] == "COMPLETE" for p in phases) else "IN_PROGRESS",
        "governing_task": live.get("task_source", "StegVerse-Labs/StegOps-Orchestrator/issues/7"),
        "manual_user_action_required": False,
        "status_model": ["implementation", "operation", "evidence", "exit_gate"],
        "phases": phases,
        "authority_boundary": {
            "roadmap_display_is_execution_authority": False,
            "implementation_is_operational_completion": False,
            "evidence_is_release_authority": False,
            "runtime_check_pass_is_overall_completion": False,
            "exit_gate_requires_machine_verifiable_evidence": True,
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
