#!/usr/bin/env python3
"""Observe adapter activation evidence without treating CI scheduling as heartbeat authority."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ecosystem-chat-adapter-monitor-watch.json"
STATUS_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-live-activation-status.json"
RECEIPT_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/receipts/ecosystem-chat-live-activation.verified.json"
AUTHORIZED_PROVIDER_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/receipts/ecosystem-chat-authorized-provider-activation.latest.json"


def fetch(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "StegVerse-Site-Activation-Evidence-Watch/3.0"})
    with urlopen(request, timeout=30) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("source_not_object")
    return value


def digest(value: dict, field: str) -> str:
    material = dict(value)
    material.pop(field, None)
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    blockers: list[str] = []
    status: dict = {}
    receipt: dict = {}
    authorized_provider: dict = {}

    try:
        status = fetch(STATUS_URL)
        if status.get("repository") != "StegVerse-org/LLM-adapter":
            blockers.append("adapter_status_repository_invalid")
        if status.get("manual_user_action_required") is not False:
            blockers.append("adapter_status_manual_action_escalation")
        if status.get("state") == "PENDING" and not status.get("blockers"):
            blockers.append("adapter_pending_status_missing_blocker")
    except Exception as exc:
        blockers.append(f"adapter_status_source_unavailable:{type(exc).__name__}")

    receipt_present = False
    try:
        receipt = fetch(RECEIPT_URL)
        receipt_present = True
        if receipt.get("state") != "VERIFIED":
            blockers.append("adapter_receipt_not_verified")
        if receipt.get("blockers"):
            blockers.append("adapter_verified_receipt_has_blockers")
    except HTTPError as exc:
        if exc.code != 404:
            blockers.append(f"adapter_receipt_source_unavailable:HTTPError_{exc.code}")
    except Exception as exc:
        blockers.append(f"adapter_receipt_source_unavailable:{type(exc).__name__}")

    authorized_provider_present = False
    authorized_provider_valid = False
    try:
        authorized_provider = fetch(AUTHORIZED_PROVIDER_URL)
        authorized_provider_present = True
        if authorized_provider.get("schema") != "stegverse.ecosystem_chat.authorized_provider_activation.v1":
            blockers.append("authorized_provider_receipt_schema_invalid")
        elif authorized_provider.get("result_sha256") != digest(authorized_provider, "result_sha256"):
            blockers.append("authorized_provider_receipt_hash_invalid")
        elif authorized_provider.get("manual_user_action_required") is not False:
            blockers.append("authorized_provider_receipt_manual_action_escalation")
        elif authorized_provider.get("publication_authorized") is not False or authorized_provider.get("repository_mutation_authorized") is not False:
            blockers.append("authorized_provider_receipt_authority_escalation")
        else:
            authorized_provider_valid = True
            blockers.extend(str(value) for value in authorized_provider.get("blockers", []) if str(value))
    except HTTPError as exc:
        blockers.append(f"authorized_provider_receipt_source_unavailable:HTTPError_{exc.code}")
    except Exception as exc:
        blockers.append(f"authorized_provider_receipt_source_unavailable:{type(exc).__name__}")

    verified = receipt_present and not blockers
    payload = {
        "schema": "stegverse.ecosystem_chat.adapter_monitor_watch.v2",
        "repository": "StegVerse-Labs/Site",
        "source_repository": "StegVerse-org/LLM-adapter",
        "generated_at": now,
        "state": "VERIFIED_RECEIPT_OBSERVED" if verified else "PENDING_RUNTIME_EVIDENCE",
        "blockers": sorted(set(blockers or status.get("blockers", []))),
        "adapter_status_state": status.get("state"),
        "adapter_status_blockers": status.get("blockers", []),
        "adapter_verified_receipt_present": receipt_present,
        "authorized_provider_receipt_present": authorized_provider_present,
        "authorized_provider_receipt_valid": authorized_provider_valid,
        "authorized_provider_state": authorized_provider.get("state"),
        "authorized_provider_blockers": authorized_provider.get("blockers", []),
        "authorized_provider_result_sha256": authorized_provider.get("result_sha256"),
        "next_machine_action": "continue_activation_import" if verified else "satisfy_authorized_provider_configuration" if authorized_provider_valid and authorized_provider.get("state") == "CONFIGURATION_REQUIRED" else "continue_runtime_activation_verification",
        "manual_user_action_required": False,
        "heartbeat_boundary": {
            "github_actions_is_runtime_heartbeat": False,
            "ci_observation_defines_heartbeat_cadence": False,
            "runtime_heartbeat_authority_modified": False
        },
        "authority_boundary": {
            "watch_is_activation_authority": False,
            "watch_is_deployment_authority": False,
            "watch_is_execution_authority": False,
            "watch_is_release_authority": False,
            "configuration_receipt_is_provider_authorization": False
        }
    }
    payload["watch_sha256"] = digest(payload, "watch_sha256")
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"ADAPTER ACTIVATION EVIDENCE WATCH: {payload['state']} blockers={len(payload['blockers'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
