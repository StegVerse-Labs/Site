#!/usr/bin/env python3
"""Validate partially supported and disputed CACS Claim, Review, and projection vectors."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from check_cacs_claims import validate_claim, validate_review

ROOT = Path(__file__).resolve().parents[1]
PARTIAL_CLAIM = ROOT / "data/cacs-partially-supported-claim.fixture.json"
DISPUTED_CLAIM = ROOT / "data/cacs-disputed-claim.fixture.json"
PARTIAL_REVIEW = ROOT / "data/cacs-claim-review-partially-supported.fixture.json"
DISPUTED_REVIEW = ROOT / "data/cacs-claim-review-disputed.fixture.json"
PARTIAL_PROJECTION = ROOT / "data/cacs-public-projection-partially-supported.fixture.json"
DISPUTED_PROJECTION = ROOT / "data/cacs-public-projection-disputed.fixture.json"


def fail(message: str) -> None:
    raise ValueError(message)


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"root must be an object: {path.relative_to(ROOT)}")
    return value


def joined(items: list[str]) -> str:
    return " ".join(items).lower()


def contains_affirmative_claim(text: str, terms: tuple[str, ...], negated_phrases: tuple[str, ...]) -> bool:
    """Detect affirmative claims without rejecting explicit denial or prohibition language."""
    scrubbed = " ".join(text.lower().split())
    for phrase in negated_phrases:
        scrubbed = scrubbed.replace(phrase, "")
    return any(term in scrubbed for term in terms)


def asserts_full_support(text: str) -> bool:
    return contains_affirmative_claim(
        text,
        ("fully supported", "universally supported"),
        (
            "not fully supported",
            "never be rendered as fully supported",
            "must not be rendered as fully supported",
            "may not be rendered as fully supported",
            "not universally supported",
            "never be rendered as universally supported",
            "must not be rendered as universally supported",
            "may not be rendered as universally supported",
        ),
    )


def mislabels_disputed_history(text: str) -> bool:
    return contains_affirmative_claim(
        text,
        ("confirmed linkage", "verified linkage", "fully supported", "current assurance"),
        (
            "not confirmed",
            "cannot be rendered as supported, confirmed, verified, or current assurance",
            "not current assurance",
            "no current assurance",
            "not fully supported",
        ),
    )


def validate_pair(claim: dict[str, Any], review: dict[str, Any], kind: str) -> None:
    validate_claim(claim, f"{kind} claim")
    validate_review(review, f"{kind} review")
    if review["claim_id"] != claim["claim_id"]:
        fail(f"{kind}: review does not reference Claim")
    if f"review:{review['review_id']}" not in claim["review_refs"]:
        fail(f"{kind}: Claim does not reference Review")
    if claim["correspondence_status"] != "partially_supported":
        fail(f"{kind}: Claim must be partially_supported")
    if review["correspondence_status"] != "partially_supported":
        fail(f"{kind}: Review must be partially_supported")
    if review["disposition"] != "publish_with_qualification":
        fail(f"{kind}: Review must require qualified publication")
    if review.get("authority_effect") != "NONE":
        fail(f"{kind}: authority_effect must be NONE")


def validate_partial(claim: dict[str, Any], review: dict[str, Any], projection: dict[str, Any]) -> None:
    validate_pair(claim, review, "partial")
    dimensions = claim["evidence_dimensions"]
    if dimensions.get("scope_correspondent") != "ESTABLISHED":
        fail("partial: current bounded publication requires established scope correspondence")
    if "PARTIAL" not in dimensions.values():
        fail("partial: at least one evidence dimension must be PARTIAL")
    qualification = joined(review["required_qualifications"])
    if "partially supported" not in qualification and "partial" not in qualification:
        fail("partial: Review must visibly require partial-support labeling")
    active = projection["active_claim"]
    if active.get("claim_id") != claim["claim_id"]:
        fail("partial projection: wrong active Claim")
    if active.get("correspondence_status") != "partially_supported":
        fail("partial projection: must preserve partially_supported status")
    visible = joined(active.get("qualification", []) + projection.get("qualification_rules", []))
    if "partially supported" not in visible and "partial" not in visible:
        fail("partial projection: visible partial-support qualification missing")
    if asserts_full_support(visible):
        fail("partial projection: must not assert full support")


def validate_disputed(claim: dict[str, Any], review: dict[str, Any], projection: dict[str, Any]) -> None:
    validate_pair(claim, review, "disputed")
    dimensions = claim["evidence_dimensions"]
    findings = review["dimension_findings"]
    if "DISPUTED" not in dimensions.values() or "DISPUTED" not in findings.values():
        fail("disputed: Claim and Review must preserve disputed evidence")
    if dimensions.get("scope_correspondent") != "DISPUTED":
        fail("disputed: scope correspondence must remain DISPUTED")
    history = [item for item in projection["historical_claims"] if item.get("claim_id") == claim["claim_id"]]
    if len(history) != 1 or history[0].get("public_label") != "DISPUTED_HISTORY":
        fail("disputed projection: disputed Claim must appear exactly once as DISPUTED_HISTORY")
    visible = (history[0].get("reason", "") + " " + joined(projection.get("qualification_rules", []))).lower()
    if "disputed" not in visible:
        fail("disputed projection: dispute visibility missing")
    if mislabels_disputed_history(history[0].get("reason", "")):
        fail("disputed projection: dispute may not be mislabeled as confirmed or current")
    if projection["active_claim"].get("claim_id") == claim["claim_id"]:
        fail("disputed projection: scope-disputed Claim cannot be selected as current")


def main() -> int:
    try:
        partial_claim = load(PARTIAL_CLAIM)
        partial_review = load(PARTIAL_REVIEW)
        disputed_claim = load(DISPUTED_CLAIM)
        disputed_review = load(DISPUTED_REVIEW)
        partial_projection = load(PARTIAL_PROJECTION)
        disputed_projection = load(DISPUTED_PROJECTION)
        validate_partial(partial_claim, partial_review, partial_projection)
        validate_disputed(disputed_claim, disputed_review, disputed_projection)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"CACS_DISPUTE_PARTIAL_FAIL: {exc}")
        return 1
    print("CACS_DISPUTE_PARTIAL_PASS: partial qualification and dispute visibility verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
