#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "hugging-face-analysis.html"
PAPER = ROOT / "nvidia-hugging-face-governance-analysis.html"
HANDOFF = ROOT / "docs" / "NVIDIA_HUGGING_FACE_ANALYSIS_MIRROR_HANDOFF.md"
META = ROOT / "data" / "nvidia-hugging-face-analysis.json"
INDEX = ROOT / "data" / "research-analysis-index" / "nvidia-hugging-face-governance-analysis.json"
PAPERS = ROOT / "Papers.html"
NEWS = ROOT / "news-releases.html"

def require(path, markers):
    text = path.read_text(encoding="utf-8")
    missing = [m for m in markers if m not in text]
    if missing:
        raise SystemExit(f"FAIL: {path}: missing markers: {missing}")

require(HUB,[
    "Living Analysis Lane",
    "Unselected Node not established.",
    "(What is this?)",
    "Connect a StegVerse Node",
    "Page arrival is not permission to create a Node.",
    "Refresh verifies an already-established Node",
    "Successfully refreshed.",
    "Failed to refresh.",
    "View / test Hugging Face observation capability",
    "assets/stegverse-node-continuity.js",
    "nodeApi.registerDevice()",
    "nodeApi.status()",
    "When Capability Becomes Infrastructure",
    "nvidia-hugging-face-governance-analysis.html",
    "SV-DN-1 governed Hugging Face observation",
    "stegos-node/sv-dn1-resident-observation-v3.html",
    "Related StegVerse papers",
    "Interoperability can establish that a capability can work here"
])
require(PAPER,["When Capability Becomes Infrastructure","Independent analysis","Five questions that should remain separate","Identity","Provenance","Compatibility","Authority / admissibility","Reconstruction","Capability can originate anywhere. Authority does not simply travel with capability.","/stegos-node/sv-dn1-resident-observation-v3.html"])
require(HANDOFF,["## Source of truth","## Public thesis","## Public response entrypoint","## Public analysis hub and paper","## Node-consent interface contract","## Completion boundary"])
require(PAPERS,["nvidia-hugging-face-governance-analysis.html","When Capability Becomes Infrastructure"])
require(NEWS,["hugging-face-analysis.html","Hugging Face, NVIDIA, and the Path From Capability to Consequence"])
meta=json.loads(META.read_text(encoding="utf-8")); idx=json.loads(INDEX.read_text(encoding="utf-8"))
assert meta["analysis_id"]==idx["analysis_id"]=="SV-NVIDIA-HF-GOVERNANCE-001"
assert meta["analysis_hub"]==idx["public_path"]=="/hugging-face-analysis.html"
assert meta["paper"]==idx["paper_path"]=="/nvidia-hugging-face-governance-analysis.html"
assert meta["claims"]["analysis_hub_publication_observed"] is False
assert meta["claims"]["runtime_activation_claimed"] is False
assert len(meta["framework"])==5
print("PASS: NVIDIA-Hugging Face analysis hub + paper + explicit Node consent interface contract")
