#!/usr/bin/env python3
"""Execute the Site-to-portable-node runtime slice with authenticated custody."""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "portable-node-site-runtime.json"
BASE_URL = os.getenv("STEGVERSE_TEST_NODE_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def canonical_sha256(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fetch_json(url: str, *, data: dict | None = None, headers: dict[str, str] | None = None) -> dict:
    body = None if data is None else json.dumps(data).encode("utf-8")
    request = Request(url, data=body, headers=headers or {}, method="POST" if body is not None else "GET")
    with urlopen(request, timeout=10) as response:
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"HTTP {response.status} from {url}")
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object from {url}")
    return value


def wait_for_health() -> dict:
    last_error = "unobserved"
    for _ in range(60):
        try:
            health = fetch_json(f"{BASE_URL}/health")
            if health.get("status") == "ok":
                return health
        except (OSError, URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(1)
    raise RuntimeError(f"portable node health not ready: {last_error}")


def main() -> int:
    blockers: list[str] = []
    evidence: dict[str, object] = {}

    try:
        health = wait_for_health()
        evidence["health"] = health
        if health.get("governed_provider_enabled") is not False:
            blockers.append("provider_not_fail_closed")
        if health.get("storage_durable_across_restarts") is not True:
            blockers.append("durability_not_declared")
        if health.get("master_records_submission_enabled") is not True:
            blockers.append("master_records_submission_not_enabled")

        advertisement = fetch_json(f"{BASE_URL}/api/stegverse-node")
        evidence["advertisement"] = advertisement
        claimed = advertisement.get("advertisement_sha256")
        binding = dict(advertisement)
        binding.pop("advertisement_sha256", None)
        if advertisement.get("schema") != "stegverse.node.endpoint-advertisement.v1":
            blockers.append("advertisement_schema_invalid")
        if advertisement.get("node_id") != "ecosystem-chat-portable-node":
            blockers.append("portable_node_identity_invalid")
        if advertisement.get("capability_id") != "ecosystem-chat-gateway":
            blockers.append("capability_identity_invalid")
        if advertisement.get("health_bound") is not True:
            blockers.append("advertisement_not_health_bound")
        for key in ("authority_granted", "publication_authority", "execution_authority"):
            if advertisement.get(key) is not False:
                blockers.append(f"advertisement_{key}_must_be_false")
        if claimed != canonical_sha256(binding):
            blockers.append("advertisement_digest_invalid")
        if advertisement.get("endpoint") != f"{BASE_URL}/api/ecosystem-chat":
            blockers.append("advertised_chat_endpoint_mismatch")
        if advertisement.get("health_endpoint") != f"{BASE_URL}/health":
            blockers.append("advertised_health_endpoint_mismatch")

        identity = {
            "transition_id": "transition.site.runtime-proof.0001",
            "run_id": "site-runtime-proof.0001",
            "event_id": "site-runtime-proof:event:0001",
            "origin_manifest_id": "origin.site.runtime-proof.0001",
            "parent_transition_id": None,
            "previous_receipt_id": None,
        }
        request_payload = {
            "message": "Explain the current governed Ecosystem Chat runtime boundary.",
            "session_id": "site-runtime-proof-session",
            "requested_route": "Site",
            "transition_intent": "explain",
            "transition_destination": "ecosystem-chat.html#how-it-works",
            "goal": "verify the existing Site-to-portable-node custody path",
            "execution_model": "allowlisted_task_request_only",
            "raw_shell_allowed": False,
            "authority_required": True,
            "rate_limit_required": True,
            "receipt_required_for_execution": True,
            "interaction_profile": {"governance": 100},
            "interaction_bands": ["intra", "receipt"],
            "math_solver_supported": True,
            "transition_identity": identity,
        }
        response = fetch_json(
            advertisement["endpoint"],
            data=request_payload,
            headers={"Content-Type": "application/json", "X-SteGVerse-Session": request_payload["session_id"]},
        )
        evidence["governed_response"] = response
        for key in ("transition_id", "run_id", "event_id", "origin_manifest_id"):
            if response.get(key) != identity[key]:
                blockers.append(f"response_{key}_mismatch")
        provider = response.get("provider") or {}
        if provider.get("used") is True:
            blockers.append("provider_unexpectedly_used")
        authority = response.get("authority") or {}
        if authority.get("provider_output_is_authority") is not False:
            blockers.append("provider_authority_boundary_invalid")
        if response.get("sqlite_persisted") is not True:
            blockers.append("transition_not_persisted")
        if response.get("storage_durable_across_restarts") is not True:
            blockers.append("response_durability_not_declared")
        custody = response.get("custody_submission") or {}
        if custody.get("submitted") is not True or custody.get("state") != "RECORDED":
            blockers.append("authenticated_custody_not_recorded")
        if response.get("master_record_status") != "RECORDED":
            blockers.append("master_record_status_not_recorded")
        if not response.get("master_record_ref"):
            blockers.append("master_record_reference_missing")
        if response.get("reconstruction_status") != "PASS":
            blockers.append("transition_reconstruction_not_pass")
        if authority.get("master_records_installed") is not True:
            blockers.append("master_records_authority_not_observed")

        status = fetch_json(f"{BASE_URL}/api/transitions/{identity['transition_id']}")
        evidence["transition_status"] = status
        if status.get("master_record_status") != "RECORDED":
            blockers.append("status_master_record_not_recorded")
        if status.get("reconstruction_status") != "PASS":
            blockers.append("status_reconstruction_not_pass")
        if status.get("master_record_ref") != response.get("master_record_ref"):
            blockers.append("master_record_reference_mismatch")
        if status.get("final_receipt_id") != response.get("final_receipt_id"):
            blockers.append("final_receipt_identity_mismatch")
    except Exception as exc:
        blockers.append(f"runtime_exception:{type(exc).__name__}:{exc}")

    payload = {
        "schema": "stegverse.site.portable_node_runtime_verification.v2",
        "state": "VERIFIED_CUSTODY_SLICE" if not blockers else "BLOCKED",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "node_base_url": BASE_URL,
        "runtime_path": [
            "portable_node_identity",
            "health_bound_advertisement",
            "site_governed_request",
            "bounded_response",
            "local_transition_persistence",
            "authenticated_master_records_custody",
            "transition_reconstruction",
        ],
        "blockers": blockers,
        "evidence": evidence,
        "provider_execution": "DISABLED_FAIL_CLOSED",
        "custody_verified": not blockers,
        "reconstruction_verified": not blockers,
        "activation_verified": False,
        "authority_granted": False,
        "manual_user_action_required": False,
    }
    binding = dict(payload)
    payload["receipt_sha256"] = canonical_sha256(binding)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
