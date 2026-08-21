#!/usr/bin/env python3
"""Validate version-coverage accounting without equating coverage with release or activation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "data/ecosystem-version-coverage.json"
STATUS = ROOT / "data/ecosystem-version-status.json"
EXPECTED_ACCOUNTS = {
    "StegVerse",
    "Admissible-Existence",
    "AdmittedCode",
    "Data-Continuation",
    "GCAT-BCAT-Engine",
    "master-records",
    "StegGhost",
    "StegVerse-002",
    "StegVerse-Labs",
    "StegVerse-org",
    "formalism-tests",
}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_VERSION_COVERAGE=FAIL\n- {message}")


def main() -> None:
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    if coverage.get("schema_version") != "1.1.0":
        fail("coverage schema_version mismatch")
    if coverage.get("scope_id") != "CORE-GOVERNED-LIFECYCLE-V1":
        fail("unexpected coverage scope")
    if coverage.get("authority_effect") != "NONE":
        fail("coverage metadata must not grant authority")

    required = coverage.get("required_components", [])
    ids = [item.get("component_id") for item in required]
    if len(required) != 13 or len(ids) != len(set(ids)):
        fail("core lifecycle denominator must contain 13 unique components")

    present = [item for item in required if item.get("declaration_state") == "PRESENT"]
    missing = [item for item in required if item.get("declaration_state") != "PRESENT"]
    for item in present:
        if item.get("version_path") != "VERSION.json":
            fail(f"noncanonical version path: {item.get('repository')}")
        if not item.get("component_version") or not item.get("declaration_commit"):
            fail(f"present declaration lacks version/commit: {item.get('repository')}")
        if item.get("version_stage") not in {"DEVELOPMENT", "RELEASE_CANDIDATE", "RELEASED"}:
            fail(f"invalid version stage: {item.get('repository')}")
        if not item.get("validator_path") or not item.get("validator_commit"):
            fail(f"component lacks owner-local version validator evidence: {item.get('repository')}")

    summary = coverage.get("coverage", {})
    if summary.get("required_component_count") != len(required):
        fail("required component count drift")
    if summary.get("declarations_present") != len(present):
        fail("present declaration count drift")
    if summary.get("declarations_missing") != len(missing):
        fail("missing declaration count drift")
    expected_percent = round((len(present) / len(required)) * 100, 2)
    if float(summary.get("declaration_coverage_percent", -1)) != expected_percent:
        fail("coverage percentage drift")
    if summary.get("missing_repositories", []) != [item.get("repository") for item in missing]:
        fail("missing repository list drift")

    validation = coverage.get("contract_validation_coverage", {})
    validation_total = (
        int(validation.get("locally_validated", 0))
        + int(validation.get("validator_installed_pending_hosted_evidence", 0))
        + int(validation.get("validator_not_yet_installed", 0))
    )
    if validation_total != len(required):
        fail("contract validation accounting does not match denominator")
    installed = int(validation.get("locally_validated", 0)) + int(validation.get("validator_installed_pending_hosted_evidence", 0))
    expected_install_percent = round((installed / len(required)) * 100, 2)
    if float(validation.get("validator_installation_coverage_percent", -1)) != expected_install_percent:
        fail("validator installation coverage percentage drift")
    if validation.get("validator_not_yet_installed") != 0:
        fail("core lifecycle validator installation is no longer complete")
    if validation.get("fully_contract_validated") is True and validation.get("validator_installed_pending_hosted_evidence"):
        fail("installed validators are not equivalent to execution evidence")

    discovery = coverage.get("full_ecosystem_repository_discovery", {})
    if discovery.get("state") not in {"PENDING", "IN_PROGRESS"}:
        fail("full ecosystem discovery may not claim completion before repository denominator exists")
    if discovery.get("version_coverage_complete") is not False:
        fail("core coverage must not masquerade as full ecosystem version coverage")
    observed_accounts = set(discovery.get("installed_accounts_observed", []))
    if discovery.get("state") == "IN_PROGRESS" and observed_accounts != EXPECTED_ACCOUNTS:
        fail("installed ecosystem account enumeration mismatch")

    aggregate = coverage.get("aggregate_release", {})
    if aggregate.get("state") != "NOT_AGGREGATELY_RELEASED" or aggregate.get("version") is not None:
        fail("version coverage must not create an aggregate release")
    if aggregate.get("component_version_coverage_is_release") is not False:
        fail("declaration coverage cannot be release evidence")

    public_release = status.get("ecosystem_release", {})
    if public_release.get("state") != "NOT_AGGREGATELY_RELEASED" or public_release.get("version") is not None:
        fail("public status disagrees with coverage release boundary")

    print("ECOSYSTEM_VERSION_COVERAGE=PASS")
    print(f"CORE_DECLARATION_COVERAGE={len(present)}/{len(required)}")
    print(f"CORE_VALIDATOR_INSTALLATION={installed}/{len(required)}")
    print(f"CORE_DECLARATION_COVERAGE_PERCENT={expected_percent}")
    print(f"CORE_VALIDATOR_INSTALLATION_PERCENT={expected_install_percent}")
    print(f"FULL_ECOSYSTEM_DISCOVERY={discovery.get('state')}")
    print("AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED")
    print("AUTHORITY_EFFECT=NONE")


if __name__ == "__main__":
    main()
