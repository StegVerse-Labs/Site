import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("claims", ROOT / "scripts" / "check_session_work_claims.py")
claims = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(claims)


def base_claim(claim_id: str, task_id: str, work_key: str, surfaces: list[str], paths: list[str]) -> dict:
    return {
        "claim_id": claim_id,
        "session_worker_id": f"worker-{claim_id}",
        "task_id": task_id,
        "originating_goal": "test goal",
        "repository": "StegVerse-Labs/Site",
        "branch": f"test/{claim_id.lower()}",
        "role": "IMPLEMENTATION",
        "state": "CLAIMED",
        "normalized_work_key": work_key,
        "dependency_surface_keys": surfaces,
        "claimed_paths": paths,
        "handoff": "docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md",
        "handoff_revision": "test",
        "claim_created_at": "2026-08-09T14:02:00-05:00",
        "claim_expires_when": "test complete",
        "expected_evidence": ["test"],
        "collision_boundaries": ["test"],
        "next_task_after_release": "next",
    }


class SessionWorkClaimTests(unittest.TestCase):
    def registry(self, existing: list[dict]) -> dict:
        return {
            "repository": "StegVerse-Labs/Site",
            "policy": {
                "one_active_owner_per_task": True,
                "one_active_owner_per_dependency_surface": True,
                "missing_or_stale_claim_fails_closed": True,
                "incidental_dependency_cannot_become_governing_objective": True,
                "distinct_support_roles_require_explicit_non_overlap": True,
                "collision_redirects_to_next_unclaimed_canonical_task": True,
            },
            "claims": existing,
        }

    def test_registry_rejects_duplicate_task_owner(self):
        a = base_claim("A", "TASK-1", "alpha", ["surface:a"], ["a.py"])
        b = base_claim("B", "TASK-1", "beta", ["surface:b"], ["b.py"])
        failures = claims.validate_registry(self.registry([a, b]))
        self.assertTrue(any("task collision" in failure for failure in failures))

    def test_registry_rejects_shared_dependency_surface(self):
        a = base_claim("A", "TASK-1", "alpha", ["deploy:render"], ["a.py"])
        b = base_claim("B", "TASK-2", "beta", ["deploy:render"], ["b.py"])
        failures = claims.validate_registry(self.registry([a, b]))
        self.assertTrue(any("dependency surface collision" in failure for failure in failures))

    def test_render_convergence_blocks_second_adjacent_task(self):
        owner = base_claim("RENDER-OWNER", "TASK-A", "deploy-observation", ["deploy:render"], ["deploy/a.py"])
        candidate = base_claim("ADJACENT", "TASK-B", "unrelated-adjacent-work", ["deploy:render"], ["feature/b.py"])
        candidate["incidental_dependency_keys"] = ["deploy:render"]
        candidate["governing_dependency_keys"] = []
        candidate["next_unclaimed_canonical_task"] = "TASK-B-NEXT"
        decision = claims.evaluate_candidate(self.registry([owner]), candidate)
        self.assertEqual("BLOCK", decision["decision"])
        self.assertEqual("TASK-B-NEXT", decision["next_action"])

    def test_render_cannot_be_promoted_without_canonical_critical_evidence(self):
        candidate = base_claim("ADJACENT", "TASK-B", "unrelated-adjacent-work", ["feature:b"], ["feature/b.py"])
        candidate["governing_dependency_keys"] = ["deploy:render"]
        candidate["incidental_dependency_keys"] = []
        candidate["canonical_task_marks_render_critical"] = False
        decision = claims.evaluate_candidate(self.registry([]), candidate)
        self.assertEqual("BLOCK", decision["decision"])
        self.assertTrue(any("Render cannot become governing objective" in failure for failure in decision["failures"]))

    def test_distinct_support_requires_explicit_non_overlap(self):
        owner = base_claim("OWNER", "TASK-A", "alpha", ["surface:shared"], ["a.py"])
        owner["distinct_support_role"] = True
        candidate = base_claim("VALIDATOR", "TASK-B", "beta", ["surface:shared"], ["b.py"])
        candidate["role"] = "VALIDATION"
        candidate["distinct_support_role"] = True
        decision = claims.evaluate_candidate(self.registry([owner]), candidate)
        self.assertEqual("ADMIT", decision["decision"])

    def test_missing_claim_evidence_fails_closed(self):
        decision = claims.evaluate_candidate(self.registry([]), {"claim_id": "X"})
        self.assertEqual("BLOCK", decision["decision"])
        self.assertEqual("MISSING_REQUIRED_CLAIM_EVIDENCE", decision["reason"])

    def test_canonical_registry_is_valid(self):
        registry = json.loads((ROOT / "data" / "session-work-claims.json").read_text(encoding="utf-8"))
        self.assertEqual([], claims.validate_registry(registry))


if __name__ == "__main__":
    unittest.main()
