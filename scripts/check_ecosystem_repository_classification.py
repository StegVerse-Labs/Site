#!/usr/bin/env python3
"""Validate repository classification without converting evaluation into version/release authority."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "data/ecosystem-repository-classification.json"
UNIVERSE = ROOT / "data/ecosystem-repository-universe.json"
ALLOWED_CLASSES = {"ACTIVE_COMPONENT","RESEARCH_FORMALISM","MIRROR_LEGACY","TELEMETRY_SUPPORT","CONTROL_METADATA","UNCLASSIFIED"}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_REPOSITORY_CLASSIFICATION=FAIL\n- {message}")


def main() -> None:
    data = json.loads(CLASSIFICATION.read_text(encoding="utf-8"))
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))

    if data.get("schema_version") != "1.4.0":
        fail("classification schema_version mismatch")
    if data.get("raw_repository_denominator") != 203:
        fail("classification denominator must remain 203 until a newer universe is machine-proven")
    if universe.get("progress", {}).get("raw_repositories_enumerated") != 203:
        fail("universe source does not prove 203 repositories")
    if universe.get("progress", {}).get("repository_enumeration_complete") is not True:
        fail("classification requires completed raw enumeration")
    if data.get("authority_effect") != "NONE" or data.get("activation_effect") is not False:
        fail("classification may not grant authority or activation")

    universe_repositories = {
        f"{account['login']}/{name}"
        for account in universe.get("accounts", [])
        for name in account.get("repositories", [])
    }
    records = data.get("records", [])
    repositories = [record.get("repository") for record in records]
    if len(repositories) != len(set(repositories)):
        fail("duplicate repository classification record")
    for record in records:
        repo = record.get("repository")
        cls = record.get("class")
        obligation = str(record.get("version_obligation", ""))
        if repo not in universe_repositories:
            fail(f"classification references repository outside universe: {repo}")
        if cls not in ALLOWED_CLASSES:
            fail(f"invalid class for {repo}: {cls}")
        if not record.get("evidence") or not record.get("authority_summary"):
            fail(f"classification lacks evidence/summary: {repo}")
        if cls == "ACTIVE_COMPONENT" and obligation != "COMPONENT_VERSION_REQUIRED":
            fail(f"active component lacks component-version obligation: {repo}")
        if cls == "UNCLASSIFIED" and not record.get("classification_blocker"):
            fail(f"unclassified record lacks explicit blocker: {repo}")
        if cls == "TELEMETRY_SUPPORT" and obligation != "SCHEMA_AND_DATA_VERSIONING_REQUIRED":
            fail(f"telemetry support version obligation drift: {repo}")
        if cls == "CONTROL_METADATA" and "VERSION_REQUIRED" not in obligation:
            fail(f"control metadata lacks protocol/schema version obligation: {repo}")
        if cls == "RESEARCH_FORMALISM" and "VERSION_REQUIRED" not in obligation:
            fail(f"research/formalism record lacks artifact/test/schema version obligation: {repo}")

    counts = Counter(record["class"] for record in records)
    resolved = len(records) - counts["UNCLASSIFIED"]
    progress = data.get("progress", {})
    expected = {
        "records_evaluated": len(records),
        "resolved_classifications": resolved,
        "evaluated_but_unclassified": counts["UNCLASSIFIED"],
        "repositories_not_yet_evaluated": 203 - len(records),
        "active_components_identified": counts["ACTIVE_COMPONENT"],
        "research_formalisms_identified": counts["RESEARCH_FORMALISM"],
        "mirror_legacy_identified": counts["MIRROR_LEGACY"],
        "telemetry_support_identified": counts["TELEMETRY_SUPPORT"],
        "control_metadata_identified": counts["CONTROL_METADATA"],
    }
    for key, value in expected.items():
        if progress.get(key) != value:
            fail(f"classification progress drift for {key}: expected {value}, got {progress.get(key)}")
    if float(progress.get("evaluation_percent", -1)) != round(len(records) / 203 * 100, 2):
        fail("evaluation percentage drift")
    if float(progress.get("resolved_classification_percent", -1)) != round(resolved / 203 * 100, 2):
        fail("resolved classification percentage drift")
    if progress.get("full_active_version_denominator_established") is not False:
        fail("partial classification cannot establish the full active version denominator")
    if data.get("aggregate_release") != "NOT_AGGREGATELY_RELEASED":
        fail("classification cannot create aggregate release")

    print("ECOSYSTEM_REPOSITORY_CLASSIFICATION=PASS")
    print(f"REPOSITORY_CLASSIFICATION_EVALUATED={len(records)}/203")
    print(f"REPOSITORY_CLASSIFICATION_RESOLVED={resolved}/203")
    print(f"ACTIVE_COMPONENTS_IDENTIFIED={counts['ACTIVE_COMPONENT']}")
    print(f"RESEARCH_FORMALISMS_IDENTIFIED={counts['RESEARCH_FORMALISM']}")
    print(f"TELEMETRY_SUPPORT_IDENTIFIED={counts['TELEMETRY_SUPPORT']}")
    print(f"CONTROL_METADATA_IDENTIFIED={counts['CONTROL_METADATA']}")
    print(f"UNCLASSIFIED_EVALUATED={counts['UNCLASSIFIED']}")
    print("FULL_ACTIVE_VERSION_DENOMINATOR=NOT_ESTABLISHED")
    print("AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED")
    print("AUTHORITY_EFFECT=NONE")


if __name__ == "__main__":
    main()
