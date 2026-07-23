#!/usr/bin/env python3
"""Validate the non-authorizing cross-repository live baseline handoff."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data/framework-evaluations/stegverse-live-baseline-handoff-status.json"
REQUEST = ROOT / "data/framework-evaluations/stegverse-live-baseline-execution-request.json"
CANONICAL_VALIDATOR = "scripts/check_stegverse_live_baseline_runtime_readiness.py"
LEGACY_VALIDATOR_ALIAS = "scripts/check_stegverse_live-baseline-runtime-readiness.py"
NO_AUTHORITY = {
    "comparison": False,
    "admissibility": False,
    "certification": False,
    "execution": False,
    "custody": False,
    "parentage": False,
}


def require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def valid_commit(value: object) -> bool:
    return isinstance(value, str) and len(value) == 40 and all(c in "0123456789abcdef" for c in value)


def main() -> int:
    require(STATUS.is_file(), "missing live baseline handoff status")
    require(REQUEST.is_file(), "missing live baseline execution request")
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    request = json.loads(REQUEST.read_text(encoding="utf-8"))

    require(status.get("schema_version") == "1.0.0", "unsupported schema_version")
    require(status.get("source_request_id") == request.get("request_id"), "source request mismatch")
    require(status.get("source_repository") == "StegVerse-Labs/Site", "source repository mismatch")
    require(status.get("destination_repository") == "StegVerse-org/LLM-adapter", "destination repository mismatch")
    require(status.get("destination_path") == "intake/stegverse-live-baseline-execution-request-v1.json", "destination path mismatch")
    require(valid_commit(status.get("destination_commit")), "invalid destination commit")
    require(status.get("destination_readiness_path") == "status/stegverse-live-baseline-runtime-readiness.json", "destination readiness path mismatch")
    require(valid_commit(status.get("destination_readiness_commit")), "invalid destination readiness commit")

    validator_path = status.get("destination_validator_path")
    require(validator_path in {CANONICAL_VALIDATOR, LEGACY_VALIDATOR_ALIAS}, "destination validator path mismatch")
    if validator_path == LEGACY_VALIDATOR_ALIAS:
        require(
            CANONICAL_VALIDATOR in (status.get("destination_aggregate_includes") or []),
            "legacy validator alias requires canonical aggregate binding",
        )
    require(valid_commit(status.get("destination_validator_commit")), "invalid destination validator commit")

    require(status.get("destination_provider_authority_binding_path") == "status/stegverse-live-baseline-provider-authority-binding.json", "provider authority binding path mismatch")
    require(valid_commit(status.get("destination_provider_authority_binding_commit")), "invalid provider authority binding commit")
    require(status.get("destination_provider_authority_validator_path") == "scripts/check_stegverse_live_baseline_provider_authority_binding.py", "provider authority validator path mismatch")
    require(valid_commit(status.get("destination_provider_authority_validator_commit")), "invalid provider authority validator commit")
    require(status.get("provider_authority_state") == "REQUESTED_NOT_APPROVED", "provider authority cannot be inferred as approved")
    require(status.get("provider_authority_reuse_first") is True, "provider path must preserve reuse-first binding")
    require(status.get("handoff_state") == "RECEIVED_PENDING_PREREQUISITES", "unexpected handoff state")
    require(status.get("destination_readiness_state") == "BLOCKED", "pending prerequisites require BLOCKED destination readiness")
    require(status.get("dispatch_state") == "NOT_DISPATCHED", "handoff cannot claim dispatch")
    require(status.get("destination_execution_authorized") is False, "destination execution authority escalated")
    require(status.get("source_execution_authorized") is False, "source execution authority escalated")
    require(status.get("source_custody_authorized") is False, "source custody authority escalated")
    require(len(status.get("required_next_evidence") or []) >= 6, "required next evidence incomplete")
    require(len(status.get("prohibited_inferences") or []) >= 7, "missing bounded prohibited inferences")
    require(status.get("authority") == NO_AUTHORITY, "handoff authority boundary changed")
    require(request.get("dispatch", {}).get("authorized") is False, "source request cannot be dispatched while handoff is pending prerequisites")

    print("STEGVERSE LIVE BASELINE HANDOFF: PROVIDER AUTHORITY REQUESTED_NOT_APPROVED / DESTINATION BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
