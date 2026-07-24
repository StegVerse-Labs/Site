#!/usr/bin/env python3
"""Validate CACS Claim and Claim Review fixtures without external packages."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_TIME = datetime(2026, 7, 24, 23, 59, 59, tzinfo=timezone.utc)

CLAIM_FILES = (
    ROOT / "data/cacs-claim.fixture.json",
    ROOT / "data/cacs-overstated-claim.fixture.json",
    ROOT / "data/cacs-superseding-claim.fixture.json",
    ROOT / "data/cacs-withdrawn-claim.fixture.json",
    ROOT / "data/cacs-stale-evidence-claim.fixture.json",
)
REVIEW_FILES = (
    ROOT / "data/cacs-claim-review-supported.fixture.json",
    ROOT / "data/cacs-claim-review-overstated.fixture.json",
    ROOT / "data/cacs-claim-review-superseding.fixture.json",
    ROOT / "data/cacs-claim-review-withdrawn.fixture.json",
    ROOT / "data/cacs-claim-review-stale-evidence.fixture.json",
)

CLAIM_REQUIRED = {
    "claim_id", "claim_text", "claimant", "scope", "assumptions",
    "supporting_artifact_refs", "evidence_dimensions", "test_refs",
    "authority_refs", "falsification_conditions", "not_established",
    "correspondence_status", "review_refs", "timestamp", "hash",
}
CLAIM_OPTIONAL = {
    "lifecycle_state", "supersedes_claim_id", "evidence_valid_through",
    "withdrawal_reason",
}
REVIEW_REQUIRED = {
    "review_id", "claim_id", "reviewer", "review_scope", "artifact_refs",
    "dimension_findings", "correspondence_status", "required_qualifications",
    "disposition", "timestamp", "hash",
}
REVIEW_OPTIONAL = {"supersedes_review_id", "authority_effect"}
CLAIM_STATUSES = {
    "supported", "partially_supported", "unsupported", "overstated",
    "superseded", "withdrawn",
}
LIFECYCLE_STATES = {"active", "superseded", "withdrawn", "stale"}
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


def parse_timestamp(value: Any, label: str) -> datetime:
    require_nonempty_string(value, label)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{label}: expected RFC3339-compatible timestamp")
    if parsed.tzinfo is None:
        fail(f"{label}: timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def validate_claim(claim: dict[str, Any], label: str) -> None:
    require_exact_keys(claim, CLAIM_REQUIRED, CLAIM_OPTIONAL, label)
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
    parse_timestamp(claim["timestamp"], f"{label}.timestamp")
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

    lifecycle = claim.get("lifecycle_state", "active")
    if lifecycle not in LIFECYCLE_STATES:
        fail(f"{label}.lifecycle_state: invalid value {lifecycle!r}")
    if lifecycle == "withdrawn":
        if status != "withdrawn":
            fail(f"{label}: withdrawn lifecycle requires withdrawn correspondence status")
        require_nonempty_string(claim.get("withdrawal_reason"), f"{label}.withdrawal_reason")
    elif claim.get("withdrawal_reason") is not None:
        fail(f"{label}: withdrawal_reason is only valid for withdrawn claims")

    supersedes = claim.get("supersedes_claim_id")
    if supersedes is not None:
        require_nonempty_string(supersedes, f"{label}.supersedes_claim_id")
        if supersedes == claim["claim_id"]:
            fail(f"{label}: claim cannot supersede itself")

    valid_through_raw = claim.get("evidence_valid_through")
    if valid_through_raw is not None:
        valid_through = parse_timestamp(valid_through_raw, f"{label}.evidence_valid_through")
        is_expired = valid_through < VALIDATION_TIME
        if lifecycle == "stale" and not is_expired:
            fail(f"{label}: stale lifecycle requires expired evidence_valid_through")
        if is_expired and lifecycle != "stale":
            fail(f"{label}: expired evidence requires lifecycle_state=stale")
    elif lifecycle == "stale":
        fail(f"{label}: stale lifecycle requires evidence_valid_through")


def validate_review(review: dict[str, Any], label: str) -> None:
    require_exact_keys(review, REVIEW_REQUIRED, REVIEW_OPTIONAL, label)
    require_nonempty_string(review["review_id"], f"{label}.review_id")
    require_nonempty_string(review["claim_id"], f"{label}.claim_id")
    require_object(review["reviewer"], f"{label}.reviewer")
    require_object(review["review_scope"], f"{label}.review_scope")
    require_string_list(review["artifact_refs"], f"{label}.artifact_refs", 1)
    require_string_list(review["required_qualifications"], f"{label}.required_qualifications")
    parse_timestamp(review["timestamp"], f"{label}.timestamp")
    require_nonempty_string(review["hash"], f"{label}.hash")

    findings = review["dimension_findings"]
    require_object(findings, f"{label}.dimension_findings")
    invalid = {key: value for key, value in findings.items() if value not in REVIEW_VALUES}
    if invalid:
        fail(f"{label}.dimension_findings: invalid values {invalid}")

    status = review["correspondence_status"]
    disposition = review["disposition"]
    if status not in CLAIM_STATUSES:
        fail(f"{label}.correspondence_status: invalid value {status!r}")
    if disposition not in DISPOSITIONS:
        fail(f"{label}.disposition: invalid value {disposition!r}")
    if review.get("authority_effect") != "NONE":
        fail(f"{label}: authority_effect must be NONE")
    if status == "overstated" and disposition != "quarantine":
        fail(f"{label}: overstated review must quarantine the claim")
    if status == "withdrawn" and disposition != "withdraw":
        fail(f"{label}: withdrawn review must withdraw the claim")
    if status == "partially_supported" and disposition != "publish_with_qualification":
        fail(f"{label}: partially supported review requires qualified publication")
    if status == "supported" and disposition not in {"publish", "publish_with_qualification", "supersede"}:
        fail(f"{label}: supported review must permit bounded publication or supersession")
    if disposition in {"publish_with_qualification", "withdraw", "supersede"} and not review["required_qualifications"]:
        fail(f"{label}: disposition {disposition} requires explicit qualifications")


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
        if expected_ref not in claim["review_refs"]:
            fail(f"claim {claim['claim_id']} does not reference review {review['review_id']}")

    superseded_targets: set[str] = set()
    for claim in claims:
        parent_id = claim.get("supersedes_claim_id")
        if not parent_id:
            continue
        if parent_id not in claim_by_id:
            fail(f"claim {claim['claim_id']} supersedes unknown claim {parent_id}")
        if parent_id in superseded_targets:
            fail(f"claim {parent_id} has multiple active supersessors")
        superseded_targets.add(parent_id)
        if claim.get("lifecycle_state", "active") != "active":
            fail(f"superseding claim {claim['claim_id']} must be active")
        if claim["timestamp"] <= claim_by_id[parent_id]["timestamp"]:
            fail(f"superseding claim {claim['claim_id']} must be newer than {parent_id}")

    for review in reviews:
        parent_review_id = review.get("supersedes_review_id")
        if parent_review_id is None:
            continue
        if parent_review_id not in review_by_id:
            fail(f"review {review['review_id']} supersedes unknown review {parent_review_id}")
        if review["timestamp"] <= review_by_id[parent_review_id]["timestamp"]:
            fail(f"superseding review {review['review_id']} must be newer than {parent_review_id}")
        if review["disposition"] != "supersede":
            fail(f"review {review['review_id']} with supersedes_review_id must use supersede disposition")

    for claim in claims:
        lifecycle = claim.get("lifecycle_state", "active")
        matching_reviews = [review for review in reviews if review["claim_id"] == claim["claim_id"]]
        dispositions = {review["disposition"] for review in matching_reviews}
        if lifecycle == "withdrawn" and "withdraw" not in dispositions:
            fail(f"withdrawn claim {claim['claim_id']} lacks withdrawal review")
        if lifecycle == "stale":
            if "publish_with_qualification" not in dispositions:
                fail(f"stale claim {claim['claim_id']} lacks qualified-publication review")
            qualifications = " ".join(
                item for review in matching_reviews for item in review["required_qualifications"]
            ).lower()
            if "historical" not in qualifications and "stale" not in qualifications and "expired" not in qualifications:
                fail(f"stale claim {claim['claim_id']} must be visibly qualified as historical, stale, or expired")

    required_vectors = {
        "cacs-claim-stegverse-refusal-001": "supported",
        "cacs-claim-overstated-001": "overstated",
        "cacs-claim-stegverse-refusal-002": "supported",
        "cacs-claim-withdrawn-001": "withdrawn",
        "cacs-claim-stale-evidence-001": "partially_supported",
    }
    for claim_id, status in required_vectors.items():
        claim = claim_by_id.get(claim_id)
        if claim is None or claim["correspondence_status"] != status:
            fail(f"required lifecycle vector {claim_id} with status {status} not found")


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
        "bounded support, overstated quarantine, supersession, withdrawal, and stale-evidence vectors verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
