#!/usr/bin/env python3
"""Validate the public ecosystem version/status projection without granting authority."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data/ecosystem-version-status.json"
PAGE = ROOT / "ecosystem-version.html"
HOME = ROOT / "index.html"

REQUIRED_STATES = {"BUILT", "VALIDATED", "RELEASED", "DEPLOYED", "RUNTIME_PROVEN", "ACTIVATED"}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_VERSION_STATUS=FAIL\n- {message}")


def main() -> None:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    home = HOME.read_text(encoding="utf-8")

    if data.get("schema_version") != "1.0.0":
        fail("schema_version must remain explicit")
    if data.get("projection_role") != "PUBLIC_USER_FACING_NON_AUTHORITATIVE_STATUS":
        fail("projection role must remain non-authoritative")
    if data.get("authority_effect") != "NONE" or data.get("activation_effect") is not False:
        fail("status projection must not grant authority or activation")

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
    if len(components) < 5:
        fail("expected at least five user-visible component projections")
    ids = [component.get("component_id") for component in components]
    if len(ids) != len(set(ids)):
        fail("duplicate component_id")
    for component in components:
        if not component.get("display_name") or not component.get("source_of_truth"):
            fail(f"component missing display/source metadata: {component.get('component_id')}")
        if not component.get("user_summary"):
            fail(f"component missing user_summary: {component.get('component_id')}")
        if component.get("release_version") is not None and "RELEASED" not in component.get("states", []):
            fail(f"component claims release version without RELEASED state: {component.get('component_id')}")

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
    ]
    for marker in required_page_markers:
        if marker not in page:
            fail(f"version page missing marker: {marker}")

    if "ecosystem-version.html" not in home:
        fail("home does not expose Version & Status navigation")

    print("ECOSYSTEM_VERSION_STATUS=PASS")
    print("AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED")
    print(f"COMPONENT_PROJECTIONS={len(components)}")
    print("AUTHORITY_EFFECT=NONE")
    print("ACTIVATION_EFFECT=false")


if __name__ == "__main__":
    main()
