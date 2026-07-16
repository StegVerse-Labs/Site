#!/usr/bin/env python3
"""Build a non-authorizing External Chat activation evidence record.

The record correlates the exact Site commit, workflow run, local diagnostic,
post-deployment live receipt, Pages deployment URL, and mutation-disabled
posture. It is evidence of what was observed, not deployment, mutation,
certification, publication, or standing authority.

After writing the evidence record, this script automatically imports durable
owner-repository activation states and refreshes the machine-owned Ecosystem Chat
activation state. Scheduled/current-main workflow runs therefore maintain the
continuation plan without manual observation or artifact transfer.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from import_ecosystem_chat_external_activation_states import main as import_external_states
from update_ecosystem_chat_activation_state import main as update_activation_state

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
LOCAL = REPORTS / "site-task-diagnostic.json"
LIVE = REPORTS / "external-chat-live-verification.json"
OUTPUT = REPORTS / "external-chat-activation-evidence.json"


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


def env(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def main() -> int:
    local = load(LOCAL)
    live = load(LIVE)

    local_passed = bool(local and local.get("status") == "PASSED")
    live_passed = bool(live and live.get("result") == "PASS")
    mutation_disabled = bool(live and live.get("mutation_required_disabled") is True)

    if local_passed and live_passed and mutation_disabled:
        result = "OBSERVED_NON_MUTATING_PUBLIC_PATHS"
        failure_class = None
    elif not local_passed:
        result = "LOCAL_VALIDATION_NOT_CONFIRMED"
        failure_class = (local or {}).get("failure_class") or "LOCAL_RECEIPT_MISSING"
    elif not live:
        result = "LIVE_EVIDENCE_NOT_AVAILABLE"
        failure_class = "LIVE_RECEIPT_MISSING"
    else:
        result = "LIVE_EVIDENCE_NOT_CONFIRMED"
        failure_class = live.get("failure_class") or "LIVE_CONTRACT_NOT_CONFIRMED"

    generated_at = datetime.now(timezone.utc).isoformat()
    evidence: dict[str, Any] = {
        "schema_version": "1.0.0",
        "record_type": "external_chat_activation_evidence",
        "generated_at": generated_at,
        "result": result,
        "failure_class": failure_class,
        "repository": env("GITHUB_REPOSITORY") or "StegVerse-Labs/Site",
        "commit_sha": env("GITHUB_SHA"),
        "ref": env("GITHUB_REF"),
        "event_name": env("GITHUB_EVENT_NAME"),
        "workflow": env("GITHUB_WORKFLOW"),
        "workflow_run_id": env("GITHUB_RUN_ID"),
        "workflow_run_attempt": env("GITHUB_RUN_ATTEMPT"),
        "workflow_job": env("GITHUB_JOB"),
        "pages_deployment_url": env("STEGVERSE_PAGES_DEPLOYMENT_URL"),
        "gateway_base_url": env("STEGVERSE_GATEWAY_BASE_URL"),
        "local_validation": {
            "present": local is not None,
            "passed": local_passed,
            "receipt_sha256": canonical_sha256(local),
            "status": (local or {}).get("status"),
            "failed_validator": (local or {}).get("failed_validator"),
            "authority_effect": (local or {}).get("authority_effect"),
        },
        "post_deployment_live_verification": {
            "present": live is not None,
            "passed": live_passed,
            "receipt_sha256": canonical_sha256(live),
            "result": (live or {}).get("result"),
            "failure_class": (live or {}).get("failure_class"),
            "mutation_required_disabled": (live or {}).get("mutation_required_disabled"),
            "observation_count": len((live or {}).get("observations", [])) if isinstance((live or {}).get("observations", []), list) else None,
        },
        "authority_boundary": {
            "evidence_is_deployment_authority": False,
            "evidence_is_repository_mutation_authority": False,
            "evidence_is_publication_authority": False,
            "evidence_is_certification": False,
            "evidence_creates_standing": False,
            "mutation_remains_separately_authorized": True,
        },
    }
    binding = dict(evidence)
    evidence["evidence_sha256"] = hashlib.sha256(
        json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    REPORTS.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"EXTERNAL CHAT ACTIVATION EVIDENCE: {result}")
    print(f"Receipt: {OUTPUT.relative_to(ROOT)}")

    import_result = import_external_states()
    if import_result != 0:
        raise SystemExit(import_result)
    state_result = update_activation_state()
    if state_result != 0:
        raise SystemExit(state_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
