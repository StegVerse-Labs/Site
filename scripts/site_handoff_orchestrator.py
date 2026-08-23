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

from check_session_work_claims import load_registry

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
STATE = ROOT / "data" / "site-orchestration-state.json"
REPORT = ROOT / "site_handoff_orchestration.report.json"
RETIREMENT_VALIDATOR = ROOT / "scripts" / "check_session_retirement.py"
RETIREMENT_REPORT = ROOT / "session_retirement.report.json"
CLAIM_VALIDATOR = ROOT / "scripts" / "check_session_work_claims.py"
CLAIM_REPORT = ROOT / "session_work_claims.report.json"
ACTIVE_CLAIM_STATES = {"CLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED"}
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


def run_validator(path: Path, report_path: Path, label: str, failures: list[str]) -> dict[str, Any]:
    """Run a repository validator and consume its machine report fail-closed."""
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return {"status": "FAIL", "failures": ["validator missing"]}
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if not report_path.exists():
        failures.append(f"{label} validator produced no report")
        return {
            "status": "FAIL",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "failures": ["report missing"],
        }
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"{label} report invalid JSON: {exc}")
        return {"status": "FAIL", "failures": [f"invalid report JSON: {exc}"]}
    report["returncode"] = result.returncode
    report["stdout"] = result.stdout.strip()
    report["stderr"] = result.stderr.strip()
    if result.returncode != 0 or report.get("status") != "PASS":
        failures.append(f"{label} validation failed")
    return report


def active_branch_claims() -> list[dict[str, Any]]:
    try:
        registry = load_registry()
    except (OSError, ValueError, json.JSONDecodeError):
        return []
    return [claim for claim in registry.get("claims", []) if claim.get("state") in ACTIVE_CLAIM_STATES]


def claim_handoff_exists(claim: dict[str, Any]) -> bool:
    handoff_ref = claim.get("handoff")
    if not isinstance(handoff_ref, str) or not handoff_ref:
        return False
    path = (ROOT / handoff_ref).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return False
    return path.is_file()


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

    retirement_validation = run_validator(RETIREMENT_VALIDATOR, RETIREMENT_REPORT, "session retirement", failures)
    claim_validation = run_validator(CLAIM_VALIDATOR, CLAIM_REPORT, "session pre-work claims", failures)

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
    possible_overlap_groups = []
    for workload in workloads:
        matches = [
            {"number": item["number"], "title": item["title"], "url": item["html_url"]}
            for item in [*open_issues, *open_prs]
            if overlaps(item.get("title", ""), workload["workload"])
        ]
        assignments.append({**workload, "matching_open_work": matches})
        if len(matches) > 1:
            possible_overlap_groups.append({**workload, "matches": matches})

    event = os.getenv("GITHUB_EVENT_NAME", "local")
    ref_name = os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME", "")
    branch_claim = None
    if event == "pull_request" and ref_name and ref_name != "main":
        branch_claims = [claim for claim in active_branch_claims() if claim.get("branch") == ref_name]
        if len(branch_claims) != 1:
            failures.append(f"pull request branch must resolve to exactly one active pre-work claim: {ref_name}")
        else:
            branch_claim = branch_claims[0]
            if not claim_handoff_exists(branch_claim):
                failures.append(f"pull request branch claim handoff is missing or outside repository: {ref_name}")

        # A validated exact-branch pre-work claim is the machine-readable ownership
        # proof. The token heuristic remains only as a legacy fallback for branches
        # whose work is directly enumerated in the broad Site handoff.
        branch_tokens = normalized(ref_name.replace("/", " ").replace("-", " "))
        owns_declared_work = branch_claim is not None or any(branch_tokens & normalized(item["workload"]) for item in workloads)
        if not owns_declared_work and "orchestrat" not in ref_name.lower() and "handoff" not in ref_name.lower() and "claim" not in ref_name.lower():
            failures.append("pull request does not map to an unfinished handoff workload")

    report = {
        "schema_version": "1.4.0",
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
        "prework_claim_validation": claim_validation,
        "pull_request_branch_claim": branch_claim,
        "assignments": assignments,
        "possible_overlap_groups": possible_overlap_groups,
        "possible_overlap_policy": "diagnostic only; machine-readable active claims are blocking authority",
        "failures": failures,
        "next_action": (
            "repair retirement state or pre-work claim admission before mutable work"
            if failures
            else "continue only the workload admitted by the collision-free pre-work claim registry"
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"SITE_HANDOFF_ORCHESTRATION_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
