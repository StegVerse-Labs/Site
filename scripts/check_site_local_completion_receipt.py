#!/usr/bin/env python3
"""Validate Site local completion receipt outputs."""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_MD = ROOT / "docs" / "SITE_LOCAL_COMPLETION_RECEIPT.md"
RECEIPT_JSON = ROOT / "docs" / "SITE_LOCAL_COMPLETION_RECEIPT.json"
WRITER = ROOT / "scripts" / "write_site_local_completion_receipt.py"
TASK_RUNNER = ROOT / "scripts" / "run_site_task.py"
VALIDATE_WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
TASK_WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"

REQUIRED_JSON_KEYS = {
    "schema",
    "repository",
    "generated_at",
    "local_completion_state",
    "activation_state",
    "workflow_surface",
    "active_workflows",
    "artifacts",
    "missing",
    "non_claims",
}

REQUIRED_MD_TERMS = {
    "# Site Local Completion Receipt",
    "local_completion_state:",
    "activation_state: pending_external_evidence",
    "workflow_surface: consolidated_two_workflow_surface",
    "This receipt confirms local repository-managed continuation surfaces exist.",
    "does not activate the Site mirror",
    "does not grant commit-time permission",
}

REQUIRED_TASK_TERMS = {
    "local-completion-receipt",
    "write_site_local_completion_receipt.py",
    "check_site_local_completion_receipt.py",
}

REQUIRED_WORKFLOW_TERMS = {
    "Site Task Runner",
    "python scripts/run_site_task.py",
    "local-completion-receipt",
}

FORBIDDEN_TERMS = {
    "activation_state: activated",
    "local_completion_state: activated",
    "grants commit-time permission",
    "Site is proof authority",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    md = read(RECEIPT_MD)
    raw = read(RECEIPT_JSON)
    writer = read(WRITER)
    task_runner = read(TASK_RUNNER)
    validate_workflow = read(VALIDATE_WORKFLOW)
    task_workflow = read(TASK_WORKFLOW)
    data = json.loads(raw)

    missing_keys = sorted(REQUIRED_JSON_KEYS - set(data))
    if missing_keys:
        fail("receipt JSON missing keys: " + ", ".join(missing_keys))

    if data.get("schema") != "site_local_completion_receipt.v0.1":
        fail("receipt schema mismatch")
    if data.get("repository") != "StegVerse-Labs/Site":
        fail("receipt repository mismatch")
    if data.get("activation_state") != "pending_external_evidence":
        fail("receipt activation state must remain pending_external_evidence")
    if data.get("workflow_surface") != "consolidated_two_workflow_surface":
        fail("receipt workflow surface must reference consolidated two-workflow state")
    if data.get("local_completion_state") not in {"complete", "incomplete"}:
        fail("invalid local_completion_state")
    if not isinstance(data.get("artifacts"), list):
        fail("artifacts must be a list")
    if data.get("active_workflows") != [".github/workflows/validate.yml", ".github/workflows/site-task-runner.yml"]:
        fail("active workflow list must match consolidated Site workflow surface")
    if data.get("local_completion_state") == "complete" and data.get("missing"):
        fail("complete receipt cannot have missing artifacts")

    for term in REQUIRED_MD_TERMS:
        if term not in md:
            fail(f"receipt markdown missing term: {term}")
    for term in REQUIRED_TASK_TERMS:
        if term not in task_runner:
            fail(f"task runner missing term: {term}")
    for term in REQUIRED_WORKFLOW_TERMS:
        if term not in task_workflow:
            fail(f"task workflow missing term: {term}")
    if "Site Bootstrap Validate" not in validate_workflow:
        fail("validate workflow missing bootstrap name")
    if "site_local_completion_receipt.v0.1" not in writer:
        fail("receipt writer missing schema marker")

    combined = md + "\n" + raw
    for term in FORBIDDEN_TERMS:
        if term in combined:
            fail(f"forbidden receipt term present: {term}")

    print("PASS: Site local completion receipt is valid and non-authorizing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
