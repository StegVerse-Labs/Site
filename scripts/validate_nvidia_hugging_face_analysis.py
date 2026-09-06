#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


for path in (HUB, PAPER, HANDOFF, META, INDEX, PAPERS, NEWS, LIVING_VALIDATOR):
    if not path.exists():
        raise SystemExit(f"FAIL: missing {path.relative_to(ROOT)}")

# The hub is now the analytical record itself. Node status remains shared/passive,
# while SV-DN-1 remains the distinct technical observation/evidence surface.
require(HUB, [
    "This page is the analysis itself",
    "Current analytical assessment",
    "Evidence → metric → interpretation",
    "Observation coverage and gaps",
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
    "## Corrected completion boundary",
    "Site #1069",
])
require(PAPERS, ["nvidia-hugging-face-governance-analysis.html", "When Capability Becomes Infrastructure"])
require(NEWS, ["hugging-face-analysis.html", "Hugging Face"])

meta = json.loads(META.read_text(encoding="utf-8"))
idx = json.loads(INDEX.read_text(encoding="utf-8"))
assert meta["analysis_id"] == idx["analysis_id"] == "SV-NVIDIA-HF-GOVERNANCE-001"
assert meta["analysis_hub"] == idx["public_path"] == "/hugging-face-analysis.html"
assert meta["paper"] == idx["paper_path"] == "/nvidia-hugging-face-governance-analysis.html"
assert meta["claims"]["runtime_activation_claimed"] is False
assert meta["claims"]["longitudinal_change_claimed"] is False
assert len(meta["framework"]) == 5

subprocess.run([sys.executable, str(LIVING_VALIDATOR)], cwd=ROOT, check=True)
print("PASS: NVIDIA-Hugging Face fixed paper + living analysis + technical evidence links")
