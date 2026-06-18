#!/usr/bin/env python3
"""Verify Site paper alias files resolve to the Publisher-mirrored papers page."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ALIAS_FILES = {
    "Papers.html": {
        "kind": "canonical_page",
        "must_contain": [
            "StegVerse Papers",
            "Mirrored paper outputs",
        ],
    },
    "papers.html": {
        "kind": "redirect",
        "must_contain": [
            "url=Papers.html",
            "href=\"Papers.html\"",
        ],
    },
    "papers/index.html": {
        "kind": "canonical_page",
        "must_contain": [
            "StegVerse Papers",
            "Mirrored paper outputs",
        ],
    },
    "publisher/papers.html": {
        "kind": "redirect",
        "must_contain": [
            "url=../Papers.html",
            "href=\"../Papers.html\"",
        ],
    },
    "publisher/papers/index.html": {
        "kind": "redirect",
        "must_contain": [
            "url=../../Papers.html",
            "href=\"../../Papers.html\"",
        ],
    },
}


def fail(message: str) -> int:
    print(f"paper alias check failed: {message}")
    return 1


def main() -> int:
    for relative_path, expectation in REQUIRED_ALIAS_FILES.items():
        path = REPO_ROOT / relative_path
        if not path.exists():
            return fail(f"missing alias file: {relative_path}")
        if not path.is_file():
            return fail(f"alias path is not a file: {relative_path}")

        content = path.read_text(encoding="utf-8")
        for expected in expectation["must_contain"]:
            if expected not in content:
                return fail(
                    f"{relative_path} does not satisfy {expectation['kind']} expectation; "
                    f"missing {expected!r}"
                )

    print("valid: Site paper aliases resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
