#!/usr/bin/env python3
"""Validate CACS Claim and Claim Review fixtures without external packages."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CLAIM_FILES = (
    ROOT / "data/cacs-claim.fixture.json",
    ROOT / "data/cacs-overstated-claim.fixture.json",
)
REVIEW_FILES = (
    ROOT / "data/cacs-claim-review-supported.fixture.json",
    ROOT / "data/cacs-claim-review-overstated.fixture.json",
)

CLAIM_REQUIRED = {
    "claim_id", "claim_text", "claimant", "scope", "assumptions",
    "supporting_artifact_refs", "evidence_dimensions", "test_refs",
    "authority_refs", "falsification_conditions", "not_established",
    "correspondence_status", "review_refs", "timestamp", "hash",
}
REVIEW_REQUIRED = {
    "review_id", "claim_id", "reviewer", "review_scope", "artifact_refs",
    "dimension_findings", "correspondence_status", "required_qualifications",
    "disposition", "timestamp", "hash",
}
CLAIM_STATUSES = {
    "supported", "partially_supported", "unsupported", "overstated",
    "superseded", "withdrawn",
}
EVIDENCE_VALUES = {
    "ESTABLISHED", "PARTIAL", "NOT_ESTABLISHED", "NOT_APPLICABLE",
    "DISPUTED", "SUPERSEDED",
}
REVIEW_VALUES = {
    "CONFIRMED", "PARTIAL", "NOT_CONFIRMED", "DISPUTED", "NOT_REVIEWED",
}
DISPOSITIONS = {
    "publish", "publish_with_qualification", "quarantine", "withdraw", "supersede",
}
UNIVERSAL_TERMS = re.compile(
    r"\b(all|always|any|every|guarantee(?:s|d)?|universal(?:ly)?|never)\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise ValueError(message)


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"root must be an object: {path.relative_to(ROOT)}")
    return value


def require_exact_keys(value: dict[str, Any], required: set[str], optional: set[str], label: str) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing:
        fail(f"{label}: missing fields {sorted(missing)}")
    if extra:
        fail(f"{label}: unexpected fields {sorted(extra)}")


def require_nonempty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label}: expected non-empty string")


def require_object(value: Any, label: str) -> None:
    if not isinstance(value, dict) or not value:
        fail(f"{label}: expected non-empty object")


def require_string_list(value: Any, label: str, minimum: int = 0) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        fail(f"{label}: expected list with at least {minimum} item(s)")
    for index, item in enumerate(value):
        require_nonempty_string(item, f"{label}[{index}]")


def require_timestamp(value: Any, label: str) -> None:
    require_nonempty_string(value, label)
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{label}: expected RFC3339-compatible timestamp")


def validate_claim(claim: dict[str, Any], label: str) -> None:
    require_exact_keys(claim, CLAIM_REQUIRED, set(), label)
    require_nonempty_string(claim["claim_id"], f"{label}.claim_id")
    require_nonempty_string(claim["claim_text"], f"{label}.claim_text")
    require_object(claim["claimant"], f"{label}.claimant")
    require_object(claim["scope"], f"{label}.scope")
    require_string_list(claim["assumptions"], f"{label}.assumptions")
    require_string_list(claim["supporting_artifact_refs"], f"{label}.supporting_artifact_refs", 1)
    require_string_list(claim["test_refs"], f"{label}.test_refs")
    require_string_list(claim["authority_refs"], f"{label}.authority_refs")
    require_string_list(claim["falsification_conditions"], f"{label}.falsification_conditions", 1)
    require_string_list(claim["not_established"], f"{label}.not_established", 1)
    require_string_list(claim["review_refs"], f"{label}.review_refs")
    require_timestamp(claim["timestamp"], f"{label}.timestamp")
    require_nonempty_string(claim["hash"], f"{label}.hash")

    status = claim["correspondence_status"]
    if status not in CLAIM_STATUSES:
        fail(f"{label}.correspondence_status: invalid value {status!r}")

    dimensions = claim["evidence_dimensions"]
    require_object(dimensions, f"{label}.evidence_dimensions")
    invalid = {key: value for key, value in dimensions.items() if value not in EVIDENCE_VALUES}
    if invalid:
        fail(f"{label}.evidence_dimensions: invalid values {invalid}")
    if "scope_correspondent" not in dimensions:
        fail(f"{label}: scope_correspondent dimension is mandatory")

    scope_correspondent = dimensions["scope_correspondent"]
    universal = bool(UNIVERSAL_TERMS.search(claim["claim_text"]))
    missing_high_assurance = any(
        dimensions.get(name) not in {"ESTABLISHED", "NOT_APPLICABLE"}
        for name in ("reconstructable", "independently_reproduced", "production_observed")
    )

    if status == "supported" and scope_correspondent != "ESTABLISHED":
        fail(f"{label}: supported claims require scope_correspondent=ESTABLISHED")
    if status == "supported" and universal and missing_high_assurance:
        fail(f"{label}: universal claim cannot be supported while high-assurance dimensions remain unestablished")
    if status == "overstated":
        if scope_correspondent not in {"NOT_ESTABLISHED", "DISPUTED"}:
            fail(f"{label}: overstated claims require scope_correspondent NOT_ESTABLISHED or DISPUTED")
        if not universal:
            fail(f"{label}: overstated negative vector must contain an overbroad or universal assertion")
        if not claim["review_refs"]:
            fail(f"{label}: overstated claims require at least one review reference")


def validate_review(review: dict[str, Any], label: str) -> None:
    require_exact_keys(review, REVIEW_REQUIRED, {"supersedes_review_id", "authority_effect"}, label)
    require_nonempty_string(review["review_id"], f"{label}.review_id")
    require_nonempty_string(review["claim_id"], f"{label}.claim_id")
    require_object(review["reviewer"], f"{label}.reviewer")
    require_object(review["review_scope"], f"{label}.review_scope")
    require_string_list(review["artifact_refs"], f"{label}.artifact_refs", 1)
    require_string_list(review["required_qualifications"], f"{label}.required_qualifications")
    require_timestamp(review["timestamp"], f"{label}.timestamp")
    require_nonempty_string(review["hash"], f"{label}.hash")

    findings = review["dimension_findings"]
    require_object(findings, f"{label}.dimension_findings")
    invalid = {key: value for key, value in findings.items() if value not in REVIEW_VALUES}
    if invalid:
        fail(f"{label}.dimension_findings: invalid values {invalid}")

    status = review["correspondence_status"]
    if status not in CLAIM_STATUSES:
        fail(f"{label}.correspondence_status: invalid value {status!r}")
    if review["disposition"] not in DISPOSITIONS:
        fail(f"{label}.disposition: invalid value {review['disposition']!r}")
    if review.get("authority_effect") != "NONE":
        fail(f"{label}: authority_effect must be NONE")
    if status == "overstated" and review["disposition"] != "quarantine":
        fail(f"{label}: overstated review must quarantine the claim")
    if status == "supported" and review["disposition"] not in {"publish", "publish_with_qualification"}:
        fail(f"{label}: supported review must permit bounded publication")


def validate_links(claims: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> None:
    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    review_by_id = {review["review_id"]: review for review in reviews}
    if len(claim_by_id) != len(claims):
        fail("duplicate claim_id")
    if len(review_by_id) != len(reviews):
        fail("duplicate review_id")

    for review in reviews:
        claim = claim_by_id.get(review["claim_id"])
        if claim is None:
            fail(f"review {review['review_id']} references unknown claim {review['claim_id']}")
        if review["correspondence_status"] != claim["correspondence_status"]:
            fail(f"review {review['review_id']} status does not match claim status")
        expected_ref = f"review:{review['review_id']}"
        if claim["review_refs"] and expected_ref not in claim["review_refs"]:
            fail(f"claim {claim['claim_id']} does not reference review {review['review_id']}")

    overstated = claim_by_id.get("cacs-claim-overstated-001")
    supported = claim_by_id.get("cacs-claim-stegverse-refusal-001")
    if overstated is None or overstated["correspondence_status"] != "overstated":
        fail("required overstated negative vector not found")
    if supported is None or supported["correspondence_status"] != "supported":
        fail("required bounded supported vector not found")


def main() -> int:
    try:
        claims = []
        for path in CLAIM_FILES:
            claim = load(path)
            validate_claim(claim, str(path.relative_to(ROOT)))
            claims.append(claim)

        reviews = []
        for path in REVIEW_FILES:
            review = load(path)
            validate_review(review, str(path.relative_to(ROOT)))
            reviews.append(review)

        validate_links(claims, reviews)
    except ValueError as exc:
        print(f"CACS_VALIDATION_FAIL: {exc}")
        return 1

    print(
        "CACS_VALIDATION_PASS: "
        f"{len(claims)} claims and {len(reviews)} reviews; "
        "bounded support and overstated quarantine vectors verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
