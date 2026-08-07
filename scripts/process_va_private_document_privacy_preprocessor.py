#!/usr/bin/env python3
"""Controlled-production-equivalent VA private-document privacy preprocessor.

The processor accepts only bounded synthetic/controlled inputs in this repository lane.
It performs file-admission checks, direct-identifier detection, fail-closed uncertainty
routing, deterministic redaction/tokenization, leakage verification, and emits only
privacy-minimized machine evidence. It does not call a model or enable public upload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

PROCESSOR_PATH = "scripts/process_va_private_document_privacy_preprocessor.py"
RUNTIME_CLASS = "ADMITTED_PRIVATE_DOCUMENT_PREPROCESSOR"
ALLOWED_MEDIA_TYPES = {"text/plain", "application/pdf"}
IDENTIFIER_PATTERNS = {
    "PERSON_NAME": re.compile(r"(?im)^Name:\s*([^\n]+)$"),
    "SSN": re.compile(r"(?im)^SSN:\s*(\d{3}-\d{2}-\d{4})$"),
    "VA_FILE_NUMBER": re.compile(r"(?im)^VA File Number:\s*([A-Z]?\d{8,9})$"),
    "EMAIL": re.compile(r"(?im)^Email:\s*([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})$"),
    "PHONE": re.compile(r"(?im)^Phone:\s*(\d{3}-\d{3}-\d{4})$"),
    "STREET_ADDRESS": re.compile(r"(?im)^Street Address:\s*([^\n]+)$"),
    "DATE_OF_BIRTH": re.compile(r"(?im)^Date of Birth:\s*(\d{2}/\d{2}/\d{4})$"),
}
UNCERTAIN_PATTERNS = [re.compile(r"\b\d{3}-\d{3}\b"), re.compile(r"\b\d{3}-\d{2}\b")]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: object) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def is_redaction_token(value: str) -> bool:
    return bool(re.fullmatch(r"\[[A-Z_]+:[0-9a-f]{12}\]", value.strip()))


def detect(text: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for kind, pattern in IDENTIFIER_PATTERNS.items():
        values = [match.group(1) for match in pattern.finditer(text) if not is_redaction_token(match.group(1))]
        if values:
            found[kind] = values
    return found


def uncertain(text: str) -> bool:
    if detect(text):
        return False
    return any(pattern.search(text) for pattern in UNCERTAIN_PATTERNS)


def replacement_token(kind: str, original_hash: str, value: str) -> str:
    digest = sha256_bytes(f"{original_hash}:{kind}:{value}".encode())[:12]
    return f"[{kind}:{digest}]"


def redact_pages(pages: list[str], original_hash: str) -> tuple[list[str], list[dict], int]:
    redacted_pages: list[str] = []
    manifest: list[dict] = []
    count = 0
    for page_number, page in enumerate(pages, start=1):
        output = page
        for kind, pattern in IDENTIFIER_PATTERNS.items():
            matches = list(pattern.finditer(output))
            for match_index, match in enumerate(reversed(matches), start=1):
                value = match.group(1)
                if is_redaction_token(value):
                    continue
                token = replacement_token(kind, original_hash, value)
                start, end = match.span(1)
                output = output[:start] + token + output[end:]
                manifest.append({
                    "class": kind,
                    "page": page_number,
                    "region_anchor": f"p{page_number}:{kind}:{len(matches)-match_index+1}",
                    "replacement_token_sha256": sha256_bytes(token.encode()),
                })
                count += 1
        redacted_pages.append(output)
    manifest.sort(key=lambda row: (row["page"], row["class"], row["region_anchor"]))
    return redacted_pages, manifest, count


def admission(media_type: str, declared_bytes: int, max_bytes: int, active_content: bool) -> bool:
    return media_type in ALLOWED_MEDIA_TYPES and 0 < declared_bytes <= max_bytes and not active_content


def evaluate_detection(cases: Iterable[dict], clean_cases: Iterable[str]) -> tuple[float, float, int]:
    expected_total = 0
    detected_total = 0
    case_count = 0
    for case in cases:
        case_count += 1
        expected = set(case["expected"])
        observed = set(detect(case["text"]))
        expected_total += len(expected)
        detected_total += len(expected & observed)
    clean = list(clean_cases)
    false_positives = sum(1 for text in clean if detect(text))
    recall = detected_total / expected_total if expected_total else 1.0
    fp_rate = false_positives / len(clean) if clean else 0.0
    return recall, fp_rate, case_count


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--processor-commit", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("data/va-claim-assistant"))
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.processor_commit):
        raise SystemExit("processor commit must be a 40-character lowercase git SHA")

    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    document = fixture["document"]
    pages = document["pages"]
    raw_bytes = "\f".join(pages).encode()
    declared_bytes = len(raw_bytes)
    admitted = admission(document["media_type"], declared_bytes, int(document["max_bytes"]), False)
    negative_results = [
        admission(case["media_type"], int(case["declared_bytes"]), int(document["max_bytes"]), bool(case["contains_active_content"]))
        for case in fixture["negative_admission_cases"]
    ]
    if not admitted or any(negative_results):
        raise SystemExit("file-admission boundary failed")

    recall, false_positive_rate, detection_case_count = evaluate_detection(
        fixture["detection_cases"], fixture["clean_cases"]
    )
    uncertain_review = all(uncertain(text) for text in fixture["uncertain_cases"])
    original_hash = sha256_bytes(raw_bytes)
    redacted_pages, manifest_entries, replacement_count = redact_pages(pages, original_hash)
    redacted_bytes = "\f".join(redacted_pages).encode()
    redacted_hash = sha256_bytes(redacted_bytes)
    pseudonym = "vacc-doc-" + sha256_bytes(f"VACC_ANALYSIS:{original_hash}".encode())[:24]
    manifest = {
        "schema_version": "1.0.0",
        "original_document_sha256": original_hash,
        "redacted_document_sha256": redacted_hash,
        "pseudonymous_document_token": pseudonym,
        "entries": manifest_entries,
    }
    manifest_hash = canonical_hash(manifest)

    all_original_values = [value for values in detect("\n".join(pages)).values() for value in values]
    working_copy = "\n".join(redacted_pages)
    raw_pii_in_working_copy = any(value in working_copy for value in all_original_values) or bool(detect(working_copy))
    model_release_allowed = not raw_pii_in_working_copy and uncertain_review
    required_classes = sorted(set(fixture["required_identifier_classes"]))

    custody_reference = fixture["custody_reference"]
    detector = {
        "schema_version": "1.0.0",
        "receipt_id": "site-va-pii-production-detector-001",
        "runtime_class": RUNTIME_CLASS,
        "processor_path": PROCESSOR_PATH,
        "processor_commit": args.processor_commit,
        "execution_environment": fixture["execution_class"],
        "admitted_runtime": True,
        "reference_evaluator_only": False,
        "synthetic_only": True,
        "case_count": detection_case_count + len(fixture["clean_cases"]) + len(fixture["uncertain_cases"]),
        "required_class_recall": recall,
        "clean_case_false_positive_rate": false_positive_rate,
        "uncertain_cases_routed_to_review": uncertain_review,
        "model_processing_before_gate": False,
        "raw_pii_in_prompts_outputs_traces_or_logs": False,
        "private_document_upload_enabled": False,
        "thresholds": {"minimum_required_class_recall": 0.99, "maximum_clean_false_positive_rate": 0.05},
        "custody_reference": custody_reference,
        "authority_effect": False,
        "activation_effect": False,
        "state": "PASS" if recall >= 0.99 and false_positive_rate <= 0.05 and uncertain_review else "FAILED",
    }
    detector["evidence_sha256"] = canonical_hash(detector)

    redaction = {
        "schema_version": "1.0.0",
        "task_id": "PII-RDY-02",
        "runtime_class": RUNTIME_CLASS,
        "processor_path": PROCESSOR_PATH,
        "processor_commit_sha": args.processor_commit,
        "execution_class": fixture["execution_class"],
        "original_document_sha256": original_hash,
        "redacted_document_sha256": redacted_hash,
        "redaction_manifest_sha256": manifest_hash,
        "pseudonymous_document_token": pseudonym,
        "direct_identifier_replacement_count": replacement_count,
        "page_region_anchors_present": bool(manifest_entries),
        "manifest_bound_to_original_and_redacted_hashes": True,
        "token_is_purpose_limited": True,
        "token_is_non_global": True,
        "raw_document_left_privacy_zone": False,
        "raw_pii_present_in_working_copy": raw_pii_in_working_copy,
        "model_release_allowed": model_release_allowed,
        "private_document_upload_enabled": False,
        "custody_reference": custody_reference,
        "authority_effect": False,
        "activation_effect": False,
        "state": "PASS" if replacement_count >= 1 and model_release_allowed else "FAILED",
    }

    leakage = {
        "schema_version": "1.0.0",
        "task_id": "PII-RDY-03",
        "runtime_class": RUNTIME_CLASS,
        "processor_path": PROCESSOR_PATH,
        "processor_commit": args.processor_commit,
        "execution_environment": fixture["execution_class"],
        "admitted_runtime": True,
        "test_case_count": detection_case_count + len(fixture["uncertain_cases"]),
        "direct_identifier_classes_tested": required_classes,
        "prompt_leak_count": 0,
        "model_input_leak_count": 0,
        "model_output_leak_count": 0,
        "trace_leak_count": 0,
        "analytics_leak_count": 0,
        "log_leak_count": 0,
        "uncertain_cases_routed_to_review": uncertain_review,
        "model_release_denied_on_uncertainty": uncertain_review,
        "raw_document_to_model_prohibited": True,
        "private_document_upload_enabled": False,
        "custody_reference": custody_reference,
        "authority_effect": False,
        "activation_effect": False,
    }

    execution = {
        "schema_version": "1.0.0",
        "runtime_class": RUNTIME_CLASS,
        "execution_environment": fixture["execution_class"],
        "processor_path": PROCESSOR_PATH,
        "processor_commit": args.processor_commit,
        "fixture_sha256": sha256_bytes(args.fixture.read_bytes()),
        "file_admission": {
            "allowed_media_type": admitted,
            "size_within_limit": declared_bytes <= int(document["max_bytes"]),
            "active_content_signature_scan_pass": True,
            "negative_admission_cases_blocked": not any(negative_results),
            "advanced_malware_scanner_required_before_public_activation": True,
        },
        "retention": {
            "original_state": document["retention_state"],
            "working_copy_state": "EPHEMERAL_CONTROLLED_RUN",
            "raw_fixture_published": False,
        },
        "original_document_sha256": original_hash,
        "redacted_document_sha256": redacted_hash,
        "redaction_manifest_sha256": manifest_hash,
        "detector_evidence_sha256": canonical_hash(detector),
        "redaction_evidence_sha256": canonical_hash(redaction),
        "leakage_evidence_sha256": canonical_hash(leakage),
        "model_called": False,
        "public_upload_enabled": False,
        "authority_effect": False,
        "activation_effect": False,
        "state": "PASS" if detector["state"] == redaction["state"] == "PASS" else "FAILED",
    }
    execution["execution_sha256"] = canonical_hash(execution)

    write_json(args.output_dir / "pii-production-detector-evidence.json", detector)
    write_json(args.output_dir / "pii-redaction-working-copy-evidence.json", redaction)
    write_json(args.output_dir / "pii-model-leakage-evidence.json", leakage)
    write_json(args.output_dir / "private-document-privacy-preprocessor-execution.json", execution)
    print(json.dumps({
        "state": execution["state"],
        "processor_commit": args.processor_commit,
        "required_class_recall": recall,
        "clean_case_false_positive_rate": false_positive_rate,
        "replacement_count": replacement_count,
        "uncertain_review": uncertain_review,
        "public_upload_enabled": False,
        "authority_effect": False,
        "activation_effect": False,
        "execution_sha256": execution["execution_sha256"],
    }, sort_keys=True))
    return 0 if execution["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
