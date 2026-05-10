#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
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
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def list_files(folder: Path) -> list[Path]:
    if not folder.exists() or not folder.is_dir():
        return []
    return sorted([item for item in folder.iterdir() if item.is_file()], key=lambda p: p.name)


def receipt_exists(folder: Path, stem: str, suffixes: list[str]) -> bool:
    for suffix in suffixes:
        if (folder / f"{stem}.{suffix}.json").exists():
            return True
        if (folder / f"{stem}.{suffix}.md").exists():
            return True
    return False


def collect_known_bundle_stems(root: Path, dirs: list[str]) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for rel in dirs:
        folder = root / rel
        for path in list_files(folder):
            if path.suffix.lower() != ".zip":
                continue
            seen.setdefault(path.stem, []).append(rel)
    return seen


def deficiency(code: str, path: str, detail: Any, severity: str = "repair_required") -> dict[str, Any]:
    return {
        "code": code,
        "path": path,
        "detail": detail,
        "severity": severity,
    }


def check_required_dirs(root: Path, required: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    results = []
    deficiencies = []
    for rel in required:
        path = root / rel
        passed = path.exists() and path.is_dir()
        results.append({
            "check": "required_directory_exists",
            "path": rel,
            "passed": passed,
            "detail": "exists" if passed else "missing",
        })
        if not passed:
            deficiencies.append(deficiency("required_directory_missing", rel, "Directory is required but missing.", "fail_closed"))
    return results, deficiencies


def check_report_writeability(out_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    marker = out_dir / ".path-function-sentinel-write-test.tmp"
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        marker.write_text("ok", encoding="utf-8")
        data = marker.read_text(encoding="utf-8")
        marker.unlink()
        passed = data == "ok" and not marker.exists()
        result = {
            "check": "report_directory_write_test",
            "path": out_dir.as_posix(),
            "passed": passed,
            "detail": "marker_write_read_delete_ok" if passed else "marker_write_read_delete_failed",
        }
        defs = [] if passed else [deficiency("report_directory_not_writeable", out_dir.as_posix(), result["detail"], "fail_closed")]
        return [result], defs
    except Exception as exc:
        return [{
            "check": "report_directory_write_test",
            "path": out_dir.as_posix(),
            "passed": False,
            "detail": f"write_test_failed:{exc}",
        }], [deficiency("report_directory_not_writeable", out_dir.as_posix(), str(exc), "fail_closed")]


def check_incoming(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    incoming = root / "incoming"
    results = []
    deficiencies = []

    known_dirs = [
        "installed_bundles",
        "failed_bundles",
        "sandbox_queue",
        "privileged_queue",
    ]
    known = collect_known_bundle_stems(root, known_dirs)

    if not incoming.exists():
        result = {
            "check": "incoming_exists",
            "path": "incoming",
            "passed": False,
            "detail": "incoming_missing",
        }
        return [result], [deficiency("incoming_missing", "incoming", "incoming/ directory is missing.", "fail_closed")]

    files = list_files(incoming)
    non_zip = [path.name for path in files if path.suffix.lower() != ".zip"]
    if non_zip:
        results.append({
            "check": "incoming_contains_only_zip_files",
            "path": "incoming",
            "passed": False,
            "detail": {"non_zip_files": non_zip},
        })
        for name in non_zip:
            deficiencies.append(deficiency("incoming_non_zip_file", f"incoming/{name}", "incoming/ should contain only ZIP bundle candidates."))
    else:
        results.append({
            "check": "incoming_contains_only_zip_files",
            "path": "incoming",
            "passed": True,
            "detail": "ok",
        })

    counts = Counter(path.name for path in files)
    duplicate_names = [name for name, count in counts.items() if count > 1]
    results.append({
        "check": "incoming_has_no_duplicate_names",
        "path": "incoming",
        "passed": len(duplicate_names) == 0,
        "detail": duplicate_names if duplicate_names else "ok",
    })
    for name in duplicate_names:
        deficiencies.append(deficiency("incoming_duplicate_name", f"incoming/{name}", "Duplicate incoming bundle name detected."))

    already_routed = []
    for path in files:
        if path.suffix.lower() != ".zip":
            continue
        if path.stem in known:
            item = {
                "file": path.name,
                "also_present_in": known[path.stem],
            }
            already_routed.append(item)
            deficiencies.append(deficiency("incoming_already_routed_bundle_name", f"incoming/{path.name}", item))

    results.append({
        "check": "incoming_has_no_already_routed_bundle_names",
        "path": "incoming",
        "passed": len(already_routed) == 0,
        "detail": already_routed if already_routed else "ok",
    })

    return results, deficiencies


def check_receipts(root: Path, folder_name: str, suffixes: list[str], check_name: str, deficiency_code: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    folder = root / folder_name
    results = []
    deficiencies = []

    if not folder.exists():
        results.append({
            "check": f"{check_name}_folder_exists",
            "path": folder_name,
            "passed": False,
            "detail": "missing",
        })
        deficiencies.append(deficiency(f"{folder_name}_missing", folder_name, "Queue/archive directory is missing.", "fail_closed"))
        return results, deficiencies

    zip_files = [path for path in list_files(folder) if path.suffix.lower() == ".zip"]
    missing = []
    for path in zip_files:
        if not receipt_exists(folder, path.stem, suffixes):
            missing.append(path.name)
            deficiencies.append(deficiency(deficiency_code, f"{folder_name}/{path.name}", f"Missing receipt suffix among {suffixes}."))

    results.append({
        "check": check_name,
        "path": folder_name,
        "passed": len(missing) == 0,
        "detail": {"missing_receipts_for": missing} if missing else "ok",
    })
    return results, deficiencies


def determine_verdict(deficiencies: list[dict[str, Any]]) -> str:
    if not deficiencies:
        return "IDLE_READY"
    if any(item.get("severity") == "fail_closed" for item in deficiencies):
        return "FAIL_CLOSED"
    return "SANDBOX_TASK_REQUIRED"


def build_sandbox_task(report: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "schema": "stegverse.sandbox_repair_task.v1",
        "task_id": "path-function-repair-task",
        "formal_milestone": policy.get("formal_milestone", "MS-012H — Path Function Sentinel Sandbox Loop"),
        "source_report": "path_function_reports/path-function-sentinel-report.json",
        "purpose": "Repair path-function deficiencies detected by the sentinel, test repairs in sandbox, then return a repair bundle through ingestion.",
        "required_flow": [
            "Review deficiencies.",
            "Construct candidate repair in sandbox.",
            "Run sandbox repair test.",
            "If repair passes, emit repair bundle into incoming/.",
            "Ingestion applies/reroutes repair bundle.",
            "Run sentinel again.",
            "Sentinel may move to idle only when no deficiencies remain."
        ],
        "deficiencies": report.get("deficiencies", []),
        "repair_constraints": {
            "do_not_delete_evidence": True,
            "do_not_modify_workflows_without_human_approval": True,
            "do_not_create_cron_or_workflow_run_chains": True,
            "do_not_use_self_trigger_zip": True,
            "repair_bundle_must_pass_ingestion": True,
            "sentinel_idle_requires_clean_path_report": True
        },
        "expected_repair_test_report": "sandbox_reports/sandbox-repair-test-report.json",
        "expected_reentry": "incoming/<repair-bundle>.zip",
        "idle_condition": "next sentinel run returns IDLE_READY"
    }


def write_sandbox_task_markdown(path: Path, task: dict[str, Any]) -> None:
    lines = [
        "# Sandbox Repair Task",
        "",
        f"Generated: `{task['generated_at']}`",
        f"Task: `{task['task_id']}`",
        f"Source report: `{task['source_report']}`",
        "",
        "## Required Flow",
        "",
    ]
    for step in task.get("required_flow", []):
        lines.append(f"- {step}")

    lines.extend(["", "## Deficiencies", ""])
    for item in task.get("deficiencies", []):
        lines.append(f"- `{item.get('code')}` `{item.get('path')}` — {item.get('detail')}")

    lines.extend(["", "## Repair Constraints", ""])
    for key, value in task.get("repair_constraints", {}).items():
        lines.append(f"- `{key}`: `{value}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def state_payload(verdict: str, report: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "schema": "stegverse.path_function_sentinel_state.v2",
        "sentinel_id": "path-function-sentinel-sandbox-loop-v2",
        "verdict": verdict,
        "report_path": "path_function_reports/path-function-sentinel-report.json",
        "sandbox_task": "sandbox_tasks/path-function-repair-task.json" if verdict == "SANDBOX_TASK_REQUIRED" else None,
        "summary": report.get("summary", {}),
    }


def write_state(root: Path, policy: dict[str, Any], verdict: str, report: dict[str, Any]) -> None:
    locations = policy.get("state_locations", {}) if isinstance(policy.get("state_locations", {}), dict) else {}
    if verdict == "IDLE_READY":
        idle_path = root / locations.get("idle", "idle_sentinels/path-function-sentinel.idle.json")
        write_json(idle_path, state_payload(verdict, report))
    else:
        triggered_path = root / locations.get("triggered", "triggered_loop/path-function-sentinel.triggered.json")
        write_json(triggered_path, state_payload(verdict, report))


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Path Function Sentinel Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Verdict: `{report['verdict']}`",
        "",
        "## Summary",
        "",
    ]

    for key, value in report.get("summary", {}).items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Deficiencies", ""])
    if report.get("deficiencies"):
        for item in report.get("deficiencies", []):
            lines.append(f"- `{item.get('code')}` `{item.get('path')}` — {item.get('detail')}")
    else:
        lines.append("- none")

    lines.extend(["", "## Checks", ""])
    for item in report.get("results", []):
        mark = "✅" if item.get("passed") else "❌"
        lines.append(f"- {mark} `{item.get('check')}` `{item.get('path')}` — {item.get('detail')}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, policy: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    required = [str(item) for item in policy.get("required_directories", [])]
    results: list[dict[str, Any]] = []
    deficiencies: list[dict[str, Any]] = []

    r, d = check_required_dirs(root, required)
    results.extend(r)
    deficiencies.extend(d)

    r, d = check_report_writeability(out_dir)
    results.extend(r)
    deficiencies.extend(d)

    r, d = check_incoming(root)
    results.extend(r)
    deficiencies.extend(d)

    checked = policy.get("checked_queues", {}) if isinstance(policy.get("checked_queues", {}), dict) else {}

    installed_suffixes = checked.get("installed_bundles", {}).get("zip_receipt_suffixes", ["installed"])
    r, d = check_receipts(root, "installed_bundles", installed_suffixes, "installed_bundles_have_installed_receipts", "installed_zip_missing_installed_receipt")
    results.extend(r)
    deficiencies.extend(d)

    failed_suffixes = checked.get("failed_bundles", {}).get("zip_receipt_suffixes", ["failure", "stale"])
    r, d = check_receipts(root, "failed_bundles", failed_suffixes, "failed_bundles_have_failure_or_stale_receipts", "failed_zip_missing_failure_or_stale_receipt")
    results.extend(r)
    deficiencies.extend(d)

    sandbox_suffixes = checked.get("sandbox_queue", {}).get("zip_receipt_suffixes", ["failure", "sandbox", "sandbox-task"])
    r, d = check_receipts(root, "sandbox_queue", sandbox_suffixes, "sandbox_queue_has_sandbox_receipts", "sandbox_zip_missing_sandbox_receipt")
    results.extend(r)
    deficiencies.extend(d)

    privileged_suffixes = checked.get("privileged_queue", {}).get("zip_receipt_suffixes", ["privileged-task"])
    r, d = check_receipts(root, "privileged_queue", privileged_suffixes, "privileged_queue_has_privileged_receipts", "privileged_zip_missing_privileged_receipt")
    results.extend(r)
    deficiencies.extend(d)

    verdict = determine_verdict(deficiencies)

    report = {
        "generated_at": utc_now(),
        "schema": "stegverse.path_function_sentinel_report.v2",
        "formal_milestone": policy.get("formal_milestone", "MS-012H — Path Function Sentinel Sandbox Loop"),
        "sentinel_id": "path-function-sentinel-sandbox-loop-v2",
        "verdict": verdict,
        "summary": {
            "checks_total": len(results),
            "checks_passed": len([item for item in results if item.get("passed")]),
            "checks_failed": len([item for item in results if not item.get("passed")]),
            "deficiencies_total": len(deficiencies),
            "failed_paths": sorted(set(str(item.get("path")) for item in deficiencies)),
        },
        "deficiencies": deficiencies,
        "results": results,
        "sandbox_task_written": verdict == "SANDBOX_TASK_REQUIRED",
        "safety": {
            "bounded_single_pass": True,
            "deleted_evidence": False,
            "moved_bundles": False,
            "edited_workflows": False,
            "created_recursive_trigger": False,
            "repair_requires_sandbox": True,
        },
    }

    write_state(root, policy, verdict, report)

    locations = policy.get("state_locations", {}) if isinstance(policy.get("state_locations", {}), dict) else {}
    if verdict == "SANDBOX_TASK_REQUIRED":
        task = build_sandbox_task(report, policy)
        write_json(root / locations.get("sandbox_task_json", "sandbox_tasks/path-function-repair-task.json"), task)
        write_sandbox_task_markdown(root / locations.get("sandbox_task_md", "sandbox_tasks/path-function-repair-task.md"), task)

    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/path-tests/path-function-sentinel-policy-v2.json")
    parser.add_argument("--out-dir", default="path_function_reports")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, None)
    if policy is None:
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    out_dir = root / args.out_dir
    report = run(root, policy, out_dir)

    locations = policy.get("state_locations", {}) if isinstance(policy.get("state_locations", {}), dict) else {}
    latest_json = root / locations.get("latest_report", "path_function_reports/path-function-sentinel-report.json")
    latest_md = root / locations.get("latest_markdown", "path_function_reports/path-function-sentinel-report.md")

    write_json(latest_json, report)
    write_markdown(latest_md, report)

    print(json.dumps({
        "verdict": report["verdict"],
        "checks_total": report["summary"]["checks_total"],
        "checks_failed": report["summary"]["checks_failed"],
        "deficiencies_total": report["summary"]["deficiencies_total"],
        "sandbox_task_written": report["sandbox_task_written"],
        "failed_paths": report["summary"]["failed_paths"],
    }, indent=2))

    return 0 if report["verdict"] in {"IDLE_READY", "SANDBOX_TASK_REQUIRED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
