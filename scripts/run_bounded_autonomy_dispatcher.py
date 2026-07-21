#!/usr/bin/env python3
"""Execute Site autonomy actions within an explicit repository authority boundary."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "autonomy"
POLICY_PATH = DATA / "mutation-authority-policy.json"
FRESHNESS_POLICY_PATH = DATA / "freshness-policy.json"
ACTIONS_PATH = DATA / "public-next-actions.json"
INVENTORY_PATH = DATA / "public-ecosystem-inventory.json"
STATUS_PATH = DATA / "live-status.json"
EXECUTIONS_PATH = DATA / "action-executions.json"
OBJECTIVE_PATH = DATA / "objective-contract.json"
RUNTIME_CHECKS_PATH = DATA / "runtime-checks.json"
SITE = "StegVerse-Labs/Site"


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ensure_allowed(policy: dict[str, Any], action: str, path: Path) -> None:
    allowed = policy.get("allowed_actions", {}).get(action, {}).get("allowed_paths", [])
    relative = path.relative_to(ROOT).as_posix()
    if relative not in allowed:
        raise RuntimeError(f"DENY action={action} path={relative}")


def ensure_site_objective(policy: dict[str, Any], now: str) -> dict[str, Any]:
    ensure_allowed(policy, "ENSURE_SITE_OBJECTIVE_CONTRACT", OBJECTIVE_PATH)
    payload = {
        "schema_version": "1.0",
        "objective_id": "site-public-autonomy-observability",
        "repository": SITE,
        "requested_capability": "Continuously display governed autonomous task execution, branching, convergence, results, and corrective actions on the public Site.",
        "required_user_outcome": "A visitor can inspect current and completed autonomous work without reading GitHub history or relying on conversational claims.",
        "required_runtime_evidence": [
            "scheduled_workflow_run_success",
            "machine_persisted_public_inventory",
            "machine_persisted_action_execution_log",
            "live_page_loads_current_repository_owned_telemetry",
            "mobile_user_flow_verified"
        ],
        "disallowed_substitutes": [
            "workflow file exists",
            "issue exists",
            "conversation says complete",
            "local placeholder telemetry",
            "repository write without observed runtime"
        ],
        "completion_policy": {
            "require_live_execution": True,
            "require_user_visible_outcome": True,
            "unknown_is_complete": False
        },
        "generated_by": "bounded-autonomy-dispatcher",
        "generated_at": now
    }
    changed = not OBJECTIVE_PATH.exists() or load(OBJECTIVE_PATH, {}) != payload
    if changed:
        write(OBJECTIVE_PATH, payload)
    return {"action": "ENSURE_SITE_OBJECTIVE_CONTRACT", "status": "APPLIED" if changed else "NO_CHANGE", "path": OBJECTIVE_PATH.relative_to(ROOT).as_posix()}


def load_freshness_policy() -> dict[str, Any]:
    freshness = load(FRESHNESS_POLICY_PATH, {})
    if freshness.get("schema_version") != "1.0":
        raise RuntimeError("DENY invalid freshness policy schema")
    max_age = freshness.get("maximum_age_minutes")
    cadence = freshness.get("scheduled_interval_minutes")
    if not isinstance(max_age, int) or not isinstance(cadence, int) or max_age < cadence:
        raise RuntimeError("DENY invalid freshness policy values")
    authority = freshness.get("authority", {})
    if authority.get("freshness_pass_is_overall_completion") is not False:
        raise RuntimeError("DENY freshness policy grants completion authority")
    if authority.get("manual_user_action_required") is not False:
        raise RuntimeError("DENY freshness policy introduces manual dependency")
    return freshness


def ensure_runtime_checks(policy: dict[str, Any], now: str) -> dict[str, Any]:
    ensure_allowed(policy, "ENSURE_SITE_RUNTIME_CHECK_SPEC", RUNTIME_CHECKS_PATH)
    freshness = load_freshness_policy()
    max_age = freshness["maximum_age_minutes"]
    payload = {
        "schema_version": "1.1",
        "repository": SITE,
        "objective_id": "site-public-autonomy-observability",
        "generated_at": now,
        "freshness_policy_path": FRESHNESS_POLICY_PATH.relative_to(ROOT).as_posix(),
        "checks": [
            {"id": "telemetry-file", "type": "http-json", "url": "https://stegverse-labs.github.io/Site/data/autonomy/live-status.json", "required": True},
            {"id": "live-page", "type": "http-html", "url": "https://stegverse-labs.github.io/Site/autonomy-live.html", "required": True},
            {"id": "roadmap-page", "type": "http-html", "url": "https://stegverse-labs.github.io/Site/autonomy-roadmap.html", "required": True},
            {"id": "freshness", "type": "json-field", "path": "generated_at", "max_age_minutes": max_age, "policy_path": FRESHNESS_POLICY_PATH.relative_to(ROOT).as_posix(), "required": True},
            {"id": "machine-mode", "type": "json-field", "path": "mode", "allowed": ["PUBLIC_MACHINE_GENERATED_AUTONOMY_TELEMETRY"], "required": True},
            {"id": "live-mobile-flow", "type": "browser", "url": "https://stegverse-labs.github.io/Site/autonomy-live.html", "ready_selector": "#graph", "minimum_text_characters": 40, "viewport": {"width": 390, "height": 844}, "required": True},
            {"id": "roadmap-mobile-flow", "type": "browser", "url": "https://stegverse-labs.github.io/Site/autonomy-roadmap.html", "ready_selector": "#phases", "minimum_text_characters": 120, "viewport": {"width": 390, "height": 844}, "required": True}
        ],
        "completion_effect": "NONE_UNTIL_EXECUTED",
        "authority": {"runtime_check_pass_is_completion": False, "all_objective_evidence_required": True}
    }
    changed = not RUNTIME_CHECKS_PATH.exists() or load(RUNTIME_CHECKS_PATH, {}) != payload
    if changed:
        write(RUNTIME_CHECKS_PATH, payload)
    return {
        "action": "ENSURE_SITE_RUNTIME_CHECK_SPEC",
        "status": "APPLIED" if changed else "NO_CHANGE",
        "path": RUNTIME_CHECKS_PATH.relative_to(ROOT).as_posix(),
        "freshness_policy_path": FRESHNESS_POLICY_PATH.relative_to(ROOT).as_posix(),
        "max_age_minutes": max_age
    }


def main() -> None:
    now = stamp()
    policy = load(POLICY_PATH, {})
    if policy.get("default") != "DENY" or policy.get("cross_repository_mutation") is not False:
        raise SystemExit("AUTONOMY DISPATCH: DENY invalid mutation policy")

    actions = load(ACTIONS_PATH, {"actions": []})
    inventory = load(INVENTORY_PATH, {"repositories": []})
    records: list[dict[str, Any]] = []

    site_entry = next((r for r in inventory.get("repositories", []) if r.get("repository") == SITE), None)
    if site_entry is None or "objective_contract" in site_entry.get("missing_gates", []):
        records.append(ensure_site_objective(policy, now))
    else:
        records.append({"action": "ENSURE_SITE_OBJECTIVE_CONTRACT", "status": "SATISFIED", "path": OBJECTIVE_PATH.relative_to(ROOT).as_posix()})

    records.append(ensure_runtime_checks(policy, now))

    denied = []
    for action in actions.get("actions", [])[:25]:
        repository = action.get("repository")
        if repository and repository != SITE:
            denied.append({
                "action_id": action.get("action_id"),
                "repository": repository,
                "requested_action": action.get("action"),
                "status": "DENIED_CROSS_REPOSITORY_AUTHORITY",
                "reason": "Site workflow token is not authorized to mutate another repository.",
                "machine_owned_next_action": "retain in queue for an authorized repository-owned runner"
            })

    execution = {
        "schema_version": "1.0",
        "generated_at": now,
        "actor": "github-actions[bot]",
        "policy_id": policy.get("policy_id"),
        "applied": records,
        "denied": denied,
        "manual_user_action_required": False,
        "completion_claimed": False
    }
    ensure_allowed(policy, "PERSIST_EXECUTION_RECORD", EXECUTIONS_PATH)
    write(EXECUTIONS_PATH, execution)

    status = load(STATUS_PATH, {})
    graph = status.setdefault("task_graph", {})
    nodes = graph.setdefault("nodes", [])
    nodes = [n for n in nodes if n.get("id") not in {"bounded-dispatch", "site-objective-contract", "site-runtime-check-spec", "cross-repo-authority-gate"}]
    nodes.extend([
        {
            "id": "bounded-dispatch", "title": "Execute bounded remediation actions", "status": "COMPLETE",
            "result": f"Applied or verified {len(records)} Site-owned controls and evaluated {len(denied)} cross-repository actions under deny-by-default authority.",
            "owner": SITE, "updated_at": now, "depends_on": ["next-action-planning"],
            "task_url": "https://github.com/StegVerse-Labs/StegOps-Orchestrator/issues/7"
        },
        {
            "id": "site-objective-contract", "title": "Bind Site autonomy objective", "status": "COMPLETE",
            "result": "A machine-readable outcome contract defines the required public observability capability and disallowed substitutes.",
            "owner": SITE, "updated_at": now, "depends_on": ["bounded-dispatch"]
        },
        {
            "id": "site-runtime-check-spec", "title": "Define Site runtime verification checks", "status": "COMPLETE",
            "result": f"Endpoint, cadence-aware freshness ({records[-1].get('max_age_minutes')} minutes), machine-mode, and mobile checks are bound to the canonical policy.",
            "owner": SITE, "updated_at": now, "depends_on": ["bounded-dispatch"]
        },
        {
            "id": "cross-repo-authority-gate", "title": "Route external repository remediation",
            "status": "BLOCKED_BY_REPOSITORY_AUTHORITY" if denied else "COMPLETE",
            "current_step": f"{len(denied)} actions require repository-owned runners; none were falsely executed by Site.",
            "owner": SITE, "updated_at": now, "depends_on": ["bounded-dispatch"]
        }
    ])
    graph["nodes"] = nodes
    edges = graph.setdefault("edges", [])
    wanted = [
        {"from": "next-action-planning", "to": "bounded-dispatch", "type": "resplit"},
        {"from": "bounded-dispatch", "to": "site-objective-contract", "type": "split"},
        {"from": "bounded-dispatch", "to": "site-runtime-check-spec", "type": "split"},
        {"from": "bounded-dispatch", "to": "cross-repo-authority-gate", "type": "split"}
    ]
    existing = {(e.get("from"), e.get("to"), e.get("type")) for e in edges}
    edges.extend(e for e in wanted if (e["from"], e["to"], e["type"]) not in existing)
    status["generated_at"] = now
    status.setdefault("corrective_actions", [])
    status["corrective_actions"] = [a for a in status["corrective_actions"] if a.get("id") != "authorized-repository-runners"]
    if denied:
        status["corrective_actions"].append({
            "id": "authorized-repository-runners",
            "action": "Install repository-owned bounded runners for queued external remediations",
            "status": "MACHINE_ACTION_REQUIRED",
            "reason": f"{len(denied)} queued actions cannot be mutated by Site's repository-scoped token."
        })
    write(STATUS_PATH, status)
    print(f"BOUNDED AUTONOMY DISPATCH: COMPLETE applied={len(records)} denied={len(denied)}")


if __name__ == "__main__":
    main()
