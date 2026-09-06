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
    "What changes when AI capability moves closer to real-world execution?",
    "Working capability is not the same thing as permission to act.",
    "We have a baseline, but not enough history to claim a trend.",
    "Five questions we keep separate",
    "hugging-face-analysis.html",
    "nvidia-hugging-face-governance-analysis.html",
    "stegos-node/sv-dn1-resident-observation-v3.html",
    "assets/stegverse-node-status.js",
])
require(HUB, [
    "Hugging Face Analysis Home",
    "Back to the Hugging Face analysis landing page",
    "Where things stand today",
    "What we know",
    "What we do not know yet",
    "What would change this assessment",
    "What we are watching",
    "Technical details",
    "Technical record and methodology",
    "data/nvidia-hugging-face-living-analysis.json",
    "assets/stegverse-node-status.js",
    "stegos-node/sv-dn1-resident-observation-v3.html",
    "nvidia-hugging-face-governance-analysis.html",
])
require(PAPER, [
    "When Capability Becomes Infrastructure",
    "Independent analysis",
    "Five questions that should remain separate",
    "Identity",
    "Provenance",
    "Compatibility",
    "Authority / admissibility",
    "Reconstruction",
    "Capability can originate anywhere. Authority does not simply travel with capability.",
    "/stegos-node/sv-dn1-resident-observation-v3.html",
])
require(HANDOFF, [
    "## Source of truth",
    "## Public thesis",
    "## Living-analysis contract",
    "Site #1075",
    "public-first",
])
require(PAPERS, ["nvidia-hugging-face-governance-analysis.html", "When Capability Becomes Infrastructure"])
require(NEWS, ["hugging-face.html", "Hugging Face"])

meta = json.loads(META.read_text(encoding="utf-8"))
idx = json.loads(INDEX.read_text(encoding="utf-8"))
assert meta["analysis_id"] == idx["analysis_id"] == "SV-NVIDIA-HF-GOVERNANCE-001"
assert meta["landing_page"] == "/hugging-face.html"
assert meta["analysis_hub"] == idx["public_path"] == "/hugging-face-analysis.html"
assert meta["paper"] == idx["paper_path"] == "/nvidia-hugging-face-governance-analysis.html"
assert meta["analysis_contract"]["public_first_plain_language"] is True
assert meta["analysis_contract"]["technical_notation_secondary"] is True
assert meta["claims"]["runtime_activation_claimed"] is False
assert meta["claims"]["longitudinal_change_claimed"] is False
assert len(meta["framework"]) == 5

subprocess.run([sys.executable, str(LIVING_VALIDATOR)], cwd=ROOT, check=True)
print("PASS: NVIDIA-Hugging Face landing + living analysis + fixed paper + technical evidence links")
