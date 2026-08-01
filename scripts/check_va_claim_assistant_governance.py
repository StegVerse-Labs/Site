#!/usr/bin/env python3
"""Validate VA Claim Assistant source and answer governance contracts.

This validator is intentionally dependency-free so it can run in GitHub Actions
without installing third-party packages. It enforces the semantic invariants that
matter for activation and exercises one passing and two failing fixtures.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "va-claim-assistant"

AUTHORITY_RANK = {
    "CONTROLLING": 1,
    "OFFICIAL_OPERATIONAL": 2,
    "PROFESSIONAL_SUPPORT": 3,
    "EXPERIENTIAL": 4,
}
ROUTES = {
    "claim_type", "evidence_requirement", "service_connection",
    "rating_criteria", "effective_date", "appeal_or_supplemental_claim",
    "cp_examination", "document_organization", "lay_statement",
    "private_record_collection", "procedural_filing",
    "representation_referral", "urgent_safety",
}
CAPABILITIES = {
    "BOUNDED_PROCEDURAL_ASSISTANT", "SOURCE_GROUNDED_ASSISTANT",
    "DOCUMENT_AWARE_ASSISTANT", "GOVERNED_CLAIM_SESSION",
}


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level value must be an object")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(registry.get("registry_id") == "va-claim-assistant-source-registry",
            "registry_id is not canonical", errors)
    require(registry.get("activation_effect") is False,
            "registry must not activate the assistant", errors)
    require(registry.get("authority_effect") is False,
            "registry must not grant authority", errors)

    policy = registry.get("policy", {})
    required_true = {
        "higher_authority_overrides_lower_authority",
        "non_federal_sources_require_admission_review",
        "experiential_sources_cannot_establish_law_or_medical_nexus",
        "stale_or_superseded_controlling_sources_fail_closed",
        "all_material_answers_require_source_provenance",
        "missing_local_secrets_require_tvc_resolution_before_blocker",
    }
    for key in required_true:
        require(policy.get(key) is True, f"policy {key} must be true", errors)

    classes = registry.get("authority_classes", [])
    seen_classes: set[str] = set()
    seen_ranks: set[int] = set()
    for item in classes:
        class_id = item.get("id")
        rank = item.get("rank")
        require(class_id in AUTHORITY_RANK, f"unknown authority class: {class_id}", errors)
        if class_id in AUTHORITY_RANK:
            require(rank == AUTHORITY_RANK[class_id],
                    f"authority rank mismatch for {class_id}", errors)
        require(class_id not in seen_classes, f"duplicate authority class: {class_id}", errors)
        require(rank not in seen_ranks, f"duplicate authority rank: {rank}", errors)
        seen_classes.add(class_id)
        seen_ranks.add(rank)
    require(seen_classes == set(AUTHORITY_RANK), "authority classes are incomplete", errors)

    seen_sources: set[str] = set()
    for source in registry.get("sources", []):
        source_id = source.get("source_id")
        require(isinstance(source_id, str) and bool(source_id), "source_id missing", errors)
        require(source_id not in seen_sources, f"duplicate source_id: {source_id}", errors)
        seen_sources.add(source_id)
        authority = source.get("authority_class")
        require(authority in AUTHORITY_RANK, f"invalid source authority: {authority}", errors)
        require(source.get("admitted") is True, f"source not admitted: {source_id}", errors)
        require(str(source.get("url", "")).startswith("https://"),
                f"source URL must use HTTPS: {source_id}", errors)
        if authority == "CONTROLLING":
            require(source.get("freshness_check_required") is True,
                    f"controlling source must require freshness: {source_id}", errors)
        if source_id == "BVA-DECISIONS":
            warning = str(source.get("required_warning", "")).lower()
            require("nonprecedential" in warning,
                    "BVA source must carry nonprecedential warning", errors)
    return errors


def validate_answer(answer: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(answer.get("route") in ROUTES, "answer route is invalid", errors)
    require(answer.get("capability_state") in CAPABILITIES,
            "answer capability_state is invalid", errors)

    flags = answer.get("authority_flags", {})
    for key in ("adjudication", "representation", "medical_opinion", "rating", "execution", "publication"):
        require(flags.get(key) is False, f"authority flag {key} must be false", errors)

    admitted = {source.get("source_id"): source for source in registry.get("sources", [])}
    proposition_ids: set[str] = set()
    for proposition in answer.get("propositions", []):
        proposition_id = proposition.get("proposition_id")
        require(isinstance(proposition_id, str) and bool(proposition_id),
                "proposition_id missing", errors)
        require(proposition_id not in proposition_ids,
                f"duplicate proposition_id: {proposition_id}", errors)
        proposition_ids.add(proposition_id)
        kind = proposition.get("kind")
        support = proposition.get("support", [])
        if kind in {"SOURCE_FACT", "PROCEDURAL_GUIDANCE", "INFERENCE"}:
            require(bool(support), f"{kind} proposition lacks support: {proposition_id}", errors)
        for citation in support:
            source_id = citation.get("source_id")
            authority = citation.get("authority_class")
            if authority == "USER_RECORD":
                require(bool(citation.get("document_hash")),
                        f"user-record citation lacks document hash: {proposition_id}", errors)
                require(bool(citation.get("page_anchor")),
                        f"user-record citation lacks page anchor: {proposition_id}", errors)
                continue
            source = admitted.get(source_id)
            require(source is not None, f"citation uses unadmitted source: {source_id}", errors)
            if source is not None:
                require(authority == source.get("authority_class"),
                        f"citation authority escalation for {source_id}", errors)

    for contradiction in answer.get("contradictions", []):
        for proposition_id in contradiction.get("related_proposition_ids", []):
            require(proposition_id in proposition_ids,
                    f"contradiction references unknown proposition: {proposition_id}", errors)

    receipt_hash = answer.get("receipt_hash", "")
    require(isinstance(receipt_hash, str) and len(receipt_hash) == 64 and
            all(char in "0123456789abcdef" for char in receipt_hash),
            "receipt_hash must be 64 lowercase hexadecimal characters", errors)
    return errors


def main() -> int:
    registry = load(DATA / "source-registry.json")
    registry_errors = validate_registry(registry)
    if registry_errors:
        raise SystemExit("Registry validation failed:\n- " + "\n- ".join(registry_errors))

    valid = load(DATA / "fixtures" / "valid-answer-record.json")
    valid_errors = validate_answer(valid, registry)
    if valid_errors:
        raise SystemExit("Valid fixture failed:\n- " + "\n- ".join(valid_errors))

    expected_failures = {
        "invalid-authority-escalation.json": {"authority flag adjudication", "authority flag rating"},
        "invalid-unsupported-proposition.json": {"SOURCE_FACT proposition lacks support"},
    }
    for filename, expected_fragments in expected_failures.items():
        errors = validate_answer(load(DATA / "fixtures" / filename), registry)
        if not errors:
            raise SystemExit(f"Negative fixture unexpectedly passed: {filename}")
        combined = "\n".join(errors)
        for fragment in expected_fragments:
            if fragment not in combined:
                raise SystemExit(f"Negative fixture {filename} missed expected failure: {fragment}")

    print("VA Claim Assistant governance validation: PASS")
    print("- source registry semantic checks: PASS")
    print("- valid answer fixture: PASS")
    print("- authority escalation fixture: REJECTED as expected")
    print("- unsupported proposition fixture: REJECTED as expected")
    print("- activation effect: NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
