#!/usr/bin/env python3
"""Fail closed when the Site Task Runner regains independent trigger authority."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

WORKFLOW = Path(".github/workflows/site-task-runner.yml")
TERMINAL_CONTRACT = Path("scripts/check_site_orchestration_terminal_receipt.py")


def fail(message: str) -> None:
    print(f"SITE_ORCHESTRATION_CONTRACT: FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not WORKFLOW.is_file():
        fail(f"missing {WORKFLOW}")

    text = WORKFLOW.read_text(encoding="utf-8")
    on_block = text.split("permissions:", 1)[0]

    forbidden = {
        "push:": "Site Task Runner must not start independently on repository pushes",
        "schedule:": "Site Task Runner must not own a schedule",
        "pull_request:": "Site Task Runner must not start independently on pull requests",
    }
    for marker, reason in forbidden.items():
        if marker in on_block:
            fail(reason)

    required = (
        "workflow_run:",
        "- Site Bootstrap Validate - No Non-TV/TVC Credential Authority",
        "github.event.workflow_run.conclusion == 'success'",
        "github.event.workflow_run.head_branch == 'main'",
        "ref: ${{ steps.transition.outputs.sha }}",
        "cancel-in-progress: true",
        "github.event.workflow_run.conclusion || 'manual'",
        "if: github.event_name == 'workflow_run'",
        "Write terminal orchestration receipt",
        "write_site_orchestration_terminal_receipt.py",
        "site-orchestration-terminal-receipt.json",
        "check_semantic_shorthand_live_routes.py",
        "semantic-shorthand-live-verification.json",
        "regenerate_on_current_main()",
        "git reset --hard origin/main",
        "Generated-state push raced with main",
        "for attempt in 1 2 3",
    )
    for marker in required:
        if marker not in text:
            fail(f"required orchestration marker absent: {marker}")

    if "github.ref == 'refs/heads/main'" in text:
        fail("mutation/deployment must be authorized by the successful upstream workflow_run, not merely by branch context")

    if "git rebase origin/main" in text or "git pull --rebase" in text:
        fail("generated-state persistence must regenerate on current main instead of rebasing stale generated snapshots")

    if not TERMINAL_CONTRACT.is_file():
        fail(f"missing {TERMINAL_CONTRACT}")
    completed = subprocess.run([sys.executable, str(TERMINAL_CONTRACT)], text=True, check=False)
    if completed.returncode != 0:
        fail("terminal receipt contract failed")

    print("SITE_ORCHESTRATION_CONTRACT: PASS")
    print("worker_trigger_authority=workflow_run_after_successful_bootstrap")
    print("manual_dispatch_authority=validation_only")
    print("push_authority=false")
    print("schedule_authority=false")
    print("superseded_run_policy=cancel_same_sha_same_conclusion_only")
    print("rejected_bootstrap_cannot_preempt_valid_main_transition=true")
    print("generated_state_conflict_policy=REGENERATE_ON_CURRENT_MAIN")
    print("generated_state_writeback_retries=3")
    print("terminal_receipt_required=true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
