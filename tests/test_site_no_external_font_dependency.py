"""D-P6: Site pages carry no hosted web-font dependency.

Every page renders with local or system font stacks; a fonts.googleapis.com / fonts.gstatic.com
reference would make page rendering depend on an external host, which the owner directive forbids.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")
SKIP = {".git", "node_modules"}


class NoExternalFontDependencyTests(unittest.TestCase):
    def test_no_hosted_font_references(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if path.suffix not in {".html", ".css", ".js"} or SKIP & set(path.parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            offenders += [f"{path.relative_to(ROOT)}: {h}" for h in HOSTS if h in text]
        self.assertEqual(offenders, [])

    def test_transition_table_keeps_system_font_fallbacks(self):
        page = (ROOT / "transition-table-visual.html").read_text(encoding="utf-8")
        self.assertIn("--mono:  'Space Mono', monospace;", page)
        self.assertIn("--sans:  'Syne', sans-serif;", page)


if __name__ == "__main__":
    unittest.main()
