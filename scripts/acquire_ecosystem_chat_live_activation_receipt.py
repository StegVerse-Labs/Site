#!/usr/bin/env python3
"""Acquire and validate retained Ecosystem Chat activation evidence.

The immutable VERIFIED receipt remains the only activation input. Until it exists, the
adapter's stable non-authorizing blocker status is imported so continuation does not
depend on expiring workflow artifacts or manual inspection.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ecosystem-chat-destination-activation-receipt.json"
STATUS = ROOT / "data" / "ecosystem-chat-destination-activation-import-status.json"
SOURCE_URL = os.getenv(
    "STEGVERSE_ECOSYSTEM_CHAT_ACTIVATION_RECEIPT_URL",
    "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/receipts/ecosystem-chat-live-activation.verified.json",
)
SOURCE_STATUS_URL = os.getenv(
    "STEGVERSE_ECOSYSTEM_CHAT_ACTIVATION_STATUS_URL",
    "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-live-activation-status.json",
)
TIMEOUT = float(os.getenv("STEGVERSE_ECOSYSTEM_CHAT_ACTIVATION_FETCH_TIMEOUT_SECONDS", "20"))


def canonical_sha(payload: dict[str, Any], field: str) -> str:
    material = dict(payload)
    material.pop(field, None)
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def fetch_json(url: str) -> dict[str, Any]:
    with request.urlopen(url, timeout=TIMEOUT) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("source_not_object")
    return value


def validate_pending_status(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("pending_status_not_object")
    if value.get("schema") != "stegverse.ecosystem_chat.live_activation_status.v1":
        raise ValueError("pending_status_schema_mismatch")
    if value.get("repository") != "StegVerse-org/LLM-adapter":
        raise ValueError("pending_status_repository_mismatch")
    if value.get("state") not in {"PENDING", "VERIFIED"}:
        raise ValueError("pending_status_state_invalid")
    if value.get("manual_user_action_required") is not False:
        raise ValueError("pending_status_manual_action_invalid")
    boundary = value.get("authority_boundary") or {}
    if any(
        boundary.get(key) is not False
        for key in (
            "status_is_activation_authority",
            "status_is_deployment_authority",
            "status_is_custody",
            "status_is_release_authority",
        )
    ):
        raise ValueError("pending_status_authority_escalation")
    if canonical_sha(value, "status_sha256") != value.get("status_sha256"):
        raise ValueError("pending_status_digest_mismatch")
    blockers = value.get("blockers")
    if not isinstance(blockers, list) or any(not isinstance(item, str) for item in blockers):
        raise ValueError("pending_status_blockers_invalid")
    return value


def write_status(
    state: str,
    reason: str,
    receipt: dict[str, Any] | None = None,
    pending_status: dict[str, Any] | None = None,
) -> None:
    payload = {
        "schema": "stegverse.site.ecosystem_chat_activation_import.v1",
        "state": state,
        "reason": reason,
        "source_url": SOURCE_URL,
        "source_status_url": SOURCE_STATUS_URL,
        "receipt_present": receipt is not None,
        "receipt_state": receipt.get("state") if receipt else None,
        "receipt_sha256": receipt.get("result_sha256") if receipt else None,
        "source_activation_state": pending_status.get("state") if pending_status else None,
        "source_blockers": pending_status.get("blockers", []) if pending_status else [],
        "source_gates": pending_status.get("gates", {}) if pending_status else {},
        "source_status_sha256": pending_status.get("status_sha256") if pending_status else None,
        "manual_user_action_required": False,
        "authority_granted": False,
        "deployment_authorized": False,
        "release_authorized": False,
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate(receipt: Any) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise ValueError("receipt_not_object")
    if receipt.get("schema") != "stegverse.ecosystem_chat.live_activation.v1":
        raise ValueError("receipt_schema_mismatch")
    if receipt.get("state") != "VERIFIED":
        raise ValueError("receipt_not_verified")
    if receipt.get("blockers") != []:
        raise ValueError("receipt_contains_blockers")
    if receipt.get("authority_granted") is not False:
        raise ValueError("receipt_authority_escalation")
    if receipt.get("publication_authorized") is not False:
        raise ValueError("receipt_publication_escalation")
    if receipt.get("repository_mutation_authorized") is not False:
        raise ValueError("receipt_mutation_escalation")
    if receipt.get("result_sha256") != canonical_sha(receipt, "result_sha256"):
        raise ValueError("receipt_digest_mismatch")

    evidence = receipt.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("receipt_evidence_missing")
    health = evidence.get("health") or {}
    chat = evidence.get("chat") or {}
    transition = evidence.get("transition") or {}
    provider = chat.get("provider") or {}
    usage_custody = chat.get("master_records_usage_submission") or {}
    local_usage = chat.get("provider_usage_submission") or {}

    required = {
        "gateway_health": health.get("status") == "ok",
        "durable_storage": health.get("storage_durable_across_restarts") is True,
        "provider_enabled": health.get("governed_provider_enabled") is True,
        "transition_submission_enabled": health.get("master_records_submission_enabled") is True,
        "provider_used": provider.get("used") is True,
        "local_usage_non_custodial": local_usage.get("custody_recorded") is False,
        "provider_usage_custody": usage_custody.get("custody_recorded") is True,
        "provider_usage_reconstructability": usage_custody.get("reconstructability") == "PASS",
        "provider_usage_non_authorizing": usage_custody.get("authority_granted") is False,
        "transition_custody": transition.get("master_record_status") == "RECORDED",
        "transition_reconstructability": transition.get("reconstruction_status") == "PASS",
    }
    failed = sorted(name for name, passed in required.items() if not passed)
    if failed:
        raise ValueError("receipt_evidence_gate_failed:" + ",".join(failed))
    return receipt


def import_pending_status(reason: str) -> int:
    try:
        status = validate_pending_status(fetch_json(SOURCE_STATUS_URL))
        write_status("PENDING_SOURCE_RECEIPT", reason, pending_status=status)
        print(f"ECOSYSTEM_CHAT_ACTIVATION_PENDING:{','.join(status.get('blockers', [])) or 'no_semantic_blockers'}")
    except error.HTTPError as exc:
        write_status("PENDING_SOURCE_RECEIPT", f"{reason};status_http_{exc.code}")
    except (error.URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        write_status("PENDING_SOURCE_RECEIPT", f"{reason};status_unavailable:{type(exc).__name__}")
    return 0


def main() -> int:
    try:
        receipt = validate(fetch_json(SOURCE_URL))
    except error.HTTPError as exc:
        if exc.code == 404:
            return import_pending_status("verified_receipt_not_yet_published")
        return import_pending_status(f"source_http_status_{exc.code}")
    except (error.URLError, TimeoutError, OSError) as exc:
        return import_pending_status(f"source_transport_error:{type(exc).__name__}")
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        write_status("REJECTED_SOURCE_RECEIPT", str(exc))
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_status("VERIFIED_SOURCE_RECEIPT_IMPORTED", "all_activation_evidence_gates_passed", receipt)
    print("ECOSYSTEM_CHAT_ACTIVATION_RECEIPT_IMPORTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
