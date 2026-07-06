#!/usr/bin/env python3
"""Verify AI Entry workflow validators accept current supported commands."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ai-entry-supported-validation-commands.json"
CANONICAL = ROOT / ".github" / "workflows" / "validate.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate.yml"
NO_MANUAL = ROOT / "scripts" / "check_ai_entry_no_manual_tasks.py"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_SUPPORTED_VALIDATION_COMMANDS_FAIL: {message}")


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.supported_validation_commands.v0.1":
        stop("bad schema version")
    commands = data.get("supported_commands", [])
    if len(commands) < 3:
        stop("supported command list incomplete")
    workflow_text = CANONICAL.read_text(encoding="utf-8")
    mirror_text = MIRROR.read_text(encoding="utf-8")
    guard_text = NO_MANUAL.read_text(encoding="utf-8")
    if not any(command in workflow_text for command in commands):
        stop("canonical workflow lacks supported command")
    if not any(command in mirror_text for command in commands):
        stop("mirror workflow lacks supported command")
    for command in commands:
        if command not in guard_text:
            stop(f"guard missing {command}")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "rerun validation confirmation":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_SUPPORTED_VALIDATION_COMMANDS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
