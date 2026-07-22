#!/usr/bin/env python3
"""Validate governed value-claim stage histories, consent changes, and disputes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "ecosystem-chat-value-claim-history.fixture.json"
STAGES = ["submitted", "recognized", "attributed", "realized", "distributable", "settled"]
EVENT_TYPES = {"stage_transition", "consent_change", "revocation", "dispute"}
REUSE_SCOPES = {"interaction_only", "bounded_downstream", "licensed_reuse", "unknown"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_time(value: Any, label: str) -> datetime:
    require(isinstance(value, str) and value, f"{label}: timestamp required")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_history(history: dict[str, Any], seen_claims: set[str], seen_events: set[str]) -> None:
    claim_id = history.get("claim_id")
    require(isinstance(claim_id, str) and claim_id, "history claim_id required")
    require(claim_id not in seen_claims, f"duplicate history claim_id: {claim_id}")
    seen_claims.add(claim_id)
    require(isinstance(history.get("submission_event_id"), str), f"{claim_id}: submission_event_id required")
    require(history.get("current_stage") in STAGES, f"{claim_id}: invalid current_stage")

    events = history.get("events")
    require(isinstance(events, list) and events, f"{claim_id}: events required")
    previous_time: datetime | None = None
    effective_stage: str | None = None
    revoked = False

    for index, event in enumerate(events):
        event_id = event.get("history_event_id")
        require(isinstance(event_id, str) and event_id, f"{claim_id}: history_event_id required")
        require(event_id not in seen_events, f"duplicate history_event_id: {event_id}")
        seen_events.add(event_id)
        event_type = event.get("event_type")
        require(event_type in EVENT_TYPES, f"{event_id}: invalid event_type")
        require(event.get("authority_effect") == "NONE", f"{event_id}: authority_effect must be NONE")
        require(event.get("reuse_scope") in REUSE_SCOPES, f"{event_id}: invalid reuse_scope")
        require(isinstance(event.get("consent_refs"), list) and event["consent_refs"], f"{event_id}: consent_refs required")
        require(isinstance(event.get("evidence_refs"), list) and event["evidence_refs"], f"{event_id}: evidence_refs required")
        require(isinstance(event.get("policy_refs"), list) and event["policy_refs"], f"{event_id}: policy_refs required")

        timestamp = parse_time(event.get("timestamp"), event_id)
        require(previous_time is None or timestamp >= previous_time, f"{event_id}: history timestamps out of order")
        previous_time = timestamp

        from_stage = event.get("from_stage")
        to_stage = event.get("to_stage")
        require(to_stage in STAGES, f"{event_id}: invalid to_stage")

        if index == 0:
            require(event_type == "stage_transition", f"{claim_id}: first event must be stage_transition")
            require(from_stage is None and to_stage == "submitted", f"{claim_id}: history must begin at submitted")
            effective_stage = "submitted"
            continue

        require(from_stage == effective_stage, f"{event_id}: from_stage must match effective stage {effective_stage}")

        if event_type == "stage_transition":
            require(not revoked, f"{event_id}: revoked claim cannot advance")
            require(STAGES.index(to_stage) == STAGES.index(effective_stage) + 1, f"{event_id}: stage transition must advance exactly one stage")
            effective_stage = to_stage
        else:
            require(to_stage == effective_stage, f"{event_id}: non-stage event cannot change stage")
            if event_type == "consent_change":
                require("consent" in " ".join(event["policy_refs"]).lower(), f"{event_id}: consent policy required")
            elif event_type == "revocation":
                require("revok" in " ".join(event["consent_refs"]).lower(), f"{event_id}: revocation consent reference required")
                revoked = True
            elif event_type == "dispute":
                require(isinstance(event.get("competing_claim_refs"), list) and event["competing_claim_refs"], f"{event_id}: dispute requires competing_claim_refs")

    require(effective_stage == history.get("current_stage"), f"{claim_id}: current_stage does not match reconstructed history")


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    require(payload.get("authority_effect") == "NONE", "fixture authority_effect must be NONE")
    histories = payload.get("histories")
    require(isinstance(histories, list) and histories, "histories must be non-empty")

    seen_claims: set[str] = set()
    seen_events: set[str] = set()
    for history in histories:
        require(isinstance(history, dict), "history entries must be objects")
        validate_history(history, seen_claims, seen_events)

    print(f"PASS: reconstructed {len(histories)} governed value-claim histories")
    print("stage_skipping=REJECTED")
    print("post_revocation_advancement=REJECTED")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
