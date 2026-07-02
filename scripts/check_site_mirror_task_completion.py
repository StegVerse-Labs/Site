#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "site-mirror-task-completion-status.json"
WORKFLOW = ROOT / ".github" / "workflows" / "site-mirror-readiness.yml"
FULL_READINESS = ROOT / "scripts" / "check_site_mirror_full_readiness.py"


def main() -> int:
    if not STATUS.exists():
        raise SystemExit("SITE MIRROR TASK COMPLETION: FAIL - status missing")
    if not WORKFLOW.exists():
        raise SystemExit("SITE MIRROR TASK COMPLETION: FAIL - workflow missing")
    if not FULL_READINESS.exists():
        raise SystemExit("SITE MIRROR TASK COMPLETION: FAIL - full readiness wrapper missing")
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    expected = {
        "status_id": "site-mirror-task-completion-status",
        "repository": "StegVerse-Labs/Site",
        "repo_local_build": "AUTOMATED_VALIDATION_READY",
        "validation_workflow": ".github/workflows/site-mirror-readiness.yml",
        "validation_command": "python scripts/check_site_mirror_full_readiness.py",
        "next_action": "WAIT_FOR_AUTOMATED_WORKFLOW_RESULT",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(f"SITE MIRROR TASK COMPLETION: FAIL - {key} expected {value!r}, got {data.get(key)!r}")
    surfaces = data.get("installed_surfaces")
    if not isinstance(surfaces, list) or "scripts/check_site_mirror_full_readiness.py" not in surfaces:
        raise SystemExit("SITE MIRROR TASK COMPLETION: FAIL - full readiness wrapper not listed")
    print("SITE MIRROR TASK COMPLETION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
