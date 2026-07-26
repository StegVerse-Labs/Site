from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts.validate_ecosystem_node_canonical_events import (
    CanonicalEventValidationError,
    event_hash,
    validate_stream,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(
    (ROOT / "fixtures" / "ecosystem-node-canonical-events.json").read_text(encoding="utf-8")
)["events"]


def rehash(event):
    event["hash"] = event_hash(event)
    return event


def test_fixture_validates_with_stable_id_only_correlation():
    result = validate_stream(deepcopy(FIXTURE))
    assert result["event_count"] == 2
    assert result["correlation"] == "stable_event_id_only"
    assert result["cryptographic_hashing"] is True
    assert result["authority_effect"] == "none"


def test_hash_drift_fails_closed():
    events = deepcopy(FIXTURE)
    events[0]["human_projection"]["body"] = "tampered"
    with pytest.raises(CanonicalEventValidationError, match="hash mismatch"):
        validate_stream(events)


def test_duplicate_event_id_fails_closed():
    events = deepcopy(FIXTURE)
    events[1]["event_id"] = events[0]["event_id"]
    rehash(events[1])
    with pytest.raises(CanonicalEventValidationError, match="duplicate event_id"):
        validate_stream(events)


def test_forward_parent_reference_fails_closed():
    events = list(reversed(deepcopy(FIXTURE)))
    with pytest.raises(CanonicalEventValidationError, match="forward parent_event_id"):
        validate_stream(events)


def test_unresolved_event_evidence_reference_fails_closed():
    events = deepcopy(FIXTURE)
    events[1]["evidence_refs"] = ["event:missing-event"]
    rehash(events[1])
    with pytest.raises(CanonicalEventValidationError, match="unresolved evidence_refs"):
        validate_stream(events)


def test_duplicate_reference_fails_closed():
    events = deepcopy(FIXTURE)
    events[1]["policy_refs"] = ["policy:site-renderer-boundary"] * 2
    rehash(events[1])
    with pytest.raises(CanonicalEventValidationError, match="contains duplicates"):
        validate_stream(events)


def test_authority_claim_does_not_become_validator_authority():
    events = deepcopy(FIXTURE)
    events[1]["governed_projection"]["execution_authority"] = True
    rehash(events[1])
    result = validate_stream(events)
    assert result["authority_effect"] == "none"
