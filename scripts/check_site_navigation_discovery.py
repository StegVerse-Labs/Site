#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "site-navigation-discovery.md"


def main() -> int:
    if not PAGE.exists():
        raise SystemExit("SITE NAVIGATION DISCOVERY: FAIL - page missing")
    text = PAGE.read_text(encoding="utf-8")
    required = [
        "NAVIGATION_STRUCTURE_PENDING",
        "docs/governance/repo-standards-site-mirror-plan.md",
        "docs/governance/site-mirror-orchestration.md",
        "Do not guess navigation wiring",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit("SITE NAVIGATION DISCOVERY: FAIL - required text missing")
    print("SITE NAVIGATION DISCOVERY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
