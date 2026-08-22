#!/usr/bin/env python3
"""Validate repository classification without converting evaluation into version/release authority."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CLASSIFICATION = DATA / "ecosystem-repository-classification.json"
UNIVERSE = DATA / "ecosystem-repository-universe.json"
WAVE_GLOB = "ecosystem-repository-classification-wave-*.json"
ALLOWED_CLASSES = {"ACTIVE_COMPONENT","RESEARCH_FORMALISM","MIRROR_LEGACY","TELEMETRY_SUPPORT","CONTROL_METADATA","UNCLASSIFIED"}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_REPOSITORY_CLASSIFICATION=FAIL\n- {message}")


def validate_record(record: dict, universe_repositories: set[str]) -> None:
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
    if cls == "MIRROR_LEGACY" and obligation != "PROVENANCE_AND_DISPOSITION_VERSION_REQUIRED":
        fail(f"mirror/legacy record lacks provenance/disposition version obligation: {repo}")


def computed_progress(records: list[dict]) -> tuple[Counter, dict]:
    counts = Counter(record["class"] for record in records)
    resolved = len(records) - counts["UNCLASSIFIED"]
    progress = {
        "records_evaluated": len(records),
        "resolved_classifications": resolved,
        "evaluated_but_unclassified": counts["UNCLASSIFIED"],
        "repositories_not_yet_evaluated": 203 - len(records),
        "active_components_identified": counts["ACTIVE_COMPONENT"],
        "research_formalisms_identified": counts["RESEARCH_FORMALISM"],
        "mirror_legacy_identified": counts["MIRROR_LEGACY"],
        "telemetry_support_identified": counts["TELEMETRY_SUPPORT"],
        "control_metadata_identified": counts["CONTROL_METADATA"],
        "evaluation_percent": round(len(records) / 203 * 100, 2),
        "resolved_classification_percent": round(resolved / 203 * 100, 2),
        "full_active_version_denominator_established": False,
    }
    return counts, progress


def require_progress(label: str, declared: dict, expected: dict) -> None:
    for key, value in expected.items():
        actual = declared.get(key)
        if actual != value:
            fail(f"{label} progress drift for {key}: expected {value}, got {actual}")


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
    if data.get("aggregate_release") != "NOT_AGGREGATELY_RELEASED":
        fail("classification cannot create aggregate release")

    universe_repositories = {
        f"{account['login']}/{name}"
        for account in universe.get("accounts", [])
        for name in account.get("repositories", [])
    }

    base_records = list(data.get("records", []))
    base_repositories = [record.get("repository") for record in base_records]
    if len(base_repositories) != len(set(base_repositories)):
        fail("duplicate repository classification record in base ledger")
    for record in base_records:
        validate_record(record, universe_repositories)

    _, base_expected = computed_progress(base_records)
    require_progress("base", data.get("progress", {}), base_expected)

    combined_records = list(base_records)
    seen = set(base_repositories)
    applied_waves: list[str] = []
    latest_expected = base_expected

    for path in sorted(DATA.glob(WAVE_GLOB)):
        wave = json.loads(path.read_text(encoding="utf-8"))
        if wave.get("universe_denominator") != 203:
            fail(f"wave denominator drift: {path.name}")
        if wave.get("authority_effect") != "NONE" or wave.get("activation_effect") is not False:
            fail(f"wave may not grant authority or activation: {path.name}")
        if wave.get("aggregate_release") != "NOT_AGGREGATELY_RELEASED":
            fail(f"wave may not create aggregate release: {path.name}")
        if wave.get("base_evaluated") != len(combined_records):
            fail(f"wave base_evaluated mismatch for {path.name}: expected {len(combined_records)}, got {wave.get('base_evaluated')}")

        wave_records = list(wave.get("records", []))
        if not wave_records:
            fail(f"classification wave has no records: {path.name}")
        for record in wave_records:
            validate_record(record, universe_repositories)
            repo = record.get("repository")
            if repo in seen:
                fail(f"duplicate repository identity across classification waves: {repo}")
            seen.add(repo)
            combined_records.append(record)

        _, computed = computed_progress(combined_records)
        require_progress(path.name, wave.get("aggregate_expected", {}), computed)
        latest_expected = computed
        applied_waves.append(path.name)

    counts, final_progress = computed_progress(combined_records)
    if final_progress != latest_expected:
        fail("final aggregate progress drift")
    if final_progress["full_active_version_denominator_established"] is not False:
        fail("partial classification cannot establish the full active version denominator")

    print("ECOSYSTEM_REPOSITORY_CLASSIFICATION=PASS")
    print(f"CLASSIFICATION_WAVES_APPLIED={len(applied_waves)}")
    for wave_name in applied_waves:
        print(f"CLASSIFICATION_WAVE={wave_name}")
    print(f"REPOSITORY_CLASSIFICATION_EVALUATED={len(combined_records)}/203")
    print(f"REPOSITORY_CLASSIFICATION_RESOLVED={final_progress['resolved_classifications']}/203")
    print(f"ACTIVE_COMPONENTS_IDENTIFIED={counts['ACTIVE_COMPONENT']}")
    print(f"RESEARCH_FORMALISMS_IDENTIFIED={counts['RESEARCH_FORMALISM']}")
    print(f"MIRROR_LEGACY_IDENTIFIED={counts['MIRROR_LEGACY']}")
    print(f"TELEMETRY_SUPPORT_IDENTIFIED={counts['TELEMETRY_SUPPORT']}")
    print(f"CONTROL_METADATA_IDENTIFIED={counts['CONTROL_METADATA']}")
    print(f"UNCLASSIFIED_EVALUATED={counts['UNCLASSIFIED']}")
    print("FULL_ACTIVE_VERSION_DENOMINATOR=NOT_ESTABLISHED")
    print("AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED")
    print("AUTHORITY_EFFECT=NONE")


if __name__ == "__main__":
    main()
