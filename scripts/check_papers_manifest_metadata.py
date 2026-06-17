#!/usr/bin/env python3
"""Verify mirrored papers manifest preserves Publisher source metadata."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "papers" / "papers_manifest.json"

REQUIRED_TOP_LEVEL_FIELDS = [
    "source_repository",
    "source_ref",
    "source_path",
    "source_of_truth",
    "target_repository",
    "target_path",
    "display_policy",
    "mirror_protocol",
    "workflow",
    "generated_utc",
    "count",
    "aliases",
    "entries",
]

EXPECTED_VALUES = {
    "source_repository": "GCAT-BCAT-Engine/Publisher",
    "source_path": "papers",
    "source_of_truth": "GCAT-BCAT-Engine/Publisher/papers",
    "target_repository": "StegVerse-Labs/Site",
    "target_path": "papers",
    "display_policy": "docs/SITE_PAPER_DISPLAY_POLICY.md",
    "mirror_protocol": "docs/README_SITE_PAPERS_MIRROR.md",
    "workflow": ".github/workflows/mirror-papers.yml",
}

REQUIRED_ALIASES = [
    "Papers.html",
    "papers.html",
    "papers/index.html",
    "publisher/papers.html",
    "publisher/papers/index.html",
]


def fail(message: str) -> int:
    print(f"papers manifest metadata check failed: {message}")
    return 1


def main() -> int:
    if not MANIFEST_PATH.exists():
        return fail("missing papers/papers_manifest.json")

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in manifest:
            return fail(f"missing manifest field: {field}")

    for field, expected in EXPECTED_VALUES.items():
        if manifest.get(field) != expected:
            return fail(f"expected {field} to be {expected!r}")

    if not manifest.get("source_ref"):
        return fail("source_ref must not be empty")

    aliases = manifest.get("aliases", [])
    for alias in REQUIRED_ALIASES:
        if alias not in aliases:
            return fail(f"missing alias: {alias}")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return fail("entries must be a list")

    if manifest.get("count") != len(entries):
        return fail("count must equal entries length")

    print("valid: Site papers manifest metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
