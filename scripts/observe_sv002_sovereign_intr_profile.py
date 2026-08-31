#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROFILE_URL = "https://stegverse.org/intr/profile"
UNIVERSAL_SCHEMA = "stegverse.universal-intr-profiled-ingress/v1"
HIL_SCHEMA = "stegverse.hil-intr-materialization-ingress-profile/v1"
SV002_PROFILE = "SV002:PublicObservation"
HB_PROFILE_SCHEMA = "stegverse.intr.hb-derived-carrier-profile/v1"
HB_BINDING_SCHEMA = "stegverse.intr.hb-derived-carrier-binding/v1"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def validate_profile(profile: dict[str, Any]) -> dict[str, bool]:
    schema = profile.get("schema")
    profiles = (
        profile.get("profiles")
        if schema == UNIVERSAL_SCHEMA
        else profile.get("additional_materialization_profiles")
    )
    common = {
        "schema_supported": schema in {UNIVERSAL_SCHEMA, HIL_SCHEMA},
        "state_active": profile.get("state") == "ACTIVE_SOVEREIGN_INTR_INGRESS",
        "protocol_intr": profile.get("protocol") == "InTr",
        "profile_path": profile.get("profile_path") == "/intr/profile",
        "materialization_path": profile.get("materialization_path") == "/intr/materialization",
        "event_triggered": profile.get("event_triggered") is True,
        "second_user_device_not_required": profile.get("second_user_device_required") is False,
        "g18_not_required": profile.get("g18_required") is False,
        "tls_enabled": profile.get("tls_enabled") is True,
        "credential_authority_tvtvc": profile.get("credential_authority") == "TV/TVC",
        "github_runtime_authority_none": profile.get("github_token_runtime_authority") == "NONE",
        "execution_authority_none": profile.get("execution_authority") == "NONE",
        "discovery_authority_effect_only": profile.get("authority_effect") == "NONE_DISCOVERY_EVIDENCE_ONLY",
        "stegos_node_outbox_supported": isinstance(profile.get("supported_origins"), list)
        and "STEGOS_NODE_OUTBOX" in profile.get("supported_origins", []),
        "sv002_profile_advertised": isinstance(profiles, list) and SV002_PROFILE in profiles,
    }
    if schema == UNIVERSAL_SCHEMA:
        carrier = profile.get("heartbeat_derived_carrier")
        common.update(
            {
                "always_on_application_receiver_not_required": profile.get(
                    "always_on_application_receiver_required"
                )
                is False,
                "hb_carrier_present": isinstance(carrier, dict),
                "hb_carrier_schema": isinstance(carrier, dict)
                and carrier.get("schema") == HB_PROFILE_SCHEMA,
                "hb_binding_schema": isinstance(carrier, dict)
                and carrier.get("binding_schema") == HB_BINDING_SCHEMA,
                "hb_100hz": isinstance(carrier, dict)
                and carrier.get("reference_frequency_hz") == 100,
                "hb_10ms": isinstance(carrier, dict)
                and carrier.get("heartbeat_period_ms") == 10,
                "hb_oscillator_only": isinstance(carrier, dict)
                and carrier.get("progression_dependency") == "OSCILLATOR_ONLY",
                "hb_channel_family": isinstance(carrier, dict)
                and carrier.get("channel_family") == "H1_PHASE_SLOTS",
                "hb_channel_count": isinstance(carrier, dict)
                and carrier.get("channel_count") == 16,
                "hb_channel_selection": isinstance(carrier, dict)
                and carrier.get("channel_selection")
                == "PAYLOAD_SHA256_FIRST64_MOD_16",
                "hb_carrier_non_authorizing": isinstance(carrier, dict)
                and carrier.get("carrier_presence_grants_admission_authority") is False
                and carrier.get("carrier_presence_grants_execution_authority") is False
                and carrier.get("carrier_presence_grants_credential_authority") is False
                and carrier.get("carrier_presence_grants_routing_authority") is False
                and carrier.get("carrier_presence_grants_transition_authority") is False
                and carrier.get("carrier_presence_grants_receiving_authority") is False,
            }
        )
    elif schema == HIL_SCHEMA:
        common.update(
            {
                "always_on_receiver_not_required": profile.get("always_on_receiver_required")
                is False,
                "direct_node_credentials_none": profile.get(
                    "direct_node_credential_requirement"
                )
                == "NONE",
                "direct_node_tvc_authorization_not_required": profile.get(
                    "direct_node_tvc_authorization_required"
                )
                is False,
                "exact_request_validation": profile.get("exact_request_validation_required")
                is True,
                "write_once_queue_admission": profile.get("write_once_queue_admission") is True,
            }
        )
    return common


