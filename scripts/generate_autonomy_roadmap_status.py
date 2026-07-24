#!/usr/bin/env python3
"""Generate fail-closed, role-aware autonomy roadmap state."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "autonomy"
LIVE = DATA / "live-status.json"
RUNTIME = DATA / "runtime-verification-evidence.json"
INVENTORY = DATA / "public-ecosystem-inventory.json"
ROLE_REPORT = DATA / "repository-role-classification.json"
OUT = DATA / "roadmap-status.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> None:
    live = load(LIVE)
    runtime = load(RUNTIME) if RUNTIME.exists() else {}
    inventory = load(INVENTORY) if INVENTORY.exists() else {}
    roles = load(ROLE_REPORT) if ROLE_REPORT.exists() else {}
    repository_count = int(inventory.get("repository_count", 0) or 0)
    role_complete = int(roles.get("role_exit_gate_complete", 0) or 0)
    role_incomplete = int(roles.get("role_exit_gate_incomplete", repository_count) or 0)
    action_count = int(live.get("summary", {}).get("next_actions", 0) or 0)
    runtime_pass = (
        runtime.get("state") == "PASS"
        and int(runtime.get("required_checks", 0) or 0) > 0
        and runtime.get("required_checks") == runtime.get("passed_required_checks")
    )
    role_model_active = inventory.get("completion_model") == "ROLE_SPECIFIC_EXIT_GATES" and ROLE_REPORT.exists()
    inventory_current = live.get("mode") == "PUBLIC_MACHINE_GENERATED_AUTONOMY_TELEMETRY"
    truth_complete = role_model_active and inventory_current and repository_count > 0

    phases = [
        {
            "id": "truth-layer",
            "title": "Phase 1 — Truth layer",
            "implementation": "COMPLETE" if role_model_active else "ADVANCED",
            "operation": "COMPLETE" if truth_complete else "RESCAN_REQUIRED",
            "evidence": "ROLE_SPECIFIC" if role_model_active else "ROLE_NEUTRAL_OR_STALE",
            "exit_gate": "COMPLETE" if truth_complete else "INCOMPLETE",
            "progress_percent": 100 if truth_complete else (94 if role_model_active else 82),
            "completed": [
                "public inventory machinery",
                "objective and evidence inspection",
                "repository-role taxonomy",
                "role-specific exit-gate model",
                "role-aware action generation",
            ] if role_model_active else ["public inventory machinery", "objective and evidence inspection"],
            "remaining": [] if truth_complete else ["execute a current role-aware ecosystem rescan", "persist current role assignments and exit-gate results"],
            "blockers": [] if truth_complete else ["the latest public inventory has not yet been regenerated under the role-specific completion model"],
        },
        {
            "id": "execution-layer",
            "title": "Phase 2 — Execution layer",
            "implementation": "ADVANCED",
            "operation": "PARTIAL",
            "evidence": "ROLE_AWARE" if role_model_active else "PARTIAL",
            "exit_gate": "INCOMPLETE",
            "progress_percent": 66 if role_model_active else 58,
            "completed": ["bounded Site dispatch", "deny-by-default external routing", "role-aware remediation planning"],
            "remaining": ["execute the regenerated role-specific action queue", "install only the destination runners required by each repository role", "automatic convergence after destination evidence changes"],
            "blockers": [f"{action_count} actions remain in the last persisted queue; the next role-aware cycle may materially reduce this count"],
        },
        {
            "id": "runtime-verification-layer",
            "title": "Phase 3 — Runtime verification layer",
            "implementation": "COMPLETE",
            "operation": "COMPLETE" if runtime_pass else "REPAIR_INSTALLED_RESULT_PENDING",
            "evidence": "SUFFICIENT" if runtime_pass else "RECORDED_FAILURE_AND_REPAIR",
            "exit_gate": "COMPLETE" if runtime_pass else "INCOMPLETE",
            "progress_percent": 100 if runtime_pass else 68,
            "completed": ["endpoint checks", "mobile-browser checks", "machine-mode checks", "cadence-aware freshness policy", "role-scoped runtime requirement"],
            "remaining": [] if runtime_pass else ["observe a new Site runtime PASS receipt", "verify runtime only for repositories assigned a runtime-bearing role"],
            "blockers": [] if runtime_pass else [f"latest Site runtime evidence: {runtime.get('passed_required_checks', 0)} of {runtime.get('required_checks', 0)} required checks passed"],
        },
        {
            "id": "governance-layer",
            "title": "Phase 4 — Governance layer",
            "implementation": "ADVANCED",
            "operation": "PARTIAL",
            "evidence": "ROLE_SPECIFIC",
            "exit_gate": "INCOMPLETE",
            "progress_percent": 64 if role_model_active else 55,
            "completed": ["fail-closed classification", "repository-scoped mutation authority", "role-specific admissibility boundaries", "non-runtime repositories no longer fail runtime-only gates"],
            "remaining": ["automatic role-assignment downgrade when evidence changes", "successor eligibility by repository role", "cross-repository admissibility completion"],
            "blockers": [f"{role_incomplete} repositories remain incomplete against their own role-specific exit gates"] if role_model_active else ["role-specific classification has not yet executed"],
        },
        {
            "id": "continuity-layer",
            "title": "Phase 5 — Continuity layer",
            "implementation": "PARTIAL",
            "operation": "PARTIAL",
            "evidence": "PARTIAL",
            "exit_gate": "INCOMPLETE",
            "progress_percent": 46,
            "completed": ["Site handoff", "generated-state preservation", "continuity repositories now have a distinct custody and reconstruction exit model"],
            "remaining": ["human-readable ecosystem map", "operational inheritance packet", "debt and service inventory", "transfer and shutdown procedures", "durable ecosystem master record"],
            "blockers": ["ecosystem-wide continuity packet remains incomplete"],
        },
    ]

    payload = {
        "schema_version": "1.5",
        "generated_from": str(LIVE.relative_to(ROOT)),
        "runtime_evidence_source": str(RUNTIME.relative_to(ROOT)),
        "repository_role_taxonomy_source": "data/autonomy/repository-role-taxonomy.json",
        "repository_role_report_source": "data/autonomy/repository-role-classification.json",
        "source_generated_at": live.get("generated_at"),
        "overall_state": "COMPLETE" if all(p["exit_gate"] == "COMPLETE" for p in phases) else "IN_PROGRESS",
        "governing_task": live.get("task_source", "StegVerse-Labs/StegOps-Orchestrator/issues/7"),
        "manual_user_action_required": False,
        "status_model": ["implementation", "operation", "evidence", "exit_gate"],
        "repository_role_summary": {
            "completion_model": inventory.get("completion_model", "ROLE_MODEL_PENDING_EXECUTION"),
            "repositories": repository_count,
            "role_exit_gate_complete": role_complete,
            "role_exit_gate_incomplete": role_incomplete,
            "role_counts": roles.get("role_counts", {}),
        },
        "phases": phases,
        "authority_boundary": {
            "roadmap_display_is_execution_authority": False,
            "role_assignment_is_completion": False,
            "implementation_is_operational_completion": False,
            "missing_runtime_evidence_blocks_only_runtime_products": True,
            "role_exit_gate_completion_is_release_authority": False,
            "runtime_check_pass_is_overall_completion": False,
            "exit_gate_requires_machine_verifiable_role_specific_evidence": True,
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "ROLE-AWARE ROADMAP: COMPLETE "
        f"repositories={repository_count} role_complete={role_complete} role_incomplete={role_incomplete}"
    )


if __name__ == "__main__":
    main()
