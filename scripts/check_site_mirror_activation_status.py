#!/usr/bin/env python3
"""Validate Site mirror activation status against the activation ledger."""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_STATUS.md"
LEDGER_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.json"
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_STATUS_TERMS = {
    "activation_state: pending",
    "source_of_truth: Publisher",
    "ledger: docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "Site-side evidence alone does not activate the mirror.",
    "Publisher closure remains required before activation can be claimed.",
    "python scripts/check_site_mirror_activation_ledger.py",
    "python scripts/check_site_mirror_activation_status.py",
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

REQUIRED_HANDOFF_TERMS = {
    "docs/SITE_MIRROR_ACTIVATION_STATUS.md",
    "python scripts/check_site_mirror_activation_status.py",
    "activation status",
}


class ActivationStatusError(Exception):
    """Raised when Site activation status drifts from the ledger."""


def _read(path: Path) -> str:
    if not path.exists():
        raise ActivationStatusError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        raise ActivationStatusError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def main() -> int:
    try:
        status = _read(STATUS_PATH)
        ledger = _read_json(LEDGER_PATH)
        handoff = _read(HANDOFF_PATH)

        errors: list[str] = []

        missing_status_terms = _missing_terms(status, REQUIRED_STATUS_TERMS)
        if missing_status_terms:
            errors.append("activation status missing required terms: " + ", ".join(missing_status_terms))

        if ledger.get("activation_state") != "pending":
            errors.append("activation ledger must remain pending until Publisher closure evidence exists")

        if ledger.get("source_of_truth") != "Publisher":
            errors.append("activation ledger source_of_truth must be Publisher")

        required_evidence = ledger.get("required_evidence", {})
        if not isinstance(required_evidence, dict):
            errors.append("activation ledger required_evidence must be an object")
            required_evidence = {}

        missing_ledger_keys = sorted(REQUIRED_LEDGER_KEYS - set(required_evidence))
        if missing_ledger_keys:
            errors.append("activation ledger required_evidence missing keys: " + ", ".join(missing_ledger_keys))

        non_pending = sorted(
            key for key in REQUIRED_LEDGER_KEYS
            if required_evidence.get(key) != "pending"
        )
        if non_pending:
            errors.append("activation status cannot advance while ledger evidence is non-pending without Publisher closure review: " + ", ".join(non_pending))

        missing_handoff_terms = _missing_terms(handoff, REQUIRED_HANDOFF_TERMS)
        if missing_handoff_terms:
            errors.append("handoff missing activation status terms: " + ", ".join(missing_handoff_terms))

        if errors:
            for error in errors:
                print(f"activation status verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror activation status verification passed.")
        return 0
    except ActivationStatusError as exc:
        print(f"activation status verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
