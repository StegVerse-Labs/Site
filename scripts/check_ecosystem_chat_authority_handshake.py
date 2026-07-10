#!/usr/bin/env python3
"""Validate the preview-only backend authority handshake contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "authority-handshake-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "authority-handshake-response.example.json"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain an object")
    return data


def main() -> int:
    request = load(REQUEST)
    response = load(RESPONSE)

    if request.get("payload_type") != "authority_handshake_request_preview":
        return fail("request payload_type drift")
    if response.get("payload_type") != "authority_handshake_response_preview":
        return fail("response payload_type drift")
    if request.get("preview_only") is not True or response.get("preview_only") is not True:
        return fail("handshake fixtures must remain preview_only")
    if request.get("request_id") != response.get("request_id"):
        return fail("request_id mismatch")

    required_request_sections = {
        "actor", "delegation", "policy", "evidence", "operation",
        "resource_limits", "provider_posture", "solver_posture", "receipt_expectation",
    }
    missing = sorted(required_request_sections - set(request))
    if missing:
        return fail("request missing sections: " + ", ".join(missing))

    actor = request["actor"]
    delegation = request["delegation"]
    policy = request["policy"]
    evidence = request["evidence"]
    operation = request["operation"]
    limits = request["resource_limits"]
    provider = request["provider_posture"]
    solver = request["solver_posture"]
    receipt_expectation = request["receipt_expectation"]

    if actor.get("identity_verified") is not False:
        return fail("preview actor must remain unverified")
    if delegation.get("present") is not False or delegation.get("valid_at_request_time") is not False:
        return fail("preview delegation must remain absent and invalid")
    if policy.get("policy_current") is not False:
        return fail("preview policy must not be current")
    if evidence.get("freshness_checked") is not False or evidence.get("complete") is not False:
        return fail("preview evidence must remain unchecked and incomplete")
    if operation.get("allowlisted") is not False:
        return fail("preview operation must not be allowlisted")
    if operation.get("raw_shell_allowed") is not False or operation.get("repository_mutation_allowed") is not False:
        return fail("shell and repository mutation must remain disabled")
    if provider.get("live_invocation") is not False or solver.get("live_solver_execution") is not False:
        return fail("provider and solver execution must remain disabled")
    if receipt_expectation.get("site_may_issue_receipt") is not False:
        return fail("Site must not issue authority or execution receipts")

    for key, value in limits.items():
        if value != 0 and value != 0.0:
            return fail(f"preview resource limit {key} must remain zero")

    authority = response.get("authority", {})
    execution = response.get("execution", {})
    receipt = response.get("receipt", {})
    continuity = response.get("continuity", {})

    if authority.get("result") != "DENY" or authority.get("authority_granted") is not False:
        return fail("authority response must deny")
    required_reasons = {
        "IDENTITY_UNVERIFIED", "DELEGATION_ABSENT", "POLICY_NOT_CURRENT",
        "EVIDENCE_INCOMPLETE", "OPERATION_NOT_ALLOWLISTED",
    }
    if not required_reasons.issubset(set(authority.get("reason_codes", []))):
        return fail("authority response missing required reason codes")
    if execution.get("result") != "NOT_ATTEMPTED" or execution.get("execution_enabled") is not False:
        return fail("execution must remain not attempted and disabled")
    for key in ("provider_invoked", "solver_executed", "repository_mutated"):
        if execution.get(key) is not False:
            return fail(f"execution.{key} must be false")
    if receipt.get("authority_receipt_issued") is not False or receipt.get("execution_receipt_issued") is not False:
        return fail("no receipt may be issued by the preview")
    if receipt.get("receipt_id") is not None or receipt.get("receipt_issuer") is not None:
        return fail("preview receipt identity must remain null")
    if response.get("site_local_mode_before") is not True or response.get("site_local_mode_after") is not True:
        return fail("local mode must remain enabled")
    for key in ("fail_closed", "replayable_request", "reconstructable_decision", "local_mode_preserved"):
        if continuity.get(key) is not True:
            return fail(f"continuity.{key} must be true")

    print("PASS: authority handshake preview denies, fails closed, and preserves local mode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
