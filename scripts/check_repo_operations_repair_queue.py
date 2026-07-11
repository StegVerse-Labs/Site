#!/usr/bin/env python3
"""Validate Repo Operations Center repair queue artifacts.

This validator is intentionally read-only. It checks queue shape and explicit
readiness language without approving, merging, or mutating any PR.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "repo-operations-repair-queue-v0.3.json"
READY = "THIS PR IS READY FOR REVIEW."
MERGE = "THIS PR IS READY FOR MERGE."
NOT_READY = "NOT READY FOR REVIEW."


def main() -> int:
    failures: list[str] = []
    if not QUEUE.exists():
        print("REPO OPS REPAIR QUEUE: FAIL")
        print(f"- missing {QUEUE.relative_to(ROOT)}")
        return 1

    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.repo_operations.repair_queue.v0.3":
        failures.append("schema_version mismatch")
    if data.get("status") != "classified_repair_queue_self_referenced":
        failures.append("status mismatch")

    boundary = data.get("authority_boundary", {})
    for key in (
        "auto_merge_enabled",
        "repo_mutation_from_monitor_enabled",
        "destructive_actions_allowed",
    ):
        if boundary.get(key) is not False:
            failures.append(f"authority boundary must be false: {key}")
    if boundary.get("requires_review_before_merge") is not True:
        failures.append("requires_review_before_merge must be true")

    ready_items = data.get("ready_for_review", [])
    not_ready_items = data.get("not_ready_for_review", [])
    if not isinstance(ready_items, list):
        failures.append("ready_for_review must be a list")
        ready_items = []
    if not isinstance(not_ready_items, list):
        failures.append("not_ready_for_review must be a list")
        not_ready_items = []

    seen: set[tuple[str, int]] = set()
    for section, expected in (
        ("ready_for_review", READY),
        ("not_ready_for_review", NOT_READY),
    ):
        for item in data.get(section, []):
            repo = item.get("repo")
            pr = item.get("pr")
            statement = item.get("status_statement")
            if not repo or not isinstance(pr, int):
                failures.append(f"{section} item missing repo/pr: {item}")
                continue
            key = (repo, pr)
            if key in seen:
                failures.append(f"duplicate PR entry: {repo}#{pr}")
            seen.add(key)
            if section == "ready_for_review" and statement not in {READY, MERGE}:
                failures.append(f"ready PR has invalid status statement: {repo}#{pr}")
            if section == "not_ready_for_review" and statement != expected:
                failures.append(f"not-ready PR has invalid status statement: {repo}#{pr}")

    print("REPO OPS REPAIR QUEUE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
