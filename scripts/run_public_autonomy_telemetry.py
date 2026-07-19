#!/usr/bin/env python3
"""Generate public autonomy inventory, next actions, and live task telemetry.

This runner uses only public GitHub API data plus the Site repository's own
GITHUB_TOKEN. It never treats discovery, files, workflows, or documentation as
proof of operational completion. Private repository coverage is explicitly
excluded from the public report.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = ROOT / "data" / "autonomy" / "public-ecosystem-scope.json"
STATUS_PATH = ROOT / "data" / "autonomy" / "live-status.json"
INVENTORY_PATH = ROOT / "data" / "autonomy" / "public-ecosystem-inventory.json"
ACTIONS_PATH = ROOT / "data" / "autonomy" / "public-next-actions.json"
TASK_URL = "https://github.com/StegVerse-Labs/StegOps-Orchestrator/issues/7"
FRESH_DAYS = 30

PROBES = {
    "objective": [
        "autonomy/objective-contract.json",
        "data/autonomy/objective-contract.json",
        "objective-contract.json",
    ],
    "completion": [
        "autonomy/completion-evidence.json",
        "data/autonomy/completion-evidence.json",
    ],
    "workflow": [
        ".github/workflows/validate.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/main.yml",
        ".github/workflows/autonomy-telemetry.yml",
    ],
    "deployment": ["render.yaml", "vercel.json", "netlify.toml", "Dockerfile"],
    "handoff": ["SITE_MIRROR_HANDOFF.md", "README.md"],
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def stamp() -> str:
    return utcnow().isoformat().replace("+00:00", "Z")


def api_get(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "StegVerse-Public-Autonomy-Telemetry",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def content_url(repo: str, path: str, branch: str) -> str:
    return (
        "https://api.github.com/repos/"
        + repo
        + "/contents/"
        + urllib.parse.quote(path, safe="/")
        + "?ref="
        + urllib.parse.quote(branch, safe="")
    )


def fetch_content(repo: str, path: str, branch: str, token: str | None) -> tuple[Any | None, str | None]:
    try:
        return api_get(content_url(repo, path, branch), token), None
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, None
        return None, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, str(exc)


def decode(payload: Any) -> str | None:
    if not isinstance(payload, dict) or payload.get("type") != "file":
        return None
    raw = payload.get("content")
    if not isinstance(raw, str):
        return None
    try:
        return base64.b64decode(raw).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None


def parse_object(text: str | None) -> dict[str, Any] | None:
    if text is None:
        return None
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else None
    except json.JSONDecodeError:
        return None


def fresh(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed >= utcnow() - timedelta(days=FRESH_DAYS)


def strict_completion(repo: str, evidence: dict[str, Any] | None) -> tuple[bool, list[str]]:
    if not evidence:
        return False, ["completion_evidence_missing"]
    checks = {
        "repository_binding": evidence.get("repository") == repo,
        "objective_binding": isinstance(evidence.get("objective_id"), str) and bool(evidence.get("objective_id")),
        "runtime_observed": evidence.get("runtime_observed") is True,
        "user_outcome_verified": evidence.get("user_visible_outcome_verified") is True,
        "machine_verifier": evidence.get("verifier_source") in {"github-actions", "runtime-monitor", "independent-verifier"},
        "critical_blockers_zero": evidence.get("critical_blockers") == 0,
        "manual_dependency_false": evidence.get("manual_completion_dependency") is False,
        "fresh": fresh(evidence.get("verified_at")),
        "evidence_urls": isinstance(evidence.get("evidence_urls"), list) and bool(evidence.get("evidence_urls")),
    }
    failures = [name for name, passed in checks.items() if not passed]
    return not failures, failures


def list_public_repositories(org: str, token: str | None) -> tuple[list[dict[str, Any]], str | None]:
    repos: list[dict[str, Any]] = []
    page = 1
    try:
        while True:
            payload = api_get(
                f"https://api.github.com/orgs/{org}/repos?type=public&per_page=100&page={page}",
                token,
            )
            if not isinstance(payload, list):
                return repos, "unexpected response"
            repos.extend(payload)
            if len(payload) < 100:
                break
            page += 1
        return repos, None
    except urllib.error.HTTPError as exc:
        return repos, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return repos, str(exc)


def inspect(repo: dict[str, Any], token: str | None) -> dict[str, Any]:
    name = str(repo.get("full_name") or "")
    branch = str(repo.get("default_branch") or "main")
    found = {kind: [] for kind in PROBES}
    texts: dict[str, str] = {}
    errors: list[str] = []

    for kind, paths in PROBES.items():
        for path in paths:
            payload, error = fetch_content(name, path, branch, token)
            if error:
                errors.append(f"{path}: {error}")
            elif payload is not None:
                found[kind].append(path)
                text = decode(payload)
                if text is not None:
                    texts[path] = text

    objective = next((parse_object(texts.get(path)) for path in found["objective"] if parse_object(texts.get(path))), None)
    completion = next((parse_object(texts.get(path)) for path in found["completion"] if parse_object(texts.get(path))), None)
    complete, failures = strict_completion(name, completion)
    archived = bool(repo.get("archived"))
    has_code = bool(found["workflow"] or found["deployment"])

    if archived:
        classification = "STALE_OR_ABANDONED"
    elif complete and objective:
        classification = "OPERATIONALLY_COMPLETE"
    elif found["completion"] or (objective and has_code):
        classification = "IMPLEMENTATION_INSTALLED_ACTIVATION_UNVERIFIED"
    elif has_code:
        classification = "PARTIAL"
    elif found["handoff"]:
        classification = "SCAFFOLD_ONLY"
    else:
        classification = "UNKNOWN_INSUFFICIENT_EVIDENCE"

    missing: list[str] = []
    if objective is None:
        missing.append("objective_contract")
    if not complete:
        missing.extend(failures)
    if not found["workflow"]:
        missing.append("machine_validation_workflow")
    if not found["deployment"]:
        missing.append("deployment_or_runtime_configuration")
    if errors:
        missing.append("complete_repository_inspection")
    missing = sorted(set(missing))

    if classification == "OPERATIONALLY_COMPLETE":
        action = "continue scheduled freshness verification and downgrade on expiry"
    elif objective is None:
        action = "derive and install an outcome-level objective contract"
    elif not found["workflow"]:
        action = "install repository-owned runtime verification"
    elif not found["completion"]:
        action = "execute the real user flow and persist strict completion evidence"
    else:
        action = "repair stale or invalid completion evidence and rerun verification"

    return {
        "repository": name,
        "url": repo.get("html_url"),
        "archived": archived,
        "pushed_at": repo.get("pushed_at"),
        "classification": classification,
        "completion": classification == "OPERATIONALLY_COMPLETE",
        "successor_eligible": classification == "OPERATIONALLY_COMPLETE",
        "objective_contract_valid": objective is not None,
        "completion_evidence_valid": complete,
        "completion_evidence_failures": failures,
        "observed_artifacts": found,
        "inspection_errors": errors,
        "missing_gates": missing,
        "next_action": action,
    }


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    token = os.environ.get("GITHUB_TOKEN")
    organizations: list[dict[str, Any]] = []
    repositories: list[dict[str, Any]] = []
    for org in scope["organizations"]:
        repos, error = list_public_repositories(org, token)
        inspected = [inspect(repo, token) for repo in repos]
        organizations.append({
            "organization": org,
            "repository_count": len(inspected),
            "enumeration_error": error,
            "inspection_error_count": sum(bool(item["inspection_errors"]) for item in inspected),
        })
        repositories.extend(inspected)

    counts: dict[str, int] = {}
    for repo in repositories:
        counts[repo["classification"]] = counts.get(repo["classification"], 0) + 1

    inventory = {
        "schema_version": "1.0",
        "generated_at": stamp(),
        "coverage": "PUBLIC_REPOSITORIES_ONLY",
        "private_coverage_claimed": False,
        "organizations": organizations,
        "repository_count": len(repositories),
        "classification_counts": counts,
        "repositories": sorted(repositories, key=lambda item: item["repository"]),
    }

    priority = {
        "IMPLEMENTATION_INSTALLED_ACTIVATION_UNVERIFIED": 1,
        "PARTIAL": 2,
        "SCAFFOLD_ONLY": 3,
        "UNKNOWN_INSUFFICIENT_EVIDENCE": 4,
        "STALE_OR_ABANDONED": 5,
    }
    action_items = [
        {
            "action_id": "public-remediate:" + repo["repository"].replace("/", ":"),
            "repository": repo["repository"],
            "classification": repo["classification"],
            "priority": priority.get(repo["classification"], 9),
            "action": repo["next_action"],
            "missing_gates": repo["missing_gates"],
            "machine_owned": True,
            "manual_user_action_required": False,
            "status": "READY" if not repo["inspection_errors"] else "AUTOMATIC_RETRY",
        }
        for repo in repositories
        if not repo["completion"]
    ]
    action_items.sort(key=lambda item: (item["priority"], item["repository"]))
    actions = {
        "schema_version": "1.0",
        "generated_at": inventory["generated_at"],
        "coverage": inventory["coverage"],
        "action_count": len(action_items),
        "actions": action_items,
    }
    return scope, inventory, actions


def telemetry(scope: dict[str, Any], inventory: dict[str, Any], actions: dict[str, Any]) -> dict[str, Any]:
    ts = inventory["generated_at"]
    enumeration_errors = [o for o in inventory["organizations"] if o["enumeration_error"]]
    inspection_errors = sum(o["inspection_error_count"] for o in inventory["organizations"])
    operational = inventory["classification_counts"].get("OPERATIONALLY_COMPLETE", 0)
    valid_evidence = sum(1 for r in inventory["repositories"] if r["completion_evidence_valid"])
    completion_status = "COMPLETE" if inventory["repository_count"] and operational == inventory["repository_count"] else "BLOCKED_BY_EVIDENCE_COLLECTION"
    corrective: list[dict[str, Any]] = []
    if enumeration_errors:
        corrective.append({
            "id": "public-enumeration-errors",
            "action": "Retry failed public organization enumeration",
            "status": "AUTOMATIC_RETRY",
            "reason": "; ".join(f"{o['organization']}: {o['enumeration_error']}" for o in enumeration_errors),
        })
    if inspection_errors:
        corrective.append({
            "id": "public-inspection-errors",
            "action": "Retry incomplete public repository inspections",
            "status": "AUTOMATIC_RETRY",
            "reason": f"{inspection_errors} repositories had one or more inspection errors.",
        })

    return {
        "schema_version": "2.3",
        "generated_at": ts,
        "mode": "PUBLIC_MACHINE_GENERATED_AUTONOMY_TELEMETRY",
        "truthful_notice": "Generated by Site's scheduled workflow from public GitHub evidence. Private repositories are not represented; files and workflows do not prove operational completion.",
        "summary": {
            "coverage": "PUBLIC_REPOSITORIES_ONLY",
            "organizations": len(scope["organizations"]),
            "repositories": inventory["repository_count"],
            "operationally_complete": operational,
            "valid_completion_evidence": valid_evidence,
            "next_actions": actions["action_count"],
        },
        "task_graph": {
            "graph_id": "public-autonomy-cycle",
            "root_task_ids": ["public-truth-root"],
            "nodes": [
                {"id": "public-truth-root", "title": "Public ecosystem truth cycle", "status": "IN_PROGRESS", "current_step": "Public inventory, evidence inspection, classification, and action planning execute on a schedule.", "owner": "StegVerse-Labs/Site", "updated_at": ts, "depends_on": [], "task_url": TASK_URL},
                {"id": "public-enumeration", "title": "Enumerate public ecosystem repositories", "status": "COMPLETE" if not enumeration_errors else "PARTIAL", "result": f"Enumerated {inventory['repository_count']} public repositories across {len(scope['organizations'])} configured organizations.", "owner": "StegVerse-Labs/Site", "updated_at": ts, "depends_on": ["public-truth-root"], "task_url": TASK_URL},
                {"id": "public-evidence-inspection", "title": "Inspect public objective and runtime evidence", "status": "COMPLETE" if not inspection_errors else "PARTIAL", "result": f"Strict completion evidence is valid for {valid_evidence} public repositories.", "owner": "StegVerse-Labs/Site", "updated_at": ts, "depends_on": ["public-truth-root"], "task_url": TASK_URL},
                {"id": "public-classification", "title": "Classify public repository integrity", "status": "COMPLETE", "result": "Applied fail-closed outcome classifications; unknown evidence does not count as complete.", "owner": "StegVerse-Labs/Site", "updated_at": ts, "depends_on": ["public-enumeration", "public-evidence-inspection"], "task_url": TASK_URL},
                {"id": "public-action-planner", "title": "Generate public remediation queue", "status": "COMPLETE", "result": f"Generated {actions['action_count']} machine-owned public repository actions.", "owner": "StegVerse-Labs/Site", "updated_at": ts, "depends_on": ["public-classification"], "task_url": TASK_URL},
                {"id": "public-completion-gate", "title": "Apply public ecosystem completion gate", "status": completion_status, "current_step": f"{operational} of {inventory['repository_count']} public repositories satisfy strict operational completion evidence.", "owner": "StegVerse-Labs/Site", "updated_at": ts, "depends_on": ["public-classification", "public-action-planner"], "task_url": TASK_URL},
                {"id": "public-execution-runners", "title": "Dispatch repository remediation branches", "status": "READY" if actions["action_count"] else "COMPLETE", "current_step": "Bounded repository-owned execution runners remain the next autonomy layer.", "owner": "StegVerse-Labs/StegOps-Orchestrator", "updated_at": ts, "depends_on": ["public-action-planner"], "task_url": TASK_URL},
            ],
            "edges": [
                {"from": "public-truth-root", "to": "public-enumeration", "type": "split"},
                {"from": "public-truth-root", "to": "public-evidence-inspection", "type": "split"},
                {"from": "public-enumeration", "to": "public-classification", "type": "converge"},
                {"from": "public-evidence-inspection", "to": "public-classification", "type": "converge"},
                {"from": "public-classification", "to": "public-action-planner", "type": "sequence"},
                {"from": "public-classification", "to": "public-completion-gate", "type": "split"},
                {"from": "public-action-planner", "to": "public-completion-gate", "type": "converge"},
                {"from": "public-action-planner", "to": "public-execution-runners", "type": "resplit"},
            ],
        },
        "corrective_actions": corrective,
        "completed_history": [{
            "id": "public-integrity-cycle:" + ts,
            "title": "Public completion-integrity cycle",
            "status": "COMPLETE" if not enumeration_errors else "PARTIAL",
            "result": f"Processed {inventory['repository_count']} public repositories and generated {actions['action_count']} actions.",
            "completed_at": ts,
            "branch_ids": ["public-enumeration", "public-evidence-inspection", "public-classification", "public-action-planner"],
            "task_url": TASK_URL,
        }],
        "inventory_path": "data/autonomy/public-ecosystem-inventory.json",
        "next_actions_path": "data/autonomy/public-next-actions.json",
        "task_source": "StegVerse-Labs/StegOps-Orchestrator/issues/7",
    }


def write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    scope, inventory, actions = build()
    status = telemetry(scope, inventory, actions)
    write(INVENTORY_PATH, inventory)
    write(ACTIONS_PATH, actions)
    write(STATUS_PATH, status)
    print(
        "PUBLIC AUTONOMY CYCLE: COMPLETE "
        f"repositories={inventory['repository_count']} actions={actions['action_count']}"
    )


if __name__ == "__main__":
    main()
