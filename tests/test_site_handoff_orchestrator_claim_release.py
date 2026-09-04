from __future__ import annotations

import importlib.util
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest import mock

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

CLAIM_SPEC = importlib.util.spec_from_file_location(
    "check_session_work_claims_under_test",
    ROOT / "scripts/check_session_work_claims.py",
)
assert CLAIM_SPEC and CLAIM_SPEC.loader
claim_mod = importlib.util.module_from_spec(CLAIM_SPEC)
CLAIM_SPEC.loader.exec_module(claim_mod)


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
        "claimed_paths": ["scripts/example.py", "data/session-work-claims.d/test.json"],
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
    value.update({
        "role": "RELEASED_INTEGRATION",
        "state": "RELEASED",
        "pull_request": 999,
        "release_commit": "a" * 40,
        "claim_released_at": "2026-08-29T01:00:00Z",
        "archive_eligible": True,
    })
    return value


def tombstone() -> dict:
    return {
        "claim_id": "SITE-TEST-CLAIM-001",
        "terminalization_override_of": "canonical_registry",
        "state": "RELEASED",
        "pull_request": 999,
        "release_commit": "a" * 40,
        "claim_released_at": "2026-08-29T01:00:00Z",
        "archive_eligible": True,
    }


class TerminalClaimMaintenanceTests(unittest.TestCase):
    def test_accepts_only_release_metadata_changes(self) -> None:
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), released_claim())
        self.assertTrue(valid)
        self.assertEqual(reason, "PASS")

    def test_rejects_nonterminal_target(self) -> None:
        current = released_claim(); current["state"] = "CLAIMED_FOR_VALIDATION"
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid); self.assertIn("not terminal", reason)

    def test_rejects_protected_ownership_change(self) -> None:
        current = released_claim(); current["dependency_surface_keys"] = ["site:other-surface"]
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid); self.assertIn("protected", reason)

    def test_rejects_missing_release_evidence(self) -> None:
        current = released_claim(); current.pop("release_commit")
        valid, reason = mod.validate_terminal_claim_delta(base_claim(), current)
        self.assertFalse(valid); self.assertIn("release_commit", reason)

    def test_accepts_legacy_claim_with_authority_and_activation_fields_omitted(self) -> None:
        base = base_claim(); current = released_claim()
        base.pop("authority_effect"); base.pop("activation_effect")
        current.pop("authority_effect"); current.pop("activation_effect")
        valid, reason = mod.validate_terminal_claim_delta(base, current)
        self.assertTrue(valid); self.assertEqual(reason, "PASS")

    def test_rejects_introduction_of_zero_effect_fields_during_legacy_release(self) -> None:
        base = base_claim(); base.pop("authority_effect"); base.pop("activation_effect")
        current = released_claim()
        valid, reason = mod.validate_terminal_claim_delta(base, current)
        self.assertFalse(valid); self.assertIn("protected", reason)

    def test_rejects_authority_or_activation(self) -> None:
        current = released_claim(); current["authority_effect"] = True
        self.assertFalse(mod.validate_terminal_claim_delta(base_claim(), current)[0])
        current = released_claim(); current["activation_effect"] = True
        self.assertFalse(mod.validate_terminal_claim_delta(base_claim(), current)[0])

    def test_git_changed_files_falls_back_to_pr_api_when_parent_unavailable(self) -> None:
        failed = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "shallow"})()
        with mock.patch.object(mod.subprocess, "run", return_value=failed), mock.patch.object(
            mod, "_api_pr_changed_files", return_value=["data/session-work-claims.d/example.json"]
        ) as fallback:
            self.assertEqual(mod._git_changed_files(), ["data/session-work-claims.d/example.json"])
            fallback.assert_called_once_with()

    def test_git_show_json_falls_back_to_pr_base_api(self) -> None:
        failed = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "shallow"})()
        expected = {"claims": [base_claim()]}
        with mock.patch.object(mod.subprocess, "run", return_value=failed), mock.patch.object(
            mod, "_api_base_json", return_value=expected
        ) as fallback:
            self.assertEqual(mod._git_show_json("HEAD^1", "data/session-work-claims.d/example.json"), expected)
            fallback.assert_called_once_with("data/session-work-claims.d/example.json")

    def test_claim_registry_only_paths_is_fail_closed(self) -> None:
        self.assertTrue(mod.claim_registry_only_paths(["data/session-work-claims.d/example.json"]))
        self.assertTrue(mod.claim_registry_only_paths([
            "data/session-work-claims.d/one.json", "data/session-work-claims.d/two.json"
        ]))
        self.assertFalse(mod.claim_registry_only_paths([]))
        self.assertFalse(mod.claim_registry_only_paths([
            "data/session-work-claims.d/example.json", "scripts/site_handoff_orchestrator.py"
        ]))
        self.assertFalse(mod.claim_registry_only_paths(["data/session-work-claims.json"]))


class LegacyAggregateTombstoneTests(unittest.TestCase):
    def test_tombstone_preserves_protected_fields(self) -> None:
        base = base_claim()
        result = claim_mod.apply_terminalization_tombstone([base], tombstone(), set())
        self.assertEqual(result["state"], "RELEASED")
        for field in (
            "task_id", "branch", "role", "dependency_surface_keys", "claimed_paths", "handoff",
            "credential_authority", "github_token_runtime_authority", "authority_effect", "activation_effect",
        ):
            self.assertEqual(result[field], base[field], field)

    def test_tombstone_rejects_unknown_target(self) -> None:
        value = tombstone(); value["claim_id"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "exactly one canonical claim"):
            claim_mod.apply_terminalization_tombstone([base_claim()], value, set())

    def test_tombstone_rejects_active_to_active(self) -> None:
        value = tombstone(); value["state"] = "CLAIMED_FOR_VALIDATION"
        with self.assertRaisesRegex(ValueError, "not terminal"):
            claim_mod.apply_terminalization_tombstone([base_claim()], value, set())

    def test_tombstone_rejects_protected_field_injection(self) -> None:
        value = tombstone(); value["authority_effect"] = True
        with self.assertRaisesRegex(ValueError, "protected-field injection"):
            claim_mod.apply_terminalization_tombstone([base_claim()], value, set())

    def test_tombstone_rejects_missing_release_evidence(self) -> None:
        value = tombstone(); value.pop("release_commit")
        with self.assertRaisesRegex(ValueError, "missing fields"):
            claim_mod.apply_terminalization_tombstone([base_claim()], value, set())

    def test_tombstone_rejects_duplicate_target(self) -> None:
        seen = {"SITE-TEST-CLAIM-001"}
        with self.assertRaisesRegex(ValueError, "duplicate terminalization"):
            claim_mod.apply_terminalization_tombstone([base_claim()], tombstone(), seen)

    def test_tombstone_rejects_non_boolean_archive(self) -> None:
        value = tombstone(); value["archive_eligible"] = "true"
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            claim_mod.apply_terminalization_tombstone([base_claim()], value, set())

    def test_tombstone_rejects_already_terminal_target(self) -> None:
        base = deepcopy(base_claim()); base["state"] = "RELEASED"
        with self.assertRaisesRegex(ValueError, "not active"):
            claim_mod.apply_terminalization_tombstone([base], tombstone(), set())


if __name__ == "__main__":
    unittest.main()
