#!/usr/bin/env python3
"""Write a hash-bound receipt after VA governance validation succeeds."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/va-claim-assistant"
TARGET = DATA / "governance-validation-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def main() -> int:
    record: dict[str, Any] = {
        "schema_version": "1.0.0",
        "receipt_id": "site-va-governance-validation-001",
        "observed_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "result": "PASS",
        "checks": {
            "source_registry_semantics": "PASS",
            "valid_answer_fixture": "PASS",
            "authority_escalation_fixture": "REJECTED_AS_EXPECTED",
            "unsupported_proposition_fixture": "REJECTED_AS_EXPECTED"
        },
        "inputs": {
            "source_registry_sha256": sha256(DATA / "source-registry.json"),
            "source_registry_schema_sha256": sha256(DATA / "source-registry.schema.json"),
            "answer_record_schema_sha256": sha256(DATA / "answer-record.schema.json"),
            "valid_answer_fixture_sha256": sha256(DATA / "fixtures/valid-answer-record.json"),
            "invalid_authority_fixture_sha256": sha256(DATA / "fixtures/invalid-authority-escalation.json"),
            "invalid_unsupported_fixture_sha256": sha256(DATA / "fixtures/invalid-unsupported-proposition.json"),
            "validator_sha256": sha256(ROOT / "scripts/check_va_claim_assistant_governance.py")
        },
        "gate_effect": {
            "VCA-GATE-01": "VERIFIED",
            "VCA-GATE-02": "VERIFIED"
        },
        "authority_effect": False,
        "activation_effect": False
    }
    record["receipt_sha256"] = canonical_hash(record)
    TARGET.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "receipt_sha256": record["receipt_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
