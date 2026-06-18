#!/usr/bin/env python3
"""Validate the Site mirror activation ledger.

The ledger is a machine-readable Site-side activation boundary. It must remain
pending until Publisher closure evidence exists and must not claim activation
from Site-side evidence alone.
"""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
LEDGER_JSON_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.json"
LEDGER_MD_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_LEDGER.md"
HANDOFF_PATH = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_TOP_LEVEL_FIELDS = {
    "schema_version",
    "repository",
    "source_repository",
    "source_path",
    "target_path",
    "source_of_truth",
    "activation_state",
    "non_activation_rule",
    "required_evidence",
    "required_checks",
    "activation_allowed_when",
    "activation_blocked_by",
}

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

REQUIRED_CHECKS = {
    "python scripts/check_site_mirror_handoff.py",
    "python scripts/check_site_mirror_evidence_packet.py",
    "python scripts/check_site_mirror_live_evidence_state.py",
    "python scripts/check_site_mirror_closure_next_build.py",
    "python scripts/check_site_mirror_closure_guard.py",
    "python scripts/check_site_mirror_activation_ledger.py",
}

REQUIRED_MARKDOWN_TERMS = {
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "activation_state: pending",
    "Site-side evidence alone does not activate the mirror.",
    "Publisher closure remains required before activation can be claimed.",
    "python scripts/check_site_mirror_activation_ledger.py",
    "Archive Readiness",
}

REQUIRED_HANDOFF_TERMS = {
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.json",
    "docs/SITE_MIRROR_ACTIVATION_LEDGER.md",
    "python scripts/check_site_mirror_activation_ledger.py",
    "activation ledger",
}


class ActivationLedgerError(Exception):
    """Raised when the activation ledger is incomplete or overclaims."""


def _read_text(path: Path) -> str:
    if not path.exists():
        raise ActivationLedgerError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    try:
        return json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        raise ActivationLedgerError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def main() -> int:
    try:
        ledger = _read_json(LEDGER_JSON_PATH)
        ledger_md = _read_text(LEDGER_MD_PATH)
        handoff = _read_text(HANDOFF_PATH)

        errors: list[str] = []

        missing_top_level = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(ledger))
        if missing_top_level:
            errors.append("ledger JSON missing top-level fields: " + ", ".join(missing_top_level))

        if ledger.get("repository") != "StegVerse-Labs/Site":
            errors.append("ledger repository must be StegVerse-Labs/Site")

        if ledger.get("source_repository") != "GCAT-BCAT-Engine/Publisher":
            errors.append("ledger source_repository must be GCAT-BCAT-Engine/Publisher")

        if ledger.get("source_of_truth") != "Publisher":
            errors.append("ledger source_of_truth must be Publisher")

        if ledger.get("activation_state") != "pending":
            errors.append("ledger activation_state must remain pending until Publisher closure evidence exists")

        required_evidence = ledger.get("required_evidence", {})
        if not isinstance(required_evidence, dict):
            errors.append("ledger required_evidence must be an object")
            required_evidence = {}

        missing_evidence = sorted(REQUIRED_EVIDENCE_KEYS - set(required_evidence))
        if missing_evidence:
            errors.append("ledger required_evidence missing keys: " + ", ".join(missing_evidence))

        non_pending_evidence = sorted(
            key for key, value in required_evidence.items()
            if key in REQUIRED_EVIDENCE_KEYS and value != "pending"
        )
        if non_pending_evidence:
            errors.append(
                "ledger evidence values must remain pending until actual closure evidence exists: "
                + ", ".join(non_pending_evidence)
            )

        required_checks = set(ledger.get("required_checks", []))
        missing_checks = sorted(REQUIRED_CHECKS - required_checks)
        if missing_checks:
            errors.append("ledger required_checks missing commands: " + ", ".join(missing_checks))

        activation_blocked_by = set(ledger.get("activation_blocked_by", []))
        missing_blockers = sorted(REQUIRED_EVIDENCE_KEYS - activation_blocked_by)
        if missing_blockers:
            errors.append("ledger activation_blocked_by missing evidence blockers: " + ", ".join(missing_blockers))

        missing_markdown_terms = _missing_terms(ledger_md, REQUIRED_MARKDOWN_TERMS)
        if missing_markdown_terms:
            errors.append("ledger Markdown missing required terms: " + ", ".join(missing_markdown_terms))

        missing_handoff_terms = _missing_terms(handoff, REQUIRED_HANDOFF_TERMS)
        if missing_handoff_terms:
            errors.append("handoff missing activation ledger terms: " + ", ".join(missing_handoff_terms))

        if errors:
            for error in errors:
                print(f"activation ledger verification failed: {error}", file=sys.stderr)
            return 1

        print("Site mirror activation ledger verification passed.")
        return 0
    except ActivationLedgerError as exc:
        print(f"activation ledger verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
