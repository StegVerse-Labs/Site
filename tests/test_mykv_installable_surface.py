from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_mykv_manifest_is_installable_and_bound_to_existing_surface():
    manifest = json.loads((ROOT / "my-kv.webmanifest").read_text())
    assert manifest["name"] == "StegVerse MyKV"
    assert manifest["short_name"] == "MyKV"
    assert manifest["id"] == "/my-kv.html"
    assert manifest["start_url"].startswith("/my-kv.html")
    assert manifest["scope"] == "/"
    assert manifest["display"] == "standalone"
    assert any(i["sizes"] == "192x192" for i in manifest["icons"])
    assert any(i["sizes"] == "512x512" for i in manifest["icons"])


def test_mykv_html_declares_ios_install_surface_without_replacing_device_kv():
    html = (ROOT / "my-kv.html").read_text()
    assert '<link rel="manifest" href="my-kv.webmanifest">' in html
    assert '<meta name="apple-mobile-web-app-capable" content="yes">' in html
    assert '<meta name="apple-mobile-web-app-title" content="MyKV">' in html
    assert '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">' in html
    assert '<link rel="apple-touch-icon" href="assets/icons/mykv-icon-192.svg">' in html
    assert '<script src="assets/my-kv-install.js" defer></script>' in html
    assert "resident KnowledgeVault through DEVICE_KV" in html
    assert "Connect / verify KV" in html
    assert "Install your KnowledgeVault" in html


def test_install_detector_is_non_authorizing():
    script = (ROOT / "assets/my-kv-install.js").read_text()
    assert "display-mode: standalone" in script
    assert "navigator.standalone" in script
    assert "registerDevice" not in script
    assert "indexedDB" not in script
    assert "fetch(" not in script
    assert "localStorage" not in script
