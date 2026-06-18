#!/usr/bin/env python3
"""Validate Site mirror evidence transition rules.

This checker prevents evidence values from advancing beyond pending until the
ledger and handoff explicitly preserve Publisher closure as the activation
boundary.
"""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
TRANSITION_RULES_PATH = ROOT / "docs" / "SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md"
LEDGER_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.json"
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_EVIDENCE_KEYS = {
    "publisher_workflow_run_url",
    "publisher_verification_receipt_artifact",
    "publisher_live_dispatch_workflow_url",
    "site_mirror_workflow_url",
    "site_mirror_commit_sha",
    "site_evidence_artifact",
    "publisher_closure_nudge_result",
    "publisher_closure_receipt",
    "publisher_verification_tracker_activation_commit",
    "publisher_activation_status_update_commit",
}

REQUIRED_TRANSITION_TERMS = {
    "Ledger: docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "Evidence requirements: docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md",
    "Activation status: docs/SITE_MIRROR_ACTIVATION_STATUS.md",
    "Handoff: docs/SITE_MIRROR_HANDOFF.md",
    "pending",
    "observed",
    "verified",
    "activated",
    "Site-side evidence alone does not activate the mirror.",
    "Publisher closure remains required before activation can be claimed.",
    "The Site repository must not transition directly from `pending` to `activated` using Site-local evidence alone.",
    "python scripts/check_site_mirror_evidence_transition_rules.py",
    "Archive Readiness",
}

REQUIRED_HANDOFF_TERMS = {
    "docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md",
    "python scripts/check_site_mirror_evidence_transition_rules.py",
    "Evidence Transition Rules Packet",
}


class EvidenceTransitionRulesError(Exception):
    """Raised when evidence transition rules drift from the ledger or handoff."""


def _read(path: Path) -> str:
    if not path.exists():
        raise EvidenceTransitionRulesError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        raise EvidenceTransitionRulesError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def main() -> int:
    try:
        transition_rules = _read(TRANSITION_RULES_PATH)
        ledger = _read_json(LEDGER_PATH)
        handoff = _read(HANDOFF_PATH)

        errors: list[str] = []

        missing_transition_terms = _missing_terms(transition_rules, REQUIRED_TRANSITION_TERMS)
        if missing_transition_terms:
            errors.append(
                "evidence transition rules packet missing required terms: "
                + ", ".join(missing_transition_terms)
            )

        required_evidence = ledger.get("required_evidence", {})
        if not isinstance(required_evidence, dict):
            errors.append("activation ledger required_evidence must be an object")
            required_evidence = {}

        missing_ledger_keys = sorted(REQUIRED_EVIDENCE_KEYS - set(required_evidence))
        if missing_ledger_keys:
            errors.append("activation ledger missing evidence keys: " + ", ".join(missing_ledger_keys))

        non_pending = sorted(
            key for key in REQUIRED_EVIDENCE_KEYS
            if required_evidence.get(key) != "pending"
        )
        if non_pending:
            errors.append(
                "evidence transition currently blocked; these ledger values must remain pending: "
                + ", ".join(non_pending)
            )

        if ledger.get("activation_state") != "pending":
            errors.append("activation_state must remain pending until Publisher closure evidence exists")

        missing_handoff_terms = _missing_terms(handoff, REQUIRED_HANDOFF_TERMS)
        if missing_handoff_terms:
            errors.append("handoff missing evidence transition rules terms: " + ", ".join(missing_handoff_terms))

        if errors:
            for error in errors:
                print(f"evidence transition rules verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror evidence transition rules verification passed.")
        return 0
    except EvidenceTransitionRulesError as exc:
        print(f"evidence transition rules verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
