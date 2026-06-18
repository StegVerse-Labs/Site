#!/usr/bin/env python3
"""Validate the Site self-managed completion assessment."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "assessment": ROOT / "docs" / "SITE_SELF_MANAGED_COMPLETION.md",
    "handoff": ROOT / "docs" / "SITE_MIRROR_HANDOFF.md",
    "ledger": ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.json",
    "status": ROOT / "docs" / "SITE_MIRROR_ACTIVATION_STATUS.md",
}

REQUIRED = {
    "assessment": [
        "repository-managed continuation",
        "pending_publisher_closure_evidence",
        "repository_managed_continuation_ready",
        "Manual chat context required: no",
        "Publisher receipt artifact",
        "Site evidence artifact",
        "Publisher closure receipt",
        "Publisher verification tracker activation",
        "Publisher activation-status update",
    ],
    "handoff": [
        "Publisher remains authoritative",
        "Publisher closure remains required before activation can be claimed",
        "The prior chat thread is no longer required",
    ],
    "ledger": ["pending"],
    "status": ["pending"],
}

FORBIDDEN = [
    "Activation: complete",
    "Activation state: activated",
    "activation complete",
]


def main() -> int:
    for label, path in FILES.items():
        if not path.exists():
            print(f"missing {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        missing = [term for term in REQUIRED[label] if term not in text]
        blocked = [term for term in FORBIDDEN if term in text]
        if missing or blocked:
            print(f"{label} failed self-managed completion check", file=sys.stderr)
            for term in missing:
                print(f"missing: {term}", file=sys.stderr)
            for term in blocked:
                print(f"forbidden: {term}", file=sys.stderr)
            return 1
    print("site self-managed completion assessment: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
