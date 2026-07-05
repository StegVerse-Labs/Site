#!/usr/bin/env python3
"""Verify AI Entry runtime design packet remains design-only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data" / "ai-entry-runtime-design-packet.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/LLM-adapter",
    "StegVerse-org/StegVerse-SDK",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RUNTIME_DESIGN_PACKET_FAIL: {message}")


def main() -> int:
    data = json.loads(PACKET.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.runtime_design_packet.v0.1":
        stop("bad schema version")
    if data.get("state") != "design_only":
        stop("state mismatch")
    if len(data.get("required_inputs", [])) < 7:
        stop("required inputs incomplete")
    surfaces = data.get("repo_surfaces", {})
    if set(surfaces) != EXPECTED_REPOS:
        stop("repo surface set mismatch")
    flags = data.get("readiness_flags", {})
    if not flags:
        stop("readiness flags missing")
    for key, value in flags.items():
        if value is not False:
            stop(f"{key} must be false")
    if data.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "runtime design schema fixtures":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_RUNTIME_DESIGN_PACKET_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
