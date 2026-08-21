#!/usr/bin/env python3
"""Validate the public ecosystem version/status projection without granting authority."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data/ecosystem-version-status.json"
VERSION = ROOT / "VERSION.json"
PAGE = ROOT / "ecosystem-version.html"
HOME = ROOT / "index.html"

REQUIRED_STATES = {"BUILT", "VALIDATED", "RELEASED", "DEPLOYED", "RUNTIME_PROVEN", "ACTIVATED"}
REQUIRED_VERSIONED_COMPONENTS = {
    "SITE-PUBLIC-INTERFACE": ("StegVerse-Labs/Site", "2026.08.21-dev.1", "DEVELOPMENT"),
    "LLM-ADAPTER-ECOSYSTEM-CHAT-RUNTIME": ("StegVerse-org/LLM-adapter", "2026.08.21-dev.1", "DEVELOPMENT"),
    "MASTER-RECORDS-CUSTODY": ("master-records/orchestration", "2026.08.21-dev.1", "DEVELOPMENT"),
}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_VERSION_STATUS=FAIL\n- {message}")


def main() -> None:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    version = json.loads(VERSION.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    home = HOME.read_text(encoding="utf-8")

    if data.get("schema_version") != "1.0.0":
        fail("schema_version must remain explicit")
    if data.get("projection_role") != "PUBLIC_USER_FACING_NON_AUTHORITATIVE_STATUS":
        fail("projection role must remain non-authoritative")
    if data.get("authority_effect") != "NONE" or data.get("activation_effect") is not False:
        fail("status projection must not grant authority or activation")

    if version.get("schema_version") != "1.0.0":
        fail("VERSION.json schema_version must be 1.0.0")
    if version.get("repository") != "StegVerse-Labs/Site":
        fail("VERSION.json repository mismatch")
    if version.get("source_of_truth") != "docs/SITE_MIRROR_HANDOFF.md":
        fail("VERSION.json must point to the Site mirror handoff")
    if version.get("authority_effect") != "NONE":
        fail("VERSION.json must have authority_effect NONE")
    if version.get("version_stage") == "RELEASED":
        release_record = version.get("release", {})
        if not release_record.get("tag") or not release_record.get("commit") or not release_record.get("release_evidence"):
            fail("RELEASED version requires exact tag, commit, and release evidence")
    elif version.get("release", {}).get("tag") is not None or version.get("release", {}).get("commit") is not None:
        fail("development/release-candidate versions must not claim release tag or commit")

    release = data.get("ecosystem_release", {})
    if release.get("state") == "NOT_AGGREGATELY_RELEASED":
        if release.get("version") is not None:
            fail("aggregate version cannot be invented while unreleased")
        if release.get("must_not_infer_from_main") is not True:
            fail("main must not be treated as aggregate release evidence")

    vocabulary = data.get("status_vocabulary", [])
    states = {entry.get("state") for entry in vocabulary}
    if states != REQUIRED_STATES:
        fail(f"status vocabulary mismatch: {sorted(states)}")
    for entry in vocabulary:
        if not entry.get("meaning") or not isinstance(entry.get("does_not_mean"), list):
            fail(f"status vocabulary entry incomplete: {entry.get('state')}")

    components = data.get("components", [])
    if len(components) < 7:
        fail("expected at least seven user-visible component projections")
    ids = [component.get("component_id") for component in components]
    if len(ids) != len(set(ids)):
        fail("duplicate component_id")
    by_id = {component.get("component_id"): component for component in components}
    for component in components:
        if not component.get("display_name") or not component.get("source_of_truth"):
            fail(f"component missing display/source metadata: {component.get('component_id')}")
        if not component.get("user_summary"):
            fail(f"component missing user_summary: {component.get('component_id')}")
        if component.get("release_version") is not None and "RELEASED" not in component.get("states", []):
            fail(f"component claims release version without RELEASED state: {component.get('component_id')}")

    for component_id, expected in REQUIRED_VERSIONED_COMPONENTS.items():
        component = by_id.get(component_id)
        if not component:
            fail(f"required versioned component missing: {component_id}")
        repository, component_version, stage = expected
        if component.get("repository") != repository:
            fail(f"repository drift for {component_id}")
        if component.get("version_declaration") != "VERSION.json":
            fail(f"VERSION.json declaration missing for {component_id}")
        if component.get("component_version") != component_version:
            fail(f"component version drift for {component_id}")
        if component.get("version_stage") != stage:
            fail(f"version stage drift for {component_id}")
        if component.get("release_version") is not None:
            fail(f"development component must not claim release version: {component_id}")

    site = by_id["SITE-PUBLIC-INTERFACE"]
    if site.get("component_version") != version.get("component_version"):
        fail("Site public component_version drifted from VERSION.json")
    if site.get("version_stage") != version.get("version_stage"):
        fail("Site public version_stage drifted from VERSION.json")

    required_page_markers = [
        "What version of StegVerse is this?",
        "No aggregate ecosystem release is claimed yet.",
        "Built",
        "Validated",
        "Released",
        "Deployed",
        "Runtime-proven",
        "Activated",
        "data/ecosystem-version-status.json",
        version.get("component_version"),
        "LLM-adapter · 2026.08.21-dev.1",
        "Master Records · 2026.08.21-dev.1",
        "Interface → governed runtime → custody/reconstruction" if "Interface → governed runtime → custody/reconstruction" in page else "How one governed request moves through the system",
    ]
    for marker in required_page_markers:
        if not marker or marker not in page:
            fail(f"version page missing marker: {marker}")

    if "ecosystem-version.html" not in home:
        fail("home does not expose Version & Status navigation")

    print("ECOSYSTEM_VERSION_STATUS=PASS")
    print(f"SITE_COMPONENT_VERSION={version['component_version']}")
    print(f"SITE_VERSION_STAGE={version['version_stage']}")
    print("VERSIONED_CORE_CHAIN=3")
    print("AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED")
    print(f"COMPONENT_PROJECTIONS={len(components)}")
    print("AUTHORITY_EFFECT=NONE")
    print("ACTIVATION_EFFECT=false")


if __name__ == "__main__":
    main()
