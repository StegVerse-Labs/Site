#!/usr/bin/env python3
"""Project SV-DN-1 browser evidence InTr target from authentic HTTPS ingress evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

OBSERVATION_SCHEMA = "stegverse.universal-intr-ingress-observation/v1"
UNIVERSAL_PROFILE_SCHEMA = "stegverse.universal-intr-profiled-ingress/v1"
HIL_PROFILE_SCHEMA = "stegverse.hil-intr-materialization-ingress-profile/v1"
TARGET_SCHEMA = "stegos.site.sv_dn1_browser_evidence_intr_target.v1"
PROFILE_PATH = "/intr/profile"
MATERIALIZATION_PATH = "/intr/materialization"
PROFILE = "SV-DN1:BrowserObservation"
ORIGIN = "STEGOS_WEB_BOOTSTRAP_EGRESS"


class ProjectionError(ValueError):
    pass


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ProjectionError(reason)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


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
    require(isinstance(origins, list) and ORIGIN in origins, "profile_web_bootstrap_origin_missing")

    if schema == UNIVERSAL_PROFILE_SCHEMA:
        require(
            profile.get("always_on_application_receiver_required") is False,
            "profile_always_on_receiver_forbidden",
        )
        profiles = profile.get("profiles")
        require(isinstance(profiles, list) and PROFILE in profiles, "profile_sv_dn1_support_missing")
    else:
        require(profile.get("always_on_receiver_required") is False, "profile_always_on_receiver_forbidden")
        require(
            profile.get("direct_node_credential_requirement") == "NONE",
            "profile_direct_node_credential_requirement_invalid",
        )
        require(
            profile.get("direct_node_tvc_authorization_required") is False,
            "profile_direct_node_tvc_authorization_invalid",
        )
        require(profile.get("exact_request_validation_required") is True, "profile_exact_request_validation_required")
        require(profile.get("write_once_queue_admission") is True, "profile_write_once_admission_required")
        profiles = profile.get("additional_materialization_profiles")
        require(isinstance(profiles, list) and PROFILE in profiles, "profile_sv_dn1_support_missing")
    return str(schema)


def project_target(observation: Mapping[str, Any]) -> dict[str, Any]:
    require(observation.get("schema") == OBSERVATION_SCHEMA, "observation_schema_invalid")
    require(observation.get("observation_state") == "OBSERVED_HTTPS_PROFILE", "observation_state_invalid")
    require(observation.get("https_observed") is True, "https_observation_required")
    require(observation.get("http_status") == 200, "profile_http_status_mismatch")
    require(observation.get("credential_used") is False, "profile_observation_credential_forbidden")
    require(
        observation.get("github_token_runtime_authority") == "NONE",
        "observation_github_runtime_authority_forbidden",
    )
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
        "transport_origin": ORIGIN,
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
        "sv_dn1_browser_observation_profile_observed": True,
        "receiver_readiness_observed": False,
        "sdk_admission_observed": False,
        "governance_decision_observed": False,
        "master_records_custody_observed": False,
        "public_promotion_observed": False,
        "g18_completion_required": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = json.loads(args.observation.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "observation_object_required")
    target = project_target(value)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(target, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(target, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
