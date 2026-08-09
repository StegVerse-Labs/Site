#!/usr/bin/env python3
"""Validate exclusive pre-work claims for Site session and machine workers."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "session-work-claims.json"
REPORT = ROOT / "session_work_claims.report.json"
ACTIVE_STATES = {"CLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED"}
REQUIRED_FIELDS = {
    "claim_id", "session_worker_id", "task_id", "originating_goal", "repository", "branch",
    "role", "state", "normalized_work_key", "dependency_surface_keys", "claimed_paths",
    "handoff", "handoff_revision", "claim_created_at", "claim_expires_when",
    "expected_evidence", "collision_boundaries", "next_task_after_release",
}


def normalize(value: str) -> str:
    return "-".join(part for part in "".join(ch.lower() if ch.isalnum() else " " for ch in value).split() if part)


def active_claims(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [claim for claim in registry.get("claims", []) if claim.get("state") in ACTIVE_STATES]


def validate_registry(registry: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    policy = registry.get("policy", {})
    for marker in (
        "one_active_owner_per_task",
        "one_active_owner_per_dependency_surface",
        "missing_or_stale_claim_fails_closed",
        "incidental_dependency_cannot_become_governing_objective",
        "distinct_support_roles_require_explicit_non_overlap",
        "collision_redirects_to_next_unclaimed_canonical_task",
    ):
        if policy.get(marker) is not True:
            failures.append(f"policy.{marker} must be true")

    claims = active_claims(registry)
    ids: set[str] = set()
    task_owners: dict[str, list[dict[str, Any]]] = defaultdict(list)
    surface_owners: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for claim in claims:
        missing = sorted(REQUIRED_FIELDS - claim.keys())
        if missing:
            failures.append(f"claim {claim.get('claim_id', '<missing>')} missing fields: {', '.join(missing)}")
            continue
        claim_id = str(claim["claim_id"])
        if claim_id in ids:
            failures.append(f"duplicate claim_id: {claim_id}")
        ids.add(claim_id)
        if claim.get("repository") != registry.get("repository"):
            failures.append(f"claim {claim_id} repository mismatch")
        if not claim.get("claim_expires_when"):
            failures.append(f"claim {claim_id} has no release/expiration condition")
        work_key = normalize(str(claim.get("normalized_work_key", "")))
        if not work_key:
            failures.append(f"claim {claim_id} has empty normalized_work_key")
        task_owners[normalize(str(claim["task_id"]))].append(claim)
        for surface in claim.get("dependency_surface_keys", []):
            surface_owners[normalize(str(surface))].append(claim)

    for task, owners in task_owners.items():
        if len(owners) > 1:
            failures.append(f"task collision {task}: " + ", ".join(o["claim_id"] for o in owners))

    for surface, owners in surface_owners.items():
        if len(owners) <= 1:
            continue
        roles = {str(o.get("role", "")) for o in owners}
        explicit_support = all(o.get("distinct_support_role") is True for o in owners)
        path_sets = [set(map(str, o.get("claimed_paths", []))) for o in owners]
        path_overlap = any(path_sets[i] & path_sets[j] for i in range(len(path_sets)) for j in range(i + 1, len(path_sets)))
        if not explicit_support or path_overlap or len(roles) != len(owners):
            failures.append(f"dependency surface collision {surface}: " + ", ".join(o["claim_id"] for o in owners))

    return failures


def evaluate_candidate(registry: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Return deterministic admission posture for a proposed claim without mutating the registry."""
    failures: list[str] = []
    missing = sorted(REQUIRED_FIELDS - candidate.keys())
    if missing:
        return {"decision": "BLOCK", "reason": "MISSING_REQUIRED_CLAIM_EVIDENCE", "missing": missing}

    active = active_claims(registry)
    candidate_task = normalize(str(candidate["task_id"]))
    candidate_surfaces = {normalize(str(v)) for v in candidate.get("dependency_surface_keys", [])}
    candidate_paths = set(map(str, candidate.get("claimed_paths", [])))

    for claim in active:
        if normalize(str(claim["task_id"])) == candidate_task:
            failures.append(f"task already owned by {claim['claim_id']}")
        shared = candidate_surfaces & {normalize(str(v)) for v in claim.get("dependency_surface_keys", [])}
        if shared:
            support_ok = (
                candidate.get("distinct_support_role") is True
                and claim.get("distinct_support_role") is True
                and candidate.get("role") != claim.get("role")
                and not (candidate_paths & set(map(str, claim.get("claimed_paths", []))))
            )
            if not support_ok:
                failures.append(f"dependency surface already owned by {claim['claim_id']}: {', '.join(sorted(shared))}")

    governing = {normalize(str(v)) for v in candidate.get("governing_dependency_keys", [])}
    incidental = {normalize(str(v)) for v in candidate.get("incidental_dependency_keys", [])}
    if governing & incidental:
        failures.append("dependency cannot be both governing and incidental")
    if any("render" in value for value in governing) and candidate.get("canonical_task_marks_render_critical") is not True:
        failures.append("Render cannot become governing objective without canonical critical-task evidence")

    if failures:
        return {
            "decision": "BLOCK",
            "reason": "CLAIM_COLLISION_OR_UNAUTHORIZED_DEPENDENCY_PROMOTION",
            "failures": failures,
            "next_action": candidate.get("next_unclaimed_canonical_task", "resolve next unclaimed canonical task from handoff"),
        }
    return {"decision": "ADMIT", "reason": "EXCLUSIVE_PREWORK_CLAIM_AVAILABLE"}


def main() -> int:
    if not REGISTRY.exists():
        report = {"status": "FAIL", "failures": ["missing data/session-work-claims.json"]}
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("SESSION_WORK_CLAIMS_FAIL")
        return 1
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report = {"status": "FAIL", "failures": [f"invalid registry JSON: {exc}"]}
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("SESSION_WORK_CLAIMS_FAIL")
        return 1

    failures = validate_registry(registry)
    report = {
        "schema_version": "1.0.0",
        "status": "FAIL" if failures else "PASS",
        "active_claim_count": len(active_claims(registry)),
        "failures": failures,
        "next_action": "repair claim collisions before mutable work" if failures else "pre-work claims are collision-free",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"SESSION_WORK_CLAIMS_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
