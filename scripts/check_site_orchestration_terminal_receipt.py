#!/usr/bin/env python3
"""Validate the Site orchestration terminal-receipt implementation contract."""
from pathlib import Path

WRITER = Path("scripts/write_site_orchestration_terminal_receipt.py")
WORKFLOW = Path(".github/workflows/site-task-runner.yml")


def fail(message: str) -> None:
    print(f"SITE_TERMINAL_RECEIPT_CONTRACT: FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not WRITER.is_file():
        fail(f"missing {WRITER}")
    if not WORKFLOW.is_file():
        fail(f"missing {WORKFLOW}")

    writer = WRITER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    for marker in (
        "stegverse.site.orchestration-terminal-receipt.v1",
        "validated_commit_sha",
        "source_run_id",
        "generated_state_mutation",
        "pages_deployment",
        "live_route_verification",
        "terminal_state",
        "receipt_sha256",
        '"authority_effect": "NONE"',
        '"task_runner_deployment_authority": False',
        '"owner": "NATIVE_GITHUB_PAGES_WORKFLOW"',
    ):
        if marker not in writer:
            fail(f"writer missing required marker: {marker}")

    for marker in (
        "write_site_orchestration_terminal_receipt.py",
        "site-orchestration-terminal-receipt.json",
        "STEGVERSE_ORCHESTRATION_SOURCE_RUN_ID",
        "STEGVERSE_ORCHESTRATION_SHA",
        "STEGVERSE_PAGES_DEPLOYMENT_RESULT: NOT_OWNED_BY_TASK_RUNNER",
    ):
        if marker not in workflow:
            fail(f"workflow is not bound to terminal receipt marker: {marker}")

    print("SITE_TERMINAL_RECEIPT_CONTRACT: PASS")
    print("terminal_receipt_bound=true")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
