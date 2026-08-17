#!/usr/bin/env python3
"""Fail-closed validation for the StegVerse-owned endpoint activation boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "stegverse-endpoint-activation-readiness.json"
BINDING = ROOT / "assets" / "ecosystem-chat-live-binding.js"

EXPECTED_BINDINGS = {
    "TVC_ROUTE_ADMITTED",
    "credential_requirement:NONE",
    "provider_secret_export:false",
    "master_records_custody:external",
    "provider_output_is_authority:false",
}
FORBIDDEN_SITE_BINDINGS = {
    "STEGVERSE_PROVIDER_TOKEN",
    "STEGVERSE_MASTER_RECORDS_TOKEN",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "GITHUB_PAT",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    binding = BINDING.read_text(encoding="utf-8")

    require(
        state.get("schema") == "stegverse.site.endpoint-activation-readiness.v2",
        "unexpected endpoint activation readiness schema",
    )
    require(state.get("owner") == "issue/24", "endpoint activation owner must remain issue/24")
    require(
        state.get("state") == "SOVEREIGN_RUNTIME_AND_TVC_ROUTE_EVIDENCE_REQUIRED",
        "endpoint activation must remain blocked until sovereign runtime and TVC route evidence exists",
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

    legacy = state.get("legacy_external_activation_observation", {})
    require(legacy.get("provenance_only") is True, "legacy observation must be provenance-only")
    require(legacy.get("current_authority") is False, "legacy observation must not retain current authority")
    require(
        legacy.get("result_sha256") == "27dbe3f846913e0cd66221e377f6e5adcbcb6e7842a3b4565b160c310063745d",
        "legacy activation observation hash mismatch",
    )

    governance = state.get("governance", {})
    require(governance.get("credential_authority") == "TV/TVC", "credential authority must be TV/TVC")
    require(governance.get("route_authority") == "StegVerse-Labs/TVC", "route authority must remain TVC")
    require(governance.get("credential_requirement") == "NONE", "Site endpoint readiness must require no credential")
    require(governance.get("non_tv_tvc_secret_or_token_allowed") is False, "NON-TV/TVC secrets/tokens prohibited")
    require(governance.get("github_token_runtime_authority") == "NONE", "GitHub token runtime authority prohibited")
    require(governance.get("provider_secret_export_allowed") is False, "provider secret export prohibited")
    require(governance.get("master_records_secret_export_allowed") is False, "Master Records secret export prohibited")
    require(governance.get("render_required") is False, "Render must not be required")
    require(governance.get("site_may_mint_route_authority") is False, "Site must not mint route authority")
    require(governance.get("site_may_mint_provider_authority") is False, "Site must not mint provider authority")
    require(governance.get("site_may_mint_custody_authority") is False, "Site must not mint custody authority")

    configured = set(state.get("required_authorized_bindings", []))
    require(configured == EXPECTED_BINDINGS, "authorized runtime binding set mismatch")
    require(configured.isdisjoint(FORBIDDEN_SITE_BINDINGS), "forbidden Site credential binding leaked into required bindings")
    require(set(state.get("forbidden_site_bindings", [])) == FORBIDDEN_SITE_BINDINGS, "forbidden Site binding list mismatch")

    gates = set(state.get("remaining_evidence_gates", []))
    for gate in {
        "sovereign_runtime_continuity_observed",
        "persistent_stegverse_owned_endpoint_live",
        "tvc_route_admitted_with_credential_requirement_none",
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

    print("STEGVERSE_ENDPOINT_READINESS=PASS_BLOCKED")
    print("STEGVERSE_ENDPOINT_CREDENTIAL_AUTHORITY=TV_TVC")
    print("STEGVERSE_ENDPOINT_CREDENTIAL_REQUIREMENT=NONE")
    print("STEGVERSE_ENDPOINT_NON_TV_TVC_SECRET_OR_TOKEN_ALLOWED=false")
    print("STEGVERSE_ENDPOINT_GITHUB_TOKEN_RUNTIME_AUTHORITY=NONE")
    print("STEGVERSE_ENDPOINT_RENDER_REQUIRED=false")
    print("STEGVERSE_ENDPOINT_AUTHORITY_EFFECT=NONE")


if __name__ == "__main__":
    main()
