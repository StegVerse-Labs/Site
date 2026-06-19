#!/usr/bin/env python3
"""Validate the Site mirror autonomous completion assessment packet."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT_PATH = ROOT / "docs" / "SITE_MIRROR_AUTONOMOUS_COMPLETION_ASSESSMENT.md"
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
CLOSURE_GUARD_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "site-mirror-closure-guard.yml"

REQUIRED_ASSESSMENT_TERMS = {
    "Continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.",
    "Assessment state: ecosystem_managed_handoff_capable",
    "Activation state: pending_publisher_closure_evidence",
    "Full autonomous completion: not yet complete",
    "Ecosystem-managed handoff:",
    "Publisher closure receipt",
    "Publisher activation-status update commit",
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/SITE_MIRROR_CLOSURE_GUARD.md",
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md",
    "docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md",
    "scripts/check_site_mirror_autonomous_completion_assessment.py",
    "github/workflows/site-mirror-closure-guard.yml",
    "Archive Readiness",
}

REQUIRED_HANDOFF_TERMS = {
    "Goal: autonomous Site mirror completion or ecosystem-managed handoff",
    "Assessment state: ecosystem_managed_handoff_capable",
    "docs/SITE_MIRROR_AUTONOMOUS_COMPLETION_ASSESSMENT.md",
    "python scripts/check_site_mirror_autonomous_completion_assessment.py",
    "task handoff and task completion is capable of being handled by the ecosystem's own management",
}

REQUIRED_WORKFLOW_TERMS = {
    "python scripts/check_site_mirror_autonomous_completion_assessment.py",
    "docs/SITE_MIRROR_AUTONOMOUS_COMPLETION_ASSESSMENT.md",
    "scripts/check_site_mirror_autonomous_completion_assessment.py",
}

REQUIRED_EXISTING_PATHS = {
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/SITE_MIRROR_CLOSURE_GUARD.md",
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "docs/SITE_MIRROR_ACTIVATION_STATUS.md",
    "docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md",
    "docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md",
    "scripts/check_site_mirror_handoff.py",
    "scripts/check_site_mirror_closure_guard.py",
    "scripts/check_site_mirror_activation_ledger.py",
    "scripts/check_site_mirror_activation_status.py",
    "scripts/check_site_mirror_evidence_requirements.py",
    "scripts/check_site_mirror_evidence_transition_rules.py",
    "scripts/check_site_mirror_autonomous_completion_assessment.py",
    ".github/workflows/site-mirror-closure-guard.yml",
}


class AssessmentError(Exception):
    """Raised when the autonomous completion assessment is incomplete."""


def _read(path: Path) -> str:
    if not path.exists():
        raise AssessmentError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def _missing_paths(paths: set[str]) -> list[str]:
    missing: list[str] = []
    for path in sorted(paths):
        if not (ROOT / path).exists():
            missing.append(path)
    return missing


def main() -> int:
    try:
        assessment = _read(ASSESSMENT_PATH)
        handoff = _read(HANDOFF_PATH)
        workflow = _read(CLOSURE_GUARD_WORKFLOW_PATH)

        errors: list[str] = []

        checks = [
            ("autonomous completion assessment", assessment, REQUIRED_ASSESSMENT_TERMS),
            ("Site mirror handoff", handoff, REQUIRED_HANDOFF_TERMS),
            ("closure guard workflow", workflow, REQUIRED_WORKFLOW_TERMS),
        ]

        for label, text, terms in checks:
            missing = _missing_terms(text, terms)
            if missing:
                errors.append(f"{label} is missing required terms: " + ", ".join(missing))

        missing_paths = _missing_paths(REQUIRED_EXISTING_PATHS)
        if missing_paths:
            errors.append("autonomous completion assessment references missing paths: " + ", ".join(missing_paths))

        if errors:
            for error in errors:
                print(f"autonomous completion assessment failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror autonomous completion assessment passed.")
        print("Assessment state: ecosystem_managed_handoff_capable")
        print("Full autonomous completion: not yet complete")
        return 0
    except AssessmentError as exc:
        print(f"autonomous completion assessment failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
