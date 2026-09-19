#!/usr/bin/env python3
"""Validate the bounded Reconstructable Singularity Site publication."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "papers" / "reconstructable-singularity.html"
INDEX = ROOT / "Papers.html"
REGISTRY = ROOT / "public-registry.json"
HANDOFF = ROOT / "docs" / "RECONSTRUCTABLE_SINGULARITY_SITE_MIRROR_HANDOFF.md"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"RECONSTRUCTABLE SINGULARITY PUBLICATION: FAIL - {msg}")

def main() -> int:
    for path in (PAGE, INDEX, REGISTRY, HANDOFF):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")
    page = PAGE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for marker in (
        "Reconstructable Singularity",
        "Research formalism v0.1",
        "Empirical proof not claimed",
        "does not establish empirical proof",
        "distinct from the previously published",
    ):
        require(marker in page, f"page missing marker: {marker}")
    require('href="papers/reconstructable-singularity.html"' in index, "Papers index link missing")
    claims = {item.get("id"): item for item in registry.get("claims", [])}
    claim = claims.get("RECONSTRUCTABLE-SINGULARITY-001")
    require(claim is not None, "public registry claim missing")
    require(claim.get("posture") == "RESEARCH_NOTE", "registry posture must be RESEARCH_NOTE")
    require(claim.get("source_repo") == "StegVerse-Labs/admissibility-wiki", "canonical source repo mismatch")
    require("papers/reconstructable-singularity.html" in claim.get("public_pages", []), "public route missing from registry")
    for marker in (
        "Reconstructable Singularity",
        "Reconstruction Singularity",
        "Reconstructive Singularity",
        "No title is an alias for another",
        "NO_README_CHANGE_REQUIRED",
    ):
        require(marker in handoff, f"handoff missing marker: {marker}")
    print("RECONSTRUCTABLE SINGULARITY PUBLICATION: PASS - bounded research mirror, distinct naming, index, registry, and authority boundaries verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
