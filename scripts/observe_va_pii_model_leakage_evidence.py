#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

EVIDENCE = Path("data/va-claim-assistant/pii-model-leakage-evidence.json")
OUTPUT = Path("data/va-claim-assistant/pii-model-leakage-readiness.json")
REQUIRED_CLASSES = {
    "PERSON_NAME", "SSN", "VA_FILE_NUMBER", "EMAIL", "PHONE", "STREET_ADDRESS", "DATE_OF_BIRTH"
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    blockers: list[str] = []
    evidence_present = EVIDENCE.exists()
    data: dict = {}

    if not evidence_present:
        blockers.append("model_leakage_evidence_missing")
    else:
        try:
            data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        except Exception:
            blockers.append("model_leakage_evidence_invalid_json")

    if data:
        checks = {
            "runtime_class_invalid": data.get("runtime_class") != "ADMITTED_PRIVATE_DOCUMENT_PREPROCESSOR",
            "processor_path_missing": not bool(data.get("processor_path")),
            "processor_commit_invalid": not isinstance(data.get("processor_commit"), str) or len(data.get("processor_commit", "")) != 40,
            "execution_environment_invalid": data.get("execution_environment") not in {"PRODUCTION", "CONTROLLED_PRODUCTION_EQUIVALENT"},
            "runtime_not_admitted": data.get("admitted_runtime") is not True,
            "test_case_count_invalid": not isinstance(data.get("test_case_count"), int) or data.get("test_case_count", 0) < 1,
            "identifier_class_coverage_incomplete": not REQUIRED_CLASSES.issubset(set(data.get("direct_identifier_classes_tested", []))),
            "prompt_leak_detected": data.get("prompt_leak_count") != 0,
            "model_input_leak_detected": data.get("model_input_leak_count") != 0,
            "model_output_leak_detected": data.get("model_output_leak_count") != 0,
            "trace_leak_detected": data.get("trace_leak_count") != 0,
            "analytics_leak_detected": data.get("analytics_leak_count") != 0,
            "log_leak_detected": data.get("log_leak_count") != 0,
            "uncertain_review_routing_missing": data.get("uncertain_cases_routed_to_review") is not True,
            "uncertain_release_denial_missing": data.get("model_release_denied_on_uncertainty") is not True,
            "raw_document_model_boundary_missing": data.get("raw_document_to_model_prohibited") is not True,
            "private_upload_must_remain_disabled": data.get("private_document_upload_enabled") is not False,
            "custody_reference_missing": not bool(data.get("custody_reference")),
            "authority_effect_must_be_false": data.get("authority_effect") is not False,
            "activation_effect_must_be_false": data.get("activation_effect") is not False,
        }
        blockers.extend(name for name, failed in checks.items() if failed)

    receipt = {
        "schema_version": "1.0.0",
        "task_id": "PII-RDY-03",
        "state": "COMPLETE" if not blockers else "BLOCKED",
        "model_leakage_evidence_present": evidence_present,
        "blockers": blockers,
        "private_document_upload_enabled": False,
        "authority_effect": False,
        "activation_effect": False,
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_sha256"] = sha256_bytes(canonical)
    OUTPUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
