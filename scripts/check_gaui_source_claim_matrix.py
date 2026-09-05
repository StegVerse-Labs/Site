#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "research/gaui-bigame-source-claim-matrix.json"
REQUIRED = {
    "claim_id",
    "architecture",
    "claim_text_or_paraphrase",
    "source_uri",
    "source_version",
    "source_location",
    "claim_class",
    "stegverse_analogue",
    "semantic_correspondence",
    "semantic_conflict",
    "unresolved_evidence",
}


def fail(reason: str) -> None:
    raise SystemExit(f"GAUI_SOURCE_CLAIM_MATRIX=FAIL\nreason={reason}")


def main() -> int:
    if not MATRIX.is_file():
        fail("missing_matrix")
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    if data.get("public_projection_authorized") is not False:
        fail("public_projection_must_remain_false")
    if data.get("integration_claim_authorized") is not False:
        fail("integration_claim_must_remain_false")
    rules = data.get("source_rules", {})
    if rules.get("formal_publication_precedence") is not True:
        fail("formal_publication_precedence_required")
    if rules.get("social_discussion_is_specification_authority") is not False:
        fail("social_discussion_must_not_be_spec_authority")
    if rules.get("unknown_source_details_must_remain_unresolved") is not True:
        fail("unknowns_must_remain_unresolved")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        fail("claims_required")

    ids: set[str] = set()
    has_formal = False
    has_discussion = False
    has_stegverse = False
    for claim in claims:
        if not isinstance(claim, dict):
            fail("claim_must_be_object")
        missing = sorted(REQUIRED - set(claim))
        if missing:
            fail("missing_fields:" + ",".join(missing))
        if any(not isinstance(claim[k], str) or not claim[k].strip() for k in REQUIRED):
            fail("required_fields_must_be_nonempty_strings")
        cid = claim["claim_id"]
        if cid in ids:
            fail("duplicate_claim_id:" + cid)
        ids.add(cid)
        cclass = claim["claim_class"]
        if cclass == "formal_publication_metadata":
            has_formal = True
        if cclass == "public_discussion_not_formal_specification":
            has_discussion = True
            if "UNRESOLVED" not in claim["source_uri"]:
                fail("discussion_without_canonical_url_must_remain_unresolved")
            if "formal" not in claim["unresolved_evidence"].lower():
                fail("discussion_claim_must_require_formal_source")
        if claim["architecture"] == "StegVerse":
            has_stegverse = True

    if not has_formal:
        fail("at_least_one_formal_source_claim_required")
    if not has_discussion:
        fail("discussion_source_boundary_not_tested")
    if not has_stegverse:
        fail("stegverse_reference_semantic_required")

    text = MATRIX.read_text(encoding="utf-8").lower()
    prohibited_assertions = [
        "implemented interoperability",
        "formal partnership",
        "mutual endorsement",
        "bigmae owns the governed execution boundary",
    ]
    for phrase in prohibited_assertions:
        if phrase in text:
            fail("unsupported_assertion:" + phrase)

    print("GAUI_SOURCE_CLAIM_MATRIX=PASS")
    print(f"claims={len(claims)}")
    print("public_projection_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
