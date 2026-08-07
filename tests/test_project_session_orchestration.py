#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "project_session_orchestration.py"
spec = importlib.util.spec_from_file_location("project_session_orchestration", MODULE_PATH)
projector = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(projector)


def session(session_id: str, posture: str, *, safe: bool, active: bool = False, unique: bool = False):
    return {
        "session_id": session_id,
        "repository": "StegVerse-Labs/Site",
        "task_id": f"TASK-{session_id}",
        "posture": posture,
        "safe_to_archive": safe,
        "active_task_ownership": active,
        "unique_unmerged_state": unique,
        "conflicting_active_owner": False,
        "successor_execution_source": "docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md",
        "authority_checked": ["docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md"],
        "material_state_locations": ["docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md"],
        "required_before_archive": [],
        "reason": "fixture",
    }


def cross_report(status: str = "PASS"):
    return {
        "state_type": "session_orchestration_cross_repository_report",
        "status": status,
        "summary": {
            "target_count": 4,
            "passing_targets": 4 if status == "PASS" else 3,
            "owner_collision_count": 0,
            "stale_handoff_count": 0,
            "unresolved_successor_count": 0,
        },
        "delegated_dependencies": [
            {"repository": "master-records/orchestration", "state": "DEPENDENCY_BLOCKED_NOT_VERIFIED_BY_SITE_TOKEN"}
        ],
    }


class SessionProjectionTests(unittest.TestCase):
    def test_archive_candidate_is_complete_without_ui_claim(self):
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [session("a", "ARCHIVABLE", safe=True)]}
        successors, queue = projector.build(registry)
        self.assertEqual(successors["status"], "PASS")
        self.assertEqual(queue["entries"][0]["queue_state"], "COMPLETE")
        self.assertTrue(queue["entries"][0]["archive_candidate"])
        self.assertFalse(queue["entries"][0]["ui_archive_action_performed"])

    def test_current_owner_becomes_successor_frontier(self):
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [session("c", "CURRENT", safe=False, active=True)]}
        successors, queue = projector.build(registry)
        self.assertEqual(successors["frontier_state"], "READY")
        self.assertEqual(successors["next_executable"]["session_id"], "c")
        self.assertEqual(queue["entries"][0]["queue_state"], "CLAIMED")

    def test_merge_required_is_review_required_not_archive(self):
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [session("m", "MERGE_REQUIRED", safe=False, unique=True)]}
        _, queue = projector.build(registry)
        row = queue["entries"][0]
        self.assertEqual(row["queue_state"], "REVIEW_REQUIRED")
        self.assertFalse(row["archive_candidate"])

    def test_superseded_is_not_silently_archived(self):
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [session("s", "SUPERSEDED", safe=False)]}
        _, queue = projector.build(registry)
        self.assertEqual(queue["entries"][0]["queue_state"], "SUPERSEDED")
        self.assertFalse(queue["entries"][0]["archive_candidate"])

    def test_duplicate_current_owner_fails_projection(self):
        first = session("x", "CURRENT", safe=False, active=True)
        second = session("y", "CURRENT", safe=False, active=True)
        second["task_id"] = first["task_id"]
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [first, second]}
        successors, queue = projector.build(registry)
        self.assertEqual(successors["status"], "FAIL")
        self.assertEqual(queue["status"], "FAIL")
        self.assertTrue(any("multiple CURRENT owners" in value for value in successors["failures"]))

    def test_unresolved_successor_fails_closed(self):
        row = session("z", "CURRENT", safe=False, active=True)
        row["successor_execution_source"] = "does/not/exist.md"
        successors, _ = projector.build({"repository": "StegVerse-Labs/Site", "sessions": [row]})
        self.assertEqual(successors["status"], "FAIL")
        self.assertTrue(any("unresolved successor" in value for value in successors["failures"]))

    def test_cross_repository_pass_is_bound_into_projection(self):
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [session("c", "CURRENT", safe=False, active=True)]}
        successors, queue = projector.build(registry, cross_report("PASS"))
        self.assertEqual(successors["status"], "PASS")
        self.assertEqual(successors["cross_repository_authority"]["status"], "PASS")
        self.assertEqual(queue["cross_repository_authority"]["summary"]["target_count"], 4)
        self.assertEqual(len(successors["cross_repository_authority"]["delegated_dependencies"]), 1)

    def test_cross_repository_failure_blocks_frontier_and_queue(self):
        registry = {"repository": "StegVerse-Labs/Site", "sessions": [session("c", "CURRENT", safe=False, active=True)]}
        successors, queue = projector.build(registry, cross_report("FAIL"))
        self.assertEqual(successors["status"], "FAIL")
        self.assertEqual(queue["status"], "FAIL")
        self.assertEqual(successors["frontier_state"], "REVIEW_REQUIRED")
        self.assertTrue(any("cross-repository authority comparison" in value for value in successors["failures"]))


if __name__ == "__main__":
    unittest.main()
