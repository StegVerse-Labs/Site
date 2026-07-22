#!/usr/bin/env python3
"""Validate governed Ecosystem Chat value claims and their Site renderer."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "ecosystem-chat-value-claims.fixture.json"
RENDERER_CHECK = ROOT / "scripts" / "check_ecosystem_chat_value_renderer.py"

STAGES = ["submitted", "recognized", "attributed", "realized", "distributable", "settled"]
SOURCE_TYPES = {
    "user_original",
    "user_record",
    "user_observation",
    "user_correction",
    "public",
    "licensed",
    "derived",
    "unknown",
}
REUSE_SCOPES = {"interaction_only", "bounded_downstream", "licensed_reuse", "unknown"}
REWARD_CLASSES = {
    "none",
    "credit",
    "standing",
    "access",
    "capability",
    "governance",
    "royalty_candidate",
    "payment",
    "other",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def validate_claim(claim: dict[str, Any], seen: set[str]) -> None:
    claim_id = claim.get("claim_id")
    require(isinstance(claim_id, str) and claim_id, "claim_id must be non-empty")
    require(claim_id not in seen, f"duplicate claim_id: {claim_id}")
    seen.add(claim_id)

    require(isinstance(claim.get("submission_event_id"), str), f"{claim_id}: missing submission_event_id")
    require(nonempty_list(claim.get("claimant_refs")), f"{claim_id}: claimant_refs must be non-empty")

    stage = claim.get("stage")
    require(stage in STAGES, f"{claim_id}: invalid stage {stage!r}")
    stage_index = STAGES.index(stage)

    posture = claim.get("information_posture")
    require(isinstance(posture, dict), f"{claim_id}: information_posture missing")
    require(posture.get("source_type") in SOURCE_TYPES, f"{claim_id}: invalid source_type")
    require(posture.get("reuse_scope") in REUSE_SCOPES, f"{claim_id}: invalid reuse_scope")
    require(isinstance(posture.get("consent_refs"), list), f"{claim_id}: consent_refs must be a list")

    influence = claim.get("influence")
    require(isinstance(influence, dict), f"{claim_id}: influence missing")
    confidence = influence.get("confidence")
    require(isinstance(confidence, (int, float)) and 0 <= confidence <= 1, f"{claim_id}: confidence out of range")

    value = claim.get("value")
    distribution = claim.get("distribution")
    require(isinstance(value, dict), f"{claim_id}: value missing")
    require(isinstance(distribution, dict), f"{claim_id}: distribution missing")
    require(distribution.get("reward_class") in REWARD_CLASSES, f"{claim_id}: invalid reward_class")
    require(isinstance(claim.get("evidence_refs"), list), f"{claim_id}: evidence_refs must be a list")

    if stage_index >= STAGES.index("recognized"):
        require(nonempty_list(influence.get("target_event_refs")), f"{claim_id}: recognized+ requires target_event_refs")
        require(nonempty_list(claim.get("evidence_refs")), f"{claim_id}: recognized+ requires evidence_refs")
        require(influence.get("materiality") != "unassessed", f"{claim_id}: recognized+ requires assessed materiality")

    if stage_index >= STAGES.index("attributed"):
        require(nonempty_list(distribution.get("policy_refs")), f"{claim_id}: attributed+ requires policy_refs")

    if stage_index >= STAGES.index("realized"):
        require(bool(value.get("measurement_method")), f"{claim_id}: realized+ requires measurement_method")
        require(nonempty_list(value.get("baseline_refs")), f"{claim_id}: realized+ requires baseline_refs")
        require(value.get("observed_amount") is not None, f"{claim_id}: realized+ requires observed_amount")
        require(bool(value.get("unit")), f"{claim_id}: realized+ requires unit")

    if stage_index >= STAGES.index("distributable"):
        require(distribution.get("reward_class") != "none", f"{claim_id}: distributable+ requires reward_class")
        require(nonempty_list(distribution.get("contract_refs")), f"{claim_id}: distributable+ requires contract_refs")
        require(distribution.get("allocation") is not None, f"{claim_id}: distributable+ requires allocation")

    if stage == "settled":
        require(nonempty_list(distribution.get("settlement_receipt_refs")), f"{claim_id}: settled requires receipt")

    if stage == "submitted":
        require(distribution.get("reward_class") in {"none", "credit"}, f"{claim_id}: submitted claim cannot assert payable reward")
        require(not distribution.get("settlement_receipt_refs"), f"{claim_id}: submitted claim cannot have settlement receipt")

    if posture.get("reuse_scope") == "interaction_only":
        require(stage_index < STAGES.index("distributable"), f"{claim_id}: interaction-only data cannot be distributable")


def validate_renderer() -> None:
    completed = subprocess.run(
        [sys.executable, str(RENDERER_CHECK)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    require(completed.returncode == 0, f"value renderer validation failed:\n{completed.stdout.rstrip()}")
    print(completed.stdout.rstrip())


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    require(payload.get("authority_effect") == "NONE", "fixture must declare authority_effect NONE")
    claims = payload.get("claims")
    require(isinstance(claims, list) and claims, "claims must be a non-empty list")

    seen: set[str] = set()
    for claim in claims:
        require(isinstance(claim, dict), "each claim must be an object")
        validate_claim(claim, seen)

    validate_renderer()
    print(f"PASS: validated {len(claims)} governed value claims and synchronized renderer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
