#!/usr/bin/env python3
"""Verify AI Entry proposal completion remains blocked on green data."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-proposal-completion.json"
COMPLETED = (
    "proposal_packet",
    "proposal_verifier",
    "green_data_packet_alias",
    "site_validation_wired",
)
FALSE_KEYS = (
    "provider_ready",
    "sdk_ready",
    "credential_ready",
    "authority_ready",
    "receipt_ready",
    "activation_ready",
    "execution_ready",
    "repo_write_ready",
)


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_PROPOSAL_COMPLETION_FAIL: {message}")


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.proposal_completion.v0.1":
        stop("bad schema version")
    if data.get("state") != "proposal_complete_waiting_for_green_data":
        stop("state mismatch")
    completed = data.get("completed_components", {})
    for key in COMPLETED:
        if completed.get(key) is not True:
            stop(f"{key} must be true")
    blocked = data.get("blocked_inputs", {})
    if blocked.get("visible_green_data") is not False:
        stop("visible green data must be false")
    if blocked.get("tag_gate_ready") is not False:
        stop("tag gate ready must be false")
    readiness = data.get("current_readiness", {})
    for key in FALSE_KEYS:
        if readiness.get(key) is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "final no-manual-task closure":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_PROPOSAL_COMPLETION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
