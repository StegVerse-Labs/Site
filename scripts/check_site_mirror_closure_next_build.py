#!/usr/bin/env python3
"""Validate the Site mirror closure next-build packet.

This checker ensures Site closure-readiness documentation preserves the
Publisher activation boundary and does not claim activation from Site evidence
alone.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "SITE_MIRROR_CLOSURE_NEXT_BUILD.md"
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
CLOSURE_GUARD_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "site-mirror-closure-guard.yml"

REQUIRED_PACKET_TERMS = {
    "Primary handoff: docs/SITE_MIRROR_HANDOFF.md",
    "Repository: StegVerse-Labs/Site",
    "Source repository: GCAT-BCAT-Engine/Publisher",
    "Publisher verification receipt artifact",
    "Site evidence artifact",
    "Publisher closure nudge result",
    "Publisher closure receipt",
    "Publisher verification tracker activation commit",
    "Publisher activation-status update commit",
    "The Site repository must not mark the mirror activated solely because Site evidence exists.",
    "python scripts/check_site_mirror_closure_next_build.py",
    "Archive Readiness",
}

REQUIRED_HANDOFF_TERMS = {
    "Pending: actual Publisher receipt artifact",
    "actual Site evidence artifact",
    "Publisher closure receipt",
    "Publisher verification tracker activation",
    "Publisher activation-status update",
    "github/workflows/site-mirror-closure-guard.yml",
    "does not dispatch Publisher",
    "does not consume cross-repo credentials",
    "does not claim activation",
}

REQUIRED_CLOSURE_GUARD_WORKFLOW_TERMS = {
    "name: Site Mirror Closure Guard",
    "permissions:",
    "contents: read",
    "python scripts/check_site_mirror_handoff.py",
    "python scripts/check_site_mirror_closure_next_build.py",
    "Activation boundary",
    "Publisher closure remains required before activation can be claimed.",
}

FORBIDDEN_CLOSURE_GUARD_WORKFLOW_TERMS = {
    "STEGVERSE_REPO_SYNC_TOKEN",
    "secrets.",
    "curl -sS",
    "workflow_dispatches",
    "contents: write",
    "git push",
    "Activation Ready: `yes`",
    "Activation state: activated",
}


class ClosureNextBuildError(Exception):
    """Raised when the closure next-build packet is incomplete."""


def _read(path: Path) -> str:
    if not path.exists():
        raise ClosureNextBuildError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _missing_terms(markdown: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in markdown)


def _present_forbidden_terms(markdown: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term in markdown)


def main() -> int:
    try:
        packet = _read(PACKET_PATH)
        handoff = _read(HANDOFF_PATH)
        closure_guard_workflow = _read(CLOSURE_GUARD_WORKFLOW_PATH)

        errors: list[str] = []

        missing_packet_terms = _missing_terms(packet, REQUIRED_PACKET_TERMS)
        if missing_packet_terms:
            errors.append(
                "closure next-build packet is missing required terms: "
                + ", ".join(missing_packet_terms)
            )

        missing_handoff_terms = _missing_terms(handoff, REQUIRED_HANDOFF_TERMS)
        if missing_handoff_terms:
            errors.append(
                "Site mirror handoff no longer preserves pending closure boundary: "
                + ", ".join(missing_handoff_terms)
            )

        missing_workflow_terms = _missing_terms(
            closure_guard_workflow,
            REQUIRED_CLOSURE_GUARD_WORKFLOW_TERMS,
        )
        if missing_workflow_terms:
            errors.append(
                "closure guard workflow is missing required terms: "
                + ", ".join(missing_workflow_terms)
            )

        forbidden_workflow_terms = _present_forbidden_terms(
            closure_guard_workflow,
            FORBIDDEN_CLOSURE_GUARD_WORKFLOW_TERMS,
        )
        if forbidden_workflow_terms:
            errors.append(
                "closure guard workflow contains forbidden activation or credential terms: "
                + ", ".join(forbidden_workflow_terms)
            )

        if "Activation Ready: `yes`" in packet or "Activation state: activated" in packet:
            errors.append("closure next-build packet appears to overclaim activation.")

        if errors:
            for error in errors:
                print(f"closure next-build verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror closure next-build verification passed.")
        return 0
    except ClosureNextBuildError as exc:
        print(f"closure next-build verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
