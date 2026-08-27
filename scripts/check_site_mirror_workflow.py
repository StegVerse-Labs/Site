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
        "workflow_run:",
        "python scripts/run_site_task.py",
        "mirror-readiness",
        "github.event.workflow_run.conclusion == 'success'",
        "github.event.workflow_run.head_branch == 'main'",
    ]
    workflow_missing = [item for item in workflow_required if item not in workflow_text]

    on_block = workflow_text.split("permissions:", 1)[0]
    forbidden_triggers = [
        marker
        for marker in ("push:", "schedule:", "pull_request:")
        if marker in on_block
    ]
    if forbidden_triggers:
        raise SystemExit(
            "SITE MIRROR WORKFLOW: FAIL - forbidden independent worker trigger present: "
            + ", ".join(forbidden_triggers)
        )
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
    print("worker_schedule_authority=false")
    print("worker_push_authority=false")
    print("worker_pull_request_authority=false")
    print("worker_execution_trigger=SUCCESSFUL_MAIN_BOOTSTRAP_WORKFLOW_RUN")
    print("manual_dispatch=VALIDATION_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
