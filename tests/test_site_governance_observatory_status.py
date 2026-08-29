from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_site_governance_observatory_status.py"
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
OBS = (ROOT / "governance-observatory.html").read_text(encoding="utf-8")
STATUS_JSON = (ROOT / "docs" / "SITE_GOVERNANCE_OBSERVATORY_STATUS.json").read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("govobs_status", CHECKER)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


class GovernanceObservatoryHomepageValidatorTests(unittest.TestCase):
    def test_live_contract_passes(self):
        checker.main()

    def test_homepage_remains_simplified(self):
        self.assertIn("How can I help?", INDEX)
        self.assertIn('href="my-kv.html"', INDEX)
        self.assertIn('href="organizational-kv.html"', INDEX)
        self.assertNotIn('href="governance-observatory.html"', INDEX)
        self.assertEqual(INDEX.count("data-chat-prompt="), 3)

    def test_dedicated_observatory_surface_is_preserved(self):
        self.assertIn("Governance Observatory", OBS)
        self.assertIn("Site is not the source of truth", OBS)

    def test_release_awareness_evidence_is_preserved(self):
        self.assertIn('"version": "0.1.0"', STATUS_JSON)
        self.assertIn('"release_id": 377486341', STATUS_JSON)

    def test_checker_preserves_authority_none(self):
        text = CHECKER.read_text(encoding="utf-8")
        self.assertIn('print("authority_effect=NONE")', text)


if __name__ == "__main__":
    unittest.main()
