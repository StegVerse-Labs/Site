from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_site_homepage_governed_ecosystem.py"
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
GOVERNED = (ROOT / "governed-ecosystem.html").read_text(encoding="utf-8")
ADMISSIBILITY = (ROOT / "admissibility-wiki.html").read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("homepage_governed_ecosystem", CHECKER)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


class HomepageGovernedEcosystemTests(unittest.TestCase):
    def test_live_contract_passes(self):
        self.assertEqual(checker.main(), 0)

    def test_specialty_destinations_are_not_primary_homepage_navigation(self):
        self.assertNotIn('href="governed-ecosystem.html"', INDEX)
        self.assertNotIn('href="admissibility-wiki.html"', INDEX)
        self.assertIn('href="my-kv.html"', INDEX)
        self.assertIn('href="organizational-kv.html"', INDEX)

    def test_governed_ecosystem_destination_remains_present(self):
        self.assertIn("StegVerse Governed Ecosystem Mirror", GOVERNED)
        self.assertIn("Site is display-only", GOVERNED)

    def test_admissibility_destination_remains_present(self):
        self.assertIn("Admissibility Wiki", ADMISSIBILITY)
        self.assertIn("Site is a public bridge and display surface.", ADMISSIBILITY)

    def test_authority_effect_remains_none(self):
        self.assertIn('print("authority_effect=NONE")', CHECKER.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
