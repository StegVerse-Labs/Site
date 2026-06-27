#!/usr/bin/env python3
"""Validate the public TT code-representation page and homepage links."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGE = REPO_ROOT / "tt-code-representation.html"
INDEX = REPO_ROOT / "index.html"
PUBLIC_PATHS = REPO_ROOT / "docs/SITE_PUBLIC_PATHS.md"

PUBLIC_PAGE_TERMS = [
    "Transition Table Code Representation",
    "Admissible-Existence/TT",
    "public mirror surface only",
    "code_ref",
    "fixture_ref",
    "receipt_schema_ref",
    "FAIL_CLOSED",
    "SPE must still reconstruct current standing",
]

INDEX_TERMS = [
    "tt-code-representation.html",
    "TT Code Representation",
    "public mirror of canonical TT code surface, not authority",
]

PUBLIC_PATH_TERMS = [
    "/tt-code-representation.html",
    "public mirror surface",
    "Admissible-Existence/TT",
    "must not claim that it defines TT semantics",
]


def require_terms(path: Path, terms: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [term for term in terms if term not in text]


def main() -> int:
    failures: list[str] = []
    for path, terms in (
        (PUBLIC_PAGE, PUBLIC_PAGE_TERMS),
        (INDEX, INDEX_TERMS),
        (PUBLIC_PATHS, PUBLIC_PATH_TERMS),
    ):
        if not path.exists():
            failures.append(f"missing file: {path.relative_to(REPO_ROOT)}")
            continue
        missing = require_terms(path, terms)
        if missing:
            failures.append(f"{path.relative_to(REPO_ROOT)} missing terms: {missing}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: public TT code-representation page and homepage links preserve mirror boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
