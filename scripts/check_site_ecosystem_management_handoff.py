#!/usr/bin/env python3
"""Validate the Site ecosystem-management handoff.

This checker verifies that future build sessions can determine the current Site
mirror goal, pending activation boundary, next safe build candidate, and archive
readiness without relying on prior chat context.
"""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MANAGEMENT_HANDOFF_PATH = ROOT / "docs" / "SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md"
MIRROR_HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
LEDGER_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.json"

REQUIRED_MANAGEMENT_TERMS = {
    "Goal: Continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.",
    "Primary handoff: docs/SITE_MIRROR_HANDOFF.md",
    "Companion source handoff: GCAT-BCAT-Engine/Publisher/docs/PUBLISHER_MIRROR_HANDOFF.md",
    "Management state: ecosystem-managed continuation ready after this packet and checker pass",
    "python scripts/check_site_ecosystem_management_handoff.py",
    "Next-Action Selection Rules",
    "Current Next Build Candidate",
    "promote scripts/check_site_mirror_evidence_transition_rules.py into github/workflows/site-mirror-closure-guard.yml",
    "Site-side evidence alone does not activate the mirror.",
    "Publisher closure remains required before activation can be claimed.",
    "Archive Readiness",
    "prior chat thread",
}

REQUIRED_MIRROR_HANDOFF_TERMS = {
    "docs/SITE_MIRROR_HANDOFF.md",
    "Activation state: ready_for_automated_site_evidence_and_closure_nudge",
    "Pending: actual Publisher receipt artifact",
    "scripts/check_site_mirror_evidence_transition_rules.py",
    "Publisher closure remains required before activation can be claimed",
    "Archive Readiness",
}

REQUIRED_LEDGER_KEYS = {
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


class EcosystemManagementHandoffError(Exception):
    """Raised when ecosystem-management handoff verification fails."""


def _read(path: Path) -> str:
    if not path.exists():
        raise EcosystemManagementHandoffError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        raise EcosystemManagementHandoffError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def main() -> int:
    try:
        management_handoff = _read(MANAGEMENT_HANDOFF_PATH)
        mirror_handoff = _read(MIRROR_HANDOFF_PATH)
        ledger = _read_json(LEDGER_PATH)

        errors: list[str] = []

        missing_management_terms = _missing_terms(management_handoff, REQUIRED_MANAGEMENT_TERMS)
        if missing_management_terms:
            errors.append(
                "ecosystem management handoff missing required terms: "
                + ", ".join(missing_management_terms)
            )

        missing_mirror_terms = _missing_terms(mirror_handoff, REQUIRED_MIRROR_HANDOFF_TERMS)
        if missing_mirror_terms:
            errors.append(
                "mirror handoff missing required ecosystem-management boundary terms: "
                + ", ".join(missing_mirror_terms)
            )

        if ledger.get("activation_state") != "pending":
            errors.append("activation_state must remain pending until Publisher closure evidence exists")

        required_evidence = ledger.get("required_evidence", {})
        if not isinstance(required_evidence, dict):
            errors.append("activation ledger required_evidence must be an object")
            required_evidence = {}

        missing_ledger_keys = sorted(REQUIRED_LEDGER_KEYS - set(required_evidence))
        if missing_ledger_keys:
            errors.append("activation ledger missing required evidence keys: " + ", ".join(missing_ledger_keys))

        non_pending = sorted(
            key for key in REQUIRED_LEDGER_KEYS
            if required_evidence.get(key) != "pending"
        )
        if non_pending:
            errors.append(
                "ecosystem management cannot claim activation while these evidence keys are non-pending without closure reconciliation: "
                + ", ".join(non_pending)
            )

        if errors:
            for error in errors:
                print(f"ecosystem management handoff verification failed: {error}", file=sys.stderr)
            return 1

        print("Site ecosystem management handoff verification passed.")
        print("Management state: ecosystem-managed continuation ready.")
        print("Activation state: pending Publisher/Site closure evidence.")
        return 0
    except EcosystemManagementHandoffError as exc:
        print(f"ecosystem management handoff verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
