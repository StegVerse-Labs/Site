#!/usr/bin/env python3
"""Fail-closed validation for the StegVerse-owned endpoint activation boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "stegverse-endpoint-activation-readiness.json"
BINDING = ROOT / "assets" / "ecosystem-chat-live-binding.js"

EXPECTED_BINDINGS = {
    "STEGVERSE_PROVIDER_ENDPOINT",
    "STEGVERSE_PROVIDER_MODEL",
    "STEGVERSE_PROVIDER_TOKEN",
    "STEGVERSE_MASTER_RECORDS_ENDPOINT",
    "STEGVERSE_MASTER_RECORDS_TOKEN",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    binding = BINDING.read_text(encoding="utf-8")

    require(
        state.get("schema") == "stegverse.site.endpoint-activation-readiness.v1",
        "unexpected endpoint activation readiness schema",
    )
    require(state.get("owner") == "issue/24", "endpoint activation owner must remain issue/24")
    require(
        state.get("state") == "CONFIGURATION_AND_PERSISTENT_EXECUTION_REQUIRED",
        "endpoint activation must remain blocked until governed runtime evidence exists",
    )

    browser = state.get("canonical_browser_binding", {})
    require(browser.get("state") == "MERGED_AND_CI_BOUND", "canonical browser binding not recorded")
    require(browser.get("advertisement_verification_required") is True, "advertisement verification required")
    require(browser.get("health_verification_required") is True, "health verification required")
    require(browser.get("fail_closed_local_fallback") is True, "fail-closed fallback required")

    required_tokens = (
        "verified_provider_neutral_stegverse_node",
        "query:gateway",
        "window.STEGVERSE_ECOSYSTEM_GATEWAY_URL",
        "localStorage",
        "same-origin",
        "loopback",
        "provider_output_is_authority: false",
        "repository_mutation_authority: false",
    )
    for token in required_tokens:
        require(token in binding, f"canonical browser binding missing token: {token}")

    observed = state.get("latest_external_activation_observation", {})
    require(observed.get("state") == "CONFIGURATION_REQUIRED", "external observation state mismatch")
    require(
        observed.get("result_sha256") == "27dbe3f846913e0cd66221e377f6e5adcbcb6e7842a3b4565b160c310063745d",
        "external activation observation hash mismatch",
    )

    configured = set(state.get("required_authorized_bindings", []))
    require(configured == EXPECTED_BINDINGS, "authorized runtime binding set mismatch")

    gates = set(state.get("remaining_evidence_gates", []))
    for gate in {
        "persistent_stegverse_owned_endpoint_live",
        "real_provider_response_observed",
        "transition_reconstruction_verified",
        "immutable_zero_blocker_verified_receipt",
        "site_activation_complete",
        "downstream_propagation_verified",
    }:
        require(gate in gates, f"missing activation evidence gate: {gate}")

    authority = state.get("authority", {})
    require(authority and all(value is False for value in authority.values()), "authority must remain false")
    require(state.get("public_acquisition_authorized") is False, "public acquisition must remain unauthorized")
    require(state.get("manual_user_action_required") is False, "manual user action must not be assigned")

    print("StegVerse endpoint activation readiness: PASS (blocked truthfully)")


if __name__ == "__main__":
    main()
