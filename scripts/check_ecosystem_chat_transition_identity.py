#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "transition-identity.example.json"
IDENTITY_SCRIPT = ROOT / "assets" / "ecosystem-chat-transition-identity.js"
LOADER = ROOT / "assets" / "ecosystem-chat-hps.js"


def fail(message: str) -> int:
    print(f"ECOSYSTEM CHAT TRANSITION IDENTITY: FAIL - {message}")
    return 1


def main() -> int:
    for path in [FIXTURE, IDENTITY_SCRIPT, LOADER]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    record = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if record.get("record_type") != "governed_transition_relationship":
        return fail("record_type mismatch")
    if record.get("lifecycle_state") != "DECLARED":
        return fail("Site candidate must remain DECLARED")
    if record.get("origin", {}).get("origin_class") != "SITE_INPUT":
        return fail("origin_class must be SITE_INPUT")

    for key in ["transition_id", "run_id"]:
        if not record.get(key):
            return fail(f"missing {key}")
    for key in ["event_id", "origin_manifest_id"]:
        if not record.get("origin", {}).get(key):
            return fail(f"missing origin.{key}")

    relationships = record.get("relationships", {})
    if relationships.get("target_ref") != "repository:StegVerse-Labs/hybrid-collab-bridge":
        return fail("target_ref must be hybrid-collab-bridge")
    if relationships.get("repository_ref") != "StegVerse-Labs/Site":
        return fail("repository_ref drift")

    governance = record.get("governance", {})
    if governance.get("admissibility_result") != "PENDING":
        return fail("admissibility_result must remain PENDING")
    if governance.get("commit_time_validity") != "PENDING":
        return fail("commit_time_validity must remain PENDING")

    if record.get("execution", {}).get("action_ref") is not None:
        return fail("Site candidate must not claim action_ref")
    continuity = record.get("continuity", {})
    if continuity.get("final_receipt_id") is not None:
        return fail("Site candidate must not claim final receipt")
    if continuity.get("master_record_status") != "NOT_YET_SUBMITTED":
        return fail("master_record_status must be NOT_YET_SUBMITTED")
    if continuity.get("reconstruction_status") != "NOT_YET_CHECKED":
        return fail("reconstruction_status must be NOT_YET_CHECKED")

    preview = record.get("preview_payload", {})
    for key in ["raw_shell_allowed", "execution_authorized", "receipt_issued"]:
        if preview.get(key) is not False:
            return fail(f"preview_payload.{key} must be false")

    script = IDENTITY_SCRIPT.read_text(encoding="utf-8")
    for marker in [
        "transition_id",
        "run_id",
        "event_id",
        "origin_manifest_id",
        "SITE_INPUT",
        "governed_transition_relationship",
        "NOT_YET_SUBMITTED",
        "NOT_YET_CHECKED",
        "execution_authorized: false",
        "receipt_issued: false",
    ]:
        if marker not in script:
            return fail(f"identity module missing marker: {marker}")

    loader = LOADER.read_text(encoding="utf-8")
    if "assets/ecosystem-chat-transition-identity.js" not in loader:
        return fail("identity module is not loaded by ecosystem-chat-hps.js")

    print("ECOSYSTEM CHAT TRANSITION IDENTITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
