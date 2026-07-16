#!/usr/bin/env python3
"""Build the machine-owned Ecosystem Chat activation state.

The state is fail-closed. It converts local validation, live verification, and
activation-evidence records into an explicit owner-routed continuation plan.
No manual observation or confirmation is required to keep the state current.
"""
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
OUTPUT = DATA / "ecosystem-chat-activation-state.json"


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


def main() -> int:
    local = load(LOCAL)
    live = load(LIVE)
    evidence = load(EVIDENCE)

    local_ok = bool(local and local.get("status") == "PASSED")
    live_ok = bool(live and live.get("result") == "PASS")
    mutation_disabled = bool(live and live.get("mutation_required_disabled") is True)
    evidence_ok = bool(evidence and evidence.get("result") == "OBSERVED_NON_MUTATING_PUBLIC_PATHS")

    gates = {
        "site_current_main_validation": local_ok,
        "public_route_verification": live_ok,
        "mutation_required_disabled": mutation_disabled,
        "site_activation_evidence": evidence_ok,
        "destination_current_main_validation": False,
        "same_origin_authenticated_deployment": False,
        "retrieval_receipt_validation": False,
        "master_records_custody": False,
        "reconstructability_pass": False,
    }

    if all(gates.values()):
        state = "ACTIVATION_COMPLETE"
        next_actions: list[dict[str, str]] = []
    else:
        state = "ACTIVATION_PENDING_EVIDENCE"
        next_actions = []
        owner_map = {
            "site_current_main_validation": "StegVerse-Labs/Site",
            "public_route_verification": "StegVerse-Labs/Site",
            "mutation_required_disabled": "StegVerse-Labs/Site",
            "site_activation_evidence": "StegVerse-Labs/Site",
            "destination_current_main_validation": "StegVerse-org/LLM-adapter",
            "same_origin_authenticated_deployment": "StegVerse-org/LLM-adapter",
            "retrieval_receipt_validation": "StegVerse-org/LLM-adapter",
            "master_records_custody": "master-records/orchestration",
            "reconstructability_pass": "master-records/orchestration",
        }
        action_map = {
            "site_current_main_validation": "Run consolidated current-main Site validation and emit the diagnostic receipt.",
            "public_route_verification": "Verify deployed Site and gateway public routes and emit the live receipt.",
            "mutation_required_disabled": "Confirm the live route remains non-mutating unless separately authorized.",
            "site_activation_evidence": "Build and retain the correlated activation-evidence record.",
            "destination_current_main_validation": "Run usage-session verification on destination current-main.",
            "same_origin_authenticated_deployment": "Deploy the authorized same-origin gateway or proxy topology.",
            "retrieval_receipt_validation": "Emit and validate retrieval and provider-usage receipts.",
            "master_records_custody": "Ingest Site, retrieval, and provider receipts into authenticated custody.",
            "reconstructability_pass": "Run reconstruction against the custody chain and emit PASS evidence.",
        }
        for gate, passed in gates.items():
            if not passed:
                next_actions.append({
                    "gate": gate,
                    "owner": owner_map[gate],
                    "action": action_map[gate],
                    "manual_user_action_required": "false",
                })

    generated_at = datetime.now(timezone.utc).isoformat()
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "record_type": "ecosystem_chat_activation_state",
        "generated_at": generated_at,
        "state": state,
        "manual_user_action_required": False,
        "local_manual_tasks": "eliminated",
        "continuation_mode": "workflow_managed_owner_routed",
        "gates": gates,
        "next_actions": next_actions,
        "source_receipts": {
            "site_task_diagnostic": {"present": local is not None, "sha256": canonical_sha256(local)},
            "live_verification": {"present": live is not None, "sha256": canonical_sha256(live)},
            "activation_evidence": {"present": evidence is not None, "sha256": canonical_sha256(evidence)},
        },
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
    print(f"ECOSYSTEM CHAT ACTIVATION STATE: {state}")
    print(f"Receipt: {OUTPUT.relative_to(ROOT)}")
    print(f"Owner-routed actions: {len(next_actions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
