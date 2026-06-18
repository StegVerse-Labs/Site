#!/usr/bin/env python3
"""Validate Site mirror priority queue packet structure."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "docs" / "SITE_MIRROR_PRIORITY_QUEUE.md"
COMPLETION_PATH = ROOT / "docs" / "SITE_MIRROR_TASK_COMPLETION_VERIFICATION.md"
APPENDIX_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF_APPENDIX_PRIORITY_QUEUE.md"

REQUIRED_QUEUE_TERMS = {
    "P0:",
    "P1:",
    "P2:",
    "P3:",
    "Selection Rule",
    "Completion Verification Rule",
    "Current Queue Seed",
    "Archive Readiness",
}

REQUIRED_COMPLETION_TERMS = {
    "Verification Inputs",
    "Completion Evidence Types",
    "Completion States",
    "Completion Rule",
    "Blocked Rule",
    "Archive Readiness",
}

REQUIRED_APPENDIX_TERMS = {
    "docs/SITE_MIRROR_PRIORITY_QUEUE.md",
    "docs/SITE_MIRROR_TASK_COMPLETION_VERIFICATION.md",
    "docs/SITE_MIRROR_TASK_LOOP_TRACKER.md",
    "Current Continuation Candidate",
    "Archive Readiness",
}


class PriorityQueueError(Exception):
    """Raised when priority queue packets are incomplete."""


def _read(path: Path) -> str:
    if not path.exists():
        raise PriorityQueueError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def main() -> int:
    try:
        checks = [
            ("priority queue packet", _read(QUEUE_PATH), REQUIRED_QUEUE_TERMS),
            ("completion verification packet", _read(COMPLETION_PATH), REQUIRED_COMPLETION_TERMS),
            ("priority queue handoff appendix", _read(APPENDIX_PATH), REQUIRED_APPENDIX_TERMS),
        ]

        errors: list[str] = []
        for label, text, terms in checks:
            missing = _missing_terms(text, terms)
            if missing:
                errors.append(f"{label} missing required terms: " + ", ".join(missing))

        if errors:
            for error in errors:
                print(f"priority queue verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror priority queue verification passed.")
        return 0
    except PriorityQueueError as exc:
        print(f"priority queue verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
