#!/usr/bin/env python3
"""Validate positive authority evaluation while execution remains separate."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "authority-handshake-positive-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "authority-handshake-positive-response.example.json"


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

    if request.get("request_id") != response.get("request_id"):
        return fail("request_id mismatch")
    if request.get("preview_only") is not True or response.get("preview_only") is not True:
        return fail("positive fixtures must remain preview_only")
    if request.get("requested_local_mode_change") is not False:
        return fail("positive preview must not request local-mode change")

    actor = request.get("actor", {})
    delegation = request.get("delegation", {})
    policy = request.get("policy", {})
    evidence = request.get("evidence", {})
    operation = request.get("operation", {})
    limits = request.get("resource_limits", {})

    if actor.get("identity_verified") is not True:
        return fail("identity must be verified")
    if delegation.get("present") is not True or delegation.get("valid_at_request_time") is not True:
        return fail("delegation must be present and valid")
    if "ecosystem_chat.gateway.evaluate" not in delegation.get("scope", []):
        return fail("delegation scope missing gateway evaluation")
    if policy.get("policy_current") is not True:
        return fail("policy must be current")
    if evidence.get("freshness_checked") is not True or evidence.get("complete") is not True:
        return fail("evidence must be fresh-checked and complete")
    if operation.get("allowlisted") is not True or operation.get("name") != "ecosystem_chat.gateway.evaluate":
        return fail("operation must be the allowlisted evaluation operation")
    if operation.get("raw_shell_allowed") is not False or operation.get("repository_mutation_allowed") is not False:
        return fail("shell and repository mutation must remain disabled")
    if operation.get("provider_invocation_requested") is not False or operation.get("solver_execution_requested") is not False:
        return fail("positive authority preview must not request provider or solver execution")

    required_limits = {
        "max_provider_calls": 1,
        "max_solver_steps": 8,
        "max_execution_seconds": 5,
        "max_cost_usd": 0.01,
    }
    if limits != required_limits:
        return fail("resource limits must match the bounded positive fixture")

    authority = response.get("authority", {})
    execution = response.get("execution", {})
    receipt = response.get("receipt", {})
    continuity = response.get("continuity", {})

    if authority.get("result") != "ALLOW" or authority.get("authority_granted") is not True:
        return fail("authority must ALLOW")
    if authority.get("scope") != ["ecosystem_chat.gateway.evaluate"]:
        return fail("authority scope must remain evaluation-only")
    if execution.get("result") != "NOT_ATTEMPTED" or execution.get("execution_enabled") is not False:
        return fail("execution must remain separate and not attempted")
    for key in ("provider_invoked", "solver_executed", "repository_mutated"):
        if execution.get(key) is not False:
            return fail(f"execution.{key} must remain false")
    if receipt.get("authority_receipt_issued") is not False or receipt.get("execution_receipt_issued") is not False:
        return fail("preview must not issue receipts")
    if receipt.get("required_issuer") != "governed_backend_authority":
        return fail("governing backend must be the required receipt issuer")
    for key in ("fail_closed", "replayable_request", "reconstructable_decision", "local_mode_preserved", "authority_execution_separated"):
        if continuity.get(key) is not True:
            return fail(f"continuity.{key} must be true")
    if response.get("site_local_mode_before") is not True or response.get("site_local_mode_after") is not True:
        return fail("local mode must remain preserved")

    print("PASS: authority may ALLOW evaluation while execution remains NOT_ATTEMPTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
