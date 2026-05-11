#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists() or not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Could not read JSON {path}: {exc}") from exc


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def run_step(root: Path, step: dict[str, Any], timeout: int) -> dict[str, Any]:
    missing = [path for path in step.get("required_files", []) if not (root / str(path)).exists()]
    if missing:
        return {
            "step_id": step.get("step_id"),
            "skipped": True,
            "reason": "missing required files",
            "missing": missing,
            "exit_code": None
        }

    command = [str(part) for part in step.get("command", [])]
    started = utc_now()
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "step_id": step.get("step_id"),
            "skipped": False,
            "started_at": started,
            "finished_at": utc_now(),
            "exit_code": result.returncode,
            "stdout_tail": (result.stdout or "")[-5000:],
            "stderr_tail": (result.stderr or "")[-5000:],
            "command": command
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "step_id": step.get("step_id"),
            "skipped": False,
            "started_at": started,
            "finished_at": utc_now(),
            "exit_code": None,
            "timeout": True,
            "stdout_tail": str(exc.stdout or "")[-5000:],
            "stderr_tail": str(exc.stderr or "")[-5000:],
            "command": command
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/transition-automation/transition-automation-controller-policy-v1.json")
    parser.add_argument("--out-dir", default="transition_discovery_reports")
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, None)
    if not isinstance(policy, dict):
        raise SystemExit(f"Missing or invalid controller policy: {args.policy}")

    results = []
    for step in policy.get("steps", []):
        result = run_step(root, step, args.timeout)
        results.append(result)
        failed = result.get("exit_code") not in (0, None) and not result.get("skipped")
        if failed and not step.get("continue_on_failure", False):
            break

    report = {
        "generated_at": utc_now(),
        "schema": "stegverse.transition_automation_controller_report.v1",
        "policy_id": policy.get("policy_id"),
        "results": results,
        "summary": {
            "steps_total": len(policy.get("steps", [])),
            "steps_executed": sum(1 for r in results if not r.get("skipped")),
            "steps_skipped": sum(1 for r in results if r.get("skipped")),
            "steps_succeeded": sum(1 for r in results if r.get("exit_code") == 0),
            "steps_failed": sum(1 for r in results if r.get("exit_code") not in (0, None) and not r.get("skipped")),
        }
    }

    out = root / args.out_dir
    write_json(out / "transition-automation-controller-report.json", report)

    md = [
        "# Transition Automation Controller Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Policy: `{report.get('policy_id')}`",
        "",
        "## Summary",
        ""
    ]
    for k, v in report["summary"].items():
        md.append(f"- `{k}`: `{v}`")
    md.extend(["", "## Steps", ""])
    for item in results:
        md.append(f"- `{item.get('step_id')}` exit=`{item.get('exit_code')}` skipped=`{item.get('skipped', False)}` reason=`{item.get('reason', '')}`")
    (out / "transition-automation-controller-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
