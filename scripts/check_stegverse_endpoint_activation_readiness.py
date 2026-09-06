#!/usr/bin/env python3
"""Fail-closed validation for the StegVerse-owned endpoint activation boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "stegverse-endpoint-activation-readiness.json"
BINDING = ROOT / "assets" / "ecosystem-chat-live-binding.js"

COMPATIBILITY_STATE = "CONFIGURATION_AND_PERSISTENT_EXECUTION_REQUIRED"
CURRENT_BLOCKER_STATE = "AUTHENTIC_SOVEREIGN_EXECUTION_AND_CUSTODY_RECONSTRUCTION_REQUIRED"
EXPECTED_MISSING_PREDICATES = {
    "real_model_process_observed",
    "private_endpoint_only",
    "ephemeral_e1_e2_execution_observed",
    "measured_usage_persisted",
    "provider_usage_reconstruction_pass",
    "transition_reconstruction_pass",
}
PROHIBITED_TOKEN_PREREQUISITES = {
    "STEGVERSE_PROVIDER_TOKEN",
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
        state.get("state") == COMPATIBILITY_STATE,
        "legacy endpoint activation compatibility state must remain stable",
    )
    require(
        state.get("state_semantics") == "COMPATIBILITY_CLASS_ONLY",
        "legacy readiness state must be explicitly compatibility-only",
    )
    require(
        state.get("current_blocker_state") == CURRENT_BLOCKER_STATE,
        "current endpoint blocker must require authentic sovereign execution and custody/reconstruction evidence",
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
    require(observed.get("repository") == "StegVerse-Labs/.github", "current carrier repository mismatch")
    require(
        observed.get("path") == "receipts/ecosystem-chat-sovereign-inference/SHWP-ECOSYSTEM-CHAT-INFERENCE-001.json",
        "current carrier receipt path mismatch",
    )
    require(observed.get("task_id") == "SHWP-ECOSYSTEM-CHAT-INFERENCE-001", "current carrier task mismatch")
    require(
        observed.get("transition_id") == "SOVEREIGN_LOCAL_MODEL_RUNTIME_NOT_YET_VERIFIED",
        "current carrier transition mismatch",
    )
    require(observed.get("completed") is False, "unverified carrier receipt must remain incomplete")

    require(state.get("credential_authority") == "TV/TVC", "credential authority must remain TV/TVC")
    require(state.get("credential_requirement") == "NONE", "canonical local route credential requirement must be NONE")
    configured = set(state.get("required_authorized_bindings", []))
    require(not configured, "provider or custody bearer-token bindings must not be canonical activation prerequisites")

    prohibited = set(state.get("prohibited_activation_prerequisites", []))
    require(
        PROHIBITED_TOKEN_PREREQUISITES.issubset(prohibited),
        "provider and Master Records token prerequisites must be explicitly prohibited",
    )
    require(state.get("third_party_dependency_is_blocker") is False, "third-party dependency must not block canonical activation")
    require(state.get("third_party_inference_required") is False, "third-party inference must not be required")

    gates = set(state.get("remaining_evidence_gates", []))
    require(
        EXPECTED_MISSING_PREDICATES.issubset(gates),
        "current sovereign execution/custody evidence gates are incomplete",
    )
    for gate in {
        "immutable_zero_blocker_verified_receipt",
        "site_activation_complete",
        "downstream_propagation_verified",
    }:
        require(gate in gates, f"missing activation evidence gate: {gate}")
    require(
        "authorized_bindings_present_at_runtime_secret_boundary" not in gates,
        "superseded provider-token binding gate must not return",
    )

    authority = state.get("authority", {})
    require(authority and all(value is False for value in authority.values()), "authority must remain false")
    require(state.get("public_acquisition_authorized") is False, "public acquisition must remain unauthorized")
    require(state.get("manual_user_action_required") is False, "manual user action must not be assigned")

    print("StegVerse endpoint activation readiness: PASS (authentic sovereign execution/custody still required)")


if __name__ == "__main__":
    main()
