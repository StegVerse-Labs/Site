#!/usr/bin/env python3
"""Validate the Site self-managed completion assessment."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "assessment": ROOT / "docs" / "SITE_SELF_MANAGED_COMPLETION.md",
    "handoff": ROOT / "docs" / "SITE_MIRROR_HANDOFF.md",
    "management_handoff": ROOT / "docs" / "SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md",
    "ledger": ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.json",
    "status": ROOT / "docs" / "SITE_MIRROR_ACTIVATION_STATUS.md",
}

GOAL = "Goal: Continue building without manual actions needed through completion"
ECOSYSTEM_GOAL = "task handoff and task completion are capable of being handled by the ecosystem's own management"

REQUIRED = {
    "assessment": [
        GOAL,
        ECOSYSTEM_GOAL,
        "Repository: StegVerse-Labs/Site",
        "Activation state: pending_publisher_closure_evidence",
        "Self-management state: repository_managed_continuation_ready",
        "Repository-managed continuation: ready",
        "Activation: pending",
        "Manual chat context required: no",
        "Manual evidence reconstruction required: no",
        "docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md",
        "ecosystem management handoff",
        "Publisher receipt artifact",
        "Site evidence artifact",
        "Publisher closure receipt",
        "Publisher verification tracker activation",
        "Publisher activation-status update",
    ],
    "handoff": [
        GOAL,
        ECOSYSTEM_GOAL,
        "Repository: StegVerse-Labs/Site",
        "Activation state: pending_publisher_closure_evidence",
        "Self-management state: repository_managed_continuation_ready",
        "docs/SITE_SELF_MANAGED_COMPLETION.md",
        "docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md",
        "python scripts/check_site_self_managed_completion.py",
        "Publisher remains authoritative",
        "Publisher closure remains required before activation can be claimed",
        "The prior chat thread is no longer required",
    ],
    "management_handoff": [
        GOAL,
        "management_state: self_managed_handoff_ready",
        "manual_action_requirement: none_for_site_evidence_entry",
        "remaining_dependency: live workflow artifact production and Publisher closure observation",
        "thread_archive_ready: true",
    ],
    "ledger": ["pending"],
    "status": ["pending"],
}

FORBIDDEN = [
    "Goal: Site mirror activation hardening",
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
