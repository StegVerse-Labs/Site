#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "social-presence.json"
REQUIRED_NETWORKS = {"linkedin", "facebook"}
EXPECTED_HOST_SUFFIX = {
    "linkedin": "linkedin.com",
    "facebook": "facebook.com",
}
REQUIRED_PAGES = {
    ROOT / "social.html",
    ROOT / "social" / "linkedin.html",
    ROOT / "social" / "facebook.html",
    ROOT / "assets" / "social-presence.js",
    ROOT / "docs" / "SOCIAL_PRESENCE_MIRROR_HANDOFF.md",
}
NAVIGATION_PAGES = {
    ROOT / "index.html": 'href="social.html"',
    ROOT / "Papers.html": 'href="social.html"',
    ROOT / "news-releases.html": 'href="social.html"',
}


def fail(message: str) -> None:
    raise SystemExit(f"SOCIAL_PRESENCE_FAIL: {message}")


def host_matches(hostname: str, suffix: str) -> bool:
    host = hostname.lower().rstrip(".")
    return host == suffix or host.endswith("." + suffix)


def main() -> int:
    if not MANIFEST.is_file():
        fail("manifest missing")
    for path in REQUIRED_PAGES:
        if not path.is_file():
            fail(f"required file missing: {path.relative_to(ROOT)}")
    for path, marker in NAVIGATION_PAGES.items():
        if not path.is_file():
            fail(f"navigation page missing: {path.relative_to(ROOT)}")
        if marker not in path.read_text(encoding="utf-8"):
            fail(f"social navigation missing: {path.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema") != "stegverse.site.social-presence/v1":
        fail("unexpected manifest schema")
    if manifest.get("organization") != "StegVerse LLC":
        fail("unexpected organization identity")
    if manifest.get("site") != "https://stegverse.org/":
        fail("unexpected canonical Site URL")
    for field in ("authority_effect", "publication_authority", "identity_authority"):
        if manifest.get(field) is not False:
            fail(f"{field} must remain false")

    rows = manifest.get("networks")
    if not isinstance(rows, list):
        fail("networks must be a list")
    by_network = {row.get("network"): row for row in rows if isinstance(row, dict)}
    if set(by_network) != REQUIRED_NETWORKS:
        fail("manifest must contain exactly LinkedIn and Facebook in this bounded slice")

    for name in REQUIRED_NETWORKS:
        row = by_network[name]
        state = row.get("state")
        url = row.get("canonical_url")
        if state == "VERIFIED":
            if row.get("verification") != "VERIFIED":
                fail(f"{name}: VERIFIED state requires VERIFIED verification")
            if not isinstance(url, str) or not url:
                fail(f"{name}: VERIFIED requires canonical_url")
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.hostname:
                fail(f"{name}: canonical_url must be public HTTPS")
            if not host_matches(parsed.hostname, EXPECTED_HOST_SUFFIX[name]):
                fail(f"{name}: canonical_url hostname does not match network")
            if not row.get("platform_id"):
                fail(f"{name}: VERIFIED requires platform_id")
        else:
            if state != "PENDING_EXTERNAL_PAGE_CREATION":
                fail(f"{name}: unsupported unverified state")
            if url is not None or row.get("platform_id") is not None:
                fail(f"{name}: unverified destination must fail closed with null URL and platform_id")
            if row.get("verification") != "NOT_OBSERVED":
                fail(f"{name}: pending destination verification must remain NOT_OBSERVED")

    print("SOCIAL_PRESENCE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
