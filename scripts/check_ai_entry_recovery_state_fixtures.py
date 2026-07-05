#!/usr/bin/env python3
"""Verify AI Entry recovery state fixtures remain preview-only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "recovery-state-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "recovery-state-response.example.json"
REQUEST_FALSE = ("confirm_recovery", "allow_activation", "allow_execution")
OUTPUT_FALSE = (
    "recovery_confirmed",
    "activation_allowed",
    "execution_allowed",
    "live_provider_calls_allowed",
    "live_sdk_calls_allowed",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RECOVERY_STATE_FIXTURES_FAIL: {message}")


def main() -> int:
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    response = json.loads(RESPONSE.read_text(encoding="utf-8"))
    if request.get("schema_version") != "stegverse.site.ai_entry.recovery_state_request.v0.1":
        fail("bad request schema version")
    if response.get("schema_version") != "stegverse.site.ai_entry.recovery_state_response.v0.1":
        fail("bad response schema version")
    if request.get("request_id") != response.get("request_id"):
        fail("request/response id mismatch")
    if request.get("activation_request_id") != response.get("activation_request_id"):
        fail("activation request id mismatch")
    if request.get("mode") != "preview_only" or response.get("response_state") != "preview_only":
        fail("fixtures must remain preview_only")
    requested = request.get("requested_result", {})
    for key in REQUEST_FALSE:
        if requested.get(key) is not False:
            fail(f"request {key} must be false")
    if response.get("recovery_decision") != "DENY":
        fail("response decision must be DENY")
    outputs = response.get("decision_outputs", {})
    for key in OUTPUT_FALSE:
        if outputs.get(key) is not False:
            fail(f"response {key} must be false")
    if not response.get("missing_preconditions"):
        fail("missing preconditions required")
    print("AI_ENTRY_RECOVERY_STATE_FIXTURES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
