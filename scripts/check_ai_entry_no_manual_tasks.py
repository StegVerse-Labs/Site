#!/usr/bin/env python3
"""Verify AI Entry validation is wired so no manual verification task is required."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".github" / "workflows" / "validate.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate.yml"
AGGREGATE = ROOT / "scripts" / "check_ecosystem_chat_ai_entry.py"
STATUS = ROOT / "docs" / "AI_ENTRY_CONTRACT_SYNC_RUN_STATUS.md"
HANDOFF = ROOT / "SITE_MIRROR_HANDOFF.md"

REQUIRED_STANDARD = "python scripts/check_ecosystem_chat_ai_entry.py"
REQUIRED_FULL = "python scripts/check_ecosystem_chat_ai_entry_full.py"


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_NO_MANUAL_TASKS_FAIL: {message}")


def require_text(path: Path, markers: tuple[str, ...]) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            fail(f"{path.relative_to(ROOT)} missing {marker}")
    return text


def require_any_text(path: Path, markers: tuple[str, ...]) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    if not any(marker in text for marker in markers):
        fail(f"{path.relative_to(ROOT)} missing one of: {', '.join(markers)}")


def require_workflow_command(path: Path) -> None:
    text = require_text(path, ("workflow_dispatch",))
    if REQUIRED_STANDARD not in text and REQUIRED_FULL not in text:
        fail(f"{path.relative_to(ROOT)} missing supported AI Entry validation command")


def main() -> int:
    require_text(AGGREGATE, ("check_ecosystem_chat_adapter_extension.py", "ECOSYSTEM_CHAT_AI_ENTRY_PASS"))
    require_workflow_command(CANONICAL)
    require_workflow_command(MIRROR)
    require_text(STATUS, ("installation_complete == true", "workflow_run_confirmed == false"))
    require_text(HANDOFF, ("None for Site-side AI Entry contract sync", "Archive posture"))
    require_any_text(HANDOFF, ("complete thread can be archived", "Complete thread can be archived"))
    print("AI_ENTRY_NO_MANUAL_TASKS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
