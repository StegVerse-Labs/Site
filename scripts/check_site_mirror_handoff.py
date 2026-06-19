#!/usr/bin/env python3
"""Verify that the Site mirror handoff matches the repository structure."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_GOAL_FIELDS = {
    "Goal: autonomous Site mirror completion or ecosystem-managed handoff",
    "Repository: StegVerse-Labs/Site",
    "Source repository: GCAT-BCAT-Engine/Publisher",
    "Source path: papers",
    "Target path: papers",
    "Assessment state: ecosystem_managed_handoff_capable",
}

REQUIRED_VALIDATOR_COMMANDS = {
    "python scripts/check_paper_display_policy.py",
    "python scripts/check_transition_table_public_copy.py",
    "python scripts/check_site_public_ingestion_contract.py",
    "python scripts/check_site_mirror_evidence_packet.py",
    "python scripts/check_site_mirror_live_evidence_state.py",
    "python scripts/check_site_mirror_handoff.py",
    "python scripts/check_site_mirror_closure_next_build.py",
    "python scripts/check_site_mirror_closure_guard.py",
    "python scripts/check_site_mirror_activation_ledger.py",
    "python scripts/check_site_mirror_activation_status.py",
    "python scripts/check_site_mirror_evidence_requirements.py",
    "python scripts/check_site_mirror_evidence_transition_rules.py",
    "python scripts/check_site_mirror_autonomous_completion_assessment.py",
    "python scripts/check_papers_manifest_metadata.py",
    "python scripts/check_paper_aliases.py",
}

REQUIRED_EVIDENCE_TERMS = {
    "Publisher workflow run URL",
    "Publisher verification receipt artifact",
    "Site mirror workflow URL",
    "Site evidence artifact",
    "Publisher closure nudge result",
    "Publisher closure receipt",
    "Publisher verification tracker activation commit",
    "Publisher activation-status update commit",
}

REQUIRED_CLOSURE_TERMS = {
    "docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md",
    "Closure Next-Build Packet",
    "Site may prepare and validate closure-readiness evidence",
    "Publisher closure remains required before activation can be claimed",
}

REQUIRED_LEDGER_TERMS = {
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.md",
    "Activation Ledger Packet",
    "python scripts/check_site_mirror_activation_ledger.py",
    "Site-side evidence alone does not activate the mirror",
}

REQUIRED_STATUS_TERMS = {
    "docs/SITE_MIRROR_ACTIVATION_STATUS.md",
    "Activation Status Packet",
    "python scripts/check_site_mirror_activation_status.py",
    "activation status remains aligned with the activation ledger",
}

REQUIRED_EVIDENCE_REQUIREMENTS_TERMS = {
    "docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md",
    "Evidence Requirements Packet",
    "python scripts/check_site_mirror_evidence_requirements.py",
    "exact evidence keys required before activation may advance",
}

REQUIRED_EVIDENCE_TRANSITION_TERMS = {
    "docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md",
    "Evidence Transition Rules Packet",
    "python scripts/check_site_mirror_evidence_transition_rules.py",
    "evidence values may advance from pending",
}

REQUIRED_ASSESSMENT_TERMS = {
    "docs/SITE_MIRROR_AUTONOMOUS_COMPLETION_ASSESSMENT.md",
    "Autonomous Completion Assessment Packet",
    "python scripts/check_site_mirror_autonomous_completion_assessment.py",
    "ecosystem-managed handoff",
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
            ("Validators", REQUIRED_VALIDATOR_COMMANDS),
            ("Evidence To Capture", REQUIRED_EVIDENCE_TERMS),
            ("Closure Next-Build Packet", REQUIRED_CLOSURE_TERMS),
            ("Activation Ledger Packet", REQUIRED_LEDGER_TERMS),
            ("Activation Status Packet", REQUIRED_STATUS_TERMS),
            ("Evidence Requirements Packet", REQUIRED_EVIDENCE_REQUIREMENTS_TERMS),
            ("Evidence Transition Rules Packet", REQUIRED_EVIDENCE_TRANSITION_TERMS),
            ("Autonomous Completion Assessment Packet", REQUIRED_ASSESSMENT_TERMS),
        ]

        for section_name, terms in checks:
            missing_terms = _require_terms(markdown, terms)
            if missing_terms:
                errors.append(f"Handoff is missing required {section_name} terms: " + ", ".join(missing_terms))

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
