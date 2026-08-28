from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
CHECKER = (ROOT / "scripts/check_site_unified_governed_experience.py").read_text(encoding="utf-8")
STATUS = (ROOT / "docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md").read_text(encoding="utf-8")


class UnifiedHomepageContractTests(unittest.TestCase):
    def test_homepage_is_conversational_shell(self):
        self.assertIn("How can I help?", INDEX)
        self.assertIn('id="chatForm"', INDEX)
        self.assertIn('id="chatLog"', INDEX)
        self.assertEqual(INDEX.count("data-chat-prompt="), 3)

    def test_only_primary_kv_navigation_is_required(self):
        self.assertEqual(INDEX.count('href="my-kv.html"'), 1)
        self.assertEqual(INDEX.count('href="organizational-kv.html"'), 1)

    def test_retired_transition_directory_is_forbidden(self):
        for marker in (
            'id="transition-menu"',
            'href="#transition-menu"',
            "Continue to a governed transition",
            "Current proof status",
            "transition-grid",
        ):
            self.assertNotIn(marker, INDEX)
            self.assertIn(marker, CHECKER)

    def test_status_names_index_as_primary_public_surface(self):
        self.assertIn("Primary public operating surface: index.html conversational shell", STATUS)
        self.assertIn(
            "Homepage posture: conversation first; My KV and Organizational KV are the only primary navigation destinations",
            STATUS,
        )

    def test_site_authority_remains_none(self):
        self.assertIn("Execution authority from Site: none", STATUS)
        self.assertIn("Receipt authority from Site: none", STATUS)


if __name__ == "__main__":
    unittest.main()
