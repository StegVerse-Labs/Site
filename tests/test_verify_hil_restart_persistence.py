#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify_hil_restart_persistence.py"


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class RestartPersistenceTests(unittest.TestCase):
    def build_fixture(self, directory: Path) -> tuple[Path, Path, Path]:
        pdf = b"%PDF-1.4\nsynthetic restart persistence fixture\n%%EOF\n"
        response_hash = hashlib.sha256(pdf).hexdigest()
        unsigned = {
            "schema_version": "HIL-RECEIVER-RECEIPT-v2",
            "receipt_id": "HIL-RECEIPT-test",
            "submission_id": "HIL-SUBMISSION-test",
            "received_at": "2026-07-30T15:00:00Z",
            "submitted_file_sha256": response_hash,
            "primary_sha256": "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462",
            "prompt_sha256": "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c",
            "chain_validation_state": "PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED",
            "custody_state": "EXACT_BYTES_PERSISTED",
            "custody_backend": "portable-sqlite-chunks-v1",
            "registry_state": "RECORDED",
            "review_state": "PENDING",
            "publication_state": "NOT_AUTHORIZED",
            "object_reference": "hil/v1.1/test/response.pdf",
        }
        receipt = dict(unsigned)
        receipt["receipt_sha256"] = hashlib.sha256(canonical_json(unsigned)).hexdigest()
        status = {
            "submission_id": receipt["submission_id"],
            "submitted_file_sha256": response_hash,
            "size_bytes": len(pdf),
            "chunk_count": 1,
            "custody_backend": receipt["custody_backend"],
            "state": "ACCEPTED",
            "created_at": receipt["received_at"],
            "receipt": receipt,
        }
        receipt_path = directory / "receipt.json"
        status_path = directory / "status.json"
        pdf_path = directory / "retrieved.pdf"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        status_path.write_text(json.dumps(status), encoding="utf-8")
        pdf_path.write_bytes(pdf)
        return receipt_path, status_path, pdf_path

    def run_verifier(self, receipt: Path, status: Path, pdf: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(receipt), str(status), str(pdf)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_conforming_restart_evidence_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.build_fixture(Path(tmp))
            result = self.run_verifier(*paths)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("HIL_RESTART_PERSISTENCE=PASS", result.stdout)

    def test_changed_bytes_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            receipt, status, pdf = self.build_fixture(Path(tmp))
            pdf.write_bytes(pdf.read_bytes() + b"drift")
            result = self.run_verifier(receipt, status, pdf)
            self.assertNotEqual(result.returncode, 0)

    def test_publication_boundary_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            receipt, status, pdf = self.build_fixture(Path(tmp))
            value = json.loads(receipt.read_text())
            value["publication_state"] = "PUBLISHED"
            unsigned = {key: item for key, item in value.items() if key != "receipt_sha256"}
            value["receipt_sha256"] = hashlib.sha256(canonical_json(unsigned)).hexdigest()
            receipt.write_text(json.dumps(value), encoding="utf-8")
            status_value = json.loads(status.read_text())
            status_value["receipt"] = value
            status.write_text(json.dumps(status_value), encoding="utf-8")
            result = self.run_verifier(receipt, status, pdf)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
