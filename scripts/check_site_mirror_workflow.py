#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"
TASK_RUNNER = ROOT / "scripts" / "run_site_task.py"


def main() -> int:
    if not WORKFLOW.exists():
        raise SystemExit("SITE MIRROR WORKFLOW: FAIL - consolidated workflow missing")
    if not TASK_RUNNER.exists():
        raise SystemExit("SITE MIRROR WORKFLOW: FAIL - consolidated task runner missing")

    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    workflow_required = [
        "name: Site Task Runner",
        "workflow_dispatch:",
        "schedule:",
        "workflow_run:",
        "python scripts/run_site_task.py",
        "mirror-readiness",
    ]
    workflow_missing = [item for item in workflow_required if item not in workflow_text]
    if workflow_missing:
        raise SystemExit(
            "SITE MIRROR WORKFLOW: FAIL - required consolidated workflow text missing: "
            + ", ".join(workflow_missing)
        )

    task_runner_text = TASK_RUNNER.read_text(encoding="utf-8")
    task_runner_required = [
        '"mirror-readiness": mirror_readiness',
        'run_if_present("scripts/check_site_mirror_full_readiness.py")',
    ]
    task_runner_missing = [item for item in task_runner_required if item not in task_runner_text]
    if task_runner_missing:
        raise SystemExit(
            "SITE MIRROR WORKFLOW: FAIL - required task-runner binding missing: "
            + ", ".join(task_runner_missing)
        )

    print("SITE MIRROR WORKFLOW: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
