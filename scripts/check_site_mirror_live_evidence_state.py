#!/usr/bin/env python3
"""Check the machine-readable Site mirror live evidence state.

The state file may remain pending while live activation evidence is missing.
If it claims activation, every required evidence field must contain real evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = REPO_ROOT / "docs" / "SITE_MIRROR_LIVE_EVIDENCE_STATE.json"

REQUIRED_TOP_LEVEL = [
    "schema",
    "generated_utc",
    "source_handoff",
    "goal",
    "repository",
    "source_repository",
    "source_path",
    "target_path",
    "activation_state",
    "live_activation_verified",
    "evidence",
    "completion_rule",
    "non_claims",
]

REQUIRED_EVIDENCE = [
    "publisher_dry_run_workflow_url",
    "publisher_dry_run_receipt_commit",
    "publisher_live_dispatch_workflow_url",
    "site_mirror_workflow_url",
    "site_mirror_commit_sha",
    "manifest_source_repository",
    "manifest_source_ref",
    "manifest_source_of_truth",
    "alias_verification_results",
    "publisher_receipt_update_commit",
    "publisher_verification_tracker_commit",
    "publisher_activation_status_update_commit",
]

REQUIRED_COMMANDS = [
    "python scripts/check_paper_display_policy.py",
    "python scripts/check_papers_manifest_metadata.py",
    "python scripts/check_paper_aliases.py",
    "python scripts/check_site_mirror_evidence_packet.py",
    "python scripts/check_site_mirror_live_evidence_state.py",
]

PENDING_VALUES = {"", "PENDING", "TODO", "TBD", "UNKNOWN", "null", "None"}


def fail(message: str) -> int:
    print(f"site mirror live evidence state check failed: {message}")
    return 1


def is_pending(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() in PENDING_VALUES
    return False


def main() -> int:
    if not STATE_PATH.exists():
        return fail("missing docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json")

    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    for key in REQUIRED_TOP_LEVEL:
        if key not in state:
            return fail(f"missing top-level key: {key}")

    if state["source_handoff"] != "docs/SITE_MIRROR_HANDOFF.md":
        return fail("source_handoff must be docs/SITE_MIRROR_HANDOFF.md")

    evidence = state["evidence"]
    if not isinstance(evidence, dict):
        return fail("evidence must be an object")

    for field in REQUIRED_EVIDENCE:
        if field not in evidence:
            return fail(f"missing evidence field: {field}")

    commands = state.get("completion_rule", {}).get("required_commands", [])
    for command in REQUIRED_COMMANDS:
        if command not in commands:
            return fail(f"missing completion command: {command}")

    activated = bool(state["live_activation_verified"])
    activation_state = str(state["activation_state"]).strip()
    pending_fields = [field for field in REQUIRED_EVIDENCE if is_pending(evidence[field])]

    if activated and activation_state != "activated":
        return fail("live_activation_verified true requires activation_state activated")

    if activated and pending_fields:
        return fail("live activation cannot be verified while fields remain pending: " + ", ".join(pending_fields))

    if not activated and activation_state == "activated":
        return fail("activation_state activated requires live_activation_verified true")

    if not activated:
        print("valid: Site mirror live evidence state pending")
        return 0

    print("valid: Site mirror live evidence state activated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
