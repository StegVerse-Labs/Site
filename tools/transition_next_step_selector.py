#!/usr/bin/env python3
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


def first_existing_json(patterns: list[str], root: Path) -> tuple[Path | None, Any | None, str | None]:
    for pattern in patterns:
        for raw in sorted(glob.glob(str(root / pattern))):
            path = Path(raw)
            if not path.is_file() or path.suffix.lower() != ".json":
                continue
            try:
                return path, read_json(path), None
            except Exception as exc:
                return path, None, f"unreadable json: {exc}"
    return None, None, None


def classify_page_contract(report: Any) -> tuple[str, str]:
    if isinstance(report, dict) and report.get("passed") is True and report.get("failures") == 0:
        return "passed", "passed=true and failures=0"
    if isinstance(report, dict) and (report.get("passed") is False or (isinstance(report.get("failures"), int) and report.get("failures") > 0)):
        return "failed", f"passed={report.get('passed')!r}, failures={report.get('failures')!r}"
    return "unknown", "report does not expose passed=true and failures=0"


def classify_transition_replay(report: Any) -> tuple[str, str]:
    if isinstance(report, dict) and (report.get("passed") is True or report.get("all_replay_fixtures_verified") is True) and report.get("verdict") == "ALLOW":
        return "passed", "replay report indicates ALLOW"
    if isinstance(report, dict) and (report.get("passed") is False or report.get("verdict") in {"DENY", "FAIL_CLOSED"}):
        return "failed", f"passed={report.get('passed')!r}, verdict={report.get('verdict')!r}"
    return "unknown", "report does not expose passed/all_verified with verdict=ALLOW"


def classify_check(check: dict[str, Any], repo_root: Path) -> CheckStatus:
    check_id = str(check.get("id", "unknown"))
    workflow_name = str(check.get("workflow_name", check_id))
    path, report, error = first_existing_json(list(check.get("accepted_report_globs", [])), repo_root)
    if error:
        return CheckStatus(check_id, workflow_name, "unknown", str(path) if path else None, error)
    if report is None:
        return CheckStatus(check_id, workflow_name, "missing", None, "no readable report found")
    if check_id == "page_contract_check":
        status, reason = classify_page_contract(report)
    elif check_id == "transition_replay_check":
        status, reason = classify_transition_replay(report)
    else:
        status, reason = "unknown", f"no classifier for {check_id}"
    return CheckStatus(check_id, workflow_name, status, str(path), reason)


def select_next_action(checks: list[CheckStatus]) -> tuple[str, bool, bool, bool, str]:
    if any(c.status == "failed" for c in checks):
        return "repair_failed_contract_or_replay", False, False, True, "Required check failed."
    if any(c.status == "unknown" for c in checks):
        return "halt_for_human_review", False, False, True, "Required check could not be classified."
    if any(c.status == "missing" for c in checks):
        missing = ", ".join(c.workflow_name for c in checks if c.status == "missing")
        return "run_required_checks", False, False, False, f"Required check evidence is missing: {missing}"
    if all(c.status == "passed" for c in checks):
        return "promote_candidate_milestone", True, True, False, "All required release gates have readable passing reports."
    return "halt_for_human_review", False, False, True, "Selector reached an unclassified state."


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Next Transition Step Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Current released milestone: **{report['current_released_milestone']}**",
        f"Current candidate milestone: **{report['current_candidate_milestone']}**",
        "",
        f"Next system action: **{report['next_system_action']}**",
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
    for check in report["check_statuses"]:
        lines.append(f"- **{check['workflow_name']}**: `{check['status']}` — {check['reason']}")
    lines.extend(["", "## Safety Rule", "", "Missing or unreadable evidence never promotes a milestone.", ""])
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

    candidate = state["current_candidate_milestone"]
    released = state["current_released_milestone"]
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
        (repo_root / "data" / "next-transition-build-candidate-v1.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "next_system_action": action,
        "promotion_allowed": promotion_allowed,
        "human_required": human_required,
        "reason": reason
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
