#!/usr/bin/env python3
"""Validate the bounded Reconstructable Singularity Site publication."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "papers" / "reconstructable-singularity.html"
RECONSTRUCTIVE = ROOT / "reconstructive-singularity.html"
INDEX = ROOT / "Papers.html"
REGISTRY = ROOT / "public-registry.json"
HANDOFF = ROOT / "docs" / "RECONSTRUCTABLE_SINGULARITY_SITE_MIRROR_HANDOFF.md"
RECONSTRUCTIVE_HANDOFF = ROOT / "docs" / "RECONSTRUCTIVE_SINGULARITY_SITE_MIRROR_HANDOFF.md"
DAAI_CLAIM = ROOT / "data" / "session-work-claims.d" / "site-daai-publication-1085-20260906.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"RECONSTRUCTABLE SINGULARITY PUBLICATION: FAIL - {msg}")

def main() -> int:
    for path in (PAGE, RECONSTRUCTIVE, INDEX, REGISTRY, HANDOFF, RECONSTRUCTIVE_HANDOFF, DAAI_CLAIM):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")
    page = PAGE.read_text(encoding="utf-8")
    reconstructive = RECONSTRUCTIVE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    reconstructive_handoff = RECONSTRUCTIVE_HANDOFF.read_text(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    daai = json.loads(DAAI_CLAIM.read_text(encoding="utf-8"))["claims"][0]

    for marker in (
        "Reconstructable Singularity",
        "|C_A(I)| = 1",
        "k_A*",
        "injective on Γ_A",
        "minimum hitting-set formulation",
        "Empirical proof not claimed",
        "Related concepts — distinct, not revisions",
        "None is an alias, replacement, or superseding version of another",
    ):
        require(marker in page, f"Reconstructable paper missing marker: {marker}")

    require(index.count('href="papers/reconstructable-singularity.html"') == 1, "Papers index must contain exactly one Reconstructable entry")
    require(index.count('href="reconstructive-singularity.html"') == 1, "Papers index must retain exactly one Reconstructive entry")
    require("The Reconstructive Singularity" in reconstructive, "Reconstructive paper was not preserved")
    require("SUPERSEDED_BY_RECONSTRUCTABLE_SINGULARITY" not in reconstructive_handoff, "Reconstructive handoff incorrectly marked superseded")

    claims = {item.get("id"): item for item in registry.get("claims", [])}
    claim = claims.get("RECONSTRUCTABLE-SINGULARITY-001")
    require(claim is not None, "public registry claim missing")
    require(claim.get("posture") == "RESEARCH_NOTE", "registry posture must remain RESEARCH_NOTE")
    require(claim.get("source_repo") == "StegVerse-Labs/admissibility-wiki", "canonical source repo mismatch")
    require("papers/reconstructable-singularity.html" in claim.get("public_pages", []), "Reconstructable route missing from registry")
    require("supersed" not in (claim.get("status","").lower()), "registry must not claim supersession")

    require(daai.get("state") == "RELEASED_COMPLETE", "stale DAAI papers-publication claim still active")
    require(daai.get("archive_eligible") is True, "DAAI claim is not archive eligible after release")

    for marker in (
        "Reconstructable Singularity",
        "Reconstructive Singularity",
        "Reconstruction Singularity",
        "No title is an alias for another",
        "RELEASED_COMPLETE",
        "NO_README_CHANGE_REQUIRED",
    ):
        require(marker in handoff, f"handoff missing marker: {marker}")

    print("RECONSTRUCTABLE SINGULARITY PUBLICATION: PASS - separate research formalism, related-concepts distinction, DAAI claim reconciliation, index, registry, and authority boundaries verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
