#!/usr/bin/env python3
"""Validate Ecosystem Node canonical events and their stable-ID correlation graph."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = {
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
EVENT_TYPES = {
    "message",
    "decision",
    "execution",
    "receipt",
    "policy",
    "evidence",
    "artifact",
    "refusal",
    "quarantine",
    "override",
    "recovery",
}
REF_FIELDS = ("policy_refs", "evidence_refs", "artifact_refs", "continuity_refs")


class CanonicalEventValidationError(ValueError):
    pass


def canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def event_hash(event: Mapping[str, Any]) -> str:
    material = dict(event)
    material["hash"] = ""
    return "sha256:" + hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CanonicalEventValidationError(f"{label} must be a non-empty string")
    return value


def validate_event_shape(event: Mapping[str, Any], position: int) -> None:
    if not isinstance(event, Mapping):
        raise CanonicalEventValidationError(f"event[{position}] must be an object")
    if set(event) != REQUIRED_KEYS:
        missing = sorted(REQUIRED_KEYS - set(event))
        extra = sorted(set(event) - REQUIRED_KEYS)
        raise CanonicalEventValidationError(
            f"event[{position}] key mismatch; missing={missing}; extra={extra}"
        )
    require_text(event["event_id"], f"event[{position}].event_id")
    parent = event["parent_event_id"]
    if parent is not None:
        require_text(parent, f"event[{position}].parent_event_id")
    timestamp = require_text(event["timestamp"], f"event[{position}].timestamp")
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CanonicalEventValidationError(
            f"event[{position}].timestamp must be RFC3339-compatible"
        ) from exc
    actor = event["actor"]
    if not isinstance(actor, Mapping):
        raise CanonicalEventValidationError(f"event[{position}].actor must be an object")
    require_text(actor.get("actor_type"), f"event[{position}].actor.actor_type")
    require_text(actor.get("identity_ref"), f"event[{position}].actor.identity_ref")
    if event["event_type"] not in EVENT_TYPES:
        raise CanonicalEventValidationError(f"event[{position}] unsupported event_type")
    if not isinstance(event["human_projection"], Mapping):
        raise CanonicalEventValidationError(f"event[{position}].human_projection must be an object")
    if not isinstance(event["governed_projection"], Mapping):
        raise CanonicalEventValidationError(f"event[{position}].governed_projection must be an object")
    for field in REF_FIELDS:
        refs = event[field]
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
            raise CanonicalEventValidationError(f"event[{position}].{field} must be a string array")
        if len(refs) != len(set(refs)):
            raise CanonicalEventValidationError(f"event[{position}].{field} contains duplicates")
    supplied = event["hash"]
    if supplied != event_hash(event):
        raise CanonicalEventValidationError(f"event[{position}] hash mismatch")


def validate_stream(events: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    records = list(events)
    if not records:
        raise CanonicalEventValidationError("event stream cannot be empty")
    seen: set[str] = set()
    for position, event in enumerate(records):
        validate_event_shape(event, position)
        event_id = event["event_id"]
        if event_id in seen:
            raise CanonicalEventValidationError(f"duplicate event_id: {event_id}")
        parent = event["parent_event_id"]
        if parent is not None and parent not in seen:
            raise CanonicalEventValidationError(
                f"event {event_id} has unresolved or forward parent_event_id: {parent}"
            )
        for field in ("evidence_refs", "continuity_refs"):
            for ref in event[field]:
                if ref.startswith("event:"):
                    target = ref.removeprefix("event:")
                    if target not in seen:
                        raise CanonicalEventValidationError(
                            f"event {event_id} has unresolved {field} reference: {ref}"
                        )
        seen.add(event_id)
    stream_material = {
        "schema": "stegverse.canonical-event-stream.v1",
        "event_count": len(records),
        "event_ids": [event["event_id"] for event in records],
        "event_hashes": [event["hash"] for event in records],
    }
    stream_sha256 = "sha256:" + hashlib.sha256(
        canonical_json(stream_material).encode("utf-8")
    ).hexdigest()
    return {
        **stream_material,
        "stream_sha256": stream_sha256,
        "correlation": "stable_event_id_only",
        "cryptographic_hashing": True,
        "authority_effect": "none",
        "manual_user_action_required": False,
    }


def load_events(path: Path) -> list[Mapping[str, Any]]:
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, Mapping) and isinstance(payload.get("events"), list):
        return payload["events"]
    raise CanonicalEventValidationError("input must be an event array, stream object, or JSONL")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default=str(ROOT / "fixtures" / "ecosystem-node-canonical-events.json"),
    )
    args = parser.parse_args()
    try:
        result = validate_stream(load_events(Path(args.path)))
    except (OSError, json.JSONDecodeError, CanonicalEventValidationError) as exc:
        print("ECOSYSTEM_NODE_CANONICAL_EVENT_VALIDATION=FAIL")
        print(f"error={exc}")
        return 1
    print("ECOSYSTEM_NODE_CANONICAL_EVENT_VALIDATION=PASS")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
