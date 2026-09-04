#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "social-presence.json"
REQUIRED_NETWORKS = {"linkedin", "facebook"}
REQUIRED_PAGES = {
    ROOT / "social.html",
    ROOT / "social" / "linkedin.html",
    ROOT / "social" / "facebook.html",
    ROOT / "assets" / "social-presence.js",
    ROOT / "docs" / "SOCIAL_PRESENCE_MIRROR_HANDOFF.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"SOCIAL_PRESENCE_FAIL: {message}")


def main() -> int:
    if not MANIFEST.is_file():
        fail("manifest missing")
    for path in REQUIRED_PAGES:
        if not path.is_file():
            fail(f"required file missing: {path.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema") != "stegverse.site.social-presence/v1":
        fail("unexpected manifest schema")
    if manifest.get("authority_effect") is not False:
        fail("authority effect must remain false")

    rows = manifest.get("networks")
    if not isinstance(rows, list):
        fail("networks must be a list")
    by_network = {row.get("network"): row for row in rows if isinstance(row, dict)}
    if not REQUIRED_NETWORKS.issubset(by_network):
        fail("LinkedIn and Facebook records are required")

    for name in REQUIRED_NETWORKS:
        row = by_network[name]
        state = row.get("state")
        url = row.get("canonical_url")
        if state == "VERIFIED":
            if not isinstance(url, str) or not url:
                fail(f"{name}: VERIFIED requires canonical_url")
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.hostname:
                fail(f"{name}: canonical_url must be public HTTPS")
        else:
            if url is not None:
                fail(f"{name}: unverified destination must fail closed with canonical_url null")

    print("SOCIAL_PRESENCE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
