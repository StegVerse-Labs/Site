#!/usr/bin/env python3
"""Validate that Site local continuation work is managed by declared tasks."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SITE_MANUAL_TASK_ELIMINATION.md"
GUARD_DOC = ROOT / "docs" / "SITE_TASK_ELIMINATION_GUARD.md"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
TASK_RUNNER = ROOT / "scripts" / "run_site_task.py"
TASK_WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"
RECEIPT_CHECKER = ROOT / "scripts" / "check_site_local_completion_receipt.py"

REQUIRED_DOC_TERMS = [
    "local_manual_tasks: eliminated",
    "local_continuation: workflow_managed",
    "activation_state: pending_external_evidence",
    "github/workflows/site-task-runner.yml",
    "scripts/run_site_task.py",
    "scripts/write_site_external_evidence_state.py",
    "scripts/render_tt_code_representation_status.py",
    "scripts/update_site_final_goal_status.py",
    "scripts/check_site_final_goal_status.py",
    "scripts/check_site_final_activation_pending.py",
]

REQUIRED_GUARD_DOC_TERMS = [
    "github/workflows/site-task-runner.yml",
    "python scripts/run_site_task.py task-elimination-guard",
    "python scripts/run_site_task.py local-completion-receipt",
    "local_manual_tasks: eliminated",
    "remaining_blocker: external_workflow_evidence",
]

REQUIRED_TASK_RUNNER_TERMS = [
    "def task_elimination_guard()",
    "def local_completion_receipt()",
    "scripts/check_site_manual_task_elimination.py",
    "scripts/check_site_ecosystem_management_handoff.py",
    "scripts/write_site_local_completion_receipt.py",
    "scripts/check_site_local_completion_receipt.py",
]

REQUIRED_WORKFLOW_TERMS = [
    "Site Task Runner",
    "task-elimination-guard",
    "local-completion-receipt",
    "python scripts/run_site_task.py",
]

REQUIRED_RECEIPT_CHECKER_TERMS = [
    "site_local_completion_receipt.v0.1",
    "pending_external_evidence",
    "does not activate the Site mirror",
]

REQUIRED_HANDOFF_TERMS = [
    "github/workflows/site-task-runner.yml",
    "scripts/run_site_task.py",
    "task-elimination-guard",
    "local-completion-receipt",
    "docs/SITE_MANUAL_TASK_ELIMINATION.md",
    "docs/SITE_TASK_ELIMINATION_GUARD.md",
    "pending_external_evidence",
]

FORBIDDEN_REQUIRED_PATHS = [
    ".github/workflows/site-autonomous-continuation.yml",
    ".github/workflows/site-task-elimination-guard.yml",
    ".github/workflows/site-local-completion-receipt.yml",
]


def read(path: Path) -> str:
    if not path.exists():
        print(f"missing file: {path.relative_to(ROOT)}", file=sys.stderr)
        raise SystemExit(1)
    return path.read_text(encoding="utf-8")


def missing(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term not in text]


def main() -> int:
    errors = []
    checks = [
        ("manual task document", read(DOC), REQUIRED_DOC_TERMS),
        ("guard document", read(GUARD_DOC), REQUIRED_GUARD_DOC_TERMS),
        ("task runner", read(TASK_RUNNER), REQUIRED_TASK_RUNNER_TERMS),
        ("task workflow", read(TASK_WORKFLOW), REQUIRED_WORKFLOW_TERMS),
        ("receipt checker", read(RECEIPT_CHECKER), REQUIRED_RECEIPT_CHECKER_TERMS),
        ("handoff", read(HANDOFF), REQUIRED_HANDOFF_TERMS),
    ]
    for label, text, terms in checks:
        miss = missing(text, terms)
        if miss:
            errors.append(f"{label} missing: " + ", ".join(miss))
    for rel in FORBIDDEN_REQUIRED_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"retired workflow should not remain active: {rel}")
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        return 1
    print("PASS: Site local continuation work is managed by consolidated declared tasks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
