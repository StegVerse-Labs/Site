"""Readers accept both the organization-record field names and their legacy names.

MASTER-RECORDS-BULK-SEMANTIC-REMEDIATION-002 renamed Master Records custody fields
to organization-record fields. Writers emit only the new names; readers keep
accepting the legacy names so already-written records stay valid.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class UsageEndpointActivationEvidenceNames(unittest.TestCase):
    def run_with(self, ledger: dict) -> None:
        module = load("check_usage_endpoint_activation_evidence")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text(json.dumps(ledger), encoding="utf-8")
            module.LEDGER = path
            self.assertEqual(module.main(), 0)

    def test_new_name(self):
        ledger = json.loads((ROOT / "data/usage-endpoint-activation-evidence.json").read_text(encoding="utf-8"))
        self.assertIn("master_records_organization_record", ledger["requirements"])
        self.run_with(ledger)

    def test_legacy_name(self):
        ledger = json.loads((ROOT / "data/usage-endpoint-activation-evidence.json").read_text(encoding="utf-8"))
        ledger["requirements"]["master_records_custody"] = ledger["requirements"].pop("master_records_organization_record")
        self.run_with(ledger)


class GovernedTransitionObservatoryNames(unittest.TestCase):
    def run_with(self, executor: dict) -> int:
        module = load("check_governed_transition_observatory")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "executor.json"
            path.write_text(json.dumps(executor), encoding="utf-8")
            module.EXECUTOR = path
            return module.main()

    def executor(self) -> dict:
        return json.loads((ROOT / "data/governed-executor-status.json").read_text(encoding="utf-8"))

    def test_new_name(self):
        self.assertEqual(self.run_with(self.executor()), 0)

    def test_legacy_name(self):
        executor = self.executor()
        boundary = executor["authority_boundary"]
        boundary["projection_is_master_records_custody"] = boundary.pop("projection_is_master_records_organization_record")
        self.assertEqual(self.run_with(executor), 0)

    def test_legacy_name_still_fails_closed(self):
        executor = self.executor()
        boundary = executor["authority_boundary"]
        boundary.pop("projection_is_master_records_organization_record")
        boundary["projection_is_master_records_custody"] = True
        self.assertEqual(self.run_with(executor), 1)


class ErlKvProviderProofProjectionNames(unittest.TestCase):
    def run_with(self, projection: dict) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ("scripts/check_erl_kv_provider_proof_projection.py", "README.md",
                        "docs/ERL_KV_PROVIDER_PROOF_SITE_PROJECTION_MIRROR_HANDOFF.md"):
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, root / rel)
            (root / "data").mkdir()
            (root / "data/erl-kv-provider-proof-projection.json").write_text(json.dumps(projection), encoding="utf-8")
            return subprocess.run([sys.executable, str(root / "scripts/check_erl_kv_provider_proof_projection.py")],
                                  capture_output=True, text=True)

    def projection(self) -> dict:
        return json.loads((ROOT / "data/erl-kv-provider-proof-projection.json").read_text(encoding="utf-8"))

    def test_new_name(self):
        projection = self.projection()
        self.assertIn("master_records_organization_record_commit", projection["upstream"])
        self.assertEqual(self.run_with(projection).returncode, 0)

    def test_legacy_name(self):
        projection = self.projection()
        upstream = projection["upstream"]
        upstream["master_records_custody_commit"] = upstream.pop("master_records_organization_record_commit")
        self.assertEqual(self.run_with(projection).returncode, 0)


if __name__ == "__main__":
    unittest.main()
