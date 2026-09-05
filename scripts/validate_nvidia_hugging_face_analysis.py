#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "nvidia-hugging-face-governance-analysis.html"
HANDOFF = ROOT / "docs" / "NVIDIA_HUGGING_FACE_ANALYSIS_MIRROR_HANDOFF.md"
META = ROOT / "data" / "nvidia-hugging-face-analysis.json"
INDEX = ROOT / "data" / "research-analysis-index" / "nvidia-hugging-face-governance-analysis.json"
PAPERS = ROOT / "Papers.html"

def require(path, markers):
    text = path.read_text(encoding="utf-8")
    missing = [m for m in markers if m not in text]
    if missing:
        raise SystemExit(f"FAIL: {path}: missing markers: {missing}")

require(PAGE,["When Capability Becomes Infrastructure","Independent analysis","Five questions that should remain separate","Identity","Provenance","Compatibility","Authority / admissibility","Reconstruction","Capability can originate anywhere. Authority does not simply travel with capability.","/stegos-node/sv-dn1-resident-observation-v3.html","does not imply NVIDIA or Hugging Face affiliation, endorsement, sponsorship, validation, or participation in StegVerse"])
require(HANDOFF,["## Source of truth","## Public thesis","## Public response entrypoint","## Remaining files / modules to install","## Completion boundary"])
require(PAPERS,["nvidia-hugging-face-governance-analysis.html","When Capability Becomes Infrastructure"])
meta=json.loads(META.read_text(encoding="utf-8")); idx=json.loads(INDEX.read_text(encoding="utf-8"))
assert meta["analysis_id"]==idx["analysis_id"]=="SV-NVIDIA-HF-GOVERNANCE-001"
assert meta["claims"]["publication_observed"] is False
assert meta["claims"]["runtime_activation_claimed"] is False
assert len(meta["framework"])==5
print("PASS: NVIDIA-Hugging Face public analysis contract")
