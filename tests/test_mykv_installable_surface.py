from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PENDING_GOOGLE_DRIVE_REQUEST = "SITE-CLOUD-KV-4347408852127319cbda574f02e03edb"


class MyKVInstallableSurfaceTests(unittest.TestCase):
    def test_mykv_manifest_is_installable_and_same_origin(self):
        manifest = json.loads((ROOT / "my-kv.webmanifest").read_text())
        self.assertEqual(manifest["name"], "StegVerse MyKV")
        self.assertEqual(manifest["short_name"], "MyKV")
        self.assertEqual(manifest["id"], "/my-kv-install.html")
        self.assertTrue(manifest["start_url"].startswith("/my-kv-install.html"))
        self.assertEqual(manifest["scope"], "/")
        self.assertEqual(manifest["display"], "standalone")

    def test_install_shell_is_single_owner_facing_surface_and_bootstraps_substrate(self):
        html = (ROOT / "my-kv-install.html").read_text()
        self.assertIn('<link rel="manifest" href="my-kv.webmanifest">', html)
        self.assertIn('apple-mobile-web-app-capable', html)
        self.assertIn('/assets/stegverse-node-continuity.js?v=20260915-unified-mykv-v1', html)
        self.assertIn("StegOSResidentHealth", html)
        self.assertIn("health.repair()", html)
        self.assertIn("resident_install_health!=='HEALTHY'", html)
        self.assertIn("window.location.replace('/my-kv.html?source=installed&resident=healthy')", html)
        self.assertIn("single owner-facing installation surface", html)
        self.assertIn("There is no separate StegOS website or second owner installation step", html)
        self.assertIn("does <strong>not</strong>", html)
        self.assertNotIn("/stegos-bootstrap/index.html", html)

    def test_node_continuity_loader_carries_existing_stegos_substrate_into_mykv(self):
        loader = (ROOT / "assets" / "stegverse-node-continuity.js").read_text()
        self.assertIn("/stegos-bootstrap/stegos-bootstrap-impl.js", loader)
        self.assertIn("/stegos-bootstrap/device-local-autostart.js", loader)
        self.assertIn("/assets/stegverse-node-continuity-impl.js", loader)
        self.assertIn("/assets/stegos-resident-health.js", loader)

    def test_host_choices_are_hidden_until_resident_substrate_is_healthy(self):
        page = (ROOT / "cloud-kv-peers.html").read_text()
        self.assertGreaterEqual(page.count("data-kv-host-options hidden"), 3)
        self.assertIn("resident_install_health==='HEALTHY'", page)
        self.assertIn("revealHosts()", page)
        self.assertIn("if(!substrateReady)", page)
        self.assertIn(PENDING_GOOGLE_DRIVE_REQUEST, page)
        self.assertEqual(page.count(PENDING_GOOGLE_DRIVE_REQUEST), 1)

    def test_existing_mykv_device_kv_path_is_preserved(self):
        html = (ROOT / "my-kv.html").read_text()
        self.assertIn("resident KnowledgeVault through DEVICE_KV", html)
        self.assertIn("Connect / verify KV", html)
        self.assertIn("Install your KnowledgeVault", html)

    def test_install_shell_does_not_contain_kv_or_provider_mutation_implementation(self):
        html = (ROOT / "my-kv-install.html").read_text()
        forbidden = ["createRequest(", "adoptRequest(", "provider_operation_authorized=true", "kv_migrate", "kv_rehost"]
        for marker in forbidden:
            self.assertNotIn(marker, html)

    def test_mykv_png_icons_exist(self):
        for size in (192, 512):
            icon = ROOT / "assets" / "icons" / f"mykv-icon-{size}.png"
            self.assertTrue(icon.exists())
            self.assertTrue(icon.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
