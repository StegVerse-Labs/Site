#!/usr/bin/env python3
"""Regression tests for the governed HIL HTTPS receiver probe importer."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "check_hil_https_receiver_probe_import.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("hil_probe_import_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_import() -> dict:
    return {
        "schema_version": "HIL-HTTPS-RECEIVER-PROBE-IMPORT-v1",
        "source_repository": "StegVerse-org/LLM-adapter",
        "source_commit": "a" * 40,
        "source_evidence_path": "reports/hil-https-receiver-probe.json",
        "source_evidence_sha256": "b" * 64,
        "receiver_origin": "https://receiver.example",
        "resolved_public_addresses": ["8.8.8.8", "2606:4700:4700::1111"],
        "readiness_path": "/api/hil/readiness",
        "contract_state": "CONFORMING_V1_1_READINESS_OBSERVED",
        "tls_verified": True,
        "redirects_followed": False,
        "response_size_bytes": 4096,
        "http_status": 200,
        "primary_sha256": "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462",
        "prompt_sha256": "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c",
        "protocol_version": "HIL-PROTOCOL-v1.1",
        "prompt_version": "HIL-PROMPT-v1.1",
        "provenance_manifest_schema": "HIL-RESPONSE-PROVENANCE-v1.1",
        "mutation_performed": False,
        "authority": {
            "execution": False,
            "activation": False,
            "publication": False,
            "release": False,
            "custody": False,
            "master_record_append": False,
        },
    }


class ProbeImportValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def validate(self, payload: dict) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.json"
            path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
            self.validator.validate(path)

    def assert_rejected(self, payload: dict) -> None:
        with self.assertRaises(SystemExit):
            self.validate(payload)

    def test_accepts_public_origin_bound_evidence(self) -> None:
        self.validate(valid_import())

    def test_rejects_localhost_origin(self) -> None:
        payload = valid_import()
        payload["receiver_origin"] = "https://localhost"
        self.assert_rejected(payload)

    def test_rejects_private_loopback_link_local_and_reserved_addresses(self) -> None:
        for address in ["127.0.0.1", "10.0.0.7", "169.254.169.254", "::1", "fc00::1", "192.0.2.1"]:
            with self.subTest(address=address):
                payload = valid_import()
                payload["resolved_public_addresses"] = [address]
                self.assert_rejected(payload)

    def test_rejects_redirected_observation(self) -> None:
        payload = valid_import()
        payload["redirects_followed"] = True
        self.assert_rejected(payload)

    def test_rejects_oversized_or_empty_response(self) -> None:
        for size in [0, 65537]:
            with self.subTest(size=size):
                payload = valid_import()
                payload["response_size_bytes"] = size
                self.assert_rejected(payload)

    def test_rejects_duplicate_addresses(self) -> None:
        payload = valid_import()
        payload["resolved_public_addresses"] = ["8.8.8.8", "8.8.8.8"]
        self.assert_rejected(payload)

    def test_rejects_mutation_or_authority(self) -> None:
        payload = valid_import()
        payload["mutation_performed"] = True
        self.assert_rejected(payload)

        payload = valid_import()
        payload["authority"]["activation"] = True
        self.assert_rejected(payload)


if __name__ == "__main__":
    unittest.main()
