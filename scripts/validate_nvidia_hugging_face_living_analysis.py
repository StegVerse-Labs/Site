#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/nvidia-hugging-face-living-analysis.json"
META = ROOT / "data/nvidia-hugging-face-analysis.json"
PAGE = ROOT / "hugging-face-analysis.html"
LANDING = ROOT / "hugging-face.html"
HANDOFF = ROOT / "docs/NVIDIA_HUGGING_FACE_ANALYSIS_MIRROR_HANDOFF.md"
README = ROOT / "README.md"

errors: list[str] = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

for path in (DATA, META, PAGE, LANDING, HANDOFF, README):
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")

if DATA.exists():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    require(data.get("schema") == "stegverse.nvidia_hf_living_analysis.v2", "wrong living-analysis schema")
    require(data.get("authority_effect") == "NONE", "living analysis must grant no authority")
    require("Does Hugging Face primarily expand" in data.get("primary_research_question", ""), "primary acquisition-impact question missing")

    policy = data.get("checkpoint_policy", {})
    require(policy.get("append_only") is True, "checkpoints must be append-only")
    require(policy.get("t0_immutable") is True, "T0 must be immutable")
    require(policy.get("fabricated_checkpoints_prohibited") is True, "fabricated checkpoints must be prohibited")
    require(policy.get("failed_observation_is_gap") is True, "failed observations must remain gaps")

    baseline_policy = data.get("baseline_policy", {})
    require(baseline_policy.get("reference_baseline_id") == "B0_PRE_ACQUISITION_HF", "pre-acquisition baseline id missing")
    require(baseline_policy.get("fabricated_historical_measurements_prohibited") is True, "fabricated historical measurement prohibition missing")
    require(baseline_policy.get("preexisting_nvidia_relationships_must_be_in_baseline") is True, "pre-existing NVIDIA baseline rule missing")

    baseline = data.get("reference_baseline", {})
    require(baseline.get("baseline_id") == "B0_PRE_ACQUISITION_HF", "reference baseline missing")
    require(baseline.get("coordinate") == {"hf_capability_delta": 0, "nvidia_absorption_delta": 0}, "baseline must be graph origin")
    refs = baseline.get("evidence_refs", [])
    for required_ref in (
        "HF_PREACQ_INFERENCE_PROVIDERS_2025",
        "HF_PREACQ_MULTI_BACKEND_2025",
        "HF_PREACQ_OPEN_ROBOTICS_2025",
    ):
        require(required_ref in refs, f"pre-acquisition evidence ref missing: {required_ref}")
    require("NVIDIA robotics collaboration already existed" in " ".join(baseline.get("baseline_characteristics", [])), "pre-existing NVIDIA relationship not retained in baseline")

    model = data.get("measurement_model", {})
    cap = model.get("capability_axis", {})
    absorb = model.get("absorption_axis", {})
    require(cap.get("axis_id") == "HF_CAPABILITY_CHANGE", "capability axis id missing")
    require(absorb.get("axis_id") == "NVIDIA_ABSORPTION_CHANGE", "absorption axis id missing")
    cap_metrics = cap.get("component_metrics", [])
    absorb_metrics = absorb.get("component_metrics", [])
    require(len(cap_metrics) == 6, "capability axis must define six component metrics")
    require(len(absorb_metrics) == 6, "absorption axis must define six component metrics")
    require(len({m.get("metric_id") for m in cap_metrics}) == len(cap_metrics), "duplicate capability metric ids")
    require(len({m.get("metric_id") for m in absorb_metrics}) == len(absorb_metrics), "duplicate absorption metric ids")
    for metric in cap_metrics:
        for field in ("metric_id", "public_question", "expansion_signal", "contraction_signal"):
            require(bool(metric.get(field)), f"capability metric missing {field}")
    for metric in absorb_metrics:
        for field in ("metric_id", "public_question", "absorption_signal", "decoupling_signal"):
            require(bool(metric.get(field)), f"absorption metric missing {field}")

    combined = model.get("combined_trajectory", {})
    require(combined.get("graph_type") == "TWO_AXIS_BASELINE_DEVIATION", "two-axis graph contract missing")
    require(combined.get("x_axis") == "HF_CAPABILITY_CHANGE", "wrong x axis")
    require(combined.get("y_axis") == "NVIDIA_ABSORPTION_CHANGE", "wrong y axis")
    require(combined.get("axes_independent") is True, "axes must be independent")
    require(combined.get("zero_sum_interpretation_prohibited") is True, "zero-sum interpretation must be prohibited")
    require(combined.get("arbitrary_percentages_prohibited") is True, "arbitrary percentages must be prohibited")
    require(combined.get("fabricated_coordinates_prohibited") is True, "fabricated coordinates must be prohibited")
    require("every defined component" in combined.get("coordinate_rule", ""), "coordinate completeness rule missing")
    require(combined.get("baseline_point") == {"baseline_id": "B0_PRE_ACQUISITION_HF", "x": 0, "y": 0, "plottable": True}, "baseline graph point malformed")

    trajectory = data.get("trajectory", {})
    positions = trajectory.get("checkpoint_positions", [])
    require(isinstance(positions, list) and positions, "trajectory checkpoint positions missing")
    for p in positions:
        if p.get("plottable"):
            require(isinstance(p.get("x"), (int, float)) and isinstance(p.get("y"), (int, float)), f"plottable coordinate missing numeric x/y for {p.get('checkpoint_id')}")
        else:
            require(p.get("x") is None and p.get("y") is None and bool(p.get("reason")), f"unplottable checkpoint must retain null coordinate and reason: {p.get('checkpoint_id')}")

    evidence = data.get("evidence_registry", {})
    require(isinstance(evidence, dict) and evidence, "evidence registry missing")
    for ref in refs:
        require(ref in evidence, f"unresolved baseline evidence ref {ref}")

    checkpoints = data.get("checkpoints", [])
    require(isinstance(checkpoints, list) and checkpoints, "at least one authentic checkpoint required")
    if checkpoints:
        require(checkpoints[0].get("checkpoint_id") == "T0", "first retained checkpoint must remain T0")
        require(checkpoints[0].get("observed_at") == "2026-09-06T04:55:00Z", "T0 observed_at changed; immutable checkpoint violated")
        legacy_ids = [m.get("metric_id") for m in checkpoints[0].get("metrics", [])]
        require(legacy_ids == [
            "distribution_execution_proximity",
            "standing_execution_authority",
            "artifact_identity_observability",
            "reconstructability_contract",
            "longitudinal_change_evidence",
        ], "T0 legacy metric sequence changed")
        require(data.get("current_checkpoint") == checkpoints[-1].get("checkpoint_id"), "current_checkpoint must reference final retained checkpoint")
        for index, cp in enumerate(checkpoints):
            require(cp.get("checkpoint_id") == f"T{index}", f"checkpoint sequence gap at T{index}")
            require(bool(cp.get("authenticity_note")), f"T{index} missing authenticity note")
            try:
                datetime.fromisoformat(str(cp.get("observed_at", "")).replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"T{index} observed_at is not ISO-8601")

    require(data.get("longitudinal_state") == "PRE_ACQUISITION_REFERENCE_ESTABLISHED_POST_ACQUISITION_VECTOR_PENDING", "current longitudinal state mismatch")

