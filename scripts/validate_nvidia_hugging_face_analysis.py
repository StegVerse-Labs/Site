#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "nvidia-hugging-face-governance-analysis.html"
HANDOFF = ROOT / "docs" / "NVIDIA_HUGGING_FACE_ANALYSIS_MIRROR_HANDOFF.md"

required_page = [
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
    "does not imply NVIDIA or Hugging Face affiliation, endorsement, sponsorship, validation, or participation in StegVerse",
]
required_handoff = [
    "## Source of truth",
    "## Public thesis",
    "## Public response entrypoint",
    "## Remaining files / modules to install",
    "## Completion boundary",
]

def require(path: Path, markers):
    text = path.read_text(encoding="utf-8")
    missing = [m for m in markers if m not in text]
    if missing:
        raise SystemExit(f"FAIL: {path}: missing markers: {missing}")

require(PAGE, required_page)
require(HANDOFF, required_handoff)
print("PASS: NVIDIA-Hugging Face public analysis contract")
