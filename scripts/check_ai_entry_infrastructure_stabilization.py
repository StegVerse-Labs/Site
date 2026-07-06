#!/usr/bin/env python3
"""Verify AI Entry infrastructure stabilization record."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "ai-entry-infrastructure-stabilization.json"
NO_MANUAL = ROOT / "scripts" / "check_ai_entry_no_manual_tasks.py"


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_INFRASTRUCTURE_STABILIZATION_FAIL: {message}")


def main() -> int:
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.infrastructure_stabilization.v0.1":
        stop("bad schema version")
    if data.get("state") != "patched_pending_visible_rerun":
        stop("state mismatch")
    site_fix = data.get("site_fix", {})
    if site_fix.get("brittle_handoff_prose_removed") is not True:
        stop("site prose fix not recorded")
    if site_fix.get("structured_no_manual_state_checked") is not True:
        stop("structured state check not recorded")
    guard_text = NO_MANUAL.read_text(encoding="utf-8")
    if "None for Site-side AI Entry contract sync" in guard_text:
        stop("brittle handoff prose dependency still present")
    if "ai-entry-no-manual-closure.json" not in guard_text:
        stop("structured closure state not checked")
    sdk_fix = data.get("sdk_fix", {})
    if sdk_fix.get("demo_packet_session_argument_supplied") is not True:
        stop("sdk session argument fix not recorded")
    if sdk_fix.get("demo_session_fixture_present") is not True:
        stop("sdk fixture fix not recorded")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "infrastructure stabilization verification":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_INFRASTRUCTURE_STABILIZATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
