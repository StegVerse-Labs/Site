from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_site_task_diagnostic_contract.py"

spec = importlib.util.spec_from_file_location("site_task_diagnostic_contract", CHECKER_PATH)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


class SiteTaskDiagnosticContractTests(unittest.TestCase):
    def test_live_contract_passes(self):
        self.assertEqual(checker.main(), 0)

    def test_retired_github_secret_markers_are_forbidden_not_required(self):
        self.assertNotIn("STEGVERSE_REPO_SYNC_TOKEN", checker.RETENTION_REQUIRED)
        self.assertIn("STEGVERSE_REPO_SYNC_TOKEN", checker.RETENTION_FORBIDDEN)
        self.assertIn("secrets.", checker.RETENTION_FORBIDDEN)

    def test_current_validation_only_retention_markers_are_required(self):
        for marker in (
            "permissions:\n  contents: read",
            "persist-credentials: false",
            "Validate activation-retention credential boundary",
            "Validate checked-in activation-state consistency without mutation",
        ):
            self.assertIn(marker, checker.RETENTION_REQUIRED)

    def test_current_root_handoff_wording_is_required(self):
        expected = "This file is the current handoff and task source of truth for " + chr(96) + "StegVerse-Labs/Site" + chr(96) + "."
        self.assertIn(expected, checker.HANDOFF_REQUIRED)
        self.assertTrue(str(checker.HANDOFF).endswith("docs/SITE_MIRROR_HANDOFF.md"))

    def test_live_retention_workflow_contains_no_retired_authority_markers(self):
        body = checker.RETENTION_WORKFLOW.read_text(encoding="utf-8")
        for marker in checker.RETENTION_FORBIDDEN:
            self.assertNotIn(marker, body)


if __name__ == "__main__":
    unittest.main()
