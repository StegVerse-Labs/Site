#!/usr/bin/env python3
"""Validate the Site TT code-representation mirror contract."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs/SITE_TT_CODE_REPRESENTATION_MIRROR.md"

REQUIRED_TERMS = [
    "Admissible-Existence/TT",
    "canonical source",
    "Site does not become the source of truth",
    "dist/transition-element-propagation-bundle.manifest.json",
    "transition_id",
    "code_ref",
    "fixture_ref",
    "receipt_schema_ref",
    "FAIL_CLOSED",
    "github/workflows/transition-element-code-validation.yml",
]


def main() -> int:
    text = DOC.read_text(encoding="utf-8")
    missing = [term for term in REQUIRED_TERMS if term not in text]
    if missing:
        print(f"FAIL: missing required mirror terms: {missing}")
        return 1
    print("PASS: Site TT code-representation mirror preserves canonical boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
