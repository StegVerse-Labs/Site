#!/usr/bin/env python3
"""Fail-closed handoff-driven workload reconciliation for StegVerse-Labs/Site."""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
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
TERMINAL_CLAIM_STATES = {"RELEASED", "RELEASED_COMPLETE", "MERGED_INTO_CANONICAL_WORKSTREAM", "SATISFIED_BY_EXISTING_STATE", "COMPLETE", "COMPLETED"}
CLAIM_RELEASE_MUTABLE_FIELDS = {
    "state",
    "role",
    "pull_request",
    "release_commit",
    "claim_released_at",
    "archive_eligible",
}
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


def claim_registry_only_paths(paths: list[str]) -> bool:
    if not paths:
        return False
    return all(
        path.startswith("data/session-work-claims.d/") and path.endswith(".json")
        for path in paths
    )


def validate_terminal_claim_delta(
    base_claim: dict[str, Any],
    current_claim: dict[str, Any],
) -> tuple[bool, str]:
    if not isinstance(base_claim, dict) or not isinstance(current_claim, dict):
        return False, "claim objects required"
    claim_id = base_claim.get("claim_id")
    if not isinstance(claim_id, str) or not claim_id or current_claim.get("claim_id") != claim_id:
        return False, "claim identity changed"
    if base_claim.get("state") not in ACTIVE_CLAIM_STATES:
        return False, "base claim is not active"
    if current_claim.get("state") not in TERMINAL_CLAIM_STATES:
        return False, "proposed claim is not terminal"

    protected_base = {key: value for key, value in base_claim.items() if key not in CLAIM_RELEASE_MUTABLE_FIELDS}
    protected_current = {key: value for key, value in current_claim.items() if key not in CLAIM_RELEASE_MUTABLE_FIELDS}
    if protected_base != protected_current:
        return False, "protected claim ownership or authority fields changed"

    if current_claim.get("authority_effect") is not False:
        return False, "terminalization may not grant authority"
    if current_claim.get("activation_effect") is not False:
        return False, "terminalization may not grant activation"
    if not isinstance(current_claim.get("pull_request"), int) or current_claim["pull_request"] <= 0:
        return False, "terminalization pull_request evidence required"
    if not isinstance(current_claim.get("release_commit"), str) or not current_claim["release_commit"]:
        return False, "terminalization release_commit evidence required"
    if not isinstance(current_claim.get("claim_released_at"), str) or not current_claim["claim_released_at"]:
        return False, "terminalization claim_released_at evidence required"
    return True, "PASS"


def _pull_request_event() -> dict[str, Any] | None:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        return None
    path = Path(event_path)
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict) or not isinstance(value.get("pull_request"), dict):
        return None
    return value


def _api_pr_changed_files() -> list[str]:
    if not TOKEN:
        return []
    event = _pull_request_event()
    if event is None:
        return []
    number = event.get("pull_request", {}).get("number") or event.get("number")
    if not isinstance(number, int) or number <= 0:
        return []
    try:
        rows = api(f"/pulls/{number}/files?per_page=100")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return []
    if not isinstance(rows, list) or len(rows) >= 100:
        return []
    result: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            return []
        filename = row.get("filename")
        if not isinstance(filename, str) or not filename:
            return []
        result.append(filename)
    return result


def _api_base_json(path: str) -> dict[str, Any] | None:
    if not TOKEN:
        return None
    event = _pull_request_event()
    if event is None:
        return None
    base = event.get("pull_request", {}).get("base", {})
    ref = base.get("sha") if isinstance(base, dict) else None
    if not isinstance(ref, str) or not ref:
        return None
    encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    try:
        row = api(f"/contents/{encoded_path}?ref={urllib.parse.quote(ref, safe='')}")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return None
    if not isinstance(row, dict) or row.get("encoding") != "base64":
        return None
    content = row.get("content")
    if not isinstance(content, str):
        return None
    try:
        decoded = base64.b64decode(content, validate=False).decode("utf-8")
        value = json.loads(decoded)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _git_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD^1", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if paths:
            return paths
    return _api_pr_changed_files()


