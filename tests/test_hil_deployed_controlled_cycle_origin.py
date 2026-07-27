#!/usr/bin/env python3
"""Regression tests for deployed HIL controlled-cycle origin admissibility."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "check_hil_deployed_controlled_cycle_evidence.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("hil_deployed_cycle_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load deployed-cycle validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DeployedCycleOriginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_rejects_localhost_and_local_literals(self) -> None:
        for origin in (
            "https://localhost",
            "https://service.localhost",
            "https://127.0.0.1",
            "https://10.0.0.7",
            "https://169.254.169.254",
            "https://[::1]",
            "https://[fc00::1]",
        ):
            with self.subTest(origin=origin):
                self.assertFalse(self.validator.valid_https_origin(origin))

    def test_rejects_credentials_paths_queries_and_fragments(self) -> None:
        for origin in (
            "https://user:pass@example.com",
            "https://example.com/api",
            "https://example.com?token=x",
            "https://example.com#fragment",
            "http://example.com",
        ):
            with self.subTest(origin=origin):
                self.assertFalse(self.validator.valid_https_origin(origin))

    @patch("socket.getaddrinfo")
    def test_accepts_hostname_only_when_all_answers_are_global(self, mocked) -> None:
        mocked.return_value = [
            (2, 1, 6, "", ("8.8.8.8", 443)),
            (10, 1, 6, "", ("2606:4700:4700::1111", 443, 0, 0)),
        ]
        self.assertTrue(self.validator.valid_https_origin("https://receiver.example"))

        mocked.return_value = [
            (2, 1, 6, "", ("8.8.8.8", 443)),
            (2, 1, 6, "", ("10.0.0.7", 443)),
        ]
        self.assertFalse(self.validator.valid_https_origin("https://receiver.example"))

    @patch("socket.getaddrinfo", side_effect=OSError("resolution failed"))
    def test_rejects_unresolvable_hostname(self, mocked) -> None:
        self.assertFalse(self.validator.valid_https_origin("https://missing.example"))


if __name__ == "__main__":
    unittest.main()
