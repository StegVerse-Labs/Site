#!/usr/bin/env python3
"""Validate the fail-closed current-main Site validation evidence record."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "data" / "site-current-main-validation-evidence.json"
ALLOWED_STATES = {"UNOBSERVED", "VERIFIED", "FAILED"}
REQUIRED_EVIDENCE_FIELDS = {
    "commit_sha",
    "workflow_run_id",
    "workflow_name",
    "job_name",
    "conclusion",
    "validated_at",
    "result_artifact",
    "result_hash",
}


def fail(message: str) -> None:
    raise SystemExit(f"SITE_CURRENT_MAIN_VALIDATION_EVIDENCE_FAIL: {message}")


def main() -> int:
    payload = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))

    if payload.get("schema") != "stegverse.site.current_main_validation_evidence.v1":
        fail("schema drift")
    if payload.get("repository") != "StegVerse-Labs/Site" or payload.get("branch") != "main":
        fail("repository or branch drift")
    if payload.get("required_validation_command") != "python scripts/check_ecosystem_chat_application.py":
        fail("canonical validation command drift")

    workflows = set(payload.get("required_workflows", []))
    expected_workflows = {
        ".github/workflows/validate.yml",
        ".github/workflows/site-task-runner.yml",
    }
    if workflows != expected_workflows:
        fail("declared workflow set drift")

    state = payload.get("state")
    if state not in ALLOWED_STATES:
        fail("invalid state")

    evidence = payload.get("evidence", {})
    if set(evidence) != REQUIRED_EVIDENCE_FIELDS:
        fail("evidence field set drift")

    rule = payload.get("verification_rule", {})
    expected_rule = {
        "verified_state": "VERIFIED",
        "all_evidence_fields_required": True,
        "conclusion_must_equal": "success",
        "commit_must_be_current_main": True,
        "validator_output_must_equal": "ECOSYSTEM_CHAT_APPLICATION_PASS",
        "workflow_identity_must_match_declared_workflow": True,
    }
    for key, expected in expected_rule.items():
        if rule.get(key) != expected:
            fail(f"verification rule drift: {key}")

    boundaries = payload.get("authority_boundaries", {})
    if not boundaries or any(value is not False for value in boundaries.values()):
        fail("authority boundary exceeded")

    populated = {key: value for key, value in evidence.items() if value not in (None, "")}
    blockers = payload.get("current_blockers", [])

    if state == "UNOBSERVED":
        if populated:
            fail("unobserved state contains asserted workflow evidence")
        required_blockers = {
            "CURRENT_MAIN_WORKFLOW_RUN_UNOBSERVED",
            "VALIDATION_RECEIPT_UNOBSERVED",
        }
        if not required_blockers.issubset(set(blockers)):
            fail("unobserved blockers missing")
    elif state == "VERIFIED":
        if len(populated) != len(REQUIRED_EVIDENCE_FIELDS):
            fail("verified state requires complete evidence")
        if evidence.get("conclusion") != "success":
            fail("verified state requires success conclusion")
        if blockers:
            fail("verified state may not retain blockers")
        sha = str(evidence.get("commit_sha", ""))
        if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha.lower()):
            fail("verified commit SHA invalid")
        if not isinstance(evidence.get("workflow_run_id"), int) or evidence["workflow_run_id"] <= 0:
            fail("verified workflow run ID invalid")
        result_hash = str(evidence.get("result_hash", ""))
        if not result_hash.startswith("sha256:") or len(result_hash) != 71:
            fail("verified result hash invalid")
    else:
        if not populated:
            fail("failed state requires observed failure evidence")
        if evidence.get("conclusion") == "success":
            fail("failed state may not claim success")
        if not blockers:
            fail("failed state requires blockers")

    print(f"SITE_CURRENT_MAIN_VALIDATION_EVIDENCE_PASS state={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
