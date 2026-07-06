#!/usr/bin/env python3
"""Verify AI Entry validation is wired so no manual verification task is required."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".github" / "workflows" / "validate.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate.yml"
AGGREGATE = ROOT / "scripts" / "check_ecosystem_chat_ai_entry.py"
STATUS = ROOT / "docs" / "AI_ENTRY_CONTRACT_SYNC_RUN_STATUS.md"
HANDOFF = ROOT / "SITE_MIRROR_HANDOFF.md"
CLOSURE = ROOT / "data" / "ai-entry-no-manual-closure.json"
REGISTRY = ROOT / "data" / "ai-entry-supported-validation-commands.json"


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


def require_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_workflow_command(path: Path, supported_commands: list[str]) -> None:
    text = require_text(path, ("workflow_dispatch",))
    if not any(command in text for command in supported_commands):
        fail(f"{path.relative_to(ROOT)} missing supported AI Entry validation command")


def main() -> int:
    registry = require_json(REGISTRY)
    supported_commands = registry.get("supported_commands", [])
    if len(supported_commands) < 3:
        fail("supported validation command registry incomplete")

    closure = require_json(CLOSURE)
    if closure.get("manual_tasks_remaining") != []:
        fail("manual tasks must remain empty in closure state")
    if closure.get("archive_ready") is not True:
        fail("closure state must be archive ready")

    require_text(AGGREGATE, ("check_ecosystem_chat_adapter_extension.py", "ECOSYSTEM_CHAT_AI_ENTRY_PASS"))
    require_workflow_command(CANONICAL, supported_commands)
    require_workflow_command(MIRROR, supported_commands)
    require_text(STATUS, ("installation_complete == true", "workflow_run_confirmed == false"))
    require_text(HANDOFF, ("Archive posture",))
    print("AI_ENTRY_NO_MANUAL_TASKS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
