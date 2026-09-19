#!/usr/bin/env python3
"""Validate Reconstructable Singularity publication supersession."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "papers" / "reconstructable-singularity.html"
LEGACY = ROOT / "reconstructive-singularity.html"
INDEX = ROOT / "Papers.html"
REGISTRY = ROOT / "public-registry.json"
HANDOFF = ROOT / "docs" / "RECONSTRUCTABLE_SINGULARITY_SITE_MIRROR_HANDOFF.md"
OLD_HANDOFF = ROOT / "docs" / "RECONSTRUCTIVE_SINGULARITY_SITE_MIRROR_HANDOFF.md"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"RECONSTRUCTABLE SINGULARITY PUBLICATION: FAIL - {msg}")

def main() -> int:
    for path in (PAGE, LEGACY, INDEX, REGISTRY, HANDOFF, OLD_HANDOFF):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")
    page = PAGE.read_text(encoding="utf-8")
    legacy = LEGACY.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    old_handoff = OLD_HANDOFF.read_text(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    for marker in (
        "Reconstructable Singularity",
        "Supersedes the prior Reconstructive Singularity Site paper",
        "|C_A(I)| = 1",
        "k_A*",
        "injective on Γ_A",
        "minimum hitting-set formulation",
        "Empirical proof not claimed",
    ):
        require(marker in page, f"current paper missing marker: {marker}")

    require(index.count('href="papers/reconstructable-singularity.html"') == 1, "Papers index must contain exactly one current Reconstructable Singularity entry")
    require('href="reconstructive-singularity.html"' not in index, "old Reconstructive Singularity must not remain indexed as a paper")
    require('url=papers/reconstructable-singularity.html' in legacy, "legacy route must redirect to current paper")
    require("former Reconstructive Singularity paper has been superseded" in legacy, "legacy route must explain supersession")
    require("SUPERSEDED_BY_RECONSTRUCTABLE_SINGULARITY" in old_handoff, "old handoff not marked superseded")
    require("old URL remains only as a compatibility redirect" in handoff, "current handoff missing redirect boundary")

    claims = {item.get("id"): item for item in registry.get("claims", [])}
    claim = claims.get("RECONSTRUCTABLE-SINGULARITY-001")
    require(claim is not None, "public registry claim missing")
    require(claim.get("posture") == "RESEARCH_NOTE", "registry posture must remain RESEARCH_NOTE")
    require(claim.get("source_repo") == "StegVerse-Labs/admissibility-wiki", "canonical source repo mismatch")
    require("papers/reconstructable-singularity.html" in claim.get("public_pages", []), "current public route missing from registry")
    require("compatibility redirect only" in claim.get("status", ""), "registry does not mark legacy route as redirect only")

    print("RECONSTRUCTABLE SINGULARITY PUBLICATION: PASS - one current integrated paper, newer formalism present, legacy paper superseded by compatibility redirect, authority boundaries preserved")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
