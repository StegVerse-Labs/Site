#!/usr/bin/env python3
"""Validate the Site self-managed completion assessment."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "assessment": ROOT / "docs" / "SITE_SELF_MANAGED_COMPLETION.md",
    "handoff": ROOT / "docs" / "SITE_MIRROR_HANDOFF.md",
    "management_handoff": ROOT / "docs" / "SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md",
    "external_evidence": ROOT / "docs" / "SITE_EXTERNAL_EVIDENCE_STATE.json",
    "final_goal": ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.json",
    "final_pending": ROOT / "docs" / "SITE_FINAL_ACTIVATION_PENDING.md",
}

GOAL = "Goal: Continue building without manual actions needed through completion"
ECOSYSTEM_GOAL = "task handoff and task completion are capable of being handled by the ecosystem's own management"

REQUIRED = {
    "assessment": [
        GOAL,
        ECOSYSTEM_GOAL,
        "Repository: StegVerse-Labs/Site",
        "GCAT-BCAT-Engine/Publisher, Admissible-Existence/TT, and StegVerse-Labs/governance-observatory",
        "Activation state: pending_external_evidence",
        "Self-management state: repository_managed_continuation_ready",
        "Repository-managed continuation: ready",
        "Activation: pending",
        "Manual chat context required: no",
        "Manual evidence reconstruction required: no",
        "Manual workflow dispatch required: no",
        "TT bundle-fed status is PASS",
        "Governance Observatory status is valid",
        "final goal status reports ready",
    ],
    "handoff": [
        GOAL,
        ECOSYSTEM_GOAL,
        "Repository: StegVerse-Labs/Site",
        "Activation state: pending_external_evidence",
        "Self-management state: repository_managed_continuation_ready",
        "docs/SITE_SELF_MANAGED_COMPLETION.md",
        "python scripts/check_site_self_managed_completion.py",
        "github/workflows/site-autonomous-continuation.yml",
        "docs/SITE_FINAL_GOAL_STATUS.json",
        "Publisher remains authoritative",
        "Admissible-Existence/TT remains authoritative",
        "StegVerse-Labs/governance-observatory remains authoritative",
    ],
    "management_handoff": [
        GOAL,
        "management_state: self_managed_handoff_ready",
        "manual_action_requirement: none_for_site_evidence_entry",
        "thread_archive_ready: true",
    ],
    "external_evidence": ["pending_external_evidence"],
    "final_goal": ["site_final_goal_status.v0.1", "pending_external_evidence"],
    "final_pending": ["activation_status: pending_external_evidence"],
}

FORBIDDEN = [
    "Goal: Site mirror activation hardening",
    "Activation: complete",
    "Activation state: activated",
    "activation complete",
    "pending_publisher_closure_evidence",
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
