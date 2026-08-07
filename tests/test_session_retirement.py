#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "check_session_retirement.py"
spec = importlib.util.spec_from_file_location("check_session_retirement", MODULE_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


def receipt(**overrides):
    value = {
        "session_id": "session-test",
        "repository": "StegVerse-Labs/Site",
        "task_id": "TASK-1",
        "posture": "ARCHIVABLE",
        "authority_checked": ["docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md"],
        "active_task_ownership": False,
        "unique_unmerged_state": False,
        "safe_to_archive": True,
        "successor_execution_source": "docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md",
        "conflicting_active_owner": False,
        "material_state_locations": ["docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md"],
        "required_before_archive": [],
        "reason": "fixture",
    }
    value.update(overrides)
    return value


class SessionRetirementPostureTests(unittest.TestCase):
    def validate(self, value):
        failures = []
        validator.validate_receipt(value, 0, failures)
        return failures

    def test_archivable_is_admitted(self):
        self.assertEqual(self.validate(receipt()), [])

    def test_merge_required_is_rejected_from_archive(self):
        failures = self.validate(receipt(posture="MERGE_REQUIRED", unique_unmerged_state=True, safe_to_archive=True))
        self.assertTrue(any("MERGE_REQUIRED cannot be safe to archive" in item for item in failures))

    def test_current_requires_active_ownership(self):
        failures = self.validate(receipt(posture="CURRENT", active_task_ownership=False, safe_to_archive=False))
        self.assertTrue(any("CURRENT must set active_task_ownership=true" in item for item in failures))

    def test_superseded_is_valid_nonarchive_posture(self):
        failures = self.validate(receipt(posture="SUPERSEDED", safe_to_archive=False))
        self.assertEqual(failures, [])

    def test_conflicting_owner_blocks_archive(self):
        failures = self.validate(receipt(conflicting_active_owner=True))
        self.assertTrue(any("conflicting active owner" in item for item in failures))

    def test_missing_successor_blocks_archive(self):
        failures = self.validate(receipt(successor_execution_source=""))
        self.assertTrue(any("lacks successor execution source" in item for item in failures))

    def test_malformed_evidence_blocks_archive(self):
        failures = self.validate(receipt(authority_checked=[]))
        self.assertTrue(any("authority_checked" in item for item in failures))

    def test_active_owner_blocks_archive(self):
        failures = self.validate(receipt(active_task_ownership=True))
        self.assertTrue(any("still owns active work" in item for item in failures))

    def test_duplicate_current_owner_is_rejected(self):
        first = receipt(
            session_id="current-a",
            posture="CURRENT",
            active_task_ownership=True,
            safe_to_archive=False,
        )
        second = receipt(
            session_id="current-b",
            posture="CURRENT",
            active_task_ownership=True,
            safe_to_archive=False,
        )
        failures = validator.duplicate_current_owner_failures([first, second])
        self.assertEqual(len(failures), 1)
        self.assertIn("multiple CURRENT owners", failures[0])


if __name__ == "__main__":
    unittest.main()