if META.exists():
    meta = json.loads(META.read_text(encoding="utf-8"))
    require(meta.get("schema") == "stegverse.public-research-analysis.v2", "metadata schema not upgraded")
    require(meta.get("primary_measurement", {}).get("reference_baseline") == "B0_PRE_ACQUISITION_HF", "metadata baseline binding missing")
    require(meta.get("primary_measurement", {}).get("x_axis") == "HF_CAPABILITY_CHANGE", "metadata x axis missing")
    require(meta.get("primary_measurement", {}).get("y_axis") == "NVIDIA_ABSORPTION_CHANGE", "metadata y axis missing")
    contract = meta.get("analysis_contract", {})
    require(contract.get("pre_acquisition_reference_required") is True, "metadata pre-acquisition baseline contract missing")
    require(contract.get("preexisting_nvidia_relationships_in_baseline") is True, "metadata pre-existing NVIDIA rule missing")
    require(contract.get("zero_sum_axis_interpretation_prohibited") is True, "metadata independent-axis rule missing")
    require(meta.get("claims", {}).get("post_acquisition_complete_vector_observed") is False, "must not claim complete post-acquisition vector yet")

if PAGE.exists():
    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        "Is NVIDIA expanding Hugging Face — or absorbing it?",
        "Baseline = Hugging Face before NVIDIA's acquisition announcement.",
        "What deviation from baseline means",
        "Hugging Face capability change",
        "NVIDIA absorption change",
        "The two axes can rise together.",
        "Final combined metric",
        "The two-axis trajectory from the pre-acquisition baseline",
        "acquisition announcement alone is not a trajectory point",
        "Governance still matters, but it does not replace the two acquisition-impact axes.",
        "data/nvidia-hugging-face-living-analysis.json",
        "assets/stegverse-node-status.js",
    ):
        require(marker in page, f"living-analysis page missing marker: {marker}")
    require("More supporting evidence" not in page, "obsolete support/challenge graph label remains")
    require("More challenging evidence" not in page, "obsolete support/challenge graph label remains")
    require("registerDevice()" not in page, "living-analysis page must not directly register a Node")

if LANDING.exists():
    landing = LANDING.read_text(encoding="utf-8")
    for marker in (
        "What does NVIDIA's acquisition actually do to Hugging Face?",
        "whether NVIDIA's resources expand the open, multi-provider capability and mission Hugging Face was built for",
        "Baseline = Hugging Face before the acquisition announcement.",
        "Horizontal — Hugging Face capability",
        "Vertical — NVIDIA absorption",
        "The axes are not opposites.",
        "Governance remains part of the analysis — but it is not the primary axis.",
    ):
        require(marker in landing, f"landing page missing acquisition-impact marker: {marker}")

if HANDOFF.exists():
    handoff = HANDOFF.read_text(encoding="utf-8")
    for marker in (
        "Site #1079",
        "B0_PRE_ACQUISITION_HF",
        "HF_CAPABILITY_CHANGE",
        "NVIDIA_ABSORPTION_CHANGE",
        "two-axis",
        "pre-existing NVIDIA",
    ):
        require(marker in handoff, f"handoff missing Site #1079 marker: {marker}")

if README.exists():
    readme = README.read_text(encoding="utf-8")
    for marker in (
        "pre-acquisition Hugging Face reference",
        "Hugging Face capability change",
        "NVIDIA absorption",
        "two-axis",
        "pre-existing NVIDIA relationships",
    ):
        require(marker in readme, f"README acquisition-impact boundary missing: {marker}")

if errors:
    print("NVIDIA_HF_ACQUISITION_IMPACT_VALIDATION_FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("NVIDIA_HF_ACQUISITION_IMPACT_VALIDATION_PASS")
print("reference_baseline=B0_PRE_ACQUISITION_HF")
print("x_axis=HF_CAPABILITY_CHANGE")
print("y_axis=NVIDIA_ABSORPTION_CHANGE")
print("post_acquisition_coordinate=WITHHELD_PENDING_COMPLETE_EVIDENCE")
print("authority_effect=NONE")
