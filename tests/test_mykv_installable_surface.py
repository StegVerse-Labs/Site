from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MyKVInstallableSurfaceTests(unittest.TestCase):
    def test_mykv_manifest_is_installable_and_same_origin(self):
        manifest = json.loads((ROOT / "my-kv.webmanifest").read_text())
        self.assertEqual(manifest["name"], "StegVerse MyKV")
        self.assertEqual(manifest["short_name"], "MyKV")
        self.assertEqual(manifest["id"], "/my-kv-install.html")
        self.assertTrue(manifest["start_url"].startswith("/my-kv-install.html"))
        self.assertEqual(manifest["scope"], "/")
        self.assertEqual(manifest["display"], "standalone")
        self.assertTrue(any(i["sizes"] == "192x192" and i["type"] == "image/png" for i in manifest["icons"]))
        self.assertTrue(any(i["sizes"] == "512x512" and i["type"] == "image/png" for i in manifest["icons"]))

    def test_install_shell_has_ios_metadata_and_redirects_only_in_standalone_mode(self):
        html = (ROOT / "my-kv-install.html").read_text()
        self.assertIn('<link rel="manifest" href="my-kv.webmanifest">', html)
        self.assertIn('<meta name="apple-mobile-web-app-capable" content="yes">', html)
        self.assertIn('<meta name="apple-mobile-web-app-title" content="MyKV">', html)
        self.assertIn('<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">', html)
        self.assertIn('<link rel="apple-touch-icon" href="assets/icons/mykv-icon-192.png">', html)
        self.assertIn("display-mode: standalone", html)
        self.assertIn("navigator.standalone", html)
        self.assertIn("window.location.replace('/my-kv.html?source=installed')", html)
        self.assertIn("does not create, reinstall, replace, renumber, or migrate", html)

    def test_existing_mykv_device_kv_path_is_preserved(self):
        html = (ROOT / "my-kv.html").read_text()
        self.assertIn("resident KnowledgeVault through DEVICE_KV", html)
        self.assertIn("Connect / verify KV", html)
        self.assertIn("Install your KnowledgeVault", html)

    def test_install_shell_is_non_authorizing(self):
        html = (ROOT / "my-kv-install.html").read_text()
        self.assertNotIn("registerDevice", html)
        self.assertNotIn("indexedDB", html)
        self.assertNotIn("fetch(", html)
        self.assertNotIn("localStorage", html)

    def test_mykv_png_icons_exist(self):
        for size in (192, 512):
            icon = ROOT / "assets" / "icons" / f"mykv-icon-{size}.png"
            self.assertTrue(icon.exists())
            self.assertTrue(icon.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
