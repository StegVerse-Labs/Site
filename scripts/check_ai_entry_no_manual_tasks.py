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

REQUIRED = "python scripts/check_ecosystem_chat_ai_entry.py"


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_NO_MANUAL_TASKS_FAIL: {message}")


def require_text(path: Path, markers: tuple[str, ...]) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            fail(f"{path.relative_to(ROOT)} missing {marker}")


def main() -> int:
    require_text(AGGREGATE, ("check_ecosystem_chat_adapter_extension.py", "ECOSYSTEM_CHAT_AI_ENTRY_PASS"))
    require_text(CANONICAL, (REQUIRED, "workflow_dispatch"))
    require_text(MIRROR, (REQUIRED, "workflow_dispatch"))
    require_text(STATUS, ("installation_complete == true", "workflow_run_confirmed == false"))
    require_text(HANDOFF, ("None for Site-side AI Entry contract sync", "Complete thread can be archived"))
    print("AI_ENTRY_NO_MANUAL_TASKS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
