#!/usr/bin/env python3
"""Validate Site handoff final-pending continuation terms."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_TERMS = {
    "Result: Site preparation complete; live activation and external custody evidence pending",
    ".github/workflows/validate.yml",
    ".github/workflows/site-task-runner.yml",
    "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
    "PREPARED_NOT_DEPLOYED",
    "destination current-main tests",
    "Master-Records custody",
    "reconstructability PASS",
    "No release tag is authorized.",
}

FORBIDDEN_TERMS = {
    "Activation state: activated",
    "Activation: complete",
    "Site is proof authority",
    "live_transport.enabled: true",
    "contract_status: DEPLOYED",
}


def main() -> int:
    text = HANDOFF.read_text(encoding="utf-8")
    missing = sorted(term for term in REQUIRED_TERMS if term not in text)
    forbidden = sorted(term for term in FORBIDDEN_TERMS if term in text)
    if missing or forbidden:
        if missing:
            print("handoff final-pending check missing: " + ", ".join(missing), file=sys.stderr)
        if forbidden:
            print("handoff final-pending check forbidden: " + ", ".join(forbidden), file=sys.stderr)
        return 1
    print("PASS: Site handoff preserves current activation-blocked external-evidence boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
