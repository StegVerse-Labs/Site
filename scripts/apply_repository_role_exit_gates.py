#!/usr/bin/env python3
"""Apply role-specific exit gates to the public autonomy inventory and queue."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "autonomy"
TAXONOMY = DATA / "repository-role-taxonomy.json"
INVENTORY = DATA / "public-ecosystem-inventory.json"
ACTIONS = DATA / "public-next-actions.json"
REPORT = DATA / "repository-role-classification.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def infer_role(repository: str, taxonomy: dict[str, Any]) -> tuple[str, str]:
    lowered = repository.lower()
    for rule in taxonomy.get("inference_rules", []):
        role = str(rule.get("role", "UNCLASSIFIED"))
        for term in rule.get("name_terms", []):
            if str(term).lower() in lowered:
                return role, f"repository name matched term: {term}"
    return str(taxonomy.get("default_role", "UNCLASSIFIED")), "no deterministic role rule matched"


def evidence_signals(repo: dict[str, Any]) -> set[str]:
    signals: set[str] = set()
    observed = repo.get("observed_artifacts", {})
    if repo.get("objective_contract_valid"):
        signals.add("objective_contract")
    if observed.get("workflow"):
        signals.add("machine_validation_workflow")
    if observed.get("deployment"):
        signals.add("deployment_or_runtime_configuration")
    if repo.get("completion_evidence_valid"):
        signals.update({
            "fresh_completion_evidence",
            "runtime_observed",
            "user_visible_outcome_verified",
            "package_or_integration_evidence",
            "downstream_use_or_compatibility_evidence",
            "executed_policy_evidence",
            "fail_closed_authority_evidence",
            "publication_accuracy_evidence",
            "freshness_evidence",
            "custody_evidence",
            "reconstruction_evidence",
            "retention_or_transfer_evidence",
            "reproducible_test_evidence",
        })
    if observed.get("handoff"):
        signals.update({"source_binding", "declared_scope"})
    classification = str(repo.get("classification", ""))
    if classification in {"SCAFFOLD_ONLY", "PARTIAL", "IMPLEMENTATION_INSTALLED_ACTIVATION_UNVERIFIED"}:
        signals.add("declared_non_production_boundary")
        signals.add("non_execution_boundary")
        signals.add("non_authorizing_projection")
    return signals


def main() -> None:
    taxonomy = load(TAXONOMY)
    inventory = load(INVENTORY)
    actions = load(ACTIONS)
    roles = taxonomy["roles"]
    assignments: list[dict[str, Any]] = []
    role_counts: dict[str, int] = {}
    role_complete_counts: dict[str, int] = {}

    for repo in inventory.get("repositories", []):
        repository = str(repo.get("repository", ""))
        role, reason = infer_role(repository, taxonomy)
        required = list(roles[role]["required_exit_gates"])
        signals = evidence_signals(repo)
        missing = [gate for gate in required if gate not in signals]
        role_complete = not missing
        repo["repository_role"] = role
        repo["role_assignment_reason"] = reason
        repo["role_required_exit_gates"] = required
        repo["role_missing_exit_gates"] = missing
        repo["role_exit_gate_complete"] = role_complete
        repo["completion"] = role_complete
        repo["successor_eligible"] = role_complete
        repo["classification"] = "ROLE_EXIT_GATE_COMPLETE" if role_complete else "ROLE_EXIT_GATE_INCOMPLETE"
        repo["next_action"] = (
            "continue role-specific freshness and downgrade monitoring"
            if role_complete
            else "satisfy role-specific exit gates: " + ", ".join(missing)
        )
        role_counts[role] = role_counts.get(role, 0) + 1
        if role_complete:
            role_complete_counts[role] = role_complete_counts.get(role, 0) + 1
        assignments.append({
            "repository": repository,
            "role": role,
            "reason": reason,
            "required_exit_gates": required,
            "missing_exit_gates": missing,
            "role_exit_gate_complete": role_complete,
        })

    inventory["schema_version"] = "1.1"
    inventory["completion_model"] = "ROLE_SPECIFIC_EXIT_GATES"
    inventory["repository_role_taxonomy_path"] = str(TAXONOMY.relative_to(ROOT))
    inventory["role_counts"] = role_counts
    inventory["role_complete_counts"] = role_complete_counts
    inventory["classification_counts"] = {
        "ROLE_EXIT_GATE_COMPLETE": sum(1 for r in inventory.get("repositories", []) if r.get("role_exit_gate_complete")),
        "ROLE_EXIT_GATE_INCOMPLETE": sum(1 for r in inventory.get("repositories", []) if not r.get("role_exit_gate_complete")),
    }

    action_items = []
    for repo in inventory.get("repositories", []):
        if repo.get("role_exit_gate_complete"):
            continue
        action_items.append({
            "action_id": "role-remediate:" + str(repo["repository"]).replace("/", ":"),
            "repository": repo["repository"],
            "repository_role": repo["repository_role"],
            "priority": 1 if repo["repository_role"] == "RUNTIME_PRODUCT" else 2,
            "action": repo["next_action"],
            "missing_gates": repo["role_missing_exit_gates"],
            "machine_owned": True,
            "manual_user_action_required": False,
            "status": "READY" if not repo.get("inspection_errors") else "AUTOMATIC_RETRY",
        })
    action_items.sort(key=lambda item: (item["priority"], item["repository_role"], item["repository"]))
    actions["schema_version"] = "1.1"
    actions["completion_model"] = "ROLE_SPECIFIC_EXIT_GATES"
    actions["action_count"] = len(action_items)
    actions["actions"] = action_items

    report = {
        "schema_version": "1.0",
        "taxonomy_path": str(TAXONOMY.relative_to(ROOT)),
        "inventory_generated_at": inventory.get("generated_at"),
        "repository_count": inventory.get("repository_count", 0),
        "role_counts": role_counts,
        "role_complete_counts": role_complete_counts,
        "role_exit_gate_complete": inventory["classification_counts"]["ROLE_EXIT_GATE_COMPLETE"],
        "role_exit_gate_incomplete": inventory["classification_counts"]["ROLE_EXIT_GATE_INCOMPLETE"],
        "assignments": assignments,
        "authority": {
            "role_assignment_is_completion": False,
            "role_exit_gate_completion_is_release_authority": False,
            "manual_user_action_required": False,
        },
    }
    write(INVENTORY, inventory)
    write(ACTIONS, actions)
    write(REPORT, report)
    print(
        "ROLE-SPECIFIC CLASSIFICATION: COMPLETE "
        f"repositories={report['repository_count']} complete={report['role_exit_gate_complete']} actions={actions['action_count']}"
    )


if __name__ == "__main__":
    main()
