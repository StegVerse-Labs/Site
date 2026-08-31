#!/usr/bin/env python3
"""Project the SV002 Node InTr sync target from authentic HTTPS ingress evidence.

This module performs no network discovery. It consumes an independently captured
observation packet and fails closed unless the observed /intr/profile proves a
shared sovereign materialization ingress that explicitly supports
SV002:PublicObservation.
"""
from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

OBSERVATION_SCHEMA = "stegverse.universal-intr-ingress-observation/v1"
UNIVERSAL_PROFILE_SCHEMA = "stegverse.universal-intr-profiled-ingress/v1"
HIL_PROFILE_SCHEMA = "stegverse.hil-intr-materialization-ingress-profile/v1"
TARGET_SCHEMA = "stegos.site.sv002_intr_sync_target.v1"
PROFILE_PATH = "/intr/profile"
MATERIALIZATION_PATH = "/intr/materialization"
SV002_PROFILE = "SV002:PublicObservation"
HB_CARRIER_PROFILE_SCHEMA = "stegverse.intr.hb-derived-carrier-profile/v1"
HB_CARRIER_BINDING_SCHEMA = "stegverse.intr.hb-derived-carrier-binding/v1"


class ProjectionError(ValueError):
    pass


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ProjectionError(reason)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_hex(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical_bytes(value)
    return hashlib.sha256(raw).hexdigest()


def profile_urls(value: Any) -> tuple[str, str]:
    require(isinstance(value, str) and bool(value), "observed_profile_url_required")
    parsed = urlsplit(value)
    require(parsed.scheme == "https", "observed_profile_url_requires_https")
    require(bool(parsed.hostname), "observed_profile_hostname_required")
    require(not parsed.username and not parsed.password, "observed_profile_credentials_forbidden")
    require(not parsed.query and not parsed.fragment, "observed_profile_query_or_fragment_forbidden")
    require(parsed.path == PROFILE_PATH, "observed_profile_path_mismatch")
    origin = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    return value, origin + MATERIALIZATION_PATH


def validate_profile(profile: Mapping[str, Any]) -> str:
    schema = profile.get("schema")
    require(schema in {UNIVERSAL_PROFILE_SCHEMA, HIL_PROFILE_SCHEMA}, "profile_schema_invalid")
    common = {
        "state": "ACTIVE_SOVEREIGN_INTR_INGRESS",
        "protocol": "InTr",
        "profile_path": PROFILE_PATH,
        "materialization_path": MATERIALIZATION_PATH,
        "event_triggered": True,
        "second_user_device_required": False,
        "g18_required": False,
        "tls_enabled": True,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_EVIDENCE_ONLY",
    }
    for field, expected in common.items():
        require(profile.get(field) == expected, f"profile_{field}_mismatch")
    origins = profile.get("supported_origins")
    require(isinstance(origins, list) and "STEGOS_NODE_OUTBOX" in origins, "profile_direct_node_origin_missing")
    if schema == UNIVERSAL_PROFILE_SCHEMA:
        require(profile.get("always_on_application_receiver_required") is False, "profile_always_on_receiver_forbidden")
        profiles = profile.get("profiles")
        require(isinstance(profiles, list) and SV002_PROFILE in profiles, "profile_sv002_support_missing")
        carrier = profile.get("heartbeat_derived_carrier")
        require(isinstance(carrier, Mapping), "profile_hb_carrier_missing")
        expected_carrier = {
            "schema": HB_CARRIER_PROFILE_SCHEMA,
            "state": "SUPPORTED_MIGRATION_OPTIONAL",
            "fundamental_mode": "HB",
            "reference_frequency_hz": 100,
            "heartbeat_period_ms": 10,
            "progression_dependency": "OSCILLATOR_ONLY",
            "reference_derivation": "HB32_PROTOCOL_ANCHOR_PLUS_ELAPSED_10MS_QUANTA",
            "binding_schema": HB_CARRIER_BINDING_SCHEMA,
            "channel_family": "H1_PHASE_SLOTS",
            "channel_count": 16,
            "channel_selection": "SHA256_PACKET_ID_FIRST32_MOD_16",
            "carrier_binding_required": False,
            "legacy_unbound_packets_temporarily_accepted": True,
            "carrier_presence_grants_admission_authority": False,
            "carrier_presence_grants_execution_authority": False,
            "carrier_presence_grants_credential_authority": False,
            "carrier_presence_grants_routing_authority": False,
            "carrier_presence_grants_transition_authority": False,
            "carrier_presence_grants_receiving_authority": False,
            "credential_authority": "TV/TVC",
            "authority_effect": "NONE_DISCOVERY_EVIDENCE_ONLY",
        }
        for field, expected in expected_carrier.items():
            require(carrier.get(field) == expected, f"profile_hb_carrier_{field}_mismatch")
    else:
        require(profile.get("always_on_receiver_required") is False, "profile_always_on_receiver_forbidden")
        require(profile.get("direct_node_credential_requirement") == "NONE", "profile_direct_node_credential_requirement_invalid")
        require(profile.get("direct_node_tvc_authorization_required") is False, "profile_direct_node_tvc_authorization_invalid")
        require(profile.get("exact_request_validation_required") is True, "profile_exact_request_validation_required")
        require(profile.get("write_once_queue_admission") is True, "profile_write_once_admission_required")
        profiles = profile.get("additional_materialization_profiles")
        require(isinstance(profiles, list) and SV002_PROFILE in profiles, "profile_sv002_support_missing")
    return str(schema)


def project_target(observation: Mapping[str, Any]) -> dict[str, Any]:
    require(observation.get("schema") == OBSERVATION_SCHEMA, "observation_schema_invalid")
    require(observation.get("observation_state") == "OBSERVED_HTTPS_PROFILE", "observation_state_invalid")
    require(observation.get("https_observed") is True, "https_observation_required")
    require(observation.get("http_status") == 200, "profile_http_status_mismatch")
    require(observation.get("credential_used") is False, "profile_observation_credential_forbidden")
    require(observation.get("github_token_runtime_authority") == "NONE", "observation_github_runtime_authority_forbidden")
    require(observation.get("execution_authority") == "NONE", "observation_execution_authority_forbidden")
    require(observation.get("authority_effect") == "NONE_OBSERVATION_ONLY", "observation_authority_effect_invalid")
    require(isinstance(observation.get("observed_at"), str) and bool(observation["observed_at"]), "observed_at_required")
    require(isinstance(observation.get("evidence_ref"), str) and bool(observation["evidence_ref"]), "evidence_ref_required")
    profile_url, ingress_url = profile_urls(observation.get("observed_profile_url"))
    profile = observation.get("profile")
    require(isinstance(profile, Mapping), "profile_object_required")
    profile_schema = validate_profile(profile)
    actual_sha = sha256_hex(profile)
    require(observation.get("profile_sha256") == actual_sha, "profile_sha256_mismatch")
    return {
        "schema": TARGET_SCHEMA,
        "state": "CONFORMING_SOVEREIGN_INTR_INGRESS",
        "ingress_url": ingress_url,
        "transport_origin": "STEGOS_NODE_OUTBOX",
        "runtime_ingress_observed": True,
        "configuration_authority": "StegVerse sovereign runtime evidence projection",
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_ONLY",
        "source_profile_url": profile_url,
        "source_profile_schema": profile_schema,
        "source_profile_sha256": actual_sha,
        "runtime_profile_observed_at": observation["observed_at"],
        "runtime_profile_evidence_ref": observation["evidence_ref"],
        "sv002_materialization_profile_observed": True,
        "hb_derived_carrier_profile_observed": profile_schema == UNIVERSAL_PROFILE_SCHEMA,
        "hb_derived_carrier_profile_schema": profile.get("heartbeat_derived_carrier", {}).get("schema"),
        "hb_derived_carrier_binding_schema": profile.get("heartbeat_derived_carrier", {}).get("binding_schema"),
        "hb_derived_carrier_grants_authority": False,
        "receiver_readiness_observed": False,
        "observation_round_trip_observed": False,
        "principal_experiment_observed": False,
        "master_records_reconstruction_observed": False,
        "g18_completion_required": False,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("observation", type=Path)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    value = json.loads(a.observation.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "observation_object_required")
    target = project_target(value)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(target, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(target, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