def _git_show_json(ref: str, path: str) -> dict[str, Any] | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        try:
            value = json.loads(result.stdout)
        except json.JSONDecodeError:
            value = None
        if isinstance(value, dict):
            return value
    if ref == "HEAD^1":
        return _api_base_json(path)
    return None


def terminalization_only_claim_transition() -> tuple[dict[str, Any] | None, str]:
    changed_paths = _git_changed_files()
    if not claim_registry_only_paths(changed_paths):
        return None, "pull request is not claim-registry-only"

    changed_claims: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    for path in changed_paths:
        base_fragment = _git_show_json("HEAD^1", path)
        current_path = ROOT / path
        if base_fragment is None or not current_path.is_file():
            return None, f"claim fragment add/remove is not terminalization-only: {path}"
        try:
            current_fragment = json.loads(current_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None, f"current claim fragment invalid: {path}"
        if not isinstance(current_fragment, dict):
            return None, f"current claim fragment invalid: {path}"

        base_rows = base_fragment.get("claims")
        current_rows = current_fragment.get("claims")
        if not isinstance(base_rows, list) or not isinstance(current_rows, list):
            return None, f"claim list missing: {path}"
        base_by_id = {
            row.get("claim_id"): row
            for row in base_rows
            if isinstance(row, dict) and isinstance(row.get("claim_id"), str)
        }
        current_by_id = {
            row.get("claim_id"): row
            for row in current_rows
            if isinstance(row, dict) and isinstance(row.get("claim_id"), str)
        }
        if set(base_by_id) != set(current_by_id):
            return None, f"claim add/remove is not terminalization-only: {path}"
        for claim_id in sorted(base_by_id):
            if base_by_id[claim_id] != current_by_id[claim_id]:
                changed_claims.append((base_by_id[claim_id], current_by_id[claim_id], path))

    if len(changed_claims) != 1:
        return None, f"expected exactly one terminalized claim, observed {len(changed_claims)}"
    base_claim, current_claim, path = changed_claims[0]
    valid, reason = validate_terminal_claim_delta(base_claim, current_claim)
    if not valid:
        return None, reason
    if not claim_handoff_exists(current_claim):
        return None, "terminalized claim handoff is missing or outside repository"
    return {
        "mode": "TERMINALIZATION_ONLY_CLAIM_MAINTENANCE",
        "path": path,
        "claim": current_claim,
        "base_state": base_claim.get("state"),
        "current_state": current_claim.get("state"),
        "authority_effect": "NONE",
    }, "PASS"


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
    terminalization_only_claim = None
    if event == "pull_request" and ref_name and ref_name != "main":
        branch_claims = [claim for claim in active_branch_claims() if claim.get("branch") == ref_name]
        if len(branch_claims) == 1:
            branch_claim = branch_claims[0]
            if not claim_handoff_exists(branch_claim):
                failures.append(f"pull request branch claim handoff is missing or outside repository: {ref_name}")
        else:
            terminalization_only_claim, terminalization_reason = terminalization_only_claim_transition()
            if terminalization_only_claim is None:
                failures.append(f"pull request branch must resolve to exactly one active pre-work claim: {ref_name}")
                failures.append(f"terminalization-only claim maintenance rejected: {terminalization_reason}")
            else:
                branch_claim = terminalization_only_claim["claim"]

        # A validated exact-branch pre-work claim or a fail-closed terminalization-only
        # claim transition is machine-readable ownership proof. The token heuristic
        # remains only as a legacy fallback for broad handoff-enumerated work.
        branch_tokens = normalized(ref_name.replace("/", " ").replace("-", " "))
        owns_declared_work = branch_claim is not None or any(branch_tokens & normalized(item["workload"]) for item in workloads)
        if not owns_declared_work and "orchestrat" not in ref_name.lower() and "handoff" not in ref_name.lower() and "claim" not in ref_name.lower():
            failures.append("pull request does not map to an unfinished handoff workload")

    report = {
        "schema_version": "1.6.0",
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
        "terminalization_only_claim_maintenance": terminalization_only_claim,
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
