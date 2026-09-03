#!/usr/bin/env python3
"""Project the Site HIL InTr sync target from authentic ingress observation.

This script is intentionally incapable of discovering a runtime by itself. It
consumes an already-captured observation packet and either emits a conforming
non-authorizing target or fails closed. Source/CI cannot supply authentic runtime
evidence merely by executing this code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

OBSERVATION_SCHEMA = "stegverse.hil-intr-ingress-observation/v1"
PROFILE_SCHEMA = "stegverse.hil-intr-materialization-ingress-profile/v1"
TARGET_SCHEMA = "stegos.site.hil_intr_sync_target.v1"
PROFILE_PATH = "/intr/profile"
MATERIALIZATION_PATH = "/intr/materialization"
AUTHORITY_EFFECT = "NONE_DISCOVERY_ONLY"


class HILInTrTargetProjectionError(ValueError):
    pass


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise HILInTrTargetProjectionError(reason)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_hex(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical_bytes(value)
    return hashlib.sha256(raw).hexdigest()


def _https_profile_url(value: Any) -> tuple[str, str]:
    _require(isinstance(value, str) and bool(value), "observed_profile_url_required")
    parsed = urlsplit(value)
    _require(parsed.scheme == "https", "observed_profile_url_requires_https")
    _require(bool(parsed.hostname), "observed_profile_hostname_required")
    _require(not parsed.username and not parsed.password, "observed_profile_credentials_forbidden")
    _require(not parsed.query and not parsed.fragment, "observed_profile_query_or_fragment_forbidden")
    _require(parsed.path == PROFILE_PATH, "observed_profile_path_mismatch")
    origin = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    materialization = origin + MATERIALIZATION_PATH
    return value, materialization


def validate_profile(profile: Mapping[str, Any]) -> None:
    expected = {
        "schema": PROFILE_SCHEMA,
        "state": "ACTIVE_SOVEREIGN_INTR_INGRESS",
        "protocol": "InTr",
        "profile_path": PROFILE_PATH,
        "materialization_path": MATERIALIZATION_PATH,
        "direct_node_credential_requirement": "NONE",
        "direct_node_tvc_authorization_required": False,
        "relay_tvc_authorization_required": True,
        "event_triggered": True,
        "always_on_receiver_required": False,
        "second_user_device_required": False,
        "exact_request_validation_required": True,
        "write_once_queue_admission": True,
        "tls_enabled": True,
        "runtime_execution_attempted": False,
        "hil_receiver_readiness_claimed": False,
        "hil_custody_claimed": False,
        "g18_required": False,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_EVIDENCE_ONLY",
    }
    for field, value in expected.items():
        _require(profile.get(field) == value, f"profile_{field}_mismatch")
    origins = profile.get("supported_origins")
    _require(isinstance(origins, list), "profile_supported_origins_required")
    _require("STEGOS_NODE_OUTBOX" in origins, "profile_direct_node_origin_missing")
    _require("TVC_RELAY_EGRESS" in origins, "profile_relay_origin_missing")


def project_target(observation: Mapping[str, Any]) -> dict[str, Any]:
    _require(observation.get("schema") == OBSERVATION_SCHEMA, "observation_schema_invalid")
    _require(observation.get("observation_state") == "OBSERVED_HTTPS_PROFILE", "observation_state_invalid")
    _require(observation.get("https_observed") is True, "https_observation_required")
    _require(observation.get("http_status") == 200, "profile_http_status_mismatch")
    _require(observation.get("credential_used") is False, "profile_observation_credential_forbidden")
    _require(observation.get("github_token_runtime_authority") == "NONE", "observation_github_runtime_authority_forbidden")
    _require(observation.get("execution_authority") == "NONE", "observation_execution_authority_forbidden")
    _require(observation.get("authority_effect") == "NONE_OBSERVATION_ONLY", "observation_authority_effect_invalid")
    _require(isinstance(observation.get("observed_at"), str) and bool(observation.get("observed_at")), "observed_at_required")
    _require(isinstance(observation.get("evidence_ref"), str) and bool(observation.get("evidence_ref")), "evidence_ref_required")

    profile_url, ingress_url = _https_profile_url(observation.get("observed_profile_url"))
    profile = observation.get("profile")
    _require(isinstance(profile, Mapping), "profile_object_required")
    validate_profile(profile)
    actual_profile_sha = sha256_hex(profile)
    _require(observation.get("profile_sha256") == actual_profile_sha, "profile_sha256_mismatch")

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
        "authority_effect": AUTHORITY_EFFECT,
        "source_profile_url": profile_url,
        "source_profile_sha256": actual_profile_sha,
        "runtime_profile_observed_at": observation["observed_at"],
        "runtime_profile_evidence_ref": observation["evidence_ref"],
        "hil_execution_observed": False,
        "hil_receiver_readiness_observed": False,
        "hil_custody_observed": False,
        "g18_completion_required": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Project HIL InTr sync target from authentic runtime profile observation.")
    parser.add_argument("observation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    observation = json.loads(args.observation.read_text(encoding="utf-8"))
    if not isinstance(observation, dict):
        raise SystemExit("observation_object_required")
    target = project_target(observation)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(target, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(target, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
