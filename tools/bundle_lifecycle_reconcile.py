#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def get_json_path(obj: Any, path: str) -> Any:
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def file_status(path: Path) -> dict[str, Any]:
    return {
        "path": path.as_posix(),
        "exists": path.exists(),
        "is_file": path.is_file() if path.exists() else False,
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
    }


def find_bundle_evidence(root: Path, bundle_names: list[str], dirs: dict[str, str]) -> dict[str, Any]:
    evidence = {
        "incoming": [],
        "installed": [],
        "failed": [],
        "sandbox": [],
        "privileged": [],
        "installed_receipts": [],
        "failed_receipts": [],
        "sandbox_receipts": [],
        "privileged_receipts": [],
    }

    search_dirs = {
        "incoming": dirs.get("incoming", "incoming"),
        "installed": dirs.get("installed", "installed_bundles"),
        "failed": dirs.get("failed", "failed_bundles"),
        "sandbox": dirs.get("sandbox", "sandbox_queue"),
        "privileged": dirs.get("privileged", "privileged_queue"),
    }

    stems = {Path(name).stem for name in bundle_names}

    for key, rel_dir in search_dirs.items():
        folder = root / rel_dir
        if not folder.exists():
            continue

        for name in bundle_names:
            candidate = folder / name
            if candidate.exists():
                evidence[key].append(candidate.as_posix())

        for stem in stems:
            for receipt in sorted(folder.glob(f"{stem}*.json")):
                receipt_key = f"{key}_receipts"
                if receipt_key in evidence:
                    evidence[receipt_key].append(receipt.as_posix())

            for receipt in sorted(folder.glob(f"{stem}*.md")):
                receipt_key = f"{key}_receipts"
                if receipt_key in evidence:
                    evidence[receipt_key].append(receipt.as_posix())

    return evidence


