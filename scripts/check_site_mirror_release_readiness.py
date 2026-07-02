#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "site-mirror-release-readiness.json"


def main() -> int:
    if not STATUS.exists():
        raise SystemExit("SITE MIRROR RELEASE READINESS: FAIL - status missing")
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    expected = {
        "status_id": "site-mirror-release-readiness",
        "repository": "StegVerse-Labs/Site",
        "repo_local_status": "READY_FOR_VALIDATION",
        "validation_command": "python scripts/check_site_mirror_readiness.py",
        "next_action": "RUN_SITE_MIRROR_READINESS_VALIDATION",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(f"SITE MIRROR RELEASE READINESS: FAIL - {key} expected {value!r}, got {data.get(key)!r}")
    surfaces = data.get("installed_surfaces")
    if not isinstance(surfaces, list) or "scripts/check_site_mirror_readiness.py" not in surfaces:
        raise SystemExit("SITE MIRROR RELEASE READINESS: FAIL - readiness script not listed")
    print("SITE MIRROR RELEASE READINESS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
