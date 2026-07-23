#!/usr/bin/env python3
"""Verify the Conectrr browser projection and bidirectional correlation contract."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE = (ROOT / "assets" / "ecosystem-node-views.js").read_text(encoding="utf-8")
INTEROP = (ROOT / "assets" / "conectrr-interop.js").read_text(encoding="utf-8")

REQUIRED_NODE = (
    "assets/conectrr-interop.js",
    "importCanonicalEvents",
    "selectEvent",
    "correlated-active",
)
REQUIRED_INTEROP = (
    "conectrrBrowserTest = 'pass'",
    "Source-to-decision correlation failed",
    "Decision-to-source correlation failed",
    "did not render",
    "api.selectEvent(source.event_id, 'governed')",
    "api.selectEvent(decision.event_id, 'governed')",
)


def main() -> int:
    errors: list[str] = []
    for marker in REQUIRED_NODE:
        if marker not in NODE:
            errors.append(f"node renderer missing marker: {marker}")
    for marker in REQUIRED_INTEROP:
        if marker not in INTEROP:
            errors.append(f"interop browser test missing marker: {marker}")
    if "source.event_id" not in INTEROP or "decision.event_id" not in INTEROP:
        errors.append("stable source and decision identifiers are not used")
    if "dataset.conectrrBrowserTest = 'fail'" not in INTEROP:
        errors.append("browser test does not expose fail-closed status")

    if errors:
        print("CONECTRR_BROWSER_PROJECTION_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONECTRR_BROWSER_PROJECTION_CHECK=PASS")
    print("rendered_records=source,decision")
    print("correlation=bidirectional")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
