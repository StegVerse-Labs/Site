#!/usr/bin/env python3
"""Deterministic adversarial coverage for legacy aggregate claim tombstones."""
from __future__ import annotations

from copy import deepcopy

from check_session_work_claims import apply_terminalization_tombstone

BASE = {
    "claim_id": "TEST-LEGACY-ACTIVE-CLAIM",
    "session_worker_id": "worker:test",
    "task_id": "TEST-TASK",
    "originating_goal": "fixture",
    "repository": "StegVerse-Labs/Site",
    "branch": "fixture",
    "role": "VALIDATION",
    "state": "CLAIMED_FOR_IMPLEMENTATION",
    "normalized_work_key": "fixture",
    "dependency_surface_keys": ["site:fixture"],
    "claimed_paths": ["fixture"],
    "handoff": "docs/SITE_MIRROR_HANDOFF.md",
    "handoff_revision": "fixture",
    "claim_created_at": "2026-09-03T00:00:00Z",
    "claim_expires_when": "fixture completion",
    "expected_evidence": ["fixture"],
    "collision_boundaries": ["fixture"],
    "next_task_after_release": "none",
    "credential_authority": "TV/TVC",
    "github_token_runtime_authority": "NONE",
    "authority_effect": False,
    "activation_effect": False,
}

VALID = {
    "claim_id": "TEST-LEGACY-ACTIVE-CLAIM",
    "terminalization_override_of": "canonical_registry",
    "state": "RELEASED",
    "pull_request": 1,
    "release_commit": "deadbeef",
    "claim_released_at": "2026-09-03T00:01:00Z",
    "archive_eligible": True,
}


def must_reject(label: str, tombstone: dict, claims=None, seen=None) -> None:
    try:
        apply_terminalization_tombstone(claims or [deepcopy(BASE)], tombstone, seen)
    except ValueError:
        return
    raise AssertionError(f"expected rejection: {label}")


def main() -> int:
    result = apply_terminalization_tombstone([deepcopy(BASE)], deepcopy(VALID), set())
    assert result["state"] == "RELEASED"
    assert result["pull_request"] == 1
    assert result["release_commit"] == "deadbeef"
    assert result["claim_released_at"] == "2026-09-03T00:01:00Z"
    assert result["archive_eligible"] is True
    for protected in (
        "task_id", "branch", "role", "dependency_surface_keys", "claimed_paths", "handoff",
        "credential_authority", "github_token_runtime_authority", "authority_effect", "activation_effect",
    ):
        assert result[protected] == BASE[protected], protected

    unknown = deepcopy(VALID); unknown["claim_id"] = "UNKNOWN"
    must_reject("unknown target", unknown)
    active = deepcopy(VALID); active["state"] = "CLAIMED_FOR_VALIDATION"
    must_reject("active-to-active", active)
    protected = deepcopy(VALID); protected["authority_effect"] = True
    must_reject("protected-field injection", protected)
    missing = deepcopy(VALID); missing.pop("release_commit")
    must_reject("missing release evidence", missing)
    non_bool = deepcopy(VALID); non_bool["archive_eligible"] = "true"
    must_reject("non-boolean archive", non_bool)
    seen = {VALID["claim_id"]}
    must_reject("duplicate target", deepcopy(VALID), seen=seen)

    terminal_base = deepcopy(BASE); terminal_base["state"] = "RELEASED"
    must_reject("already terminal target", deepcopy(VALID), claims=[terminal_base])

    print("LEGACY_AGGREGATE_CLAIM_TERMINALIZATION_TESTS_PASS cases=8 authority_effect=NONE activation_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
