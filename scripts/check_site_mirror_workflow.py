#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"


def main() -> int:
    if not WORKFLOW.exists():
        raise SystemExit("SITE MIRROR WORKFLOW: FAIL - consolidated workflow missing")
    text = WORKFLOW.read_text(encoding="utf-8")
    required = [
        "name: Site Task Runner",
        "workflow_dispatch:",
        "schedule:",
        "workflow_run:",
        "python scripts/run_site_task.py",
        "mirror-readiness",
        "python scripts/check_site_mirror_full_readiness.py",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(
            "SITE MIRROR WORKFLOW: FAIL - required consolidated workflow text missing: "
            + ", ".join(missing)
        )
    print("SITE MIRROR WORKFLOW: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
