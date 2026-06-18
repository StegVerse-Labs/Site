#!/usr/bin/env python3
"""Validate Site mirror ecosystem-managed completion status files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SITE_MIRROR_ECOSYSTEM_MANAGED_COMPLETION.md"
STATE = ROOT / "docs" / "SITE_MIRROR_ECOSYSTEM_MANAGED_COMPLETION_STATE.json"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_DOC_TERMS = [
    "ecosystem-managed completion",
    "docs/SITE_MIRROR_HANDOFF.md",
    "Publisher remains the source of truth",
    "Site-side evidence alone cannot activate the mirror",
    "manual_chat_context_required: false",
    "activation_overclaim_guarded: true",
    "remaining_work_machine_readable: true",
    "actual Publisher receipt artifact",
    "actual Site evidence artifact",
    "Publisher closure receipt",
    "Publisher verification tracker activation",
    "Publisher activation-status update",
    "prior chat thread is not required",
]

REQUIRED_STATE = {
    "goal": "ecosystem_managed_completion",
    "repository": "StegVerse-Labs/Site",
    "handoff": "docs/SITE_MIRROR_HANDOFF.md",
    "status": "management_ready_pending_external_evidence",
    "archive_ready": True,
}

REQUIRED_EVIDENCE = {
    "Publisher receipt artifact",
    "Site evidence artifact",
    "Publisher closure receipt",
    "Publisher tracker activation",
    "Publisher activation status update",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"invalid: {message}")


def main() -> None:
    require(DOC.exists(), f"missing {DOC.relative_to(ROOT)}")
    require(STATE.exists(), f"missing {STATE.relative_to(ROOT)}")
    require(HANDOFF.exists(), f"missing {HANDOFF.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))

    for term in REQUIRED_DOC_TERMS:
        require(term in doc, f"missing document term: {term}")

    for key, expected in REQUIRED_STATE.items():
        require(state.get(key) == expected, f"state {key!r} must be {expected!r}")

    evidence = set(state.get("remaining_evidence", []))
    missing = sorted(REQUIRED_EVIDENCE - evidence)
    require(not missing, f"state missing remaining evidence: {missing}")

    require(
        "ready_for_automated_site_evidence_and_closure_nudge" in handoff,
        "handoff must preserve automated evidence and closure nudge state",
    )
    require(
        "Pending: actual Publisher receipt artifact" in handoff,
        "handoff must preserve pending Publisher receipt artifact boundary",
    )

    print("valid: Site mirror ecosystem-managed completion target is preserved")


if __name__ == "__main__":
    main()
