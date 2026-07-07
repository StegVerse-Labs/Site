#!/usr/bin/env python3
"""Verify AI Entry workflow validators accept current supported commands.

This checker intentionally reads the validation command contract instead of
requiring every historical command string to appear in every guard. That keeps
workflow consolidation from creating one-validator-at-a-time failures.
"""
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


def require_list(data: dict, key: str, *, minimum: int = 1) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < minimum or not all(isinstance(item, str) and item for item in value):
        stop(f"{key} must be a non-empty string list")
    return value


def require_any_marker(text: str, markers: list[str], label: str) -> None:
    if not any(marker in text for marker in markers):
        stop(f"{label} lacks accepted validation command")


def require_all_markers(text: str, markers: list[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        stop(f"{label} missing compatibility marker: {missing[0]}")


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") not in {
        "stegverse.ai_entry.supported_validation_commands.v0.1",
        "stegverse.ai_entry.supported_validation_commands.v0.2",
    }:
        stop("bad schema version")

    supported_commands = require_list(data, "supported_commands", minimum=3)
    accepted_workflow_commands = data.get("accepted_workflow_commands") or supported_commands
    if not isinstance(accepted_workflow_commands, list):
        stop("accepted_workflow_commands must be a list")
    accepted_workflow_commands = [str(command) for command in accepted_workflow_commands]

    workflow_text = CANONICAL.read_text(encoding="utf-8")
    mirror_text = MIRROR.read_text(encoding="utf-8")
    guard_text = NO_MANUAL.read_text(encoding="utf-8")

    require_any_marker(workflow_text, accepted_workflow_commands, "canonical workflow")
    require_any_marker(mirror_text, accepted_workflow_commands, "mirror workflow")

    guard_markers = data.get("accepted_guard_markers")
    if guard_markers is None:
        # v0.1 fallback: guards must show registry-driven validation, not each
        # legacy command literal.
        guard_markers = [
            "REGISTRY = ROOT / \"data\" / \"ai-entry-supported-validation-commands.json\"",
            "supported_commands = registry.get(\"supported_commands\", [])",
            "require_workflow_command(CANONICAL, supported_commands)",
            "require_workflow_command(MIRROR, supported_commands)",
        ]
    if not isinstance(guard_markers, list) or not all(isinstance(item, str) and item for item in guard_markers):
        stop("accepted_guard_markers must be a non-empty string list")
    require_all_markers(guard_text, guard_markers, "no-manual guard")

    if data.get("canonical_validation_command") and data.get("canonical_validation_command") not in supported_commands:
        stop("canonical validation command must be supported")
    if data.get("legacy_validation_commands"):
        legacy = data.get("legacy_validation_commands")
        if not isinstance(legacy, list) or not set(legacy).issubset(set(supported_commands)):
            stop("legacy validation commands must be supported")

    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "rerun validation confirmation":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_SUPPORTED_VALIDATION_COMMANDS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
