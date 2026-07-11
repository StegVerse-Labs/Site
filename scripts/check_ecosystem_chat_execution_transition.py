#!/usr/bin/env python3
"""Validate dry-run execution transition separation, limits, and recoverability."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "execution-transition-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "execution-transition-response.example.json"


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

    if request.get("payload_type") != "execution_transition_request_preview":
        return fail("request payload_type drift")
    if response.get("payload_type") != "execution_transition_response_preview":
        return fail("response payload_type drift")
    if request.get("request_id") != response.get("request_id"):
        return fail("request_id mismatch")
    if request.get("preview_only") is not True or response.get("preview_only") is not True:
        return fail("execution transition must remain preview_only")
    if request.get("dry_run") is not True or response.get("dry_run") is not True:
        return fail("execution transition must remain dry_run")

    authority = request.get("authority_input", {})
    if authority.get("authority_result") != "ALLOW":
        return fail("execution transition must consume ALLOW authority input")
    if authority.get("authority_scope") != ["ecosystem_chat.gateway.evaluate"]:
        return fail("authority scope must remain evaluation-only")
    if authority.get("authority_receipt_present") is not False:
        return fail("preview must not claim authority receipt presence")
    if authority.get("authority_receipt_required") is not True:
        return fail("authority receipt must be required")

    revalidation = request.get("commit_time_revalidation", {})
    required_checks = (
        "identity_revalidated", "delegation_revalidated", "policy_revalidated",
        "evidence_freshness_revalidated", "operation_allowlist_revalidated",
        "resource_limits_revalidated", "all_passed",
    )
    for key in required_checks:
        if revalidation.get(key) is not True:
            return fail(f"request commit_time_revalidation.{key} must be true")

    operation = request.get("operation", {})
    if operation.get("mode") != "dry_run":
        return fail("operation mode must remain dry_run")
    for key in ("provider_invocation", "solver_execution", "repository_mutation", "raw_shell"):
        if operation.get(key) is not False:
            return fail(f"operation.{key} must be false")

    limits = request.get("resource_limits", {})
    expected_limits = {
        "max_provider_calls": 1,
        "max_solver_steps": 8,
        "max_execution_seconds": 5,
        "max_cost_usd": 0.01,
    }
    if limits != expected_limits:
        return fail("resource limits drift")

    recoverability = request.get("recoverability", {})
    for key in ("rollback_required", "rollback_available", "pre_state_captured", "operator_interrupt_supported"):
        if recoverability.get(key) is not True:
            return fail(f"request recoverability.{key} must be true")
    if recoverability.get("post_state_expected") is not False:
        return fail("dry-run must not expect post-state creation")

    receipt_expectation = request.get("receipt_expectation", {})
    if receipt_expectation.get("site_may_issue_receipt") is not False:
        return fail("Site must not issue receipts")
    if receipt_expectation.get("required_issuer") != "governed_backend_authority":
        return fail("backend authority must remain required issuer")

    consumed = response.get("authority_consumption", {})
    if consumed.get("authority_result") != "ALLOW" or consumed.get("authority_scope_matched") is not True:
        return fail("response must consume matching ALLOW authority")
    if consumed.get("authority_sufficient_for_execution") is not False:
        return fail("authority alone must not be sufficient for execution")

    commit = response.get("commit_time_revalidation", {})
    if commit.get("result") != "PASS" or commit.get("all_passed") is not True:
        return fail("commit-time revalidation must pass")

    execution = response.get("execution", {})
    if execution.get("result") != "DRY_RUN_ONLY" or execution.get("execution_enabled") is not False:
        return fail("execution must remain dry-run only and disabled")
    for key in ("provider_invoked", "solver_executed", "repository_mutated", "raw_shell_used", "state_changed"):
        if execution.get(key) is not False:
            return fail(f"execution.{key} must be false")

    use = response.get("resource_use", {})
    if any(value not in (0, 0.0) for value in use.values()):
        return fail("dry-run resource use must remain zero")

    recovered = response.get("recoverability", {})
    for key in ("rollback_required", "rollback_available", "pre_state_preserved", "operator_interrupt_preserved"):
        if recovered.get(key) is not True:
            return fail(f"response recoverability.{key} must be true")
    if recovered.get("rollback_performed") is not False or recovered.get("post_state_created") is not False:
        return fail("dry-run must not perform rollback or create post-state")

    receipt = response.get("receipt", {})
    if receipt.get("authority_receipt_issued") is not False or receipt.get("execution_receipt_issued") is not False:
        return fail("preview must not issue receipts")
    if receipt.get("receipt_id") is not None or receipt.get("receipt_issuer") is not None:
        return fail("preview receipt identity must remain null")

    continuity = response.get("continuity", {})
    for key in ("authority_execution_separated", "fail_closed", "replayable", "reconstructable", "site_local_mode_preserved"):
        if continuity.get(key) is not True:
            return fail(f"continuity.{key} must be true")

    print("PASS: dry-run consumes authority without collapsing authority into execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
