from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "site_handoff_orchestrator",
    ROOT / "scripts/site_handoff_orchestrator.py",
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def base_claim() -> dict:
    return {
        "claim_id": "SITE-TEST-CLAIM-001",
        "session_worker_id": "chatgpt:test",
        "task_id": "SITE-TEST-001",
        "originating_goal": "test terminalization",
        "repository": "StegVerse-Labs/Site",
        "branch": "fix/test-branch",
        "role": "ACTIVE_IMPLEMENTATION",
        "state": "CLAIMED_FOR_IMPLEMENTATION",
        "normalized_work_key": "site-test-claim-001",
        "dependency_surface_keys": ["site:test-surface"],
        "governing_dependency_keys": ["site:test-surface"],
        "incidental_dependency_keys": [],
        "claimed_paths": [
            "scripts/example.py",
            "data/session-work-claims.d/test.json",
        ],
        "handoff": "SITE_MIRROR_HANDOFF.md",
        "handoff_revision": "TEST",
        "claim_created_at": "2026-08-29T00:00:00Z",
        "claim_expires_when": "after merge",
        "expected_evidence": ["PASS"],
        "collision_boundaries": ["no overlap"],
        "next_task_after_release": "none",
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_runtime_authority": "NONE",
        "non_tv_tvc_secret_or_token_used": False,
        "authority_effect": False,
        "activation_effect": False,
    }


def released_claim() -> dict:
    value = base_claim()
    value.update(
        {
            "role": "RELEASED_INTEGRATION",
            "state": "RELEASED",
            "pull_request": 999,
            "release_commit": "a" * 40,
            "claim_released_at": "2026-08-29T01:00:00Z",
            "archive_eligible": True,
        }
    )
    return value


class TerminalClaimMaintenanceTests(unittest.TestCase):
    def test_accepts_only_release_metadata_changes(self) -> None:
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), released_claim())
        self.assertTrue(valid)
        self.assertEqual(reason, "PASS")

    def test_rejects_nonterminal_target(self) -> None:
        current = released_claim()
        current["state"] = "CLAIMED_FOR_VALIDATION"
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid)
        self.assertIn("not terminal", reason)

    def test_rejects_protected_ownership_change(self) -> None:
        current = released_claim()
        current["dependency_surface_keys"] = ["site:other-surface"]
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid)
        self.assertIn("protected", reason)

    def test_rejects_missing_release_evidence(self) -> None:
        current = released_claim()
        current.pop("release_commit")
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid)
        self.assertIn("release_commit", reason)

    def test_rejects_authority_or_activation(self) -> None:
        current = released_claim()
        current["authority_effect"] = True
        valid, _ = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid)

        current = released_claim()
        current["activation_effect"] = True
        valid, _ = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid)

    def test_claim_registry_only_paths_is_fail_closed(self) -> None:
        self.assertTrue(
            mod.claim_registry_only_paths(
                ["data/session-work-claims.d/example.json"]
            )
        )
        self.assertTrue(
            mod.claim_registry_only_paths(
                [
                    "data/session-work-claims.d/one.json",
                    "data/session-work-claims.d/two.json",
                ]
            )
        )
        self.assertFalse(mod.claim_registry_only_paths([]))
        self.assertFalse(
            mod.claim_registry_only_paths(
                [
                    "data/session-work-claims.d/example.json",
                    "scripts/site_handoff_orchestrator.py",
                ]
            )
        )
        self.assertFalse(
            mod.claim_registry_only_paths(
                ["data/session-work-claims.json"]
            )
        )


if __name__ == "__main__":
    unittest.main()
