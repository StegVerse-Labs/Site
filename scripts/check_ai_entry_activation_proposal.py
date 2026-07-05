#!/usr/bin/env python3
"""Verify AI Entry activation proposal remains green-data dependent."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "data" / "ai-entry-activation-proposal.json"
FALSE_READY = (
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
    raise SystemExit(f"AI_ENTRY_ACTIVATION_PROPOSAL_FAIL: {message}")


def main() -> int:
    data = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.activation_proposal.v0.1":
        stop("bad schema version")
    if data.get("state") != "proposal_only_waiting_for_green_data":
        stop("state mismatch")
    inputs = data.get("proposal_inputs", {})
    if inputs.get("runtime_design_complete") is not True:
        stop("runtime design complete must be true")
    if inputs.get("runtime_design_not_ready") is not True:
        stop("runtime design not-ready must be true")
    if inputs.get("visible_green_data") is not False:
        stop("visible green data must be false")
    if inputs.get("tag_gate_ready") is not False:
        stop("tag gate ready must be false")
    if len(data.get("proposal_steps", [])) < 4:
        stop("proposal steps incomplete")
    readiness = data.get("current_readiness", {})
    for key in FALSE_READY:
        if readiness.get(key) is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "proposal completion index":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_ACTIVATION_PROPOSAL_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
