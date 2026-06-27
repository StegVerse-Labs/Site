#!/usr/bin/env python3
"""Validate Site handoff final-pending continuation terms."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_TERMS = {
    "Activation state: pending_external_evidence",
    "github/workflows/site-public-mirror-status-guard.yml",
    "python scripts/check_site_non_activation_mirror_status.py",
    "python scripts/check_site_final_activation_pending.py",
    "docs/SITE_FINAL_ACTIVATION_PENDING.md",
    "final activation remains pending on external workflow evidence",
    "first committed bundle-fed status",
    "Governance Observatory status validation passes",
}

FORBIDDEN_TERMS = {
    "Activation state: activated",
    "Activation: complete",
    "Site is proof authority",
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
    print("PASS: Site handoff preserves final-pending external evidence boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
