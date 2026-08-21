#!/usr/bin/env python3
"""Validate raw ecosystem repository enumeration without inventing a product denominator."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "data/ecosystem-repository-universe.json"
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
    raise SystemExit(f"ECOSYSTEM_REPOSITORY_UNIVERSE=FAIL\n- {message}")


def main() -> None:
    data = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.1.0":
        fail("schema_version mismatch")
    if data.get("discovery_role") != "DENOMINATOR_CONSTRUCTION_NOT_RELEASE_AUTHORITY":
        fail("discovery role drift")
    if data.get("authority_effect") != "NONE" or data.get("activation_effect") is not False:
        fail("discovery may not grant authority or activation")

    accounts = data.get("accounts", [])
    logins = [account.get("login") for account in accounts]
    if len(accounts) != 11 or set(logins) != EXPECTED_ACCOUNTS or len(logins) != len(set(logins)):
        fail("installed account inventory mismatch")

    repository_total = 0
    full_names: set[str] = set()
    for account in accounts:
        if account.get("state") != "ENUMERATED_RAW_CLASSIFICATION_PENDING":
            fail(f"account not raw-enumerated: {account.get('login')}")
        repositories = account.get("repositories", [])
        if account.get("repository_count") != len(repositories):
            fail(f"repository count drift: {account.get('login')}")
        repository_total += len(repositories)
        for name in repositories:
            full = f"{account['login']}/{name}"
            if full in full_names:
                fail(f"duplicate full repository identity: {full}")
            full_names.add(full)

    source = data.get("source", {})
    if source.get("installed_account_count") != 11:
        fail("source installed-account count drift")
    if source.get("repository_count") != repository_total:
        fail("source repository count drift")
    if repository_total != 203:
        fail(f"expected 203 enumerated repositories, saw {repository_total}")
    if source.get("stegverse_labs_second_page_observed_empty") is not True:
        fail("StegVerse-Labs page exhaustion proof missing")

    progress = data.get("progress", {})
    if progress.get("raw_accounts_enumerated") != 11 or progress.get("raw_accounts_remaining") != 0:
        fail("account enumeration progress drift")
    if progress.get("raw_repositories_enumerated") != repository_total:
        fail("raw repository progress drift")
    if float(progress.get("account_enumeration_percent", -1)) != 100.0:
        fail("account enumeration percentage must be 100")
    if progress.get("repository_enumeration_complete") is not True:
        fail("repository enumeration must be marked complete")
    if progress.get("repository_classification_complete") is not False:
        fail("raw enumeration must not masquerade as classification completion")
    if progress.get("full_version_denominator_established") is not False:
        fail("raw enumeration must not create the full version denominator")

    non_claims = data.get("non_claims", {})
    required_false = [
        "accessible_repository_equals_active_component",
        "repository_name_determines_classification",
        "enumerated_equals_classified",
        "enumerated_equals_versioned",
        "versioned_equals_released",
        "release_ready_equals_released",
        "full_ecosystem_version_coverage_complete",
    ]
    for key in required_false:
        if non_claims.get(key) is not False:
            fail(f"non-claim boundary missing: {key}")

    if data.get("aggregate_release") != "NOT_AGGREGATELY_RELEASED":
        fail("enumeration may not create an aggregate release")

    print("ECOSYSTEM_REPOSITORY_UNIVERSE=PASS")
    print("INSTALLED_ACCOUNTS=11/11")
    print(f"RAW_REPOSITORIES_ENUMERATED={repository_total}")
    print("REPOSITORY_ENUMERATION=COMPLETE")
    print("REPOSITORY_CLASSIFICATION=INCOMPLETE")
    print("FULL_VERSION_DENOMINATOR=NOT_ESTABLISHED")
    print("AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED")
    print("AUTHORITY_EFFECT=NONE")


if __name__ == "__main__":
    main()
