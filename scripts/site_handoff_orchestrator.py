#!/usr/bin/env python3
"""Fail-closed handoff-driven workload reconciliation for StegVerse-Labs/Site."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
STATE = ROOT / "data" / "site-orchestration-state.json"
REPORT = ROOT / "site_handoff_orchestration.report.json"
RETIREMENT_VALIDATOR = ROOT / "scripts" / "check_session_retirement.py"
RETIREMENT_REPORT = ROOT / "session_retirement.report.json"
REPO = os.getenv("GITHUB_REPOSITORY", "StegVerse-Labs/Site")
API = os.getenv("GITHUB_API_URL", "https://api.github.com")
TOKEN = os.getenv("GITHUB_TOKEN", "")


def api(path: str) -> Any:
    request = urllib.request.Request(
        f"{API}/repos/{REPO}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "site-handoff-orchestrator",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_remaining_work(text: str) -> list[dict[str, str]]:
    section = text.split("## Remaining work", 1)[1].split("## ", 1)[0]
    destination = ""
    items: list[dict[str, str]] = []
    in_fence = False
    for raw in section.splitlines():
        line = raw.strip()
        match = re.match(r"Destination `([^`]+)`:", line)
        if match:
            destination = match.group(1)
            continue
        if line.startswith("Downstream destinations"):
            destination = "DOWNSTREAM_AFTER_SITE_ACTIVATION"
            continue
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and line:
            items.append({"destination": destination or REPO, "workload": line})
    return items


def normalized(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 3 and token not in {"site", "work", "issue", "task", "with", "from", "into"}
    }


def overlaps(title: str, workload: str) -> bool:
    left, right = normalized(title), normalized(workload)
    return len(left & right) >= 2


def validate_retirement_state(failures: list[str]) -> dict[str, Any]:
    """Run the canonical retirement validator and consume its report fail-closed."""
    if not RETIREMENT_VALIDATOR.exists():
        failures.append("missing scripts/check_session_retirement.py")
        return {"status": "FAIL", "failures": ["validator missing"]}

    result = subprocess.run(
        [sys.executable, str(RETIREMENT_VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if not RETIREMENT_REPORT.exists():
        failures.append("session retirement validator produced no report")
        return {
            "status": "FAIL",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "failures": ["report missing"],
        }

    try:
        retirement = json.loads(RETIREMENT_REPORT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"session retirement report invalid JSON: {exc}")
        return {"status": "FAIL", "failures": [f"invalid report JSON: {exc}"]}

    retirement["returncode"] = result.returncode
    retirement["stdout"] = result.stdout.strip()
    retirement["stderr"] = result.stderr.strip()
    if result.returncode != 0 or retirement.get("status") != "PASS":
        failures.append("session retirement validation failed")
    return retirement


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        failures.append("missing docs/SITE_MIRROR_HANDOFF.md")
    if not STATE.exists():
        failures.append("missing data/site-orchestration-state.json")
    if failures:
        REPORT.write_text(json.dumps({"status": "FAIL", "failures": failures}, indent=2) + "\n")
        print("SITE_HANDOFF_ORCHESTRATION_FAIL")
        return 1

    handoff = HANDOFF.read_text(encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    required = [
        "This file is the current handoff and task source of truth",
        "## Remaining work",
        "## Machine-owned continuation",
        "Manual user action required for routine repository work: false",
    ]
    failures.extend(f"handoff missing marker: {marker}" for marker in required if marker not in handoff)
    if state.get("status") != "ACTIVE":
        failures.append("orchestration state is not ACTIVE")

    retirement_validation = validate_retirement_state(failures)
    workloads = extract_remaining_work(handoff)
    open_issues: list[dict[str, Any]] = []
    open_prs: list[dict[str, Any]] = []
    branches: list[dict[str, Any]] = []
    live_inventory = False
    if TOKEN:
        try:
            issue_rows = api("/issues?state=open&per_page=100")
            open_issues = [row for row in issue_rows if "pull_request" not in row]
            open_prs = [row for row in issue_rows if "pull_request" in row]
            branches = api("/branches?per_page=100")
            live_inventory = True
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            failures.append(f"GitHub inventory failed: {exc}")

    assignments = []
    duplicate_groups = []
    for workload in workloads:
        matches = [
            {"number": item["number"], "title": item["title"], "url": item["html_url"]}
            for item in [*open_issues, *open_prs]
            if overlaps(item.get("title", ""), workload["workload"])
        ]
        assignments.append({**workload, "matching_open_work": matches})
        if len(matches) > 1:
            duplicate_groups.append({**workload, "matches": matches})

    event = os.getenv("GITHUB_EVENT_NAME", "local")
    ref_name = os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME", "")
    if event == "pull_request" and ref_name and ref_name != "main":
        branch_tokens = normalized(ref_name.replace("/", " ").replace("-", " "))
        owns_declared_work = any(branch_tokens & normalized(item["workload"]) for item in workloads)
        if not owns_declared_work and "orchestrat" not in ref_name.lower() and "handoff" not in ref_name.lower():
            failures.append("pull request does not map to an unfinished handoff workload")

    if duplicate_groups:
        failures.append("multiple open work items appear to own the same handoff workload")

    report = {
        "schema_version": "1.1.0",
        "status_type": "site_handoff_orchestration_report",
        "status": "FAIL" if failures else "PASS",
        "repository": REPO,
        "handoff": str(HANDOFF.relative_to(ROOT)),
        "handoff_workload_count": len(workloads),
        "live_inventory": live_inventory,
        "open_issue_count": len(open_issues),
        "open_pr_count": len(open_prs),
        "branch_count_first_page": len(branches),
        "retirement_validation": retirement_validation,
        "assignments": assignments,
        "duplicate_groups": duplicate_groups,
        "failures": failures,
        "next_action": (
            "repair retirement state or reconcile existing handoff workloads and duplicate owners"
            if failures
            else "continue the highest-priority unfinished handoff workload"
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"SITE_HANDOFF_ORCHESTRATION_{report['status']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
