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
    require(data.get("schema") == "stegverse.nvidia_hf_living_analysis.v1", "wrong living-analysis schema")
    require(data.get("authority_effect") == "NONE", "living analysis must grant no authority")
    vocab = data.get("interpretation_vocabulary")
    require(vocab == ["Supports", "Challenges", "Neutral", "Indeterminate"], "interpretation vocabulary/order drift")
    policy = data.get("checkpoint_policy", {})
    require(policy.get("append_only") is True, "checkpoints must be append-only")
    require(policy.get("t0_immutable") is True, "T0 must be immutable")
    require(policy.get("fabricated_checkpoints_prohibited") is True, "fabricated checkpoints must be prohibited")
    require(policy.get("failed_observation_is_gap") is True, "failed observations must remain gaps")
    require(policy.get("higher_resolution_service_separate") is True, "public/high-resolution separation missing")

    evidence = data.get("evidence_registry", {})
    require(isinstance(evidence, dict) and evidence, "evidence registry missing")
    checkpoints = data.get("checkpoints", [])
    require(isinstance(checkpoints, list) and checkpoints, "at least one authentic checkpoint required")
    if checkpoints:
        require(checkpoints[0].get("checkpoint_id") == "T0", "first checkpoint must be T0")
        require(data.get("current_checkpoint") == checkpoints[-1].get("checkpoint_id"), "current_checkpoint must reference final retained checkpoint")
        ids = [cp.get("checkpoint_id") for cp in checkpoints]
        require(len(ids) == len(set(ids)), "duplicate checkpoint ids")
        for index, cp in enumerate(checkpoints):
            expected = f"T{index}"
            require(cp.get("checkpoint_id") == expected, f"checkpoint sequence must be append-only without gaps: expected {expected}")
            require(bool(cp.get("authenticity_note")), f"{expected} missing authenticity note")
            try:
                datetime.fromisoformat(str(cp.get("observed_at", "")).replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{expected} observed_at is not ISO-8601")
            coverage = cp.get("coverage", {})
            require(isinstance(coverage.get("successful_inputs"), list), f"{expected} successful_inputs missing")
            require(isinstance(coverage.get("gaps"), list), f"{expected} gaps missing")
            metrics = cp.get("metrics", [])
            require(isinstance(metrics, list) and metrics, f"{expected} metrics missing")
            metric_ids: set[str] = set()
            for metric in metrics:
                mid = metric.get("metric_id")
                require(isinstance(mid, str) and bool(mid), f"{expected} metric_id missing")
                if isinstance(mid, str):
                    require(mid not in metric_ids, f"{expected} duplicate metric_id {mid}")
                    metric_ids.add(mid)
                for field in (
                    "label", "observed_value", "baseline_value", "previous_value",
                    "delta_from_t0", "delta_from_previous", "interpretation", "confidence",
                    "effect_on_analysis", "interpretation_rule", "evidence_refs",
                ):
                    require(field in metric, f"{expected}/{mid} missing {field}")
                require(metric.get("interpretation") in vocab, f"{expected}/{mid} invalid interpretation")
                require(metric.get("confidence") in {"LOW", "MEDIUM", "HIGH"}, f"{expected}/{mid} invalid confidence")
                d0 = metric.get("delta_from_t0", {})
                dr = metric.get("delta_from_previous", {})
                require(isinstance(d0, dict) and "state" in d0 and "value" in d0, f"{expected}/{mid} malformed Δ0")
                require(isinstance(dr, dict) and "state" in dr and "value" in dr, f"{expected}/{mid} malformed Δr")
                refs = metric.get("evidence_refs")
                require(isinstance(refs, list) and refs, f"{expected}/{mid} evidence_refs missing")
                if isinstance(refs, list):
                    for ref in refs:
                        require(ref in evidence, f"{expected}/{mid} unresolved evidence ref {ref}")
                if index == 0:
                    require(metric.get("previous_value") is None, f"T0/{mid} must not fabricate previous value")
                    require(dr.get("value") is None, f"T0/{mid} Δr must be unavailable")
            assessment = cp.get("assessment", {})
            for field in ("state", "summary", "strongest_supporting_observation", "strongest_challenge", "next_evidence_needed"):
                require(bool(assessment.get(field)), f"{expected} assessment missing {field}")

    if len(checkpoints) == 1:
        require(data.get("longitudinal_state") == "ONE_AUTHENTIC_CHECKPOINT_ONLY", "single-checkpoint record must identify one-point longitudinal state")
        require("NO_AUTHENTIC_T1_YET" in json.dumps(data), "single-checkpoint record must explicitly state no authentic T1")

if META.exists():
    meta = json.loads(META.read_text(encoding="utf-8"))
    require(meta.get("landing_page") == "/hugging-face.html", "metadata missing distinct landing page")
    require(meta.get("living_analysis_data") == "/data/nvidia-hugging-face-living-analysis.json", "metadata missing living-analysis data binding")
    contract = meta.get("analysis_contract", {})
    require(contract.get("append_only_checkpoints") is True, "metadata append-only contract missing")
    require(contract.get("fabricated_t1_prohibited") is True, "metadata fabricated-T1 prohibition missing")
    require(contract.get("public_first_plain_language") is True, "metadata public-first UX contract missing")
    require(contract.get("technical_notation_secondary") is True, "metadata technical-secondary UX contract missing")
    require(meta.get("claims", {}).get("longitudinal_change_claimed") is False, "initial T0 metadata must not claim longitudinal change")

if PAGE.exists():
    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        "Hugging Face Analysis Home",
        "Back to the Hugging Face analysis landing page",
        "Where things stand today",
        "We have a baseline, but not enough history to claim a trend.",
        "What we know",
        "What we do not know yet",
        "What would change this assessment",
        "What we are watching",
        "What each observation means for the analysis",
        "Technical details",
        "Technical record and methodology",
        "observed value → T0 baseline → previous checkpoint → Δ₀ / Δᵣ → interpretation rule → evidence reference",
        "data/nvidia-hugging-face-living-analysis.json",
        "assets/stegverse-node-status.js",
        "stegos-node/sv-dn1-resident-observation-v3.html",
        "nvidia-hugging-face-governance-analysis.html",
    ):
        require(marker in page, f"living-analysis page missing marker: {marker}")
    require("registerDevice()" not in page, "living-analysis page must not directly register a Node")
    require("Qwen/Qwen3-8B" not in page, "living-analysis page must not imply one direct browser fetch is the canonical analytical record")
    require("fetch('data/nvidia-hugging-face-living-analysis.json'" in page, "page must load canonical living-analysis record")

