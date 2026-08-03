#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data/va-claim-assistant/pii-redaction-working-copy-evidence.json"
OUTPUT = ROOT / "data/va-claim-assistant/pii-redaction-working-copy-readiness.json"

REQUIRED_TRUE = [
    "page_region_anchors_present",
    "manifest_bound_to_original_and_redacted_hashes",
    "token_is_purpose_limited",
    "token_is_non_global",
    "model_release_allowed",
]
REQUIRED_FALSE = [
    "raw_document_left_privacy_zone",
    "raw_pii_present_in_working_copy",
    "private_document_upload_enabled",
    "authority_effect",
    "activation_effect",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    blockers = []
    evidence_present = EVIDENCE.exists()
    evidence = None
    if not evidence_present:
        blockers.append("redaction_working_copy_evidence_missing")
    else:
        try:
            evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        except Exception:
            blockers.append("redaction_working_copy_evidence_invalid_json")

    if evidence is not None:
        expected = {
            "schema_version": "1.0.0",
            "task_id": "PII-RDY-02",
            "runtime_class": "ADMITTED_PRIVATE_DOCUMENT_PREPROCESSOR",
            "state": "PASS",
        }
        for key, value in expected.items():
            if evidence.get(key) != value:
                blockers.append(f"invalid_{key}")
        if evidence.get("execution_class") not in {"PRODUCTION", "CONTROLLED_PRODUCTION_EQUIVALENT"}:
            blockers.append("invalid_execution_class")
        for key in ["processor_path", "custody_reference", "pseudonymous_document_token"]:
            if not isinstance(evidence.get(key), str) or not evidence.get(key):
                blockers.append(f"missing_{key}")
        for key in ["processor_commit_sha"]:
            value = evidence.get(key, "")
            if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
                blockers.append(f"invalid_{key}")
        for key in ["original_document_sha256", "redacted_document_sha256", "redaction_manifest_sha256"]:
            value = evidence.get(key, "")
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                blockers.append(f"invalid_{key}")
        if evidence.get("original_document_sha256") == evidence.get("redacted_document_sha256"):
            blockers.append("redacted_hash_must_differ_from_original")
        if not isinstance(evidence.get("direct_identifier_replacement_count"), int) or evidence.get("direct_identifier_replacement_count", 0) < 1:
            blockers.append("no_identifier_replacements_recorded")
        for key in REQUIRED_TRUE:
            if evidence.get(key) is not True:
                blockers.append(f"{key}_not_true")
        for key in REQUIRED_FALSE:
            if evidence.get(key) is not False:
                blockers.append(f"{key}_not_false")

    state = "COMPLETE" if not blockers else "BLOCKED"
    receipt = {
        "schema_version": "1.0.0",
        "task_id": "PII-RDY-02",
        "state": state,
        "redaction_working_copy_evidence_present": evidence_present,
        "blockers": sorted(set(blockers)),
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
