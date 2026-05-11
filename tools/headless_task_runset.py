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


def run_task(task_path: str, policy: str, timeout: int) -> dict[str, Any]:
    command = [
        "python",
        "tools/headless_cmd_runner.py",
        "--policy",
        policy,
        "--task",
        task_path
    ]
    started = utc_now()
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "task_path": task_path,
            "started_at": started,
            "finished_at": utc_now(),
            "exit_code": result.returncode,
            "stdout": (result.stdout or "")[-4000:],
            "stderr": (result.stderr or "")[-4000:],
            "command": command
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "task_path": task_path,
            "started_at": started,
            "finished_at": utc_now(),
            "exit_code": None,
            "stdout": str(exc.stdout or "")[-4000:],
            "stderr": str(exc.stderr or "")[-4000:],
            "command": command,
            "timeout": True
        }


def validate_runset(root: Path, runset: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    if runset.get("schema") != "stegverse.headless_task_runset.v1":
        errors.append("unsupported runset schema")

    allowed = set(runset.get("allowed_task_authority_classes", []))
    denied = set(runset.get("denied_task_authority_classes", []))

    for task in runset.get("tasks", []):
        task_path = root / str(task)
        task_obj = load_json(task_path, None)
        if not isinstance(task_obj, dict):
            errors.append(f"missing or invalid task: {task}")
            continue
        authority = task_obj.get("authority_class")
        if authority in denied:
            errors.append(f"task authority denied: {task} authority={authority}")
        if allowed and authority not in allowed:
            errors.append(f"task authority not allowlisted: {task} authority={authority}")

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--runset", default="data/headless-task-runsets/transition-discovery-automation-runset-v1.json")
    parser.add_argument("--policy", default="data/headless-task-policy-v1.json")
    parser.add_argument("--out-dir", default="headless_cmd_reports")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    runset = load_json(root / args.runset, None)
    if not isinstance(runset, dict):
        raise SystemExit(f"Missing or invalid runset: {args.runset}")

    valid, errors = validate_runset(root, runset)
    results = []
    if valid:
        for task in runset.get("tasks", []):
            if not (root / str(task)).exists():
                results.append({"task_path": str(task), "skipped": True, "reason": "task file missing"})
                continue
            result = run_task(str(task), args.policy, args.timeout)
            results.append(result)
            if runset.get("stop_on_failure") and result.get("exit_code") not in (0,):
                break

    report = {
        "generated_at": utc_now(),
        "schema": "stegverse.headless_task_runset_report.v1",
        "runset_id": runset.get("runset_id"),
        "valid": valid,
        "errors": errors,
        "results": results,
        "summary": {
            "tasks_declared": len(runset.get("tasks", [])),
            "tasks_executed": sum(1 for r in results if not r.get("skipped")),
            "tasks_succeeded": sum(1 for r in results if r.get("exit_code") == 0),
            "tasks_failed": sum(1 for r in results if r.get("exit_code") not in (0, None) and not r.get("skipped")),
            "tasks_skipped": sum(1 for r in results if r.get("skipped")),
        }
    }

    out = root / args.out_dir
    write_json(out / "headless-task-runset-report.json", report)
    md = [
        "# Headless Task Runset Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Runset: `{report.get('runset_id')}`",
        f"Valid: `{valid}`",
        "",
        "## Summary",
        ""
    ]
    for k, v in report["summary"].items():
        md.append(f"- `{k}`: `{v}`")
    if errors:
        md.extend(["", "## Errors", ""])
        for error in errors:
            md.append(f"- `{error}`")
    md.extend(["", "## Results", ""])
    for item in results:
        md.append(f"- `{item.get('task_path')}` exit=`{item.get('exit_code')}` skipped=`{item.get('skipped', False)}`")
    (out / "headless-task-runset-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(report["summary"], indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
