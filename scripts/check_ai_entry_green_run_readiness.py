#!/usr/bin/env python3
"""Verify AI Entry validation includes all stabilization and closure checks before reading CI status."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGGREGATE = ROOT / "scripts" / "check_ecosystem_chat_ai_entry.py"
FULL = ROOT / "scripts" / "check_ecosystem_chat_ai_entry_full.py"

AGGREGATE_CHECKS = (
    "scripts/check_ecosystem_chat_backend.py",
    "scripts/check_ecosystem_chat_ui_route_priority.py",
    "scripts/check_ecosystem_chat_adapter_extension.py",
    "scripts/check_ai_entry_no_manual_tasks.py",
    "scripts/check_ai_entry_release_readiness.py",
    "scripts/check_ai_entry_validation_stabilization.py",
)

FULL_CHECKS = (
    "scripts/check_ai_entry_green_run_readiness.py",
    "scripts/check_ai_entry_workflow_parity.py",
    "scripts/check_ai_entry_workflow_commands.py",
    "scripts/check_ai_entry_automation_closure.py",
)

REQUIRED_FILES = (
    "fixtures/ecosystem-chat/route-precedence-cases.json",
    "data/ai-entry-release-readiness.json",
    "data/ai-entry-validation-stabilization.json",
    "data/ai-entry-workflow-parity.json",
    "data/ai-entry-automation-closure.json",
    "docs/AI_ENTRY_ROUTE_PRIORITY_STATUS.md",
    "docs/AI_ENTRY_ACTIONS_AUTO_RUN_STATUS.md",
    "SITE_MIRROR_HANDOFF.md",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_GREEN_RUN_READINESS_FAIL: {message}")


def require_markers(path: Path, markers: tuple[str, ...]) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            fail(f"{path.relative_to(ROOT)} missing {marker}")


def main() -> int:
    require_markers(AGGREGATE, AGGREGATE_CHECKS)
    require_markers(FULL, FULL_CHECKS)
    for rel_path in REQUIRED_FILES:
        if not (ROOT / rel_path).exists():
            fail(f"missing required file {rel_path}")
    print("AI_ENTRY_GREEN_RUN_READINESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
