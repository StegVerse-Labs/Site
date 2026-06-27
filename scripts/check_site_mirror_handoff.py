#!/usr/bin/env python3
"""Verify that the Site mirror handoff matches the current repository structure.

The handoff is the build-continuation source of truth. This checker validates
that it still names the current goal, preserves canonical-source boundaries, and
lists repository files that actually exist.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_GOAL_FIELDS = {
    "Goal: Continue building without manual actions needed through completion",
    "task handoff and task completion are capable of being handled by the ecosystem's own management",
    "Repository: StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher, Admissible-Existence/TT, and StegVerse-Labs/governance-observatory",
    "papers, TT propagation artifacts, and Governance Observatory source-intake status",
    "Target path: papers, docs, and public HTML surfaces",
    "Activation state: pending_external_evidence",
    "Self-management state: repository_managed_continuation_ready",
}

REQUIRED_BOUNDARY_TERMS = {
    "The Site mirror must not become a separate editorial source of truth.",
    "Publisher remains authoritative for papers.",
    "Admissible-Existence/TT remains authoritative for Transition Table code-representation semantics.",
    "StegVerse-Labs/governance-observatory remains authoritative for Governance Observatory source-intake records.",
    "must not redefine transition-element semantics",
    "display does not certify external sources",
}

REQUIRED_AUTONOMOUS_TERMS = {
    "github/workflows/site-autonomous-continuation.yml",
    "Sync TT Code Representation",
    "Validate Governance Observatory Status",
    "write external evidence state",
    "update final goal status",
    "validate final goal status",
    "commit computed state changes",
}

REQUIRED_TT_TERMS = {
    "tt-code-representation.html",
    "github/workflows/sync-tt-code-representation.yml",
    "python scripts/render_tt_code_representation_status.py",
    "python scripts/check_site_tt_code_representation_mirror.py",
    "data/tt/transition-element-propagation-bundle.manifest.json",
    "docs/SITE_TT_CODE_REPRESENTATION_STATUS.md",
    "docs/SITE_TT_CODE_REPRESENTATION_STATUS.json",
    "pending fail-closed status",
}

REQUIRED_OBSERVATORY_TERMS = {
    "governance-observatory.html",
    "docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md",
    "docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json",
    "python scripts/check_site_governance_observatory_status.py",
    "github/workflows/validate-governance-observatory-status.yml",
}

REQUIRED_FINAL_STATUS_TERMS = {
    "github/workflows/site-final-goal-status.yml",
    "python scripts/update_site_final_goal_status.py",
    "python scripts/check_site_final_goal_status.py",
    "docs/SITE_FINAL_GOAL_STATUS.md",
    "docs/SITE_FINAL_GOAL_STATUS.json",
    "pending_external_evidence",
}

REQUIRED_ARCHIVE_TERMS = {
    "complete thread is ready for archiving",
    "automated final goal status reports `ready`",
}

FORBIDDEN_TERMS = {
    "Activation state: activated",
    "Activation: complete",
    "Activation state: pending_publisher_closure_evidence",
    "Site is proof authority",
    "TT authority source: StegVerse-Labs/Site",
}


class HandoffError(Exception):
    """Raised when the handoff is incomplete or inconsistent."""


def _load_handoff() -> str:
    if not HANDOFF_PATH.exists():
        raise HandoffError(f"Missing handoff: {HANDOFF_PATH.relative_to(ROOT)}")
    return HANDOFF_PATH.read_text(encoding="utf-8")


def _extract_built_files(markdown: str) -> list[str]:
    match = re.search(
        r"## Built Files\s+```text\s+(.*?)\s+```",
        markdown,
        flags=re.DOTALL,
    )
    if not match:
        raise HandoffError("Missing Built Files text block in Site mirror handoff.")

    files = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    if not files:
        raise HandoffError("Built Files block is empty.")
    return files


def _repository_path(display_path: str) -> Path:
    if display_path.startswith("github/workflows/"):
        display_path = f".{display_path}"
    return ROOT / display_path


def _check_built_files_exist(display_paths: list[str]) -> list[str]:
    missing = []
    for display_path in display_paths:
        if not _repository_path(display_path).exists():
            missing.append(display_path)
    return missing


def _require_terms(markdown: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in markdown)


def _reject_terms(markdown: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term in markdown)


def main() -> int:
    try:
        markdown = _load_handoff()
        built_files = _extract_built_files(markdown)

        errors: list[str] = []

        missing_files = _check_built_files_exist(built_files)
        if missing_files:
            errors.append("Built Files contains paths that do not exist: " + ", ".join(missing_files))

        checks = [
            ("Current Goal", REQUIRED_GOAL_FIELDS),
            ("Canonical Boundaries", REQUIRED_BOUNDARY_TERMS),
            ("Autonomous Continuation", REQUIRED_AUTONOMOUS_TERMS),
            ("TT Code Representation", REQUIRED_TT_TERMS),
            ("Governance Observatory", REQUIRED_OBSERVATORY_TERMS),
            ("Final Goal Status", REQUIRED_FINAL_STATUS_TERMS),
            ("Archive Readiness", REQUIRED_ARCHIVE_TERMS),
        ]

        for section_name, terms in checks:
            missing_terms = _require_terms(markdown, terms)
            if missing_terms:
                errors.append(f"Handoff is missing required {section_name} terms: " + ", ".join(missing_terms))

        forbidden_terms = _reject_terms(markdown, FORBIDDEN_TERMS)
        if forbidden_terms:
            errors.append("Handoff contains obsolete or forbidden terms: " + ", ".join(forbidden_terms))

        if errors:
            for error in errors:
                print(f"handoff verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror handoff verification passed.")
        print(f"Verified built file count: {len(built_files)}")
        return 0
    except HandoffError as exc:
        print(f"handoff verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
