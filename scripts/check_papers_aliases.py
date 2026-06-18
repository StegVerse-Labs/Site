#!/usr/bin/env python3
"""Verify local Site paper alias files exist and point toward Papers.html."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ALIAS_TARGETS = {
    "Papers.html": "StegVerse Papers",
    "papers.html": "Papers.html",
    "papers/index.html": "StegVerse Papers",
    "publisher/papers.html": "../Papers.html",
    "publisher/papers/index.html": "../../Papers.html",
}


def fail(message: str) -> int:
    print(f"paper alias check failed: {message}")
    return 1


def main() -> int:
    for rel_path, expected_text in ALIAS_TARGETS.items():
        path = REPO_ROOT / rel_path
        if not path.exists():
            return fail(f"missing alias target: {rel_path}")
        text = path.read_text(encoding="utf-8")
        if expected_text not in text:
            return fail(f"alias target missing expected text: {rel_path}")

    print("valid: Site paper aliases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
