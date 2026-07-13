#!/usr/bin/env python3
"""Validate the final Site activation-pending boundary."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FINAL_PENDING = ROOT / "docs" / "SITE_FINAL_ACTIVATION_PENDING.md"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_FINAL_TERMS = {
    "activation_status: pending_external_evidence",
    "structurally complete up to the remaining external evidence boundary",
    "first committed bundle-fed TT status",
    "Governance Observatory status validation result",
    "TT sync workflow produces the first committed bundle-fed status.",
    "Governance Observatory status validation passes.",
    "This record does not grant commit-time permission.",
    "Let the repository workflows produce the required evidence.",
}

REQUIRED_HANDOFF_TERMS = {
    "Result: Site preparation complete; live activation and external custody evidence pending",
    ".github/workflows/validate.yml",
    ".github/workflows/site-task-runner.yml",
    "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
    "contract_status: PREPARED_NOT_DEPLOYED",
    "live_transport_enabled: false",
    "destination current-main tests",
    "Master-Records custody",
    "reconstructability PASS",
    "No release tag is authorized.",
}

FORBIDDEN_TERMS = {
    "activation_status: complete",
    "Activation state: activated",
    "grants commit-time permission",
    "Site is source repository for Publisher",
    "Site is source repository for TT",
}


def read(path: Path) -> str:
    if not path.exists():
        print(f"missing file: {path.relative_to(ROOT)}", file=sys.stderr)
        raise SystemExit(1)
    return path.read_text(encoding="utf-8")


def missing(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def present(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term in text)


def main() -> int:
    final_pending = read(FINAL_PENDING)
    handoff = read(HANDOFF)
    errors: list[str] = []

    missing_final = missing(final_pending, REQUIRED_FINAL_TERMS)
    if missing_final:
        errors.append("final activation pending file missing terms: " + ", ".join(missing_final))

    missing_handoff = missing(handoff, REQUIRED_HANDOFF_TERMS)
    if missing_handoff:
        errors.append("handoff missing final activation pending terms: " + ", ".join(missing_handoff))

    forbidden = present(final_pending + "\n" + handoff, FORBIDDEN_TERMS)
    if forbidden:
        errors.append("forbidden activation terms present: " + ", ".join(forbidden))

    if errors:
        for error in errors:
            print(f"final activation pending verification failed: {error}", file=sys.stderr)
        return 1

    print("PASS: Site final activation remains pending on verified external deployment, custody, and reconstructability evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