def observe(output_dir: Path, attempts: int, delay_seconds: int) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    last_receipt: dict[str, Any] | None = None
    for attempt in range(1, attempts + 1):
        body = b""
        headers: dict[str, str] = {}
        status = None
        error = None
        try:
            req = urllib.request.Request(
                f"{PROFILE_URL}?sv002_profile_proof={int(time.time())}-{attempt}",
                headers={
                    "Accept": "application/json",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-Agent": "StegVerse-SV002-InTr-Profile-Observer/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                status = int(response.status)
                body = response.read()
                headers = {k.lower(): v for k, v in response.headers.items()}
        except Exception as exc:
            error = repr(exc)

        profile = None
        checks: dict[str, bool] = {}
        if status == 200:
            try:
                parsed = json.loads(body)
                if isinstance(parsed, dict):
                    profile = parsed
                    checks = validate_profile(parsed)
                else:
                    error = "profile response is not a JSON object"
            except Exception as exc:
                error = "profile JSON parse failed: " + repr(exc)

        conforming = status == 200 and profile is not None and bool(checks) and all(checks.values())
        classification = "OBSERVED_CONFORMING" if conforming else "OBSERVED_BLOCKED"
        receipt = {
            "schema": "stegverse.sv002-sovereign-intr-profile-proof/v1",
            "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "attempt": attempt,
            "profile_url": PROFILE_URL,
            "http_status": status,
            "profile_sha256_raw": hashlib.sha256(body).hexdigest() if body else None,
            "profile_sha256_canonical": hashlib.sha256(canonical_bytes(profile)).hexdigest()
            if isinstance(profile, dict)
            else None,
            "profile_schema": profile.get("schema") if isinstance(profile, dict) else None,
            "checks": checks,
            "classification": classification,
            "error": error,
            "credential_used": False,
            "github_actions_runtime_authority": False,
            "execution_authority": False,
            "authority_effect": "NONE_OBSERVATION_ONLY",
            "activation_effect": False,
            "target_projection_performed": False,
            "receiver_readiness_observed": False,
            "observation_round_trip_observed": False,
            "principal_experiment_observed": False,
            "master_records_reconstruction_observed": False,
        }
        last_receipt = receipt
        (output_dir / "profile.body").write_bytes(body)
        (output_dir / "profile.headers.json").write_text(
            json.dumps(headers, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (output_dir / "profile.parsed.json").write_text(
            json.dumps(profile, indent=2, sort_keys=True) + "\n"
            if isinstance(profile, dict)
            else "null\n",
            encoding="utf-8",
        )
        (output_dir / "receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if conforming:
            return receipt
        if attempt < attempts:
            time.sleep(delay_seconds)

    assert last_receipt is not None
    return last_receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evidence/sv002-sovereign-intr-profile"),
    )
    parser.add_argument("--attempts", type=int, default=6)
    parser.add_argument("--delay-seconds", type=int, default=10)
    args = parser.parse_args()
    receipt = observe(args.output_dir, args.attempts, args.delay_seconds)
    print(json.dumps(receipt, sort_keys=True))
    # Observation completes successfully even when blocked; classification is the evidence.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
