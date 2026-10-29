"""Regression test: scripts/mirror_papers.py must never delete native Site papers
or overwrite a hand-maintained Papers.html (StegVerse-Labs/Site#1633 lane 3).

Standard library only; run with: python3 -m unittest tests/test_mirror_papers_native_preservation.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mirror_papers.py"
NATIVE_PAGE = "<!doctype html><html><body><h1>Featured publications</h1>When AI Services Fail</body></html>\n"


class MirrorPapersNativePreservation(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.tmp / "scripts" / "mirror_papers.py")
        papers = self.tmp / "papers"
        (papers / "when-ai-services-fail").mkdir(parents=True)
        (papers / "when-ai-services-fail" / "index.html").write_text("native", encoding="utf-8")
        (papers / "when-ai-services-fail" / "paper.pdf").write_bytes(b"%PDF-native")
        (papers / "GCAT").mkdir()
        (papers / "GCAT" / "old.tex").write_text("old mirrored", encoding="utf-8")
        (papers / "papers_manifest.json").write_text(json.dumps(
            {"entries": [{"path": "GCAT/old.tex"}, {"path": "../escape.txt"}]}), encoding="utf-8")
        (self.tmp / "escape.txt").write_text("outside papers/", encoding="utf-8")
        source = self.tmp / "_source" / "papers" / "GCAT"
        source.mkdir(parents=True)
        (source / "new.tex").write_text("new mirrored", encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_mirror(self) -> dict:
        done = subprocess.run([sys.executable, str(self.tmp / "scripts" / "mirror_papers.py")],
                              cwd=self.tmp, capture_output=True, text=True, check=True)
        return json.loads(done.stdout)

    def test_native_papers_and_hand_maintained_index_survive(self) -> None:
        (self.tmp / "Papers.html").write_text(NATIVE_PAGE, encoding="utf-8")
        result = self.run_mirror()
        papers = self.tmp / "papers"
        self.assertEqual((papers / "when-ai-services-fail" / "index.html").read_text(encoding="utf-8"), "native")
        self.assertEqual((papers / "when-ai-services-fail" / "paper.pdf").read_bytes(), b"%PDF-native")
        self.assertFalse((papers / "GCAT" / "old.tex").exists(), "previously mirrored file is replaced")
        self.assertEqual((papers / "GCAT" / "new.tex").read_text(encoding="utf-8"), "new mirrored")
        self.assertTrue((self.tmp / "escape.txt").exists(), "manifest paths outside papers/ are never deleted")
        self.assertEqual((self.tmp / "Papers.html").read_text(encoding="utf-8"), NATIVE_PAGE)
        self.assertFalse(result["papers_html_written"])
        self.assertIn('name="stegverse-generator"', (papers / "index.html").read_text(encoding="utf-8"))
        manifest = json.loads((papers / "papers_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual([e["path"] for e in manifest["entries"]], ["GCAT/new.tex"])

    def test_generated_index_is_still_regenerated(self) -> None:
        self.run_mirror()  # no Papers.html yet: written with the generator marker
        first = (self.tmp / "Papers.html").read_text(encoding="utf-8")
        self.assertIn('name="stegverse-generator"', first)
        result = self.run_mirror()
        self.assertTrue(result["papers_html_written"])
        self.assertTrue((self.tmp / "papers" / "when-ai-services-fail" / "paper.pdf").exists())


if __name__ == "__main__":
    unittest.main()
