"""Offline snapshot custody, outage and interrupted-capture regressions."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/capture_8374_discovery_mirrors.py"
spec = importlib.util.spec_from_file_location("discovery_mirrors", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def fetch(self, url):
        data = {"/offer": {"document": "OFFER__MACHINE__READABLE__01", "version": "fixture"},
                "/openapi.json": {"openapi": "3.1.0", "paths": {}},
                "/.well-known/x402": {"version": 1, "resources": [m.ORIGIN + "/crossing"]}}
        return json.dumps(data[url.removeprefix(m.ORIGIN)]).encode(), "application/json", url

    def seed(self):
        return m.capture(self.root, self.fetch)

    def pointer(self):
        return self.root / m.MIRROR / "current.json"

    def rewrite_pointer(self, value):
        self.pointer().write_text(json.dumps(value))

    def test_offline_outage_still_reads_all_three_copies(self):
        original = self.seed()
        with mock.patch.object(m.urllib.request, "urlopen", side_effect=OSError("origin offline")):
            actual = m.validate(self.root)
        self.assertEqual(actual, original)
        self.assertIs(actual["live_payment_authorization"], False)
        for row in actual["documents"]:
            self.assertTrue((self.root / m.MIRROR / row["mirror_path"]).is_file())

    def test_body_tamper_rejected(self):
        row = self.seed()["documents"][0]
        (self.root / m.MIRROR / row["mirror_path"]).write_bytes(b"{}")
        with self.assertRaisesRegex(ValueError, "size/hash mismatch"):
            m.validate(self.root)

    def test_missing_document_rejected(self):
        row = self.seed()["documents"][1]
        (self.root / m.MIRROR / row["mirror_path"]).unlink()
        with self.assertRaises(OSError):
            m.validate(self.root)

    def test_path_escape_rejected_before_read(self):
        value = self.seed()
        value["documents"][0]["mirror_path"] = "../../outside.json"
        self.rewrite_pointer(value)
        with self.assertRaisesRegex(ValueError, "path mismatch"):
            m.validate(self.root)

    def test_live_authorization_flag_cannot_be_promoted(self):
        value = self.seed()
        value["live_payment_authorization"] = True
        self.rewrite_pointer(value)
        with self.assertRaisesRegex(ValueError, "non-authorizing"):
            m.validate(self.root)

    def test_partial_network_failure_preserves_entire_old_generation(self):
        self.seed()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        calls = []
        def broken(url):
            calls.append(url)
            if len(calls) == 2:
                raise OSError("capture interrupted")
            return self.fetch(url)
        with self.assertRaises(OSError):
            m.capture(self.root, broken)
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        m.validate(self.root)

    def test_html_and_wrong_json_shapes_do_not_publish(self):
        for body, media in [(b"<html>gateway</html>", "text/html"), (b"[]", "application/json"), (b"{}", "application/json")]:
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    m.capture(self.root, lambda url: (body, media, url))
                self.assertFalse(self.pointer().exists())

    def test_identical_recapture_preserves_content_address_and_raw_bytes(self):
        first = self.seed()
        second = self.seed()
        self.assertEqual(first["generation"], second["generation"])
        for row in second["documents"]:
            self.assertEqual((self.root / m.MIRROR / row["mirror_path"]).read_bytes(), self.fetch(row["source_url"])[0])


if __name__ == "__main__":
    unittest.main()
