#!/usr/bin/env python3
"""Validate governed aspect events, registry conformance, and cross-aspect conflicts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ecosystem-chat-governed-aspects.registry.json"
EVENTS = ROOT / "data" / "ecosystem-chat-governed-aspect-events.fixture.json"
CONFLICTS = ROOT / "data" / "ecosystem-chat-governed-aspect-conflicts.fixture.json"
SCHEMA = ROOT / "schemas" / "ecosystem-chat-governed-aspect-event.schema.json"

ALLOWED_EVENT_TYPES = {
    "observation", "determination", "transition", "conflict", "quarantine",
    "refusal", "override", "revocation", "correction", "supersession",
    "recovery", "receipt",
}
ALLOWED_AUTHORITY_EFFECTS = {"NONE", "OBSERVE", "REVIEW_REQUIRED", "QUARANTINE", "DENY", "ALLOW"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: Any, label: str) -> datetime:
    require(isinstance(value, str) and value, f"{label}: timestamp required")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_event(event: dict[str, Any], registry: dict[str, dict[str, Any]], seen: set[str]) -> None:
    event_id = event.get("aspect_event_id")
    require(isinstance(event_id, str) and event_id, "aspect_event_id required")
    require(event_id not in seen, f"duplicate aspect_event_id: {event_id}")
    seen.add(event_id)

    require(event.get("schema_version") == "0.1.0", f"{event_id}: unsupported schema_version")
    require(isinstance(event.get("interaction_id"), str) and event["interaction_id"], f"{event_id}: interaction_id required")
    aspect_id = event.get("aspect_id")
    require(aspect_id in registry, f"{event_id}: unknown aspect_id {aspect_id!r}")
    require(event.get("event_type") in ALLOWED_EVENT_TYPES, f"{event_id}: invalid event_type")
    require(event.get("status") in registry[aspect_id]["status_values"], f"{event_id}: invalid status for {aspect_id}")
    require(isinstance(event.get("subject_refs"), list) and event["subject_refs"], f"{event_id}: subject_refs required")
    require(len(event["subject_refs"]) == len(set(event["subject_refs"])), f"{event_id}: duplicate subject_refs")
    require(isinstance(event.get("actor_ref"), str) and event["actor_ref"], f"{event_id}: actor_ref required")
    parse_time(event.get("timestamp"), event_id)
    if event.get("effective_at") is not None:
        parse_time(event["effective_at"], f"{event_id}.effective_at")
    if event.get("expires_at") is not None:
        parse_time(event["expires_at"], f"{event_id}.expires_at")
    confidence = event.get("confidence")
    require(confidence is None or isinstance(confidence, (int, float)) and 0 <= confidence <= 1, f"{event_id}: confidence out of range")
    for field in ["evidence_refs", "policy_refs", "authority_refs", "conflict_refs", "supersedes_refs"]:
        require(isinstance(event.get(field), list), f"{event_id}: {field} must be a list")
        require(len(event[field]) == len(set(event[field])), f"{event_id}: duplicate {field}")
    require(event.get("authority_effect") in ALLOWED_AUTHORITY_EFFECTS, f"{event_id}: invalid authority_effect")
    require(isinstance(event.get("hash"), str), f"{event_id}: hash required")

    if event["event_type"] in {"determination", "transition", "override", "revocation", "correction", "supersession", "recovery"}:
        require(event["evidence_refs"], f"{event_id}: evidence_refs required for governed change")
        require(event["policy_refs"], f"{event_id}: policy_refs required for governed change")
    if event["authority_effect"] in {"ALLOW", "DENY", "QUARANTINE"}:
        require(event["authority_refs"], f"{event_id}: authority_refs required for authority effect")
        require(event["policy_refs"], f"{event_id}: policy_refs required for authority effect")
    if event["event_type"] == "conflict":
        require(event["conflict_refs"], f"{event_id}: conflict_refs required")
        require(event["authority_effect"] in {"REVIEW_REQUIRED", "QUARANTINE", "DENY"}, f"{event_id}: conflict cannot allow")


def classify_conflict(aspects: dict[str, dict[str, Any]]) -> tuple[str, str]:
    def status(aspect: str) -> Any:
        return aspects.get(aspect, {}).get("status")

    if status("ownership_control") == "verified" and status("consent_permission") == "revoked" and status("disclosure_projection") == "allow":
        return "QUARANTINE", "ownership_does_not_override_revoked_consent"
    if status("realized_value") == "verified" and status("admissibility") == "deny" and status("distribution_allocation") == "authorized":
        return "DENY", "value_does_not_override_inadmissibility"
    if status("authorship") == "human" and status("source_provenance") == "generated":
        return "REVIEW_REQUIRED", "human_only_authorship_conflicts_with_model_generation"
    if status("source_provenance") == "captured" and status("derivation_transformation") == "derived":
        return "REVIEW_REQUIRED", "captured_record_cannot_simultaneously_assert_derivation"
    if status("privacy_sensitivity") == "restricted" and status("disclosure_projection") == "allow" and aspects["disclosure_projection"].get("redaction_required") is False:
        return "DENY", "restricted_projection_requires_redaction"
    if status("settlement") == "settled" and not aspects["settlement"].get("settlement_receipt_refs"):
        return "DENY", "settlement_requires_receipt"
    if status("authority_delegation") == "active" and aspects["authority_delegation"].get("delegation_validity") == "expired":
        return "DENY", "active_authority_requires_current_delegation"
    if status("standing_capability") == "earned" and aspects["standing_capability"].get("execution_permission_inferred") is True:
        return "DENY", "standing_does_not_grant_execution"
    if status("originality_novelty") == "publicly_novel" and not aspects["originality_novelty"].get("comparison_boundary_refs"):
        return "REVIEW_REQUIRED", "public_novelty_requires_comparison_boundary"
    if status("consent_permission") == "limited" and aspects["consent_permission"].get("reuse_scope") == "interaction_only" and status("disclosure_projection") == "allow" and aspects["disclosure_projection"].get("destination") == "GCAT-BCAT-Engine/Publisher":
        return "DENY", "interaction_only_reuse_blocks_publication"
    if status("consent_permission") == "revoked" and status("reward_incentive") == "royalty_candidate" and status("distribution_allocation") == "provisional":
        return "DENY", "revoked_claim_cannot_advance"
    if status("outcome_utility") == "observed" and status("cost_externalities") == "unassessed":
        return "REVIEW_REQUIRED", "successful_outcome_requires_externality_posture"
    return "COMPLETE", "no_conflict"


def main() -> int:
    require(SCHEMA.exists(), "missing governed aspect event schema")
    registry_payload = load(REGISTRY)
    event_payload = load(EVENTS)
    conflict_payload = load(CONFLICTS)

    require(registry_payload.get("authority_effect") == "NONE", "registry authority_effect must be NONE")
    require(event_payload.get("authority_effect") == "NONE", "event fixture authority_effect must be NONE")
    require(conflict_payload.get("authority_effect") == "NONE", "conflict fixture authority_effect must be NONE")

    aspects = registry_payload.get("aspects")
    require(isinstance(aspects, list) and aspects, "registry aspects required")
    registry = {entry["id"]: entry for entry in aspects}
    require(len(registry) == len(aspects), "duplicate registry aspect id")

    events = event_payload.get("events")
    require(isinstance(events, list) and events, "events required")
    seen: set[str] = set()
    previous_time: datetime | None = None
    for event in events:
        require(isinstance(event, dict), "events must be objects")
        validate_event(event, registry, seen)
        current_time = parse_time(event["timestamp"], event["aspect_event_id"])
        require(previous_time is None or current_time >= previous_time, f"{event['aspect_event_id']}: stream timestamps out of order")
        previous_time = current_time

    cases = conflict_payload.get("cases")
    require(isinstance(cases, list) and cases, "conflict cases required")
    seen_cases: set[str] = set()
    for case in cases:
        case_id = case.get("case_id")
        require(isinstance(case_id, str) and case_id, "case_id required")
        require(case_id not in seen_cases, f"duplicate conflict case: {case_id}")
        seen_cases.add(case_id)
        result, conflict = classify_conflict(case.get("aspects", {}))
        require(result == case.get("expected_result"), f"{case_id}: expected {case.get('expected_result')} got {result}")
        require(conflict == case.get("required_conflict"), f"{case_id}: expected conflict {case.get('required_conflict')} got {conflict}")
        require(result in {"DENY", "QUARANTINE", "REVIEW_REQUIRED"}, f"{case_id}: conflict must fail closed")

    print("ECOSYSTEM_CHAT_GOVERNED_ASPECT_RUNTIME_CHECK=PASS")
    print(f"registry_aspects={len(registry)}")
    print(f"aspect_events={len(events)}")
    print(f"conflict_cases={len(cases)}")
    print("conflict_allow_count=0")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
