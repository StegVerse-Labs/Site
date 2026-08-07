#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "check_session_cross_repository.py"
spec = importlib.util.spec_from_file_location("check_session_cross_repository", MODULE_PATH)
checker = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(checker)


def target(repo: str, scope: str, *, active: bool = True, expected_sha: str = "handoff-sha"):
    return {
        "repository": repo,
        "branch": "main",
        "mode": "github",
        "canonical_handoff": "HANDOFF.md",
        "expected_handoff_sha": expected_sha,
        "required_markers": ["OWNER", "STATE"],
        "task_id": f"TASK-{repo}",
        "claim_scope": scope,
        "claim_active": active,
        "canonical_owner": f"owner:{repo}",
        "successor_execution_source": "workflow.yml",
    }


def config(*targets):
    return {"schema_version": "1.0.0", "policy": {}, "targets": list(targets)}


def fetcher_factory(overrides=None):
    overrides = overrides or {}

    def fetcher(target_value, path):
        key = (target_value["repository"], path)
        if key in overrides:
            value = overrides[key]
            if isinstance(value, Exception):
                raise value
            return value
        if path == "HANDOFF.md":
            return {"sha": "handoff-sha", "content": "OWNER\nSTATE\n"}
        return {"sha": "successor-sha", "content": "ok\n"}

    return fetcher


class CrossRepositoryComparisonTests(unittest.TestCase):
    def test_valid_distinct_claim_scopes_pass(self):
        report = checker.evaluate(
            config(target("org/a", "SCOPE_A"), target("org/b", "SCOPE_B")),
            fetcher_factory(),
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["summary"]["passing_targets"], 2)
        self.assertEqual(report["owner_collisions"], [])

    def test_stale_handoff_fails_closed(self):
        report = checker.evaluate(
            config(target("org/a", "SCOPE_A"), target("org/b", "SCOPE_B")),
            fetcher_factory({("org/b", "HANDOFF.md"): {"sha": "new-sha", "content": "OWNER\nSTATE\n"}}),
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("STALE_HANDOFF" in value for value in report["failures"]))

    def test_missing_authority_marker_fails_closed(self):
        report = checker.evaluate(
            config(target("org/a", "SCOPE_A"), target("org/b", "SCOPE_B")),
            fetcher_factory({("org/b", "HANDOFF.md"): {"sha": "handoff-sha", "content": "OWNER\n"}}),
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("MISSING_AUTHORITY" in value for value in report["failures"]))

    def test_unresolved_successor_fails_closed(self):
        report = checker.evaluate(
            config(target("org/a", "SCOPE_A"), target("org/b", "SCOPE_B")),
            fetcher_factory({("org/b", "workflow.yml"): FileNotFoundError("missing")}),
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("UNRESOLVED_SUCCESSOR" in value for value in report["failures"]))

    def test_duplicate_active_claim_scope_fails_closed(self):
        report = checker.evaluate(
            config(target("org/a", "SAME_SCOPE"), target("org/b", "SAME_SCOPE")),
            fetcher_factory(),
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["summary"]["owner_collision_count"], 1)
        self.assertTrue(any("CONFLICTING_OWNER" in value for value in report["failures"]))

    def test_inactive_same_scope_is_not_owner_collision(self):
        report = checker.evaluate(
            config(target("org/a", "SAME_SCOPE"), target("org/b", "SAME_SCOPE", active=False)),
            fetcher_factory(),
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["owner_collisions"], [])

    def test_duplicate_repository_entry_is_ambiguous(self):
        report = checker.evaluate(
            config(target("org/a", "SCOPE_A"), target("org/a", "SCOPE_B")),
            fetcher_factory(),
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("AMBIGUOUS_REPOSITORY_TARGET" in value for value in report["failures"]))


if __name__ == "__main__":
    unittest.main()
