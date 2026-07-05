#!/usr/bin/env python3
"""Verify AI Entry runtime design completion index remains not-ready."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-runtime-design-completion.json"
COMPLETED = (
    "runtime_design_packet",
    "runtime_design_packet_verifier",
    "runtime_design_request_fixture",
    "runtime_design_response_fixture",
    "runtime_design_fixture_verifier",
    "site_validation_wired",
)


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RUNTIME_DESIGN_COMPLETION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.runtime_design_completion.v0.1":
        stop("bad schema version")
    if data.get("state") != "design_complete_not_ready":
        stop("state mismatch")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            stop(f"{key} must be true")
    flags = data.get("readiness_flags", {})
    if not flags:
        stop("readiness flags missing")
    for key, value in flags.items():
        if value is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "green-data-dependent activation proposal":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_RUNTIME_DESIGN_COMPLETION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
