#!/usr/bin/env python3
"""Validate the Site mirror closure guard packet and workflow."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GUARD_PACKET_PATH = ROOT / "docs" / "SITE_MIRROR_CLOSURE_GUARD.md"
GUARD_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "site-mirror-closure-guard.yml"
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_PACKET_TERMS = {
    "github/workflows/site-mirror-closure-guard.yml",
    ".github/workflows/site-mirror-closure-guard.yml",
    "Use read-only contents permission.",
    "scripts/check_site_mirror_handoff.py",
    "scripts/check_site_mirror_closure_next_build.py",
    "scripts/check_site_mirror_closure_guard.py",
    "Publisher closure remains required before activation can be claimed",
    "Archive Readiness",
}

REQUIRED_WORKFLOW_TERMS = {
    "name: Site Mirror Closure Guard",
    "workflow_dispatch:",
    "permissions:",
    "contents: read",
    "python scripts/check_site_mirror_handoff.py",
    "python scripts/check_site_mirror_closure_next_build.py",
    "python scripts/check_site_mirror_closure_guard.py",
    "Publisher closure remains required before activation can be claimed.",
}

REQUIRED_HANDOFF_TERMS = {
    "docs/SITE_MIRROR_CLOSURE_GUARD.md",
    "python scripts/check_site_mirror_closure_guard.py",
    "no-secret closure guard workflow",
    "Publisher closure remains required before activation can be claimed",
}


class ClosureGuardError(Exception):
    """Raised when the closure guard packet or workflow is incomplete."""


def _read(path: Path) -> str:
    if not path.exists():
        raise ClosureGuardError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def main() -> int:
    try:
        packet = _read(GUARD_PACKET_PATH)
        workflow = _read(GUARD_WORKFLOW_PATH)
        handoff = _read(HANDOFF_PATH)

        errors: list[str] = []

        checks = [
            ("closure guard packet", packet, REQUIRED_PACKET_TERMS),
            ("closure guard workflow", workflow, REQUIRED_WORKFLOW_TERMS),
            ("Site mirror handoff", handoff, REQUIRED_HANDOFF_TERMS),
        ]

        for label, text, terms in checks:
            missing = _missing_terms(text, terms)
            if missing:
                errors.append(f"{label} is missing required terms: " + ", ".join(missing))

        if errors:
            for error in errors:
                print(f"closure guard verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror closure guard verification passed.")
        return 0
    except ClosureGuardError as exc:
        print(f"closure guard verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
