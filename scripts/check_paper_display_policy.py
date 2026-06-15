#!/usr/bin/env python3
"""Verify Site paper display policy and mirror configuration."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    Path("docs/SITE_PAPER_DISPLAY_POLICY.md"),
    Path("docs/README_SITE_PAPERS_MIRROR.md"),
    Path("scripts/mirror_papers.py"),
    Path(".github/workflows/mirror-papers.yml"),
]

REQUIRED_POLICY_TERMS = [
    "GCAT-BCAT-Engine/Publisher",
    "Papers.html",
    "papers.html",
    "papers/index.html",
    "publisher/papers.html",
    "publisher/papers/index.html",
    "source repository: GCAT-BCAT-Engine/Publisher",
    "source path: papers",
    "target path: papers",
]

REQUIRED_WORKFLOW_TERMS = [
    "name: Mirror Papers from Publisher",
    "default: \"GCAT-BCAT-Engine/Publisher\"",
    "DEFAULT_SOURCE_REPOSITORY: \"GCAT-BCAT-Engine/Publisher\"",
    "DEFAULT_SOURCE_REF: \"main\"",
    "if [ ! -d \"_source/papers\" ]; then",
    "python scripts/mirror_papers.py",
    "Papers.html",
    "papers.html",
    "publisher/papers.html",
]

REQUIRED_SCRIPT_TERMS = [
    "SOURCE_PAPERS = REPO_ROOT / \"_source\" / \"papers\"",
    "TARGET_PAPERS = REPO_ROOT / \"papers\"",
    "PAPERS_HTML = REPO_ROOT / \"Papers.html\"",
    "PAPERS_LOWER_HTML = REPO_ROOT / \"papers.html\"",
    "PUBLISHER_PAPERS_HTML = PUBLISHER_DIR / \"papers.html\"",
    "PUBLISHER_PAPERS_INDEX = PUBLISHER_PAPERS_DIR / \"index.html\"",
    "papers_manifest.json",
    "GCAT-BCAT-Engine/Publisher/papers",
]


def read(path: Path) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> int:
    print(f"paper display policy check failed: {message}")
    return 1


def require_file(path: Path) -> int | None:
    if not (REPO_ROOT / path).exists():
        return fail(f"missing required file: {path}")
    return None


def require_terms(path: Path, terms: list[str]) -> int | None:
    text = read(path)
    for term in terms:
        if term not in text:
            return fail(f"missing {term!r} in {path}")
    return None


def main() -> int:
    for path in REQUIRED_FILES:
        result = require_file(path)
        if result is not None:
            return result

    result = require_terms(Path("docs/SITE_PAPER_DISPLAY_POLICY.md"), REQUIRED_POLICY_TERMS)
    if result is not None:
        return result

    result = require_terms(Path(".github/workflows/mirror-papers.yml"), REQUIRED_WORKFLOW_TERMS)
    if result is not None:
        return result

    result = require_terms(Path("scripts/mirror_papers.py"), REQUIRED_SCRIPT_TERMS)
    if result is not None:
        return result

    mirror_doc = read(Path("docs/README_SITE_PAPERS_MIRROR.md"))
    if "docs/SITE_PAPER_DISPLAY_POLICY.md" not in mirror_doc:
        return fail("mirror README does not link the Site paper display policy")

    print("valid: Site paper display policy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
