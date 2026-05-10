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
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Could not read JSON file {path}: {exc}") from exc


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def parse_arg_overrides(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid --arg value {item!r}. Use key=value.")
        key, value = item.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def apply_template(value: str, args: dict[str, str]) -> str:
    rendered = value
    for key, arg_value in args.items():
        rendered = rendered.replace("{" + key + "}", arg_value)
    return rendered


def render_command(command: list[str], args: dict[str, str]) -> list[str]:
    return [apply_template(part, args) for part in command]


def command_text(command: list[str]) -> str:
    return " ".join(command)


def fail_receipt(task: dict[str, Any], reason: str, policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "schema": "stegverse.headless_cmd_receipt.v1",
        "task_id": task.get("task_id"),
        "authority_class": task.get("authority_class"),
        "verdict": "FAIL_CLOSED",
        "reason": reason,
        "exit_code": None,
        "command": task.get("command"),
        "stdout_tail": "",
        "stderr_tail": "",
        "policy": policy.get("schema"),
    }


def validate_task(task: dict[str, Any], policy: dict[str, Any], command: list[str]) -> tuple[bool, str]:
    if task.get("schema") != "stegverse.headless_cmd_task.v1":
        return False, "Unknown or unsupported task schema."

    authority = task.get("authority_class")
    if authority in policy.get("denied_authority_classes", []):
        return False, f"Denied authority class: {authority}"

    allowed = policy.get("allowed_authority_classes", [])
    if allowed and authority not in allowed:
        return False, f"Authority class is not explicitly allowed: {authority}"

    text = command_text(command)
    for fragment in policy.get("forbidden_command_fragments", []):
        if fragment and fragment in text:
            return False, f"Forbidden command fragment found: {fragment}"

    for path in task.get("expected_inputs", []):
        if "{" in path and "}" in path:
            continue
        if not Path(path).exists():
            return False, f"Expected input missing: {path}"

    for part in command:
        for prefix in policy.get("forbidden_path_prefixes", []):
            if part == prefix.rstrip("/") or part.startswith(prefix):
                return False, f"Command references forbidden path prefix: {prefix}"

    for path in task.get("forbidden_paths", []):
        for part in command:
            if part == path.rstrip("/") or part.startswith(path):
                return False, f"Task command references forbidden path: {path}"

    return True, "Task validated."


def tail(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def write_markdown(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Headless Command Report",
        "",
        f"Generated: `{receipt.get('generated_at')}`",
        f"Task: `{receipt.get('task_id')}`",
        f"Verdict: `{receipt.get('verdict')}`",
        f"Exit code: `{receipt.get('exit_code')}`",
        f"Reason: {receipt.get('reason')}",
        "",
        "## Command",
        "",
        "```text",
        command_text(receipt.get("command", [])),
        "```",
        "",
        "## Stdout Tail",
        "",
        "```text",
        receipt.get("stdout_tail", ""),
        "```",
        "",
        "## Stderr Tail",
        "",
        "```text",
        receipt.get("stderr_tail", ""),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--policy", default="data/headless-task-policy-v1.json")
    parser.add_argument("--arg", action="append", default=[])
    args = parser.parse_args()

    task_path = Path(args.task)
    policy_path = Path(args.policy)

    task = load_json(task_path, {})
    policy = load_json(policy_path, {})

    task_args = dict(task.get("default_args", {}))
    task_args.update(parse_arg_overrides(args.arg))

    command = render_command(task.get("command", []), task_args)
    valid, reason = validate_task(task, policy, command)

    receipt_path = Path(task.get("receipt_output", f"headless_cmd_reports/{task.get('task_id', 'unknown')}.receipt.json"))
    markdown_path = Path(task.get("markdown_output", f"headless_cmd_reports/{task.get('task_id', 'unknown')}.report.md"))

    if not valid:
        receipt = fail_receipt({**task, "command": command}, reason, policy)
        write_json(receipt_path, receipt)
        write_markdown(markdown_path, receipt)
        print(json.dumps({"verdict": receipt["verdict"], "reason": reason}, indent=2))
        return 1

    started_at = utc_now()
    timeout = int(task.get("timeout_seconds", policy.get("default_timeout_seconds", 120)))

    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        exit_code = result.returncode
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        verdict = "ALLOW" if exit_code == 0 else "FAIL_CLOSED"
        result_reason = "Command exited successfully." if exit_code == 0 else "Command exited with non-zero status."
    except subprocess.TimeoutExpired as exc:
        exit_code = None
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        verdict = "FAIL_CLOSED"
        result_reason = f"Command timed out after {timeout} seconds."

    finished_at = utc_now()

    stdout_limit = int(policy.get("max_stdout_chars", 12000))
    stderr_limit = int(policy.get("max_stderr_chars", 12000))

    receipt = {
        "generated_at": finished_at,
        "schema": "stegverse.headless_cmd_receipt.v1",
        "task_id": task.get("task_id"),
        "task_path": str(task_path),
        "authority_class": task.get("authority_class"),
        "class": task.get("class"),
        "verdict": verdict,
        "reason": result_reason,
        "started_at": started_at,
        "finished_at": finished_at,
        "exit_code": exit_code,
        "command": command,
        "stdout_tail": tail(stdout, stdout_limit),
        "stderr_tail": tail(stderr, stderr_limit),
        "expected_outputs": task.get("expected_outputs", []),
        "args": task_args,
    }

    write_json(receipt_path, receipt)
    write_markdown(markdown_path, receipt)

    print(json.dumps({
        "task_id": receipt["task_id"],
        "verdict": receipt["verdict"],
        "exit_code": receipt["exit_code"],
        "receipt": str(receipt_path),
    }, indent=2))

    return 0 if verdict == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
