#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "admit_session_consolidation.py"
spec = importlib.util.spec_from_file_location("admit_session_consolidation", MODULE_PATH)
intake = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(intake)

RECEIPT_PATH = ROOT / "data" / "session-consolidation-receipts" / "AUTONOMY-ROLE-AWARE-SESSION-2026-08-04.json"


def minimal_registry():
    return {"schema_version": "1.3.0", "sessions": []}


class RegistryIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = intake.load_json(RECEIPT_PATH)

    def test_real_consolidation_receipt_is_admissible(self):
        registry = minimal_registry()
        action, failures = intake.admit(registry, copy.deepcopy(self.receipt), RECEIPT_PATH)
        self.assertEqual(action, "ADMITTED")
        self.assertEqual(failures, [])
        self.assertEqual(registry["sessions"][0]["session_id"], "autonomy-role-aware-continuation-2026-08-04")

    def test_already_admitted_is_idempotent(self):
        registry = minimal_registry()
        action, failures = intake.admit(registry, copy.deepcopy(self.receipt), RECEIPT_PATH)
        self.assertEqual((action, failures), ("ADMITTED", []))
        action, failures = intake.admit(registry, copy.deepcopy(self.receipt), RECEIPT_PATH)
        self.assertEqual((action, failures), ("ALREADY_ADMITTED", []))
        self.assertEqual(len(registry["sessions"]), 1)

    def test_conflicting_existing_disposition_fails_closed(self):
        registry = minimal_registry()
        registry["sessions"].append({
            "session_id": self.receipt["session_id"],
            "task_id": self.receipt["task_id"],
            "posture": "CURRENT",
            "safe_to_archive": False,
            "active_task_ownership": True,
            "unique_unmerged_state": False,
        })
        action, failures = intake.admit(registry, copy.deepcopy(self.receipt), RECEIPT_PATH)
        self.assertEqual(action, "REJECTED")
        self.assertTrue(any("conflicting registry disposition" in value for value in failures))

    def test_current_owner_for_same_task_fails_closed(self):
        registry = minimal_registry()
        registry["sessions"].append({
            "session_id": "other-current-session",
            "repository": self.receipt["repository"],
            "task_id": self.receipt["task_id"],
            "posture": "CURRENT",
            "active_task_ownership": True,
        })
        action, failures = intake.admit(registry, copy.deepcopy(self.receipt), RECEIPT_PATH)
        self.assertEqual(action, "REJECTED")
        self.assertTrue(any("CURRENT active owner" in value for value in failures))

    def test_unsafe_receipt_fails_closed(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["safe_to_archive"] = False
        action, failures = intake.admit(minimal_registry(), receipt, RECEIPT_PATH)
        self.assertEqual(action, "REJECTED")
        self.assertTrue(any("safe_to_archive=true" in value for value in failures))


if __name__ == "__main__":
    unittest.main()
