#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data/va-claim-assistant/pii-production-detector-evidence.json"
RECEIPT = ROOT / "data/va-claim-assistant/pii-production-detector-readiness.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    blockers: list[str] = []
    evidence = None
    if not EVIDENCE.exists():
        blockers.append("production_detector_evidence_missing")
    else:
        try:
            evidence = json.loads(EVIDENCE.read_text())
        except Exception as exc:
            blockers.append(f"production_detector_evidence_invalid_json:{type(exc).__name__}")

    if evidence is not None:
        checks = {
            "runtime_class": evidence.get("runtime_class") == "ADMITTED_PRIVATE_DOCUMENT_PREPROCESSOR",
            "admitted_runtime": evidence.get("admitted_runtime") is True,
            "not_reference_only": evidence.get("reference_evaluator_only") is False,
            "uncertain_review": evidence.get("uncertain_cases_routed_to_review") is True,
            "no_pre_gate_processing": evidence.get("model_processing_before_gate") is False,
            "no_raw_pii_leakage": evidence.get("raw_pii_in_prompts_outputs_traces_or_logs") is False,
            "upload_disabled": evidence.get("private_document_upload_enabled") is False,
            "authority_false": evidence.get("authority_effect") is False,
            "activation_false": evidence.get("activation_effect") is False,
            "state_pass": evidence.get("state") == "PASS",
            "recall_threshold": float(evidence.get("required_class_recall", -1)) >= 0.99,
            "false_positive_threshold": float(evidence.get("clean_case_false_positive_rate", 2)) <= 0.05,
            "processor_commit": isinstance(evidence.get("processor_commit"), str) and len(evidence["processor_commit"]) == 40,
            "custody_reference": bool(evidence.get("custody_reference")),
        }
        blockers.extend(name for name, passed in checks.items() if not passed)

    receipt = {
        "schema_version": "1.0.0",
        "task_id": "PII-RDY-01",
        "state": "COMPLETE" if not blockers else "BLOCKED",
        "blockers": blockers,
        "production_detector_evidence_present": evidence is not None,
        "reference_receipt_is_insufficient": True,
        "private_document_upload_enabled": False,
        "authority_effect": False,
        "activation_effect": False
    }
    if EVIDENCE.exists():
        receipt["evidence_sha256"] = digest(EVIDENCE.read_bytes())
    receipt["receipt_sha256"] = digest(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode())
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
