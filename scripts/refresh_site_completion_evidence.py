#!/usr/bin/env python3
"""Refresh strict Site completion evidence from the current runtime proof.

This script does not grant release, ecosystem-completion, admissibility, or
external mutation authority. It projects already-observed Site runtime evidence
and the current public inventory into the repository-local completion-evidence
contract used by the scheduled autonomy cycle.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "data" / "autonomy" / "runtime-verification-evidence.json"
INVENTORY_PATH = ROOT / "data" / "autonomy" / "public-ecosystem-inventory.json"
OUTPUT_PATH = ROOT / "data" / "autonomy" / "completion-evidence.json"

EVIDENCE_URLS = [
    "https://stegverse-labs.github.io/Site/autonomy-live.html",
    "https://stegverse-labs.github.io/Site/autonomy-roadmap.html",
    "https://stegverse-labs.github.io/Site/data/autonomy/live-status.json",
    "https://stegverse-labs.github.io/Site/data/autonomy/runtime-verification-evidence.json",
]


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def build_evidence(runtime: dict, inventory: dict) -> dict:
    if runtime.get("repository") != "StegVerse-Labs/Site":
        raise ValueError("runtime evidence repository mismatch")
    if runtime.get("objective_id") != "site-public-autonomy-observability":
        raise ValueError("runtime evidence objective mismatch")

    required = runtime.get("required_checks")
    passed = runtime.get("passed_required_checks")
    failed_ids = runtime.get("failed_required_check_ids")
    state = runtime.get("state")
    generated_at = runtime.get("generated_at")

    if not isinstance(required, int) or required < 1:
        raise ValueError("invalid required-check count")
    if not isinstance(passed, int) or passed < 0 or passed > required:
        raise ValueError("invalid passed-check count")
    if not isinstance(failed_ids, list):
        raise ValueError("failed_required_check_ids must be a list")
    if not isinstance(generated_at, str) or not generated_at:
        raise ValueError("runtime evidence has no generated_at")

    runtime_pass = state == "PASS" and passed == required and failed_ids == []
    repositories = inventory.get("repositories")
    organizations = inventory.get("organizations")
    if not isinstance(repositories, list) or not isinstance(organizations, list):
        raise ValueError("public inventory is incomplete")

    mobile_verified = []
    checks = runtime.get("checks")
    if isinstance(checks, list):
        by_id = {item.get("id"): item for item in checks if isinstance(item, dict)}
        if by_id.get("live-mobile-flow", {}).get("passed") is True:
            mobile_verified.append("autonomy-live.html")
        if by_id.get("roadmap-mobile-flow", {}).get("passed") is True:
            mobile_verified.append("autonomy-roadmap.html")

    return {
        "schema_version": "1.0",
        "repository": "StegVerse-Labs/Site",
        "objective_id": "site-public-autonomy-observability",
        "runtime_observed": True,
        "user_visible_outcome_verified": runtime_pass,
        "verifier_source": "github-actions-runtime-verification",
        "critical_blockers": 0 if runtime_pass else max(1, len(failed_ids)),
        "manual_completion_dependency": False,
        "verified_at": generated_at,
        "evidence_urls": EVIDENCE_URLS,
        "observed_results": {
            "runtime_verification_state": state,
            "required_checks": required,
            "passed_required_checks": passed,
            "failed_required_check_ids": failed_ids,
            "public_repository_inventory_count": len(repositories),
            "public_organization_count": len(organizations),
            "mobile_flows_verified": mobile_verified,
        },
        "authority": {
            "evidence_is_release_authority": False,
            "evidence_is_ecosystem_completion_authority": False,
            "site_runtime_completion_is_adapter_activation": False,
            "manual_user_action_required": False,
        },
    }


def main() -> int:
    evidence = build_evidence(load_object(RUNTIME_PATH), load_object(INVENTORY_PATH))
    OUTPUT_PATH.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "state": evidence["observed_results"]["runtime_verification_state"],
        "verified_at": evidence["verified_at"],
        "repository_count": evidence["observed_results"]["public_repository_inventory_count"],
        "authority_effect": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
