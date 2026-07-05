#!/usr/bin/env python3
"""Verify AI Entry authority service boundary remains preview-only and non-executing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "data" / "ai-entry-authority-service-boundary.json"
FALSE_KEYS = (
    "authority_issued",
    "execution_allowed",
    "credential_access_allowed",
    "live_provider_calls_allowed",
    "live_sdk_calls_allowed",
    "activation_request_executes",
    "repo_mutation_allowed",
)
REQUIRED_INPUTS = {
    "activation_request",
    "actor_identity_context",
    "target_surface_context",
    "provider_capture_boundary",
    "receipt_issuer_boundary",
    "sdk_access_decision_boundary",
    "operator_recoverability_boundary",
}
REQUIRED_OUTPUTS = {
    "authority_decision",
    "decision_reason",
    "missing_preconditions",
    "execution_allowed",
    "credential_access_allowed",
    "live_calls_allowed",
}


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_AUTHORITY_SERVICE_BOUNDARY_FAIL: {message}")


def main() -> int:
    data = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.authority_service_boundary.v0.1":
        fail("bad schema version")
    if data.get("state") != "boundary_defined_non_executing":
        fail("state must remain boundary_defined_non_executing")
    service = data.get("authority_service", {})
    if service.get("decision_mode") != "preview_only":
        fail("decision mode must be preview_only")
    if service.get("default_decision") != "DENY":
        fail("default decision must be DENY")
    if set(data.get("required_inputs", [])) != REQUIRED_INPUTS:
        fail("required inputs mismatch")
    if set(data.get("required_outputs", [])) != REQUIRED_OUTPUTS:
        fail("required outputs mismatch")
    contract = data.get("non_executing_contract", {})
    for key in FALSE_KEYS:
        if contract.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_AUTHORITY_SERVICE_BOUNDARY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
