#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "nvidia-hugging-face-governance-analysis.html"
PAPERS = ROOT / "Papers.html"
HANDOFF = ROOT / "docs" / "NVIDIA_HUGGING_FACE_ANALYSIS_MIRROR_HANDOFF.md"
METADATA = ROOT / "data" / "nvidia-hugging-face-analysis.json"
RESEARCH_INDEX = ROOT / "data" / "research-analysis-index" / "nvidia-hugging-face-governance-analysis.json"

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
required_papers = [
    "nvidia-hugging-face-governance-analysis.html",
    "When Capability Becomes Infrastructure",
    "CAPABILITY ≠ AUTHORITY",
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


def require_json(path: Path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"FAIL: {path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"FAIL: {path}: expected JSON object")
    return value

require(PAGE, required_page)
require(PAPERS, required_papers)
require(HANDOFF, required_handoff)
meta = require_json(METADATA)
index = require_json(RESEARCH_INDEX)
for label, value in (("metadata", meta), ("research index", index)):
    serialized = json.dumps(value, sort_keys=True)
    if "nvidia-hugging-face-governance-analysis.html" not in serialized:
        raise SystemExit(f"FAIL: {label}: missing canonical public page reference")

print("PASS: NVIDIA-Hugging Face public analysis, metadata, and Papers discovery contract")
