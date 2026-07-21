#!/usr/bin/env python3
"""Validate the Ecosystem Node canonical replay and disclosure fixture."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "ecosystem-node-canonical-events.fixture.json"
REQUIRED_FIELDS = {
    "event_id",
    "parent_event_id",
    "timestamp",
    "actor",
    "event_type",
    "human_projection",
    "governed_projection",
    "policy_refs",
    "evidence_refs",
    "artifact_refs",
    "continuity_refs",
    "hash",
}
EVENT_TYPES = {"message", "decision", "execution", "receipt", "policy", "evidence"}
ROLES = {"public", "operator", "technical", "legal", "executive", "auditor"}


def fail(message: str) -> int:
    print(f"ECOSYSTEM_NODE_REPLAY_DISCLOSURE_FAIL: {message}")
    return 1


def parse_timestamp(value: str) -> None:
    datetime.fromisoformat(value.replace("Z", "+00:00"))


def disclosed_projection(event: dict, role: str) -> tuple[dict, list[str]]:
    governed = event["governed_projection"]
    disclosure = governed.get("disclosure", {})
    allowed = set(disclosure.get(role, disclosure.get("public", [])))
    infrastructure = {"disclosure"}
    visible = {key: value for key, value in governed.items() if key in allowed or key in infrastructure}
    redacted = sorted(key for key in governed if key not in allowed and key not in infrastructure)
    return visible, redacted


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    events = payload.get("events", [])
    expected = payload.get("expected", {})
    if payload.get("schema") != "stegverse.canonical-event-stream.v0.1":
        return fail("unexpected stream schema")
    if set(payload.get("viewer_roles", [])) != ROLES:
        return fail("viewer role set is incomplete")
    if len(events) != expected.get("event_count"):
        return fail("event count does not match expected replay count")

    identifiers: set[str] = set()
    order: list[str] = []
    conversation_ids: list[str] = []
    governance_only_ids: list[str] = []
    for event in events:
        missing = REQUIRED_FIELDS - set(event)
        if missing:
            return fail(f"{event.get('event_id', '<unknown>')} missing fields: {sorted(missing)}")
        event_id = event["event_id"]
        if not isinstance(event_id, str) or not event_id:
            return fail("event_id must be a non-empty string")
        if event_id in identifiers:
            return fail(f"duplicate event_id: {event_id}")
        identifiers.add(event_id)
        order.append(event_id)
        if event["event_type"] not in EVENT_TYPES:
            return fail(f"unsupported event_type: {event['event_type']}")
        parse_timestamp(event["timestamp"])
        if event["parent_event_id"] is not None and event["parent_event_id"] not in identifiers:
            return fail(f"unresolved or forward parent reference: {event_id}")
        for ref_name in ("evidence_refs", "continuity_refs"):
            for reference in event[ref_name]:
                if reference not in identifiers:
                    return fail(f"unresolved {ref_name} reference {reference} in {event_id}")
        if event["human_projection"].get("visible_in_conversation"):
            conversation_ids.append(event_id)
        else:
            governance_only_ids.append(event_id)

    if conversation_ids != expected.get("conversation_event_ids"):
        return fail("conversation projection does not resolve to expected canonical IDs")
    if governance_only_ids != expected.get("governance_only_event_ids"):
        return fail("governance-only projection does not resolve to expected canonical IDs")

    expected_redactions = {
        item["event_id"]: sorted(item["fields"])
        for item in expected.get("public_redactions", [])
    }
    for event in events:
        visible, redacted = disclosed_projection(event, "public")
        if event["event_id"] in expected_redactions and redacted != expected_redactions[event["event_id"]]:
            return fail(f"public redaction mismatch for {event['event_id']}: {redacted}")
        if "provider_token_reference" in visible:
            return fail("public projection disclosed provider_token_reference")
        if visible.get("disclosure") is not event["governed_projection"].get("disclosure"):
            return fail("disclosure metadata must project from the canonical record")

    replayed = json.loads(json.dumps(payload, separators=(",", ":")))
    replay_order = [event["event_id"] for event in replayed["events"]]
    if replay_order != order:
        return fail("JSON replay changed event order")
    jsonl = "\n".join(json.dumps(event, separators=(",", ":")) for event in events) + "\n"
    jsonl_events = [json.loads(line) for line in jsonl.splitlines() if line]
    if [event["event_id"] for event in jsonl_events] != order:
        return fail("JSONL replay changed event order")
    if jsonl_events != events:
        return fail("JSONL replay changed canonical records")

    print("ECOSYSTEM_NODE_REPLAY_DISCLOSURE_PASS")
    print(f"events={len(events)}")
    print(f"conversation_events={len(conversation_ids)}")
    print(f"governance_only_events={len(governance_only_ids)}")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
