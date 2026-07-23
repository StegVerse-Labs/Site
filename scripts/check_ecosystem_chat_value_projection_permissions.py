#!/usr/bin/env python3
"""Validate captured/derived posture and fail-closed downstream projection permissions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "ecosystem-chat-value-claims.fixture.json"
PERMISSIONS = ROOT / "data" / "ecosystem-chat-value-projection-permissions.fixture.json"
DESTINATIONS = {
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-002/stegguardian-wiki",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def main() -> int:
    claims_payload = json.loads(CLAIMS.read_text(encoding="utf-8"))
    permissions_payload = json.loads(PERMISSIONS.read_text(encoding="utf-8"))
    require(permissions_payload.get("authority_effect") == "NONE", "authority_effect must be NONE")

    claims = {claim["claim_id"]: claim for claim in claims_payload.get("claims", [])}
    records = permissions_payload.get("records")
    require(isinstance(records, list) and records, "records must be non-empty")
    seen: set[str] = set()

    for record in records:
        claim_id = record.get("claim_id")
        require(isinstance(claim_id, str) and claim_id, "claim_id required")
        require(claim_id not in seen, f"duplicate permission record: {claim_id}")
        seen.add(claim_id)
        require(claim_id in claims, f"unknown claim_id: {claim_id}")
        claim = claims[claim_id]
        require(record.get("submission_event_id") == claim.get("submission_event_id"), f"{claim_id}: submission_event_id mismatch")
        require(record.get("information_class") in {"captured", "derived"}, f"{claim_id}: invalid information_class")
        require(isinstance(record.get("captured_source_refs"), list), f"{claim_id}: captured_source_refs must be list")
        require(isinstance(record.get("derivation_refs"), list), f"{claim_id}: derivation_refs must be list")
        if record.get("information_class") == "captured":
            require(nonempty(record.get("captured_source_refs")), f"{claim_id}: captured record needs captured_source_refs")
            require(not record.get("derivation_refs"), f"{claim_id}: captured record cannot assert derivation_refs")
        else:
            require(nonempty(record.get("derivation_refs")), f"{claim_id}: derived record needs derivation_refs")

        projection = record.get("projection")
        require(isinstance(projection, dict), f"{claim_id}: projection required")
        require(projection.get("default") == "deny", f"{claim_id}: projection must default deny")
        allowed = projection.get("allowed_destinations")
        denied = projection.get("denied_destinations")
        require(isinstance(allowed, list) and isinstance(denied, list), f"{claim_id}: destination lists required")
        require(not (set(allowed) & set(denied)), f"{claim_id}: destination cannot be both allowed and denied")
        require(set(allowed) | set(denied) == DESTINATIONS, f"{claim_id}: every known destination must be explicitly classified")
        require(set(allowed).issubset(DESTINATIONS), f"{claim_id}: unknown allowed destination")
        require(projection.get("redaction_required") is True, f"{claim_id}: redaction_required must be true")
        require(projection.get("minimum_disclosure") is True, f"{claim_id}: minimum_disclosure must be true")
        require(nonempty(projection.get("policy_refs")), f"{claim_id}: policy_refs required")
        require(nonempty(projection.get("consent_refs")), f"{claim_id}: consent_refs required")
        if allowed:
            require(nonempty(projection.get("purpose_refs")), f"{claim_id}: allowed projection requires purpose_refs")
        expires_at = projection.get("expires_at")
        if expires_at is not None:
            datetime.fromisoformat(expires_at.replace("Z", "+00:00"))

        reuse_scope = claim.get("information_posture", {}).get("reuse_scope")
        if reuse_scope == "interaction_only":
            require(not allowed, f"{claim_id}: interaction-only claim cannot allow downstream projection")
        if record.get("information_class") == "captured" and reuse_scope == "bounded_downstream":
            require(len(allowed) <= 1, f"{claim_id}: bounded captured record exceeds one allowed destination")

    require(seen == set(claims), "every claim must have exactly one projection permission record")
    print(f"PASS: validated {len(records)} captured/derived projection permission records")
    print("projection_default=DENY")
    print("redaction_required=true")
    print("minimum_disclosure=true")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
