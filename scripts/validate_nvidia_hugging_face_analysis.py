#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "hugging-face.html"
HUB = ROOT / "hugging-face-analysis.html"
PAPER = ROOT / "nvidia-hugging-face-governance-analysis.html"
HANDOFF = ROOT / "docs/NVIDIA_HUGGING_FACE_ANALYSIS_MIRROR_HANDOFF.md"
META = ROOT / "data/nvidia-hugging-face-analysis.json"
INDEX = ROOT / "data/research-analysis-index/nvidia-hugging-face-governance-analysis.json"
PAPERS = ROOT / "Papers.html"
NEWS = ROOT / "news-releases.html"
LIVING_VALIDATOR = ROOT / "scripts/validate_nvidia_hugging_face_living_analysis.py"


def require(path: Path, markers: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit(f"FAIL: {path}: missing markers: {missing}")

for path in (LANDING, HUB, PAPER, HANDOFF, META, INDEX, PAPERS, NEWS, LIVING_VALIDATOR):
    if not path.exists():
        raise SystemExit(f"FAIL: missing {path.relative_to(ROOT)}")

require(LANDING, [
    "What does NVIDIA's acquisition actually do to Hugging Face?",
    "Baseline = Hugging Face before the acquisition announcement.",
    "Horizontal — Hugging Face capability",
    "Vertical — NVIDIA absorption",
    "The axes are not opposites.",
    "hugging-face-analysis.html",
    "nvidia-hugging-face-governance-analysis.html",
    "stegos-node/sv-dn1-resident-observation-v3.html",
    "assets/stegverse-node-status.js",
])
require(HUB, [
    "Hugging Face Analysis Home",
    "Is NVIDIA expanding Hugging Face — or absorbing it?",
    "Baseline = Hugging Face before NVIDIA's acquisition announcement.",
    "Hugging Face capability change",
    "NVIDIA absorption change",
    "Final combined metric",
    "The two-axis trajectory from the pre-acquisition baseline",
    "acquisition announcement alone is not a trajectory point",
    "Technical record and methodology",
    "data/nvidia-hugging-face-living-analysis.json",
    "assets/stegverse-node-status.js",
    "stegos-node/sv-dn1-resident-observation-v3.html",
    "nvidia-hugging-face-governance-analysis.html",
])
require(PAPER, [
    "When Capability Becomes Infrastructure",
    "Independent analysis",
    "Capability can originate anywhere. Authority does not simply travel with capability.",
])
require(HANDOFF, [
    "## Source of truth",
    "Site #1079",
    "B0_PRE_ACQUISITION_HF",
    "HF_CAPABILITY_CHANGE",
    "NVIDIA_ABSORPTION_CHANGE",
])
require(PAPERS, ["nvidia-hugging-face-governance-analysis.html", "When Capability Becomes Infrastructure"])
require(NEWS, ["hugging-face.html", "Hugging Face"])

meta = json.loads(META.read_text(encoding="utf-8"))
idx = json.loads(INDEX.read_text(encoding="utf-8"))
assert meta["analysis_id"] == idx["analysis_id"] == "SV-NVIDIA-HF-GOVERNANCE-001"
assert meta["landing_page"] == "/hugging-face.html"
assert meta["analysis_hub"] == idx["public_path"] == "/hugging-face-analysis.html"
assert meta["paper"] == idx["paper_path"] == "/nvidia-hugging-face-governance-analysis.html"
assert meta["primary_measurement"]["reference_baseline"] == "B0_PRE_ACQUISITION_HF"
assert meta["primary_measurement"]["x_axis"] == "HF_CAPABILITY_CHANGE"
assert meta["primary_measurement"]["y_axis"] == "NVIDIA_ABSORPTION_CHANGE"
assert meta["primary_measurement"]["axes_independent"] is True
assert meta["claims"]["runtime_activation_claimed"] is False
assert meta["claims"]["longitudinal_change_claimed"] is False

subprocess.run([sys.executable, str(LIVING_VALIDATOR)], cwd=ROOT, check=True)
print("PASS: NVIDIA-Hugging Face pre-acquisition baseline + two-axis acquisition-impact analysis")
