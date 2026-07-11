#!/usr/bin/env python3
"""Verify the bounded Site task diagnostic contract.

This checker validates the repository-local diagnostic implementation and its
existing workflow integration. It does not execute Site tasks or grant authority.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_site_task.py"
WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

RUNNER_REQUIRED = [
    'DIAGNOSTIC_PATH = ROOT / "reports" / "site-task-diagnostic.json"',
    '"receipt_type": "site_task_diagnostic"',
    '"failed_validator": failed_validator',
    '"validator_index":',
    '"exit_code": exit_code',
    '"completed_validators": COMPLETED_VALIDATORS',
    '"authority_effect": "NONE"',
    '"site_mode": "PREVIEW_ONLY"',
    '"state_change_authorized": False',
    'failure_class="VALIDATION_FAILURE"',
    'failure_class="MISSING_REQUIRED_VALIDATOR"',
    'failure_class="TEST_READINESS_FAILURE"',
    'failure_class="UNRESOLVED_TASK_FAILURE"',
    'write_diagnostic(status="PASSED")',
]

WORKFLOW_REQUIRED = [
    "Upload Site task diagnostic",
    "if: always()",
    "actions/upload-artifact@v4",
    "site-task-diagnostic-${{ github.run_id }}-${{ github.run_attempt }}",
    "site/reports/site-task-diagnostic.json",
    "if-no-files-found: error",
    "Failed validator:",
    "Authority effect:",
]

HANDOFF_REQUIRED = [
    "Fail-path diagnostic contract",
    "reports/site-task-diagnostic.json",
    "authority_effect",
    "site_mode",
    "state_change_authorized",
    "The diagnostic is evidence of task execution only.",
]


def require_text(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing required file: {path.relative_to(ROOT)}"]
    body = path.read_text(encoding="utf-8")
    return [
        f"{path.relative_to(ROOT)} missing required text: {needle}"
        for needle in needles
        if needle not in body
    ]


def main() -> int:
    failures: list[str] = []
    failures.extend(require_text(RUNNER, RUNNER_REQUIRED))
    failures.extend(require_text(WORKFLOW, WORKFLOW_REQUIRED))
    failures.extend(require_text(HANDOFF, HANDOFF_REQUIRED))

    workflow_dir = ROOT / ".github" / "workflows"
    active_workflows = sorted(
        path.name
        for path in workflow_dir.iterdir()
        if path.is_file() and path.suffix in {".yml", ".yaml"}
    )
    if active_workflows != ["site-task-runner.yml", "validate.yml"]:
        failures.append(
            "active workflow set drift: expected exactly "
            "site-task-runner.yml and validate.yml, got "
            + ", ".join(active_workflows)
        )

    if failures:
        print("SITE_TASK_DIAGNOSTIC_CONTRACT_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("SITE_TASK_DIAGNOSTIC_CONTRACT_PASS")
    print("authority_effect=NONE")
    print("site_mode=PREVIEW_ONLY")
    print("state_change_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
