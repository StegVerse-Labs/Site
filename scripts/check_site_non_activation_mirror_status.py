#!/usr/bin/env python3
"""Check that public mirror status pages remain non-authorizing."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "docs" / "SITE_MIRROR_ACTIVATION_STATUS.md"

REQUIRED_TERMS = {
    "Non-Activation Mirror Evidence",
    "tt-code-representation.html",
    "governance-observatory.html",
    "docs/SITE_TT_CODE_REPRESENTATION_STATUS.md",
    "docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md",
    "do not activate the Publisher paper mirror",
    "do not grant execution authority",
    "TT sync workflow first bundle-fed commit has not been recorded",
    "Governance Observatory status validation pass has not been recorded",
}


def main() -> int:
    text = STATUS_PATH.read_text(encoding="utf-8")
    missing = sorted(term for term in REQUIRED_TERMS if term not in text)
    if missing:
        print("non-activation mirror status check failed: " + ", ".join(missing), file=sys.stderr)
        return 1
    print("PASS: public mirror status surfaces remain non-authorizing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
