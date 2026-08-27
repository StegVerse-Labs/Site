#!/usr/bin/env python3
"""Validate Site handoff final-pending continuation terms."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_TERMS = {
    "Result: ACTIVATION_PENDING_AUTHORIZED_REAL_PROVIDER_AND_PERSISTENT_ENDPOINT",
    "Compatibility Result: ACTIVATION_PENDING_LIVE_MACHINE_EXECUTION",
    "Manual user action required for routine repository work: false",
    "Master-Records custody",
    "provider-usage reconstruction",
    "transition reconstructability PASS",
    "immutable zero-blocker activation receipt",
    "verified downstream ingestion",
    "No tag or release is authorized.",
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
    print("PASS: Site handoff preserves current activation-blocked provider/custody/downstream evidence boundary.")
    print("canonical_result=ACTIVATION_PENDING_AUTHORIZED_REAL_PROVIDER_AND_PERSISTENT_ENDPOINT")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
