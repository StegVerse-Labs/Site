#!/usr/bin/env python3
"""Persist finite Conectrr live-verification state from workflow reports."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION = ROOT / "reports" / "conectrr-live-verification.json"
BROWSER = ROOT / "reports" / "conectrr-remote-browser-verification.json"
STATUS = ROOT / "data" / "conectrr-live-status.json"
INVENTORY = ROOT / "data" / "conectrr-session-goal-inventory.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    checked_at = datetime.now(timezone.utc).isoformat()
    publication = load(PUBLICATION) if PUBLICATION.exists() else {}
    browser = load(BROWSER) if BROWSER.exists() else {}
    publication_passed = publication.get("passed") is True
    browser_passed = browser.get("passed") is True
    state = "COMPLETE" if publication_passed and browser_passed else "RETRY"
    payload = {
        "schema": "stegverse.conectrr.live-status.v1",
        "goal_id": "SV-SITE-CONECTRR-LIVE-001",
        "state": state,
        "monitoring_state": "MACHINE_OWNED",
        "checked_at": checked_at,
        "repository": os.environ.get("GITHUB_REPOSITORY", "StegVerse-Labs/Site"),
        "commit": os.environ.get("GITHUB_SHA"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "deployed_publication_passed": publication_passed,
        "remote_browser_execution_passed": browser_passed,
        "authority_effect": "none",
        "claims_not_created": ["live_external_interoperability", "custody", "admissibility", "execution_authority"],
        "next_executable_action": "admit_genuine_conectrr_output" if state == "COMPLETE" else "retry_after_pages_or_browser_propagation",
        "release_condition_satisfied": state == "COMPLETE",
    }
    STATUS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    inventory = load(INVENTORY)
    for claim in inventory.get("claims", []):
        if claim.get("task_id") == "SV-SITE-CONECTRR-LIVE-001":
            claim["state"] = state if state == "COMPLETE" else "MACHINE_OWNED"
            claim["monitoring_state"] = "MACHINE_OWNED"
            claim["last_checked_at"] = checked_at
            claim["evidence"] = "data/conectrr-live-status.json"
            claim["release_condition_satisfied"] = state == "COMPLETE"
            claim["next_task_after_release"] = payload["next_executable_action"]
    inventory["updated_at"] = checked_at
    blockers = inventory.setdefault("session_consolidation", {}).setdefault("archive_blockers", [])
    blockers[:] = [b for b in blockers if b != "remote-browser execution receipt unavailable"]
    INVENTORY.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")

    print(f"CONECTRR_LIVE_STATUS_UPDATE={state}")
    print(f"publication={publication_passed}")
    print(f"remote_browser={browser_passed}")
    print("authority_effect=none")
    return 0 if state == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
