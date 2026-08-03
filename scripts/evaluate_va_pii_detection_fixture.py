#!/usr/bin/env python3
"""Evaluate the synthetic VA PII detection fixture.

This is a deterministic reference evaluator for validation only. Passing it does
not establish production detector readiness or authorize private document upload.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

FIXTURE = Path("data/va-claim-assistant/fixtures/pii-detection-evaluation.json")
RECEIPT = Path("data/va-claim-assistant/pii-detection-evaluation-receipt.json")

PATTERNS = {
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "PHONE": re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),
    "DATE_OF_BIRTH": re.compile(r"(?:date of birth|dob)\s*[: ]\s*\d{4}-\d{2}-\d{2}", re.I),
    "VA_FILE_NUMBER": re.compile(r"(?:VA\s*File|claim number)\s*[: ]\s*\d{7,9}\b", re.I),
    "STREET_ADDRESS": re.compile(r"\b\d{1,5}\s+[A-Za-z]+(?:\s+[A-Za-z]+)*\s+(?:Avenue|Street|Road|Drive|Lane|Boulevard)\b", re.I),
    "PERSON_NAME": re.compile(r"(?:Synthetic Veteran|Veteran|Claimant)\s*:\s*[A-Z][a-z]+\s+[A-Z][a-z]+"),
}
AMBIGUOUS_NUMBER = re.compile(r"\b\d{9}\b")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def detect(text: str) -> tuple[set[str], str]:
    classes = {name for name, pattern in PATTERNS.items() if pattern.search(text)}
    if classes:
        return classes, "REDACTION_REQUIRED"
    if AMBIGUOUS_NUMBER.search(text):
        return set(), "REVIEW_REQUIRED"
    return set(), "CLEAN"


def main() -> int:
    raw = FIXTURE.read_bytes()
    fixture = json.loads(raw)
    errors: list[str] = []
    results = []
    required_hits = 0
    required_total = 0
    clean_total = 0
    clean_false_positives = 0
    unresolved = 0

    if fixture.get("synthetic_only") is not True or fixture.get("contains_real_veteran_data") is not False:
        errors.append("fixture_must_be_synthetic_only")

    for case in fixture.get("cases", []):
        expected = set(case.get("expected_classes", []))
        detected, state = detect(case.get("text", ""))
        required_hits += len(expected & detected)
        required_total += len(expected)
        if case.get("expected_state") == "CLEAN":
            clean_total += 1
            if detected or state != "CLEAN":
                clean_false_positives += 1
        if state == "REVIEW_REQUIRED":
            unresolved += 1
        if detected != expected:
            errors.append(f"{case['case_id']}:classes:{sorted(detected)}!={sorted(expected)}")
        if state != case.get("expected_state"):
            errors.append(f"{case['case_id']}:state:{state}!={case.get('expected_state')}")
        results.append({
            "case_id": case["case_id"],
            "detected_classes": sorted(detected),
            "state": state,
            "model_release_allowed": state == "CLEAN",
        })

    recall = required_hits / required_total if required_total else 1.0
    false_positive_rate = clean_false_positives / clean_total if clean_total else 0.0
    acceptance = fixture["acceptance"]
    if recall < acceptance["required_class_recall"]:
        errors.append("required_class_recall_below_threshold")
    if false_positive_rate > acceptance["maximum_clean_case_false_positive_rate"]:
        errors.append("clean_case_false_positive_rate_above_threshold")
    if acceptance["uncertain_cases_must_route_to_review"] and unresolved < 1:
        errors.append("uncertain_case_not_routed_to_review")

    receipt = {
        "schema_version": "1.0.0",
        "fixture_id": fixture["fixture_id"],
        "state": "PASS" if not errors else "FAIL",
        "reference_evaluator_only": True,
        "production_detector_ready": False,
        "private_document_upload_enabled": False,
        "required_class_recall": recall,
        "clean_case_false_positive_rate": false_positive_rate,
        "review_required_count": unresolved,
        "case_count": len(results),
        "results": results,
        "errors": errors,
        "fixture_sha256": digest_bytes(raw),
        "authority_effect": False,
        "activation_effect": False,
    }
    canonical = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    RECEIPT.write_text(canonical)
    print(canonical, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
