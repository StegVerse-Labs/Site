#!/usr/bin/env python3
"""Verify authority decision fixtures remain DENY, preview-only, and non-executing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "authority-decision-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "authority-decision-response.example.json"
FALSE_REQUEST_EFFECTS = (
    "execution_allowed",
    "credential_access_allowed",
    "live_calls_allowed",
    "repo_mutation_allowed",
)
FALSE_RESPONSE_OUTPUTS = (
    "authority_issued",
    "execution_allowed",
    "credential_access_allowed",
    "live_calls_allowed",
    "repo_mutation_allowed",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_AUTHORITY_DECISION_FIXTURES_FAIL: {message}")


def main() -> int:
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    response = json.loads(RESPONSE.read_text(encoding="utf-8"))
    if request.get("schema_version") != "stegverse.ai_entry.authority_decision_request.v0.1":
        fail("bad request schema version")
    if response.get("schema_version") != "stegverse.ai_entry.authority_decision_response.v0.1":
        fail("bad response schema version")
    if request.get("request_id") != response.get("request_id"):
        fail("request/response id mismatch")
    if request.get("activation_request_id") != response.get("activation_request_id"):
        fail("activation request id mismatch")
    if request.get("decision_mode") != "preview_only":
        fail("request must remain preview_only")
    actor = request.get("actor_identity_context", {})
    if actor.get("actor_known") is not False or actor.get("actor_authorized") is not False:
        fail("actor must remain unknown/unauthorized in preview fixture")
    boundary = request.get("boundary_inputs_present", {})
    for key, value in boundary.items():
        if value is not False:
            fail(f"{key} must be false")
    effects = request.get("requested_effects", {})
    for key in FALSE_REQUEST_EFFECTS:
        if effects.get(key) is not False:
            fail(f"request {key} must be false")
    if response.get("authority_decision") != "DENY":
        fail("authority decision must be DENY")
    if not response.get("missing_preconditions"):
        fail("missing preconditions required")
    outputs = response.get("decision_outputs", {})
    for key in FALSE_RESPONSE_OUTPUTS:
        if outputs.get(key) is not False:
            fail(f"response {key} must be false")
    print("AI_ENTRY_AUTHORITY_DECISION_FIXTURES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
