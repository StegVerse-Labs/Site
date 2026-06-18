#!/usr/bin/env python3
"""Verify Site paper display policy and mirror configuration."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    Path("docs/SITE_PAPER_DISPLAY_POLICY.md"),
    Path("docs/README_SITE_PAPERS_MIRROR.md"),
    Path("docs/SITE_MIRROR_ACTIVATION_STATUS.md"),
    Path("scripts/mirror_papers.py"),
    Path("scripts/check_papers_manifest_metadata.py"),
    Path("scripts/write_site_mirror_evidence.py"),
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
    "DEFAULT_SOURCE_PATH: \"papers\"",
    "TARGET_REPOSITORY: \"StegVerse-Labs/Site\"",
    "python scripts/mirror_papers.py",
    "python scripts/check_papers_manifest_metadata.py",
    "python scripts/check_paper_aliases.py",
    "python scripts/write_site_mirror_evidence.py",
    "site-mirror-evidence-${{ github.run_id }}-${{ github.run_attempt }}",
    "actions/upload-artifact@v4",
    "Nudge Publisher closure workflow",
    "close-site-mirror-activation.yml/dispatches",
    "Scheduled Publisher closure remains the fallback",
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
    "mirror_metadata",
    "source_repository",
    "source_ref",
    "source_path",
    "source_of_truth",
    "target_repository",
    "display_policy",
    "mirror_protocol",
    "papers_manifest.json",
]

REQUIRED_EVIDENCE_WRITER_TERMS = [
    "SITE_MIRROR_EVIDENCE_PACKET.md",
    "SITE_MIRROR_LIVE_EVIDENCE_STATE.json",
    "site_mirror_workflow_url",
    "site_mirror_commit_sha",
    "alias_verification_results",
    "live_activation_verified",
    "PENDING",
]

REQUIRED_MANIFEST_CHECKER_TERMS = [
    "source_repository",
    "source_ref",
    "source_path",
    "source_of_truth",
    "target_repository",
    "target_path",
    "display_policy",
    "mirror_protocol",
    "workflow",
    "valid: Site papers manifest metadata",
]

REQUIRED_MIRROR_DOC_TERMS = [
    "docs/SITE_PAPER_DISPLAY_POLICY.md",
    "docs/SITE_MIRROR_ACTIVATION_STATUS.md",
    "papers/papers_manifest.json",
    "scripts/check_papers_manifest_metadata.py",
    "source_repository",
    "source_ref",
    "source_path",
    "source_of_truth",
    "Validate papers/papers_manifest.json metadata",
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

    result = require_terms(Path("scripts/write_site_mirror_evidence.py"), REQUIRED_EVIDENCE_WRITER_TERMS)
    if result is not None:
        return result

    result = require_terms(Path("scripts/check_papers_manifest_metadata.py"), REQUIRED_MANIFEST_CHECKER_TERMS)
    if result is not None:
        return result

    result = require_terms(Path("docs/README_SITE_PAPERS_MIRROR.md"), REQUIRED_MIRROR_DOC_TERMS)
    if result is not None:
        return result

    print("valid: Site paper display policy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
