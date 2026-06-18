#!/usr/bin/env python3
"""Verify that the Site mirror handoff matches the repository structure.

This checker keeps docs/SITE_MIRROR_HANDOFF.md from drifting away from the
files and automation it declares as the current source of truth for mirror
activation handoff.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_GOAL_FIELDS = {
    "Goal: Site mirror activation hardening",
    "Repository: StegVerse-Labs/Site",
    "Source repository: GCAT-BCAT-Engine/Publisher",
    "Source path: papers",
    "Target path: papers",
}

REQUIRED_VALIDATOR_COMMANDS = {
    "python scripts/check_paper_display_policy.py",
    "python scripts/check_transition_table_public_copy.py",
    "python scripts/check_site_public_ingestion_contract.py",
    "python scripts/check_site_mirror_evidence_packet.py",
    "python scripts/check_site_mirror_live_evidence_state.py",
    "python scripts/check_site_mirror_handoff.py",
    "python scripts/check_papers_manifest_metadata.py",
    "python scripts/check_paper_aliases.py",
}

REQUIRED_EVIDENCE_TERMS = {
    "Publisher workflow run URL",
    "Publisher verification receipt artifact",
    "Site mirror workflow URL",
    "Site evidence artifact",
    "Publisher closure nudge result",
    "Publisher verification tracker activation commit",
    "Publisher activation-status update commit",
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
    # Handoff display avoids leading-dot workflow paths for mobile upload safety.
    if display_path.startswith("github/workflows/"):
        display_path = f".{display_path}"
    return ROOT / display_path


def _check_built_files_exist(display_paths: list[str]) -> list[str]:
    missing = []
    for display_path in display_paths:
        if not _repository_path(display_path).exists():
            missing.append(display_path)
    return missing


def _require_terms(markdown: str, terms: set[str], section_name: str) -> list[str]:
    return sorted(term for term in terms if term not in markdown)


def main() -> int:
    try:
        markdown = _load_handoff()
        built_files = _extract_built_files(markdown)

        errors: list[str] = []

        missing_files = _check_built_files_exist(built_files)
        if missing_files:
            errors.append(
                "Built Files contains paths that do not exist: "
                + ", ".join(missing_files)
            )

        missing_goal_fields = _require_terms(markdown, REQUIRED_GOAL_FIELDS, "Current Goal")
        if missing_goal_fields:
            errors.append(
                "Current Goal is missing required fields: "
                + ", ".join(missing_goal_fields)
            )

        missing_commands = _require_terms(
            markdown,
            REQUIRED_VALIDATOR_COMMANDS,
            "Validators",
        )
        if missing_commands:
            errors.append(
                "Handoff is missing required validator commands: "
                + ", ".join(missing_commands)
            )

        missing_evidence = _require_terms(
            markdown,
            REQUIRED_EVIDENCE_TERMS,
            "Evidence To Capture",
        )
        if missing_evidence:
            errors.append(
                "Handoff is missing required evidence terms: "
                + ", ".join(missing_evidence)
            )

        if "Archive Readiness" not in markdown:
            errors.append("Handoff is missing Archive Readiness section.")

        if "Pending: actual Publisher receipt artifact" not in markdown:
            errors.append("Handoff no longer records the current pending activation evidence boundary.")

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
