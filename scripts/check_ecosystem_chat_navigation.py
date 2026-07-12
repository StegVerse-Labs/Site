#!/usr/bin/env python3
"""Verify Ecosystem Chat exposes the installed usage and route-comparison surfaces."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-chat.html"
BOOTSTRAP = ROOT / "assets" / "ecosystem-chat-hps.js"
TARGETS = {
    "ecosystem-usage.html": "Usage Ledger",
    "ecosystem-comparison.html": "Route Comparison",
}


def main() -> int:
    if not PAGE.exists() or not BOOTSTRAP.exists():
        raise SystemExit("ECOSYSTEM_CHAT_NAVIGATION_FAIL: required surface missing")

    page = PAGE.read_text(encoding="utf-8")
    script = BOOTSTRAP.read_text(encoding="utf-8")

    if 'nav class="sv-nav"' not in page:
        raise SystemExit("ECOSYSTEM_CHAT_NAVIGATION_FAIL: primary navigation missing")
    if "ensurePrimaryNavigation" not in script:
        raise SystemExit("ECOSYSTEM_CHAT_NAVIGATION_FAIL: navigation installer missing")

    for href, label in TARGETS.items():
        if href not in script or label not in script:
            raise SystemExit(f"ECOSYSTEM_CHAT_NAVIGATION_FAIL: missing {label} target")
        target = ROOT / href
        if not target.exists():
            raise SystemExit(f"ECOSYSTEM_CHAT_NAVIGATION_FAIL: target does not exist: {href}")

    for forbidden in ("authority_granted = true", "execution_enabled = true", "receipt_issued_by_site = true"):
        if forbidden in script:
            raise SystemExit(f"ECOSYSTEM_CHAT_NAVIGATION_FAIL: forbidden authority marker: {forbidden}")

    print("ECOSYSTEM_CHAT_NAVIGATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
