#!/usr/bin/env python3
"""Deterministic positive and negative fixtures for the HIL pilot toolchain."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from stegverse_jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/hil-pilot-ledger.json"
LEDGER_SCHEMA = ROOT / "data/schemas/hil-pilot-ledger.schema.json"
ACK_SCHEMA = ROOT / "data/schemas/hil-managed-receiving-acknowledgment.schema.json"
COMPARISON_SCHEMA = ROOT / "data/schemas/hil-pilot-comparison.schema.json"
VALIDATOR = ROOT / "scripts/validate_hil_pilot_ledger.py"
INGEST = ROOT / "scripts/ingest_hil_pilot_return.py"
COMPARE = ROOT / "scripts/generate_hil_pilot_comparison.py"
PRIMARY_VERSION = "v1.1"
PRIMARY_HASH = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT_VERSION = "HIL-PROMPT-v1.1"
PROMPT_HASH = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
PDF_BYTES = b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_package_hash(package: dict) -> str:
    value = dict(package)
    value.pop("package_sha256", None)
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def run(command: list[str], expect_success: bool, expected_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    combined = result.stdout + result.stderr
    if (result.returncode == 0) != expect_success:
        raise AssertionError(f"unexpected exit {result.returncode}: {' '.join(command)}\n{combined}")
    if expected_text and expected_text not in combined:
        raise AssertionError(f"missing expected text {expected_text!r}:\n{combined}")
    return result


def validate_schema(path: Path, schema_path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        raise AssertionError("; ".join(error.message for error in errors))
    return value


def package_for(pdf: bytes = PDF_BYTES) -> dict:
    package = {
        "package_id": "HIL-PACKAGE-TEST-001",
        "canonical_paper_version": PRIMARY_VERSION,
        "canonical_paper_sha256": PRIMARY_HASH,
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": PROMPT_HASH,
        "response_pdf_sha256": sha(pdf),
        "response_pdf_size": len(pdf),
    }
    package["package_sha256"] = canonical_package_hash(package)
    return package


def verified_entry(entry: dict, suffix: str) -> dict:
    result = copy.deepcopy(entry)
    result["submission_id"] = f"HIL-PILOT-VERIFIED-{suffix}"
    result["response_pdf_filename"] = f"response-{suffix.lower()}.pdf"
    result["response_pdf_sha256"] = sha((suffix + "-response").encode())
    result["response_pdf_size"] = 128
    result["package_id"] = f"HIL-PACKAGE-{suffix}"
    result["package_sha256"] = sha((suffix + "-package").encode())
    result["return_mode"] = "participant_managed_direct_return"
    result["received_timestamp"] = "2026-07-31T00:00:00Z"
    result["verification_status"] = "RETURN_PACKAGE_VERIFIED"
    result["custody_status"] = "MANAGED_RETURN_PRESERVED_NO_GOVERNED_CUSTODY"
    result["claims_withheld"] = [
        "governed_receiver_custody",
        "registry_commit",
        "private_review_acceptance",
        "publication",
        "master_record_release",
    ]
    return result


def main() -> int:
    cases = 0
    with tempfile.TemporaryDirectory(prefix="hil-pilot-fixtures-") as directory:
        temp = Path(directory)
        canonical = json.loads(LEDGER.read_text(encoding="utf-8"))

        run([sys.executable, str(VALIDATOR)], True, "PASS:")
        cases += 1

        stale = copy.deepcopy(canonical)
        stale["counts"]["completed_response_pdfs_confirmed"] = 1
        stale_path = temp / "ledger-stale-count.json"
        write_json(stale_path, stale)
        run([sys.executable, str(VALIDATOR), "--ledger", str(stale_path)], False, "derived=0")
        cases += 1

        escalated = copy.deepcopy(canonical)
        escalated["entries"][0]["registry_status"] = "REGISTERED"
        escalated_path = temp / "ledger-authority-escalation.json"
        write_json(escalated_path, escalated)
        run([sys.executable, str(VALIDATOR), "--ledger", str(escalated_path)], False, "pending entry escalates")
        cases += 1

        pdf_path = temp / "response.pdf"
        pdf_path.write_bytes(PDF_BYTES)
        package = package_for()
        package_path = temp / "package.json"
        write_json(package_path, package)
        receipt_path = temp / "receipt.json"
        write_json(receipt_path, {"response_pdf_sha256": sha(PDF_BYTES), "package_sha256": canonical_package_hash(package)})
        ack_path = temp / "ack.json"
        run([sys.executable, str(INGEST), str(pdf_path), str(package_path), "--local-receipt", str(receipt_path), "--output", str(ack_path)], True, "VERIFIED_MANAGED_RETURN")
        acknowledgment = validate_schema(ack_path, ACK_SCHEMA)
        assert acknowledgment["authority_effect"] is False
        assert acknowledgment["custody_status"] == "MANAGED_RETURN_PRESERVED_NO_GOVERNED_CUSTODY"
        cases += 1

        non_pdf = temp / "not-pdf.bin"
        non_pdf.write_bytes(b"not a pdf")
        bad_package = package_for(b"not a pdf")
        bad_package_path = temp / "non-pdf-package.json"
        write_json(bad_package_path, bad_package)
        run([sys.executable, str(INGEST), str(non_pdf), str(bad_package_path), "--output", str(temp / "non-pdf-ack.json")], False, "invalid PDF signature")
        cases += 1

        bad_signature = temp / "bad-signature.pdf"
        bad_signature.write_bytes(b"PDF-1.4 invalid")
        bad_signature_package = package_for(b"PDF-1.4 invalid")
        bad_signature_package_path = temp / "bad-signature-package.json"
        write_json(bad_signature_package_path, bad_signature_package)
        run([sys.executable, str(INGEST), str(bad_signature), str(bad_signature_package_path), "--output", str(temp / "bad-signature-ack.json")], False, "invalid PDF signature")
        cases += 1

        def reject_package(name: str, mutate, expected: str) -> None:
            candidate = package_for()
            mutate(candidate)
            path = temp / f"{name}.json"
            write_json(path, candidate)
            run([sys.executable, str(INGEST), str(pdf_path), str(path), "--output", str(temp / f"{name}-ack.json")], False, expected)

        reject_package("sha-mismatch", lambda value: value.__setitem__("response_pdf_sha256", "0" * 64), "response PDF SHA-256 mismatch")
        cases += 1
        reject_package("size-mismatch", lambda value: value.__setitem__("response_pdf_size", len(PDF_BYTES) + 1), "response PDF size mismatch")
        cases += 1
        reject_package("paper-mismatch", lambda value: value.__setitem__("canonical_paper_version", "v0"), "canonical paper identity mismatch")
        cases += 1
        reject_package("prompt-mismatch", lambda value: value.__setitem__("prompt_version", "HIL-PROMPT-v0"), "prompt identity mismatch")
        cases += 1
        reject_package("package-hash-mismatch", lambda value: value.__setitem__("package_sha256", "f" * 64), "package canonical hash mismatch")
        cases += 1

        malformed_receipt = temp / "malformed-receipt.json"
        malformed_receipt.write_text("{not-json", encoding="utf-8")
        run([sys.executable, str(INGEST), str(pdf_path), str(package_path), "--local-receipt", str(malformed_receipt), "--output", str(temp / "malformed-ack.json")], False, "JSONDecodeError")
        cases += 1

        mismatched_receipt = temp / "mismatched-receipt.json"
        write_json(mismatched_receipt, {"response_pdf_sha256": "0" * 64, "package_sha256": canonical_package_hash(package)})
        run([sys.executable, str(INGEST), str(pdf_path), str(package_path), "--local-receipt", str(mismatched_receipt), "--output", str(temp / "mismatch-ack.json")], False, "local receipt PDF hash mismatch")
        cases += 1

        authority_ack = copy.deepcopy(acknowledgment)
        authority_ack["custody_status"] = "GOVERNED_RECEIVER_CUSTODY"
        schema = json.loads(ACK_SCHEMA.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(authority_ack))
        if not errors:
            raise AssertionError("authority-escalating acknowledgment unexpectedly validated")
        cases += 1

        run([sys.executable, str(COMPARE), "--ledger", str(LEDGER), "--output", str(temp / "comparison-blocked.json")], False, "at least two verified response packages")
        cases += 1

        comparison_ledger = copy.deepcopy(canonical)
        comparison_ledger["entries"] = [
            verified_entry(canonical["entries"][0], "CLAUDE"),
            verified_entry(canonical["entries"][1], "CHATGPT"),
        ]
        comparison_ledger["counts"] = {
            "model_requests_initiated": 2,
            "completed_response_pdfs_confirmed": 2,
            "verified_return_packages": 2,
            "managed_receiving_acknowledgments": 0,
            "governed_receiver_receipts": 0,
        }
        comparison_ledger_path = temp / "comparison-ledger.json"
        write_json(comparison_ledger_path, comparison_ledger)
        run([sys.executable, str(VALIDATOR), "--ledger", str(comparison_ledger_path)], True, "PASS:")
        comparison_path = temp / "comparison.json"
        run([sys.executable, str(COMPARE), "--ledger", str(comparison_ledger_path), "--output", str(comparison_path)], True)
        comparison = validate_schema(comparison_path, COMPARISON_SCHEMA)
        for item in comparison["comparisons"]:
            assert "agreement" in item and "disagreement" in item and "uncertainty" in item
        assert comparison["limitations"]
        assert "scientific_validation" in comparison["claims_withheld"]
        cases += 1

    print(f"PASS: {cases} deterministic HIL pilot positive/negative fixture cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
