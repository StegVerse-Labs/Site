#!/usr/bin/env python3
"""Verify AI Entry cross-repo promotion record remains non-green until visible runs exist."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "ai-entry-cross-repo-promotion-record.json"
REFRESH = ROOT / "data" / "ai-entry-visibility-refresh-index.json"
EVIDENCE_SCHEMA = ROOT / "data" / "ai-entry-visible-run-evidence-schema.json"
EXPECTED_REPOS = {
    "StegVerse-Labs/Site",
    "StegVerse-org/StegVerse-SDK",
    "StegVerse-org/LLM-adapter",
}
REQUIRED_EVIDENCE_FIELDS = {
    "repo",
    "commit_sha",
    "workflow_name",
    "run_id",
    "conclusion",
    "checked_at",
    "source",
}


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_CROSS_REPO_PROMOTION_RECORD_FAIL: {message}")


def require_non_green_repo_map(repos: dict, ready_field: str) -> None:
    if set(repos) != EXPECTED_REPOS:
        stop("repo set mismatch")
    for repo, status in repos.items():
        if ready_field in status and status.get(ready_field) is not False:
            stop(f"{repo} {ready_field} must be false")
        if status.get("visible_run") is not False:
            stop(f"{repo} visible_run must be false")


def main() -> int:
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.cross_repo_promotion_record.v0.1":
        stop("bad schema version")
    if data.get("state") != "promotion_recorded_not_green":
        stop("state mismatch")
    require_non_green_repo_map(data.get("repos", {}), "promotion_ready")
    for key in ("green_data_promotion", "tag_ready", "live_activation_ready"):
        if data.get(key) is not False:
            stop(f"{key} must be false")
    refresh = json.loads(REFRESH.read_text(encoding="utf-8"))
    if refresh.get("schema_version") != "stegverse.ai_entry.visibility_refresh_index.v0.1":
        stop("bad refresh schema version")
    if refresh.get("state") != "refresh_index_recorded_not_green":
        stop("refresh state mismatch")
    require_non_green_repo_map(refresh.get("tracked_repos", {}), "promotion_ready")
    if refresh.get("promotion_allowed") is not False or refresh.get("tag_allowed") is not False:
        stop("refresh cannot allow promotion or tag")
    evidence_schema = json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
    if evidence_schema.get("schema_version") != "stegverse.ai_entry.visible_run_evidence_schema.v0.1":
        stop("bad evidence schema version")
    if set(evidence_schema.get("tracked_repos", [])) != EXPECTED_REPOS:
        stop("evidence tracked repo mismatch")
    if set(evidence_schema.get("required_fields", [])) != REQUIRED_EVIDENCE_FIELDS:
        stop("evidence field mismatch")
    if evidence_schema.get("allowed_conclusions") != ["success"]:
        stop("evidence conclusion mismatch")
    for key in ("evidence_claimed", "promotion_allowed", "tag_allowed"):
        if evidence_schema.get(key) is not False:
            stop(f"evidence schema {key} must be false")
    if data.get("manual_tasks_remaining") != [] or refresh.get("manual_tasks_remaining") != [] or evidence_schema.get("manual_tasks_remaining") != []:
        stop("manual tasks must remain empty")
    if data.get("next_goal_candidate") != "cross-repo promotion verifier":
        stop("next goal candidate mismatch")
    print("AI_ENTRY_CROSS_REPO_PROMOTION_RECORD_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
