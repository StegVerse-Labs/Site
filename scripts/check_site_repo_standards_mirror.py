#!/usr/bin/env python3
"""Validate the Site repo-standards mirror surface."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SITE_REPO_STANDARDS_MIRROR.md"
PAGE = ROOT / "repo-standards.html"

REQUIRED_DOC_PHRASES = [
    "StegVerse-Labs/repo-standards remains authoritative",
    "Site is display-only",
    "0.1.0-rc.1 release-candidate surface prepared",
    "Publisher mirror: pending",
    "admissibility-wiki mirror: pending",
    "stegguardian-wiki mirror: pending",
]

REQUIRED_PAGE_PHRASES = [
    "StegVerse Repository Standards Mirror",
    "Site is display-only",
    "does not create repository standards",
    "does not certify conformance",
    "does not grant correction authority",
    "ST-013",
]


def require(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required path: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    try:
        doc = require(DOC)
        page = require(PAGE)
        for phrase in REQUIRED_DOC_PHRASES:
            if phrase not in doc:
                raise AssertionError(f"missing doc phrase: {phrase}")
        for phrase in REQUIRED_PAGE_PHRASES:
            if phrase not in page:
                raise AssertionError(f"missing page phrase: {phrase}")
    except AssertionError as exc:
        print(f"DENY: {exc}")
        return 1
    print("ALLOW: repo standards Site mirror is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
