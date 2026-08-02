#!/usr/bin/env python3
"""Validate the governed VA Claims Guide, Chat, document workspace, and filing goals."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

GOALS = Path("data/va-claim-assistant/governed-product-goals.json")
RECEIPT = Path("data/va-claim-assistant/governed-product-goals-validation.json")

REQUIRED_GOALS = {
    "GOVERNED_VA_CLAIMS_GUIDE",
    "GOVERNED_VA_CLAIMS_CHAT",
    "PRIVATE_CLAIM_DOCUMENT_WORKSPACE",
    "VETERAN_APPROVED_AUTOMATED_CLAIM_FILING",
}
REQUIRED_FILING_GATES = {
    "require explicit veteran confirmation of each material fact and claimed condition",
    "obtain a specific unexpired submission authorization receipt",
    "submit only through an authorized VA or accredited-representative integration",
}


def canonical_sha256(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    data = json.loads(GOALS.read_text(encoding="utf-8"))
    blockers: list[str] = []

    goals = {item.get("name"): item for item in data.get("product_surfaces", [])}
    missing = sorted(REQUIRED_GOALS - set(goals))
    if missing:
        blockers.append("missing_product_goals:" + ",".join(missing))

    governance = data.get("cross_cutting_governance", {})
    for key in (
        "veteran_controls_facts",
        "veteran_controls_claim_selection",
        "veteran_controls_submission",
        "human_review_required_before_filing",
        "fail_closed_on_missing_authority_or_evidence",
    ):
        if governance.get(key) is not True:
            blockers.append(f"required_true:{key}")

    for key in (
        "raw_documents_publicly_published",
        "provider_output_is_authority",
        "assistant_is_accredited_representative",
        "assistant_is_clinician",
        "assistant_is_va_adjudicator",
        "target_rating_optimization_allowed",
    ):
        if governance.get(key) is not False:
            blockers.append(f"required_false:{key}")

    filing = goals.get("VETERAN_APPROVED_AUTOMATED_CLAIM_FILING", {})
    if filing.get("state") != "FUTURE_GOVERNED_TARGET":
        blockers.append("automated_filing_must_remain_future_target")
    stages = set(filing.get("stages", []))
    missing_stages = sorted(REQUIRED_FILING_GATES - stages)
    if missing_stages:
        blockers.append("missing_filing_gates:" + ",".join(missing_stages))

    body = {
        "schema_version": "1.0.0",
        "goal_set_id": data.get("goal_set_id"),
        "state": "PASS" if not blockers else "BLOCKED",
        "goal_count": len(goals),
        "required_goals_present": not missing,
        "veteran_submission_authority_preserved": governance.get("veteran_controls_submission") is True,
        "automated_filing_active": False,
        "authority_effect": False,
        "activation_effect": False,
        "blockers": blockers,
        "goals_sha256": canonical_sha256(data),
    }
    body["receipt_sha256"] = canonical_sha256(body)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
