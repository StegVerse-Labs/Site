#!/usr/bin/env python3
"""Build the machine-owned Ecosystem Chat activation and propagation state."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DATA = ROOT / "data"
LOCAL = REPORTS / "site-task-diagnostic.json"
LIVE = REPORTS / "external-chat-live-verification.json"
EVIDENCE = REPORTS / "external-chat-activation-evidence.json"
DESTINATION = DATA / "ecosystem-chat-destination-activation-receipt.json"
DESTINATION_IMPORT = DATA / "ecosystem-chat-destination-activation-import-status.json"
EXTERNAL_DESTINATION = DATA / "ecosystem-chat-destination-activation-state.external.json"
EXTERNAL_CUSTODY = DATA / "ecosystem-chat-custody-activation-state.external.json"
EXTERNAL_IMPORT = DATA / "ecosystem-chat-external-activation-import-status.json"
OUTPUT = DATA / "ecosystem-chat-activation-state.json"
PROPAGATION = DATA / "ecosystem-chat-activation-propagation.json"
DOWNSTREAM = [
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-002/stegguardian-wiki",
]


def load(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def canonical_sha256(value: dict[str, Any] | None) -> str | None:
    if value is None:
        return None
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def complete_gate(document: dict[str, Any] | None, name: str) -> bool:
    gates = document.get("gates", {}) if isinstance(document, dict) else {}
    gate = gates.get(name, {}) if isinstance(gates, dict) else {}
    return bool(isinstance(gate, dict) and gate.get("complete") is True)


def destination_gates(receipt: dict[str, Any] | None, import_status: dict[str, Any] | None) -> dict[str, bool]:
    if not receipt or not import_status:
        return {
            "destination_current_main_validation": False,
            "same_origin_authenticated_deployment": False,
            "retrieval_receipt_validation": False,
            "master_records_custody": False,
            "reconstructability_pass": False,
        }
    imported = import_status.get("state") == "VERIFIED_SOURCE_RECEIPT_IMPORTED"
    verified = receipt.get("state") == "VERIFIED" and receipt.get("blockers") == []
    evidence = receipt.get("evidence") or {}
    health = evidence.get("health") or {}
    chat = evidence.get("chat") or {}
    transition = evidence.get("transition") or {}
    provider_usage = chat.get("master_records_usage_submission") or {}
    local_usage = chat.get("provider_usage_submission") or {}
    provider = chat.get("provider") or {}
    return {
        "destination_current_main_validation": imported and verified,
        "same_origin_authenticated_deployment": imported and health.get("status") == "ok",
        "retrieval_receipt_validation": imported and provider.get("used") is True and local_usage.get("event_sha256") is not None,
        "master_records_custody": imported and provider_usage.get("custody_recorded") is True and transition.get("master_record_status") == "RECORDED",
        "reconstructability_pass": imported and provider_usage.get("reconstructability") == "PASS" and transition.get("reconstruction_status") == "PASS",
    }


def write_propagation(state: str, state_sha256: str, gates: dict[str, bool], source_receipts: dict[str, Any]) -> None:
    ready = state == "ACTIVATION_COMPLETE"
    packet: dict[str, Any] = {
        "schema": "stegverse.ecosystem_chat.activation_propagation.v1",
        "state": "READY_FOR_DOWNSTREAM_INGESTION" if ready else "PENDING_ACTIVATION_EVIDENCE",
        "source_repository": "StegVerse-Labs/Site",
        "source_state_path": "data/ecosystem-chat-activation-state.json",
        "source_state_sha256": state_sha256,
        "destinations": [
            {
                "repository": repository,
                "ingestion_ready": ready,
                "required_action": "ingest_verified_activation_state" if ready else "wait_for_verified_activation_state",
                "manual_user_action_required": False,
            }
            for repository in DOWNSTREAM
        ],
        "gates": gates,
        "source_receipts": source_receipts,
        "authority_boundary": {
            "propagation_is_activation_authority": False,
            "propagation_is_release_authority": False,
            "propagation_is_publication_authority": False,
            "propagation_is_custody": False,
        },
    }
    binding = dict(packet)
    packet["packet_sha256"] = hashlib.sha256(
        json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    PROPAGATION.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    local = load(LOCAL)
    live = load(LIVE)
    evidence = load(EVIDENCE)
    destination = load(DESTINATION)
    destination_import = load(DESTINATION_IMPORT)
    external_destination = load(EXTERNAL_DESTINATION)
    external_custody = load(EXTERNAL_CUSTODY)
    external_import = load(EXTERNAL_IMPORT)
    legacy = destination_gates(destination, destination_import)

    gates = {
        "site_current_main_validation": bool(local and local.get("status") == "PASSED"),
        "public_route_verification": bool(live and live.get("result") == "PASS"),
        "mutation_required_disabled": bool(live and live.get("mutation_required_disabled") is True),
        "site_activation_evidence": bool(evidence and evidence.get("result") == "OBSERVED_NON_MUTATING_PUBLIC_PATHS"),
        "destination_state_imported": bool(external_destination and external_destination.get("manual_user_action_required") is False),
        "custody_state_imported": bool(external_custody and external_custody.get("manual_user_action_required") is False),
        "external_import_status_recorded": external_import is not None,
        "destination_current_main_validation": complete_gate(external_destination, "destination_current_main_validation") or legacy["destination_current_main_validation"],
        "same_origin_authenticated_deployment": complete_gate(external_destination, "same_origin_authenticated_deployment") or legacy["same_origin_authenticated_deployment"],
        "automatic_provider_usage_submission": complete_gate(external_destination, "automatic_provider_usage_submission"),
        "retrieval_receipt_validation": complete_gate(external_destination, "retrieval_and_provider_usage_receipts") or legacy["retrieval_receipt_validation"],
        "orchestration_current_main_validation": complete_gate(external_custody, "orchestration_current_main_validation"),
        "persistent_custody_service_configuration": complete_gate(external_custody, "persistent_custody_service_configuration"),
        "master_records_custody": complete_gate(external_custody, "authenticated_custody_receipt") or legacy["master_records_custody"],
        "reconstructability_pass": complete_gate(external_custody, "reconstructability_pass") or legacy["reconstructability_pass"],
    }
    owner_map = {
        "site_current_main_validation": "StegVerse-Labs/Site",
        "public_route_verification": "StegVerse-Labs/Site",
        "mutation_required_disabled": "StegVerse-Labs/Site",
        "site_activation_evidence": "StegVerse-Labs/Site",
        "destination_state_imported": "StegVerse-Labs/Site",
        "custody_state_imported": "StegVerse-Labs/Site",
        "external_import_status_recorded": "StegVerse-Labs/Site",
        "destination_current_main_validation": "StegVerse-org/LLM-adapter",
        "same_origin_authenticated_deployment": "StegVerse-org/LLM-adapter",
        "automatic_provider_usage_submission": "StegVerse-org/LLM-adapter",
        "retrieval_receipt_validation": "StegVerse-org/LLM-adapter",
        "orchestration_current_main_validation": "master-records/orchestration",
        "persistent_custody_service_configuration": "master-records/orchestration",
        "master_records_custody": "master-records/orchestration",
        "reconstructability_pass": "master-records/orchestration",
    }
    action_map = {
        "site_current_main_validation": "Allow scheduled Site validation to emit the diagnostic receipt.",
        "public_route_verification": "Allow scheduled post-deployment route verification to emit the live receipt.",
        "mutation_required_disabled": "Preserve the non-mutating live route unless separately authorized.",
        "site_activation_evidence": "Allow Site to rebuild the correlated activation-evidence record.",
        "destination_state_imported": "Allow Site to import the checked-in adapter activation state.",
        "custody_state_imported": "Allow Site to import the checked-in custody activation state.",
        "external_import_status_recorded": "Allow Site to write the external-state import status.",
        "destination_current_main_validation": "Allow scheduled adapter validation to publish a successful current-main state.",
        "same_origin_authenticated_deployment": "Allow the authorized gateway platform to publish deployment configuration evidence.",
        "automatic_provider_usage_submission": "Allow configured gateway runtime to enable provider-owned usage submission.",
        "retrieval_receipt_validation": "Allow the deployed gateway runtime to publish retrieval and provider-usage receipts.",
        "orchestration_current_main_validation": "Allow scheduled orchestration validation to publish a current-main state.",
        "persistent_custody_service_configuration": "Allow the authorized custody platform to expose protected configuration evidence.",
        "master_records_custody": "Allow the custody service to issue an authenticated custody receipt.",
        "reconstructability_pass": "Allow the live custody verifier to publish reconstruction PASS evidence.",
    }
    complete = all(gates.values())
    state = "ACTIVATION_COMPLETE" if complete else "ACTIVATION_PENDING_EVIDENCE"
    next_actions = [
        {
            "gate": gate,
            "owner": owner_map[gate],
            "action": action_map[gate],
            "manual_user_action_required": "false",
        }
        for gate, passed in gates.items()
        if not passed
    ]
    source_receipts = {
        "site_task_diagnostic": {"present": local is not None, "sha256": canonical_sha256(local)},
        "live_verification": {"present": live is not None, "sha256": canonical_sha256(live)},
        "activation_evidence": {"present": evidence is not None, "sha256": canonical_sha256(evidence)},
        "legacy_destination_activation": {"present": destination is not None, "sha256": canonical_sha256(destination)},
        "legacy_destination_import_status": {"present": destination_import is not None, "sha256": canonical_sha256(destination_import)},
        "external_destination_activation_state": {"present": external_destination is not None, "sha256": canonical_sha256(external_destination)},
        "external_custody_activation_state": {"present": external_custody is not None, "sha256": canonical_sha256(external_custody)},
        "external_activation_import_status": {"present": external_import is not None, "sha256": canonical_sha256(external_import)},
    }
    payload: dict[str, Any] = {
        "schema_version": "1.3.0",
        "record_type": "ecosystem_chat_activation_state",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": state,
        "manual_user_action_required": False,
        "local_manual_tasks": "eliminated",
        "continuation_mode": "workflow_managed_owner_routed_cross_repository",
        "gates": gates,
        "next_actions": next_actions,
        "source_receipts": source_receipts,
        "downstream_propagation_path": "data/ecosystem-chat-activation-propagation.json",
        "authority_boundary": {
            "state_grants_deployment_authority": False,
            "state_grants_mutation_authority": False,
            "state_grants_custody_authority": False,
            "state_grants_release_authority": False,
        },
    }
    binding = dict(payload)
    payload["state_sha256"] = hashlib.sha256(
        json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_propagation(state, payload["state_sha256"], gates, source_receipts)
    print(f"ECOSYSTEM CHAT ACTIVATION STATE: {state}")
    print(f"Receipt: {OUTPUT.relative_to(ROOT)}")
    print(f"Propagation: {PROPAGATION.relative_to(ROOT)}")
    print(f"Owner-routed actions: {len(next_actions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