def validate_markers(root: Path, markers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for marker in markers:
        path = root / str(marker.get("path", ""))
        obj = load_json(path, None)
        actual = None if obj is None else get_json_path(obj, str(marker.get("json_path", "")))
        contains = marker.get("contains")
        passed = actual is not None and str(contains) in str(actual)
        results.append({
            "path": marker.get("path"),
            "json_path": marker.get("json_path"),
            "contains": contains,
            "actual": actual,
            "passed": passed,
        })
    return results


def classify(targets: list[dict[str, Any]], evidence: dict[str, Any], archive_files: list[dict[str, Any]]) -> tuple[str, list[str]]:
    target_count = len(targets)
    present_count = len([item for item in targets if item["exists"]])
    all_targets_present = target_count > 0 and present_count == target_count
    some_targets_present = 0 < present_count < target_count
    no_targets_present = present_count == 0

    installed_archive_present = any(evidence.get("installed", []))
    installed_receipt_present = bool(evidence.get("installed_receipts", [])) or any(item["exists"] for item in archive_files if item["path"].endswith(".installed.json"))
    failed_present = bool(evidence.get("failed", [])) or bool(evidence.get("failed_receipts", []))

    reasons = []

    if all_targets_present:
        reasons.append("all_target_files_present")
    elif some_targets_present:
        reasons.append("some_target_files_present")
    elif no_targets_present:
        reasons.append("no_target_files_present")

    if installed_archive_present:
        reasons.append("installed_archive_present")
    else:
        reasons.append("installed_archive_missing")

    if installed_receipt_present:
        reasons.append("installed_receipt_present")
    else:
        reasons.append("installed_receipt_missing")

    if failed_present:
        reasons.append("failed_bundle_or_receipt_present")
    else:
        reasons.append("no_failed_bundle_or_receipt_present")

    if all_targets_present and installed_archive_present and installed_receipt_present:
        return "installed_verified", reasons

    if all_targets_present and failed_present and (not installed_archive_present or not installed_receipt_present):
        return "conflicted", reasons

    if all_targets_present and (not installed_archive_present or not installed_receipt_present):
        return "files_present_but_archive_missing", reasons

    if some_targets_present:
        return "partially_installed", reasons

    if no_targets_present and failed_present:
        return "failed_only", reasons

    return "missing", reasons


def reconcile(root: Path, subject: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    dirs = policy.get("evidence_dirs", {}) if isinstance(policy.get("evidence_dirs", {}), dict) else {}
    target_files = [str(item) for item in subject.get("target_files", [])]
    bundle_names = [str(item) for item in subject.get("bundle_names", [])]
    archive_paths = [str(item) for item in subject.get("expected_installed_archive_files", [])]

    targets = [file_status(root / path) for path in target_files]
    archive_files = [file_status(root / path) for path in archive_paths]
    evidence = find_bundle_evidence(root, bundle_names, dirs)
    marker_results = validate_markers(root, subject.get("required_schema_markers", []))

    lifecycle_status, reasons = classify(targets, evidence, archive_files)

    marker_failures = [item for item in marker_results if not item["passed"]]
    if marker_failures and lifecycle_status == "installed_verified":
        lifecycle_status = "conflicted"
        reasons.append("required_schema_marker_failed")

    return {
        "generated_at": utc_now(),
        "schema": "stegverse.bundle_lifecycle_report.v1",
        "formal_milestone": subject.get("formal_milestone"),
        "subject_id": subject.get("subject_id"),
        "lifecycle_status": lifecycle_status,
        "reason_codes": reasons,
        "target_files": targets,
        "expected_installed_archive_files": archive_files,
        "bundle_evidence": evidence,
        "schema_marker_checks": marker_results,
        "policy_id": policy.get("policy_id"),
        "known_issue": subject.get("known_issue"),
        "interpretation": interpret(lifecycle_status),
    }


def interpret(status: str) -> str:
    if status == "installed_verified":
        return "Target files and installed archive evidence agree."
    if status == "files_present_but_archive_missing":
        return "Target files exist, but bundle lifecycle archive is incomplete."
    if status == "conflicted":
        return "Target files exist while failed evidence is present and installed archive evidence is incomplete."
    if status == "failed_only":
        return "Failed bundle evidence exists but target files are absent."
    if status == "partially_installed":
        return "Only some target files exist."
    if status == "missing":
        return "No target files or bundle evidence were found."
    return "Unknown lifecycle status."


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Bundle Lifecycle Reconciliation Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Subject: `{report.get('subject_id')}`",
        f"Milestone: `{report.get('formal_milestone')}`",
        f"Lifecycle status: `{report.get('lifecycle_status')}`",
        "",
        "## Interpretation",
        "",
        report.get("interpretation", ""),
        "",
        "## Reason Codes",
        "",
    ]

    for reason in report.get("reason_codes", []):
        lines.append(f"- `{reason}`")

    lines.extend(["", "## Target Files", ""])
    for item in report.get("target_files", []):
        mark = "✅" if item.get("exists") else "❌"
        lines.append(f"- {mark} `{item.get('path')}`")

    lines.extend(["", "## Expected Installed Archive Files", ""])
    for item in report.get("expected_installed_archive_files", []):
        mark = "✅" if item.get("exists") else "❌"
        lines.append(f"- {mark} `{item.get('path')}`")

    lines.extend(["", "## Bundle Evidence", ""])
    for key, values in report.get("bundle_evidence", {}).items():
        lines.append(f"### {key}")
        if values:
            for value in values:
                lines.append(f"- `{value}`")
        else:
            lines.append("- none")
        lines.append("")

    lines.extend(["## Schema Marker Checks", ""])
    for item in report.get("schema_marker_checks", []):
        mark = "✅" if item.get("passed") else "❌"
        lines.append(f"- {mark} `{item.get('path')}` `{item.get('json_path')}` contains `{item.get('contains')}`; actual=`{item.get('actual')}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", default="data/lifecycle/ms012f-lifecycle-subject-v1.json")
    parser.add_argument("--policy", default="data/lifecycle/bundle-lifecycle-reconciliation-policy-v1.json")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out-dir", default="lifecycle_reports")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    subject = load_json(root / args.subject, None)
    if subject is None:
        raise SystemExit(f"Missing or invalid subject: {args.subject}")
    policy = load_json(root / args.policy, None)
    if policy is None:
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    report = reconcile(root, subject, policy)
    out_dir = root / args.out_dir
    write_json(out_dir / "bundle-lifecycle-report.json", report)
    write_markdown(out_dir / "bundle-lifecycle-report.md", report)

    print(json.dumps({
        "subject_id": report["subject_id"],
        "lifecycle_status": report["lifecycle_status"],
        "interpretation": report["interpretation"],
    }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
