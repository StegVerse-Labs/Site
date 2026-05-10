#!/usr/bin/env python3
"""
StegVerse Transition Next-Step Selector.

This tool determines the next admissible build/promotion action from repo-resident
state, rules, and verifier reports. Missing evidence never promotes.
"""

from __future__ import annotations

import argparse
import glob
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CheckStatus:
    id: str
    workflow_name: str
    status: str
    report_path: str | None
    reason: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def lookup(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def first_existing_json(patterns: list[str], root: Path) -> tuple[Path | None, Any | None, str | None]:
    for pattern in patterns:
        for raw in sorted(glob.glob(str(root / pattern))):
            path = Path(raw)
            if not path.is_file() or path.suffix.lower() != ".json":
                continue
            try:
                return path, read_json(path), None
            except Exception as exc:  # noqa: BLE001
                return path, None, f"unreadable json: {exc}"
    return None, None, None


def classify_page_contract(report: Any) -> tuple[str, str]:
    passed = report.get("passed") if isinstance(report, dict) else None
    failures = report.get("failures") if isinstance(report, dict) else None

    if passed is True and failures == 0:
        return "passed", "passed=true and failures=0"
    if passed is False or (isinstance(failures, int) and failures > 0):
        return "failed", f"passed={passed!r}, failures={failures!r}"
    return "unknown", "report does not expose passed=true and failures=0"


def classify_transition_replay(report: Any) -> tuple[str, str]:
    if not isinstance(report, dict):
        return "unknown", "report is not a JSON object"

    passed = report.get("passed")
    verdict = report.get("verdict")
    all_verified = report.get("all_replay_fixtures_verified")

    if (passed is True or all_verified is True) and verdict == "ALLOW":
        return "passed", "replay report indicates ALLOW"
    if passed is False or verdict in {"DENY", "FAIL_CLOSED"}:
        return "failed", f"passed={passed!r}, verdict={verdict!r}"
    return "unknown", "report does not expose passed/all_verified with verdict=ALLOW"


def classify_check(check: dict[str, Any], repo_root: Path) -> CheckStatus:
    check_id = str(check.get("id", "unknown"))
    workflow_name = str(check.get("workflow_name", check_id))
    patterns = list(check.get("accepted_report_globs", []))

    path, report, error = first_existing_json(patterns, repo_root)
    if error:
        return CheckStatus(check_id, workflow_name, "unknown", str(path) if path else None, error)
    if report is None:
        return CheckStatus(check_id, workflow_name, "missing", None, "no readable report found")

    if check_id == "page_contract_check":
        status, reason = classify_page_contract(report)
    elif check_id == "transition_replay_check":
        status, reason = classify_transition_replay(report)
    else:
        status = "unknown"
        reason = f"no classifier for check id {check_id!r}"

    return CheckStatus(check_id, workflow_name, status, str(path), reason)


def select_next_action(checks: list[CheckStatus]) -> tuple[str, bool, bool, bool, str]:
    if any(c.status == "failed" for c in checks):
        failed = [c.workflow_name for c in checks if c.status == "failed"]
        return (
            "repair_failed_contract_or_replay",
            False,
            False,
            True,
            "Required check failed: " + ", ".join(failed),
        )

    if any(c.status == "unknown" for c in checks):
        unknown = [c.workflow_name for c in checks if c.status == "unknown"]
        return (
            "halt_for_human_review",
            False,
            False,
            True,
            "Required check could not be classified: " + ", ".join(unknown),
        )

    if any(c.status == "missing" for c in checks):
        missing = [c.workflow_name for c in checks if c.status == "missing"]
        return (
            "run_required_checks",
            False,
            False,
            False,
            "Required check evidence is missing: " + ", ".join(missing),
        )

    if all(c.status == "passed" for c in checks):
        return (
            "promote_candidate_milestone",
            True,
            True,
            False,
            "All required release gates have readable passing reports.",
        )

    return (
        "halt_for_human_review",
        False,
        False,
        True,
        "Selector reached an unclassified state.",
    )


def write_markdown(report: dict[str, Any], path: Path) -> None:
    checks = report["check_statuses"]
    lines = [
        "# Next Transition Step Report",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        f"Current released milestone: **{report['current_released_milestone']}**",
        f"Current candidate milestone: **{report['current_candidate_milestone']}**",
        "",
        f"Next system action: **{report['next_system_action']}**",
        "",
        f"Build allowed: `{str(report['build_allowed']).lower()}`",
        f"Promotion allowed: `{str(report['promotion_allowed']).lower()}`",
        f"Human required: `{str(report['human_required']).lower()}`",
        "",
        "## Reason",
        "",
        report["reason"],
        "",
        "## Required Checks",
        "",
    ]
    for check in checks:
        lines.append(f"- **{check['workflow_name']}**: `{check['status']}` — {check['reason']}")
        if check.get("report_path"):
            lines.append(f"  - report: `{check['report_path']}`")
    lines.extend([
        "",
        "## Safety Rule",
        "",
        "Missing or unreadable evidence never promotes a milestone.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", default="data/transition-release-state-v1.json")
    parser.add_argument("--rules", default="data/transition-decision-rules-v1.json")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out-dir", default="next_transition_step_reports")
    parser.add_argument("--write-public", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    state = read_json(repo_root / args.state)
    rules = read_json(repo_root / args.rules)

    candidate = state.get("current_candidate_milestone") or {}
    released = state.get("current_released_milestone") or {}
    checks = [classify_check(c, repo_root) for c in candidate.get("required_checks", [])]

    action, build_allowed, promotion_allowed, human_required, reason = select_next_action(checks)

    report = {
        "generated_at": utc_now(),
        "schema": "stegverse.next_transition_build_candidate.v1",
        "state_id": state.get("state_id"),
        "ruleset_id": rules.get("ruleset_id"),
        "current_released_milestone": released.get("formal_label"),
        "current_candidate_milestone": candidate.get("formal_label"),
        "next_system_action": action,
        "build_allowed": build_allowed,
        "promotion_allowed": promotion_allowed,
        "human_required": human_required,
        "reason": reason,
        "check_statuses": [asdict(c) for c in checks],
        "safety": {
            "missing_evidence_promotes": False,
            "chat_or_screenshot_promotes": False,
            "promotion_requires_all_required_checks": True
        }
    }

    out_dir = repo_root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "next_transition_step_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report, out_dir / "next_transition_step_report.md")

    if args.write_public:
        public_path = repo_root / "data" / "next-transition-build-candidate-v1.json"
        public_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "next_system_action": action,
        "build_allowed": build_allowed,
        "promotion_allowed": promotion_allowed,
        "human_required": human_required,
        "reason": reason,
    }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
