#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "reconcile_real_session_dispositions.py"
spec = importlib.util.spec_from_file_location("reconcile_real_session_dispositions", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def registry():
    return {
        "sessions": [
            {
                "session_id": "old",
                "task_id": "DESIGN",
                "posture": "ARCHIVABLE",
                "active_task_ownership": False,
                "unique_unmerged_state": False,
                "safe_to_archive": True,
                "reason": "old work was superseded by the active activation coordination",
            },
            {
                "session_id": "new",
                "task_id": "ACTIVE",
                "posture": "CURRENT",
                "active_task_ownership": True,
                "unique_unmerged_state": False,
                "safe_to_archive": False,
            },
        ]
    }


def evidence():
    return {
        "evidence_id": "fixture",
        "session_id": "old",
        "task_id": "DESIGN",
        "requested_posture": "SUPERSEDED",
        "successor_session_id": "new",
        "successor_task_id": "ACTIVE",
        "successor_owner": "issue",
        "required_source_conditions": {
            "source_active_task_ownership": False,
            "source_unique_unmerged_state": False,
            "source_reason_contains": "superseded by the active activation coordination",
            "successor_posture": "CURRENT",
            "successor_active_task_ownership": True,
        },
        "nonclaims": [],
    }


class RealDispositionTests(unittest.TestCase):
    def test_real_supersession_is_admitted_and_not_archivable(self):
        value = registry()
        receipt = mod.apply_supersession(value, evidence())
        old = value["sessions"][0]
        self.assertEqual(old["posture"], "SUPERSEDED")
        self.assertFalse(old["safe_to_archive"])
        self.assertEqual(receipt["admission_status"], "ADMITTED")
        self.assertEqual(receipt["disposition"], "SUPERSEDED")
        self.assertFalse(receipt["archive_candidate"])
        self.assertEqual(len(receipt["receipt_sha256"]), 64)

    def test_supersession_rejects_missing_reason_evidence(self):
        value = registry()
        value["sessions"][0]["reason"] = "not superseded"
        with self.assertRaises(ValueError):
            mod.apply_supersession(value, evidence())

    def test_supersession_rejects_noncurrent_successor(self):
        value = registry()
        value["sessions"][1]["posture"] = "ARCHIVABLE"
        with self.assertRaises(ValueError):
            mod.apply_supersession(value, evidence())

    def test_candidate_reason_detects_unique_unmerged_state(self):
        self.assertIn("unique_unmerged_state=true", mod.candidate_reason({"unique_unmerged_state": True}))

    def test_candidate_reason_detects_nested_chat_only_requirements(self):
        reasons = mod.candidate_reason({"session_consolidation": {"unique_chat_only_requirements_remaining": 2}})
        self.assertTrue(any("unique_chat_only_requirements_remaining=2" in value for value in reasons))

    def test_candidate_reason_does_not_invent_merge_required(self):
        self.assertEqual(mod.candidate_reason({"safe_to_archive": False, "active_task_ownership": True}), [])


if __name__ == "__main__":
    unittest.main()
