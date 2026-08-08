#!/usr/bin/env python3
"""Fail-closed observer for the final VA PII readiness requirements.

PII-RDY-08 and PII-RDY-09 are external-evidence gates. This observer never
creates that evidence and never grants authority or activation. It turns the
presence, absence, or contradiction of the named evidence into a deterministic,
inspectable receipt for the existing PII realignment workflow.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data/va-claim-assistant/pii-rdy-08-09-observer-contract.json"
RECEIPT_PATH = ROOT / "data/va-claim-assistant/pii-rdy-08-09-readiness.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def evaluate(requirement_id: str, requirement: dict) -> dict:
    evidence_path = ROOT / requirement["evidence_path"]
    base = {
        "requirement_id": requirement_id,
        "owner": requirement["owner"],
        "capability": requirement["capability"],
        "evidence_path": requirement["evidence_path"],
        "authority_effect": False,
        "activation_effect": False,
    }
    if not evidence_path.exists():
        return {
            **base,
            "state": "BLOCKED",
            "blockers": ["required_evidence_missing"],
            "evidence_sha256": None,
            "next_executable_action": f"{requirement['owner']} must produce the named evidence artifact; the observer will re-evaluate it automatically.",
        }

    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            **base,
            "state": "REVIEW_REQUIRED",
            "blockers": ["evidence_unreadable_or_invalid_json"],
            "evidence_sha256": None,
            "next_executable_action": f"{requirement['owner']} must repair the named evidence artifact.",
        }

    mismatches = []
    for key, expected in requirement["required_evidence"].items():
        actual = evidence.get(key)
        if actual != expected:
            mismatches.append({"field": key, "expected": expected, "actual": actual})

    if mismatches:
        return {
            **base,
            "state": "REVIEW_REQUIRED",
            "blockers": ["required_evidence_contract_mismatch"],
            "mismatches": mismatches,
            "evidence_sha256": sha256(evidence),
            "next_executable_action": f"{requirement['owner']} must resolve the mismatched evidence fields; no activation is permitted.",
        }

    return {
        **base,
        "state": "COMPLETE",
        "blockers": [],
        "evidence_sha256": sha256(evidence),
        "next_executable_action": None,
    }


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    results = [evaluate(rid, req) for rid, req in contract["requirements"].items()]
    states = {item["state"] for item in results}
    if states == {"COMPLETE"}:
        overall = "COMPLETE"
    elif "REVIEW_REQUIRED" in states:
        overall = "REVIEW_REQUIRED"
    elif "FAILED" in states:
        overall = "FAILED"
    else:
        overall = "BLOCKED"

    receipt = {
        "schema_version": "1.0.0",
        "task_id": contract["task_id"],
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "observation_source": "REPOSITORY_NATIVE_FAIL_CLOSED_OBSERVER",
        "state": overall,
        "authority_effect": False,
        "activation_effect": False,
        "requirements": results,
        "complete_count": sum(1 for item in results if item["state"] == "COMPLETE"),
        "required_count": len(results),
        "next_executable_action": next((item["next_executable_action"] for item in results if item["next_executable_action"]), None),
        "contract_sha256": sha256(contract),
    }
    receipt["receipt_sha256"] = sha256(receipt)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if overall in {"COMPLETE", "BLOCKED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
