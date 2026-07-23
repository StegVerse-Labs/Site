#!/usr/bin/env python3
"""Validate the machine-readable Ecosystem Chat governed aspect registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ecosystem-chat-governed-aspects.registry.json"
MODEL = ROOT / "docs" / "ECOSYSTEM_CHAT_GOVERNED_ASPECT_MODEL.md"

REQUIRED_ASPECTS = {
    "identity_participation",
    "source_provenance",
    "ownership_control",
    "consent_permission",
    "privacy_sensitivity",
    "contribution",
    "causal_influence",
    "attribution",
    "authorship",
    "originality_novelty",
    "scarcity_substitutability",
    "labor_effort",
    "compute_infrastructure",
    "outcome_utility",
    "realized_value",
    "cost_externalities",
    "risk_harm",
    "admissibility",
    "authority_delegation",
    "standing_capability",
    "reward_incentive",
    "distribution_allocation",
    "settlement",
    "jurisdiction_legal",
    "temporal_state_decay",
    "dispute_competing_claims",
    "fraud_gaming_manipulation",
    "collective_network_contribution",
    "derivation_transformation",
    "disclosure_projection",
    "custody_reconstruction",
    "confidence_uncertainty",
    "recovery_correction",
    "public_claim_communication",
}

REQUIRED_INVARIANTS = {
    "no_aspect_silently_grants_another",
    "missing_evidence_resolves_to_unresolved",
    "authoritative_changes_are_governed_events",
    "browser_state_grants_no_authority_custody_payment_or_settlement",
    "competing_determinations_remain_visible",
    "sensitivity_is_not_an_automatic_value_multiplier",
    "success_does_not_erase_invalid_consent_or_externalized_harm",
    "downstream_projection_requires_purpose_permission_redaction_and_minimum_disclosure",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def main() -> int:
    require(REGISTRY.exists(), "governed aspect registry missing")
    require(MODEL.exists(), "governed aspect model missing")

    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(payload.get("authority_effect") == "NONE", "registry authority_effect must be NONE")
    require(payload.get("default_resolution") == "UNRESOLVED", "missing evidence must resolve to UNRESOLVED")

    aspects = payload.get("aspects")
    require(isinstance(aspects, list) and aspects, "aspects must be a non-empty list")
    ids: set[str] = set()
    families: set[str] = set()

    for aspect in aspects:
        require(isinstance(aspect, dict), "each aspect must be an object")
        aspect_id = aspect.get("id")
        require(isinstance(aspect_id, str) and aspect_id, "aspect id required")
        require(aspect_id not in ids, f"duplicate aspect id: {aspect_id}")
        ids.add(aspect_id)
        family = aspect.get("family")
        require(isinstance(family, str) and family, f"{aspect_id}: family required")
        families.add(family)
        require(isinstance(aspect.get("question"), str) and aspect["question"].strip(), f"{aspect_id}: question required")
        require(nonempty_strings(aspect.get("does_not_prove")), f"{aspect_id}: does_not_prove required")
        require(nonempty_strings(aspect.get("required_refs")), f"{aspect_id}: required_refs required")
        require(nonempty_strings(aspect.get("status_values")), f"{aspect_id}: status_values required")

    missing = REQUIRED_ASPECTS - ids
    require(not missing, f"missing governed aspects: {sorted(missing)}")
    require(len(ids) == len(REQUIRED_ASPECTS), f"unexpected aspect count: {len(ids)}")
    require(len(families) >= 20, "aspect families are insufficiently separated")

    invariants = payload.get("global_invariants")
    require(nonempty_strings(invariants), "global_invariants required")
    missing_invariants = REQUIRED_INVARIANTS - set(invariants)
    require(not missing_invariants, f"missing global invariants: {sorted(missing_invariants)}")

    model_text = MODEL.read_text(encoding="utf-8")
    for marker in [
        "one interaction",
        "No aspect may silently grant another aspect",
        "Every governed submission can preserve a traceable claim",
        "Tokens are one compute-consumption measure, not a value measure",
        "Disagreement and competing determinations remain visible",
    ]:
        require(marker in model_text, f"governed aspect model missing marker: {marker}")

    print("ECOSYSTEM_CHAT_GOVERNED_ASPECTS_CHECK=PASS")
    print(f"aspect_count={len(ids)}")
    print(f"family_count={len(families)}")
    print("default_resolution=UNRESOLVED")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
