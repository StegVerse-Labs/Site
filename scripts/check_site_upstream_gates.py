#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "site-upstream-gates.json"

REQUIRED_GATES = {
    "repo-standards-release-tag",
    "admissibility-wiki-validation-receipt",
    "site-navigation-structure",
    "public-deployment-verification",
}


def main() -> int:
    if not STATUS.exists():
        raise SystemExit("SITE UPSTREAM GATES: FAIL - status missing")
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    expected = {
        "status_id": "site-upstream-gates",
        "repository": "StegVerse-Labs/Site",
        "status": "WAITING_ON_UPSTREAM_GATES",
        "automated_validation": ".github/workflows/site-mirror-readiness.yml",
        "next_action": "WAIT_FOR_UPSTREAM_GATE_EVENTS",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(f"SITE UPSTREAM GATES: FAIL - {key} expected {value!r}, got {data.get(key)!r}")
    gate_ids = {gate.get("id") for gate in data.get("gates", []) if isinstance(gate, dict)}
    missing = sorted(REQUIRED_GATES - gate_ids)
    if missing:
        raise SystemExit(f"SITE UPSTREAM GATES: FAIL - missing gates: {', '.join(missing)}")
    print("SITE UPSTREAM GATES: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
