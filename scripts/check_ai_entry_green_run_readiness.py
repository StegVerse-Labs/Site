#!/usr/bin/env python3
"""Verify AI Entry aggregate includes all stabilization checks needed before reading CI status."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGGREGATE = ROOT / "scripts" / "check_ecosystem_chat_ai_entry.py"

REQUIRED_CHECKS = (
    "scripts/check_ecosystem_chat_backend.py",
    "scripts/check_ecosystem_chat_ui_route_priority.py",
    "scripts/check_ecosystem_chat_adapter_extension.py",
    "scripts/check_ai_entry_no_manual_tasks.py",
    "scripts/check_ai_entry_release_readiness.py",
    "scripts/check_ai_entry_validation_stabilization.py",
)

REQUIRED_FILES = (
    "fixtures/ecosystem-chat/route-precedence-cases.json",
    "data/ai-entry-release-readiness.json",
    "data/ai-entry-validation-stabilization.json",
    "docs/AI_ENTRY_ROUTE_PRIORITY_STATUS.md",
    "docs/AI_ENTRY_ACTIONS_AUTO_RUN_STATUS.md",
)


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_GREEN_RUN_READINESS_FAIL: {message}")


def main() -> int:
    if not AGGREGATE.exists():
        fail("missing aggregate verifier")
    text = AGGREGATE.read_text(encoding="utf-8")
    for check in REQUIRED_CHECKS:
        if check not in text:
            fail(f"aggregate missing {check}")
    for rel_path in REQUIRED_FILES:
        if not (ROOT / rel_path).exists():
            fail(f"missing required file {rel_path}")
    print("AI_ENTRY_GREEN_RUN_READINESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