if LANDING.exists():
    landing = LANDING.read_text(encoding="utf-8")
    for marker in (
        "What changes when AI capability moves closer to real-world execution?",
        "Working capability is not the same thing as permission to act.",
        "We have a baseline, but not enough history to claim a trend.",
        "Five questions we keep separate",
        "hugging-face-analysis.html",
    ):
        require(marker in landing, f"landing page missing marker: {marker}")

if HANDOFF.exists():
    handoff = HANDOFF.read_text(encoding="utf-8")
    for marker in (
        "Site #1075",
        "distinct landing page",
        "public-first",
        "Technical notation remains secondary",
        "T0 is immutable",
    ):
        require(marker in handoff, f"handoff missing public UX contract marker: {marker}")

if README.exists():
    readme = README.read_text(encoding="utf-8")
    require("### NVIDIA–Hugging Face living analysis" in readme, "README living-analysis section missing")
    for marker in (
        "hugging-face.html",
        "public-first",
        "append-only",
        "T0",
        "Supports / Challenges / Neutral / Indeterminate",
        "Site is not the observation authority",
    ):
        require(marker in readme, f"README living-analysis boundary missing: {marker}")

if errors:
    print("NVIDIA_HF_LIVING_ANALYSIS_VALIDATION_FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("NVIDIA_HF_LIVING_ANALYSIS_VALIDATION_PASS")
print("checkpoint_count=1")
print("current_checkpoint=T0")
print("longitudinal_change_claimed=false")
print("public_first_plain_language=true")
print("authority_effect=NONE")
