#!/usr/bin/env python3
"""Fail-closed validation for the Conectrr security-above-federal-baseline overlay."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "data" / "conectrr-security-overlay.json"
CONTRACT = ROOT / "docs" / "CONECTRR_SECURITY_EXCEEDS_FEDERAL_BASELINE.md"

REQUIRED_ANCHORS = {"NIST-SP-800-53", "NIST-SP-800-207", "FIPS-140", "CISA-SECURE-BY-DESIGN"}
REQUIRED_CONTROLS = {
    "no_inferred_authority",
    "immutable_source_bytes",
    "source_digest_required",
    "semantic_digest_required",
    "algorithm_agility_required",
    "fail_closed_admission",
    "zero_trust_per_operation",
    "independent_decision_record",
    "separation_of_duties",
    "tamper_evident_receipts",
    "continuous_verification",
    "supply_chain_integrity",
    "data_minimization",
    "recovery_without_authority_escalation",
    "evidence_level_separation",
}
REQUIRED_GATE_FIELDS = {
    "source_bytes_preserved",
    "source_digest_verified",
    "semantic_digest_verified",
    "provenance_verified",
    "references_resolved",
    "policy_current",
    "algorithm_policy_passed",
    "authority_effect",
    "independent_decision_distinct",
    "reconstruction_passed",
    "publication_gate_passed",
    "custody_gate_passed",
}
REQUIRED_NONPASS_STATES = {"BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED"}


def main() -> int:
    errors: list[str] = []
    if not OVERLAY.exists():
        errors.append("missing data/conectrr-security-overlay.json")
    if not CONTRACT.exists():
        errors.append("missing docs/CONECTRR_SECURITY_EXCEEDS_FEDERAL_BASELINE.md")
    if errors:
        return fail(errors)

    payload = json.loads(OVERLAY.read_text(encoding="utf-8"))
    if payload.get("policy") != "applicable_federal_security_requirements_are_minimum_floor":
        errors.append("federal baseline is not declared as minimum floor")

    anchors = {item.get("id") for item in payload.get("baseline_anchors", [])}
    missing_anchors = sorted(REQUIRED_ANCHORS - anchors)
    if missing_anchors:
        errors.append(f"missing baseline anchors: {missing_anchors}")
    for item in payload.get("baseline_anchors", []):
        if item.get("version_policy") != "current_applicable":
            errors.append(f"baseline anchor not current-applicable: {item.get('id')}")

    controls = payload.get("required_overlay_controls", {})
    for control in sorted(REQUIRED_CONTROLS):
        if controls.get(control) is not True:
            errors.append(f"overlay control must be true: {control}")

    gate_fields = set(payload.get("production_gate_required_fields", []))
    missing_gate_fields = sorted(REQUIRED_GATE_FIELDS - gate_fields)
    if missing_gate_fields:
        errors.append(f"missing production gate fields: {missing_gate_fields}")

    states = set(payload.get("allowed_nonpass_states", []))
    if not REQUIRED_NONPASS_STATES.issubset(states):
        errors.append("fail-closed nonpass states incomplete")
    if payload.get("authority_effect") != "none":
        errors.append("authority_effect must be none")

    contract = CONTRACT.read_text(encoding="utf-8")
    for phrase in (
        "minimum acceptance floor",
        "No inferred authority",
        "Immutable source custody",
        "Fail-closed admission",
        "Dual integrity evidence",
        "Separation of duties",
        "Compliance evidence is not execution authority",
    ):
        if phrase not in contract:
            errors.append(f"contract missing phrase: {phrase}")

    if errors:
        return fail(errors)
    print("CONECTRR_SECURITY_OVERLAY_CHECK=PASS")
    print("federal_requirements=minimum_floor")
    print("stegverse_overlay=mandatory")
    print("admission=fail_closed")
    print("authority_effect=none")
    return 0


def fail(errors: list[str]) -> int:
    print("CONECTRR_SECURITY_OVERLAY_CHECK=FAIL")
    for error in errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
