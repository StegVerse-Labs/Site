from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_mykv_manifest_is_installable_and_same_origin():
    manifest = json.loads((ROOT / "my-kv.webmanifest").read_text())
    assert manifest["name"] == "StegVerse MyKV"
    assert manifest["short_name"] == "MyKV"
    assert manifest["id"] == "/my-kv-install.html"
    assert manifest["start_url"].startswith("/my-kv-install.html")
    assert manifest["scope"] == "/"
    assert manifest["display"] == "standalone"
    assert any(i["sizes"] == "192x192" and i["type"] == "image/png" for i in manifest["icons"])
    assert any(i["sizes"] == "512x512" and i["type"] == "image/png" for i in manifest["icons"])


def test_install_shell_has_ios_metadata_and_redirects_only_in_standalone_mode():
    html = (ROOT / "my-kv-install.html").read_text()
    assert '<link rel="manifest" href="my-kv.webmanifest">' in html
    assert '<meta name="apple-mobile-web-app-capable" content="yes">' in html
    assert '<meta name="apple-mobile-web-app-title" content="MyKV">' in html
    assert '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">' in html
    assert '<link rel="apple-touch-icon" href="assets/icons/mykv-icon-192.png">' in html
    assert "display-mode: standalone" in html
    assert "navigator.standalone" in html
    assert "window.location.replace('/my-kv.html?source=installed')" in html
    assert "does not create, reinstall, replace, renumber, or migrate" in html


def test_existing_mykv_device_kv_path_is_preserved():
    html = (ROOT / "my-kv.html").read_text()
    assert "resident KnowledgeVault through DEVICE_KV" in html
    assert "Connect / verify KV" in html
    assert "Install your KnowledgeVault" in html


def test_install_shell_is_non_authorizing():
    html = (ROOT / "my-kv-install.html").read_text()
    assert "registerDevice" not in html
    assert "indexedDB" not in html
    assert "fetch(" not in html
    assert "localStorage" not in html


def test_mykv_png_icons_exist():
    for size in (192, 512):
        icon = ROOT / "assets" / "icons" / f"mykv-icon-{size}.png"
        assert icon.exists()
        assert icon.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
