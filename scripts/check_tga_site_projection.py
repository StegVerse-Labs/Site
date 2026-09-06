#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "tga-reexamine.html"
JS = ROOT / "assets" / "tga-reexamine.js"
SAMPLE = ROOT / "data" / "tga" / "tga-site-sample.json"
HANDOFF = ROOT / "docs" / "TGA_SITE_PROJECTION_MIRROR_HANDOFF.md"
TASK = ROOT / "data" / "tasks" / "SITE-1028-TGA-PROJECTION.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TGA_SITE_PROJECTION=FAIL: {message}")


def main() -> int:
    for path in (HTML, JS, SAMPLE, HANDOFF, TASK):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")

    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    task = json.loads(TASK.read_text(encoding="utf-8"))

    html_markers = [
        "Canonical representation is not canonical reality",
        "Local media binding",
        "Governing context",
        "Observed / encoded event",
        "Uncertainty",
        "Provenance",
        "Authority effect: NONE",
        "assets/tga-reexamine.js",
    ]
    for marker in html_markers:
        require(marker in html, f"HTML missing marker: {marker}")

    js_markers = [
        "INTERPRETIVE_ENCODING_NOT_GROUND_TRUTH",
        "window.start_ms",
        "window.end_ms",
        "governing_context",
        "evaluation",
        "uncertainty",
        "URL.createObjectURL",
        "URL.revokeObjectURL",
    ]
    for marker in js_markers:
        require(marker in js, f"renderer missing marker: {marker}")

    # No external media acquisition path belongs in this projection.
    require("https://" not in js and "http://" not in js, "renderer contains external network URL")
    require("XMLHttpRequest" not in js, "renderer contains XMLHttpRequest")

    require(sample.get("representation", {}).get("assertion") == "INTERPRETIVE_ENCODING_NOT_GROUND_TRUTH", "sample lacks non-ground-truth assertion")
    require(sample.get("evaluation", {}).get("authority_effect") == "NONE_ANALYSIS_ONLY", "sample claims authority")
    require(sample.get("evaluation", {}).get("adjudicative_authority") == "NONE", "sample claims adjudicative authority")
    require(sample.get("evaluation", {}).get("counterfactual") is True, "sample must exercise counterfactual label")
    require(sample.get("governing_context", {}).get("temporal_application") == "COUNTERFACTUAL", "sample governing context not counterfactual")
    require(any(item.get("state") == "UNRESOLVED" for item in sample.get("observations", [])), "sample must preserve unresolved evidence")
    require(sample.get("source", {}).get("custody") == "REFERENCED", "sample must not infer media custody")
    require(sample.get("source", {}).get("uri") == "local-user-selected-video", "sample must exercise local-video reference semantics")

    window = sample.get("window", {})
    require(isinstance(window.get("start_ms"), int) and isinstance(window.get("end_ms"), int), "window offsets must be integers")
    require(window["start_ms"] >= 0 and window["end_ms"] > window["start_ms"], "invalid exact temporal window")

    required_uncertainty = {
        "source_uncertainty",
        "observation_uncertainty",
        "semantic_mapping_uncertainty",
        "rule_mapping_uncertainty",
        "interpretation_uncertainty",
        "evaluation_uncertainty",
    }
    require(required_uncertainty.issubset(sample.get("uncertainty", {})), "uncertainty dimensions incomplete")
    require(bool(sample.get("provenance")), "sample provenance missing")

    require(task.get("task_id") == "SITE-1028-TGA-PROJECTION", "task identity mismatch")
    require(task.get("owner", {}).get("type") == "repository_native_orchestrator", "task ownership is not repository-native")
    require(task.get("external_session_ownership_required") is False, "task requires external session ownership")
    require(task.get("manual_user_action_required") is False, "task unexpectedly requires user action")

    handoff_markers = [
        "canonical representation != canonical reality",
        "media availability does not imply custody",
        "counterfactual projection does not rewrite historical applicability",
        "repository_native_owner = scripts/admit_repository_tasks.py",
    ]
    for marker in handoff_markers:
        require(marker in handoff, f"handoff missing invariant: {marker}")

    print("TGA_SITE_PROJECTION=PASS")
    print("projection_surface=tga-reexamine.html")
    print("media_custody=NOT_INFERRED")
    print("authority_effect=NONE_PROJECTION_ONLY")
    print("counterfactual_and_unresolved_semantics=PRESERVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
