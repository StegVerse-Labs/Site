#!/usr/bin/env python3
"""Validate the public governed-versus-recursive comparison surface."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = {"MEASURED", "CONFIGURED", "DERIVED", "UNAVAILABLE"}


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: missing {label}: {marker}")


def main() -> int:
    html = (ROOT / "ecosystem-comparison.html").read_text(encoding="utf-8")
    script = (ROOT / "assets/ecosystem-comparison.js").read_text(encoding="utf-8")
    fixture = json.loads((ROOT / "data/llm-route-comparison-fixture.json").read_text(encoding="utf-8"))

    for marker in (
        "Governed vs Recursive",
        "Route outputs and telemetry",
        "External recursive minus StegVerse governed",
        "comparison is not authority",
        "assets/ecosystem-comparison.js",
    ):
        require(html, marker, "page marker")

    for marker in (
        "exactly two routes are required",
        "STEGVERSE_GOVERNED",
        "EXTERNAL_RECURSIVE",
        "configured values may not be presented as measured",
        "same_task_identity",
        "same_output_requirement",
        "The comparison failed closed",
    ):
        require(script, marker, "renderer invariant")

    routes = fixture.get("routes", [])
    if len(routes) != 2:
        raise SystemExit("ECOSYSTEM_COMPARISON_FAIL: fixture must contain exactly two routes")
    kinds = {route.get("route_kind") for route in routes}
    if kinds != {"STEGVERSE_GOVERNED", "EXTERNAL_RECURSIVE"}:
        raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: unexpected route kinds {sorted(kinds)}")

    for route in routes:
        if not route.get("route_id") or not route.get("metrics"):
            raise SystemExit("ECOSYSTEM_COMPARISON_FAIL: route identity and metrics required")
        for name, metric in route["metrics"].items():
            evidence = metric.get("evidence_class")
            if evidence not in EVIDENCE:
                raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: invalid evidence for {name}")
            if evidence == "UNAVAILABLE" and metric.get("value") is not None:
                raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: unavailable {name} has value")

    for name, metric in fixture.get("deltas", {}).items():
        if metric.get("evidence_class") not in EVIDENCE:
            raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: invalid delta evidence for {name}")
        if metric.get("formula") != "external_recursive - stegverse_governed":
            raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: invalid delta formula for {name}")

    invariants = fixture.get("invariants", {})
    required = {
        "same_task_identity": True,
        "same_output_requirement": True,
        "configured_values_are_measured": False,
        "comparison_is_authority": False,
        "comparison_is_admissibility": False,
    }
    for key, expected in required.items():
        if invariants.get(key) is not expected:
            raise SystemExit(f"ECOSYSTEM_COMPARISON_FAIL: invariant {key} must be {expected}")

    print("ECOSYSTEM_COMPARISON_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
