#!/usr/bin/env python3
"""Verify backend activation request/response fixtures remain preview-only and fail-closed."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "backend-activation-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "backend-activation-response.example.json"
REQUEST_FALSE = (
    "live_calls_requested",
)
AUTHORITY_FALSE = (
    "authority_issued",
    "execution_allowed",
    "credential_access_allowed",
)
CAPABILITY_FALSE = (
    "provider_adapter_calls",
    "sdk_access_calls",
    "receipt_issuer",
    "repo_mutation",
)
RESPONSE_FALSE = (
    "provider_call_performed",
    "sdk_call_performed",
    "credential_lookup_performed",
    "real_receipt_issued",
    "execution_authority_issued",
    "repo_mutation_performed",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_BACKEND_ACTIVATION_FIXTURES_FAIL: {message}")


def main() -> int:
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    response = json.loads(RESPONSE.read_text(encoding="utf-8"))
    if request.get("schema_version") != "stegverse.ai_entry.backend_activation_request.v0.1":
        fail("bad request schema version")
    if response.get("schema_version") != "stegverse.ai_entry.backend_activation_response.v0.1":
        fail("bad response schema version")
    if request.get("request_id") != response.get("request_id"):
        fail("request/response id mismatch")
    if request.get("route_id") != "activation_request_preview" or response.get("route_id") != "activation_request_preview":
        fail("route id mismatch")
    if request.get("mode") != "preview_only":
        fail("request mode must be preview_only")
    for key in REQUEST_FALSE:
        if request.get(key) is not False:
            fail(f"{key} must be false")
    authority = request.get("authority_boundary", {})
    if authority.get("authority_required") is not True:
        fail("authority_required must be true")
    for key in AUTHORITY_FALSE:
        if authority.get(key) is not False:
            fail(f"{key} must be false")
    capabilities = request.get("requested_capabilities", {})
    for key in CAPABILITY_FALSE:
        if capabilities.get(key) is not False:
            fail(f"{key} must be false")
    fail_closed = request.get("fail_closed_boundary", {})
    if fail_closed.get("default_decision") != "DENY":
        fail("request default decision must be DENY")
    if fail_closed.get("activation_request_executes") is not False:
        fail("activation_request_executes must be false")
    if response.get("decision") != "DENY":
        fail("response decision must be DENY")
    if response.get("activation_state") != "not_activated_fail_closed":
        fail("response must remain not_activated_fail_closed")
    boundary = response.get("response_boundary", {})
    for key in RESPONSE_FALSE:
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_BACKEND_ACTIVATION_FIXTURES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
