#!/usr/bin/env python3
"""Validate that Site local manual tasks are workflow-managed."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SITE_MANUAL_TASK_ELIMINATION.md"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
WORKFLOW = ROOT / ".github" / "workflows" / "site-autonomous-continuation.yml"

REQUIRED_DOC_TERMS = [
    "local_manual_tasks: eliminated",
    "local_continuation: workflow_managed",
    "activation_state: pending_external_evidence",
    "github/workflows/site-autonomous-continuation.yml",
    "scripts/write_site_external_evidence_state.py",
    "scripts/render_tt_code_representation_status.py",
    "scripts/update_site_final_goal_status.py",
    "scripts/check_site_final_goal_status.py",
    "scripts/check_site_final_activation_pending.py",
]

REQUIRED_WORKFLOW_TERMS = [
    "Build TT propagation bundle",
    "Render TT status",
    "Write external evidence state",
    "Update final goal status",
    "Validate final goal status",
    "Validate final activation boundary",
    "Commit autonomous continuation updates",
]

REQUIRED_HANDOFF_TERMS = [
    "github/workflows/site-autonomous-continuation.yml",
    "write external evidence state",
    "update final goal status",
    "pending_external_evidence",
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
        ("autonomous workflow", read(WORKFLOW), REQUIRED_WORKFLOW_TERMS),
        ("handoff", read(HANDOFF), REQUIRED_HANDOFF_TERMS),
    ]
    for label, text, terms in checks:
        miss = missing(text, terms)
        if miss:
            errors.append(f"{label} missing: " + ", ".join(miss))
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        return 1
    print("PASS: Site local manual tasks are workflow-managed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
