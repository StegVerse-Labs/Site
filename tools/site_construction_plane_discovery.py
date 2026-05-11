#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAL_MILESTONE = "MS-012K.2 — Site Construction Plane Discovery Report"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists() or not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def matches_pattern(repo_path: str, pattern: str) -> bool:
    if not repo_path or not pattern:
        return False
    if pattern.endswith("/"):
        return repo_path.startswith(pattern)
    return repo_path == pattern


def categories_for_path(repo_path: str, authority_map: dict[str, Any]) -> list[dict[str, Any]]:
    matched = []
    for name, meta in authority_map.get("path_categories", {}).items():
        for pattern in meta.get("patterns", []):
            if matches_pattern(repo_path, str(pattern)):
                matched.append({"name": name, **meta})
                break
    return matched


def classify_path(repo_path: str, authority_map: dict[str, Any]) -> dict[str, Any]:
    categories = categories_for_path(repo_path, authority_map)
    names = [item["name"] for item in categories]

    if not categories:
        verdict = "UNMAPPED_PATH_CATEGORY"
        reason = "No path category currently covers this path."
    elif any(item.get("authority_class") == "forbidden_internal_surface" for item in categories):
        verdict = "FORBIDDEN_INTERNAL_SURFACE"
        reason = "Path maps to a forbidden internal surface."
    elif any(item.get("human_approval_required") is True for item in categories):
        verdict = "HUMAN_APPROVAL_REQUIRED"
        reason = "At least one mapped path category requires human approval."
    elif any(item.get("sandbox_required") is True for item in categories):
        verdict = "SANDBOX_REQUIRED"
        reason = "At least one mapped path category requires sandbox review."
    elif any(item.get("routine_allowed") == "conditional" or item.get("human_approval_required") == "conditional" for item in categories):
        verdict = "CONDITIONAL"
        reason = "At least one mapped path category is conditional."
    else:
        verdict = "ROUTINE_ALLOWED"
        reason = "Mapped path categories are routine allowed."

    return {
        "path": repo_path,
        "verdict": verdict,
        "reason": reason,
        "categories": names,
        "authority_classes": sorted(set(str(item.get("authority_class")) for item in categories if item.get("authority_class"))),
        "sandbox_required": any(item.get("sandbox_required") is True for item in categories),
        "human_approval_required": any(item.get("human_approval_required") is True for item in categories),
    }


def add_path(paths: list[dict[str, Any]], path: str | None, source: str, source_kind: str, action_class: str | None = None, result: str | None = None) -> None:
    if not path:
        return
    paths.append({
        "path": str(path),
        "source": source,
        "source_kind": source_kind,
        "action_class": action_class,
        "result": result,
    })


def collect_ingestion_paths(root: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for rel in policy.get("inputs", {}).get("ingestion_reports", []):
        obj = load_json(root / rel, None)
        if not isinstance(obj, dict):
            continue

        reports = obj.get("reports") if isinstance(obj.get("reports"), list) else [obj]
        for report in reports:
            if not isinstance(report, dict):
                continue

            receipt = report.get("receipt", {})
            if not isinstance(receipt, dict):
                continue

            verdict = str(receipt.get("verdict", ""))
            route = str(receipt.get("route", ""))
            bundle = receipt.get("bundle_name") or receipt.get("file_name")
            action_class = infer_action_from_receipt(receipt)

            if bundle:
                if route == "ingest":
                    add_path(rows, f"installed_bundles/{bundle}", rel, "ingestion", action_class, verdict)
                elif route:
                    route_path = route if route.endswith("/") else route + "/"
                    add_path(rows, f"{route_path}{bundle}", rel, "ingestion", action_class, verdict)

            for decision in receipt.get("decisions", []):
                if isinstance(decision, dict):
                    add_path(rows, decision.get("repo_path"), rel, "ingestion_decision", action_class, decision.get("action"))

    return rows


def infer_action_from_receipt(receipt: dict[str, Any]) -> str:
    verdict = str(receipt.get("verdict", ""))
    route = str(receipt.get("route", ""))
    bundle_class = str(receipt.get("bundle_class", ""))

    if verdict == "ALLOW" and route == "ingest":
        return "archive_installed_bundle"
    if route == "failed_bundles" or "STALE" in verdict or "FAIL" in verdict:
        return "quarantine_stale_or_failed"
    if route == "sandbox_queue" or verdict == "SANDBOX_REQUIRED":
        return "hold_for_sandbox"
    if route == "privileged_queue" or verdict == "PRIVILEGED_EXECUTOR_REQUIRED" or "workflow" in bundle_class:
        return "prepare_privileged_review"
    return "observe_state"


def collect_sandbox_paths(root: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    sandbox_dir = root / policy.get("inputs", {}).get("sandbox_report_dir", "sandbox_reports")
    if not sandbox_dir.exists():
        return rows

    for path in sorted(sandbox_dir.glob("*.json")):
        obj = load_json(path, None)
        if not isinstance(obj, dict):
            continue

        reports = obj.get("reports") if obj.get("schema") == "stegverse.ephemeral_sandbox_queue_report.v1" else [obj]
        if not isinstance(reports, list):
            continue

        for report in reports:
            if not isinstance(report, dict):
                continue

            bundle = report.get("bundle_name")
            classification = str(report.get("classification", ""))
            action_class = infer_action_from_sandbox(report)

            if bundle:
                add_path(rows, f"sandbox_reviewed/{bundle}", path.as_posix(), "sandbox", action_class, classification)
                stem = Path(str(bundle)).stem
                add_path(rows, f"sandbox_reports/{stem}.sandbox-report.json", path.as_posix(), "sandbox_report", action_class, classification)
                add_path(rows, f"sandbox_reports/{stem}.sandbox-report.md", path.as_posix(), "sandbox_report", action_class, classification)

            candidate = report.get("candidate_path")
            if candidate:
                candidate_text = str(candidate)
                marker = "/incoming/"
                if marker in candidate_text:
                    add_path(rows, "incoming/" + candidate_text.split(marker, 1)[1], path.as_posix(), "sandbox_candidate", action_class, classification)
                elif candidate_text.startswith("incoming/"):
                    add_path(rows, candidate_text, path.as_posix(), "sandbox_candidate", action_class, classification)

    return rows


def infer_action_from_sandbox(report: dict[str, Any]) -> str:
    classification = str(report.get("classification", ""))
    verdict = str(report.get("verdict", ""))
    if classification == "repair_candidate_created" or verdict == "ALLOW_REENTRY":
        return "construct_sandbox_candidate"
    if classification == "privileged_review_required":
        return "prepare_privileged_review"
    if classification in {"unrepairable", "invalid_zip"}:
        return "quarantine_stale_or_failed"
    return "observe_state"


def collect_authority_paths(root: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    rel = policy.get("inputs", {}).get("transition_authority_report", "transition_authority_reports/transition-authority-audit-report.json")
    obj = load_json(root / rel, None)
    if not isinstance(obj, dict):
        return rows

    for audit in obj.get("audits", []):
        if not isinstance(audit, dict):
            continue
        action_class = audit.get("action_class")
        result = audit.get("verdict")
        for path in audit.get("paths", []):
            add_path(rows, str(path), rel, "authority_audit", action_class, result)

    return rows


def collect_discovery_paths(root: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    rel = policy.get("inputs", {}).get("transition_discovery_ledger", "transition_discovery_reports/transition-discovery-ledger.json")
    obj = load_json(root / rel, None)
    if not isinstance(obj, dict):
        return rows

    for entry in obj.get("entries", []):
        if not isinstance(entry, dict):
            continue
        add_path(
            rows,
            entry.get("observed_path"),
            rel,
            "transition_discovery",
            entry.get("action_class_unlocked"),
            entry.get("result"),
        )

    return rows


def merge_classifications(rows: list[dict[str, Any]], authority_map: dict[str, Any]) -> list[dict[str, Any]]:
    merged = {}
    for row in rows:
        path = row["path"]
        base = merged.setdefault(path, {
            **classify_path(path, authority_map),
            "observations": [],
        })
        base["observations"].append({
            "source": row.get("source"),
            "source_kind": row.get("source_kind"),
            "action_class": row.get("action_class"),
            "result": row.get("result"),
        })
    return sorted(merged.values(), key=lambda item: item["path"])


def summarize(classified: list[dict[str, Any]]) -> dict[str, Any]:
    verdict_counts = Counter(item["verdict"] for item in classified)
    category_counts = Counter()
    authority_class_counts = Counter()
    source_kind_counts = Counter()

    for item in classified:
        for cat in item.get("categories", []):
            category_counts[cat] += 1
        for cls in item.get("authority_classes", []):
            authority_class_counts[cls] += 1
        for obs in item.get("observations", []):
            source_kind_counts[str(obs.get("source_kind"))] += 1

    return {
        "paths_total": len(classified),
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "category_counts": dict(sorted(category_counts.items())),
        "authority_class_counts": dict(sorted(authority_class_counts.items())),
        "source_kind_counts": dict(sorted(source_kind_counts.items())),
        "sandbox_required_paths": sum(1 for item in classified if item.get("sandbox_required")),
        "human_approval_required_paths": sum(1 for item in classified if item.get("human_approval_required")),
        "unmapped_paths": sum(1 for item in classified if item.get("verdict") == "UNMAPPED_PATH_CATEGORY"),
        "forbidden_paths": sum(1 for item in classified if item.get("verdict") == "FORBIDDEN_INTERNAL_SURFACE"),
    }


def write_inventory_md(path: Path, classified: list[dict[str, Any]]) -> None:
    lines = [
        "# Site Construction Path Inventory",
        "",
    ]
    if not classified:
        lines.append("No construction paths were found in available reports.")
    else:
        for item in classified:
            lines.append(
                f"- `{item.get('verdict')}` `{item.get('path')}` "
                f"categories=`{', '.join(item.get('categories', [])) or 'none'}` "
                f"authority=`{', '.join(item.get('authority_classes', [])) or 'none'}`"
            )
            for obs in item.get("observations", [])[:5]:
                lines.append(
                    f"  - source=`{obs.get('source_kind')}` action=`{obs.get('action_class')}` result=`{obs.get('result')}`"
                )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report_md(path: Path, report: dict[str, Any]) -> None:
    summary = report.get("summary", {})
    lines = [
        "# Site Construction Plane Discovery Report",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Policy: `{report.get('policy_id')}`",
        f"Authority map: `{report.get('authority_map_id')}`",
        "",
        "## Summary",
        "",
        f"- `paths_total`: `{summary.get('paths_total')}`",
        f"- `sandbox_required_paths`: `{summary.get('sandbox_required_paths')}`",
        f"- `human_approval_required_paths`: `{summary.get('human_approval_required_paths')}`",
        f"- `unmapped_paths`: `{summary.get('unmapped_paths')}`",
        f"- `forbidden_paths`: `{summary.get('forbidden_paths')}`",
        "",
        "## Verdict Counts",
        "",
    ]

    for key, value in summary.get("verdict_counts", {}).items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Category Counts", ""])
    for key, value in summary.get("category_counts", {}).items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Findings", ""])
    findings = report.get("findings", [])
    if not findings:
        lines.append("No construction-plane issues detected from available reports.")
    else:
        for finding in findings:
            lines.append(f"- `{finding.get('severity')}` `{finding.get('path')}` — {finding.get('message')}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_findings(classified: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings = []
    for item in classified:
        verdict = item.get("verdict")
        if verdict == "FORBIDDEN_INTERNAL_SURFACE":
            findings.append({
                "severity": "fail_closed",
                "path": item.get("path"),
                "message": "Path maps to forbidden internal surface."
            })
        elif verdict == "UNMAPPED_PATH_CATEGORY":
            findings.append({
                "severity": "needs_transition_candidate",
                "path": item.get("path"),
                "message": "Path is not covered by current path categories."
            })
        elif verdict == "HUMAN_APPROVAL_REQUIRED":
            findings.append({
                "severity": "human_approval_required",
                "path": item.get("path"),
                "message": "Path category requires human approval before mutation."
            })
        elif verdict == "SANDBOX_REQUIRED":
            findings.append({
                "severity": "sandbox_required",
                "path": item.get("path"),
                "message": "Path category requires sandbox review."
            })
        elif verdict == "CONDITIONAL":
            findings.append({
                "severity": "conditional",
                "path": item.get("path"),
                "message": "Path category is conditionally allowed; verify action class and receipt."
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/transition-table/site-construction-plane-discovery-policy-v1.json")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, None)
    if not isinstance(policy, dict):
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    authority_map_path = policy.get("inputs", {}).get("authority_map", "data/transition-table/transition-element-action-authority-map-v1.json")
    authority_map = load_json(root / authority_map_path, None)
    if not isinstance(authority_map, dict):
        raise SystemExit(f"Missing or invalid authority map: {authority_map_path}")

    rows = []
    rows.extend(collect_ingestion_paths(root, policy))
    rows.extend(collect_sandbox_paths(root, policy))
    rows.extend(collect_authority_paths(root, policy))
    rows.extend(collect_discovery_paths(root, policy))

    classified = merge_classifications(rows, authority_map)
    summary = summarize(classified)
    findings = build_findings(classified)

    report = {
        "schema": "stegverse.site_construction_plane_discovery_report.v1",
        "generated_at": utc_now(),
        "policy_id": policy.get("policy_id"),
        "formal_milestone": FORMAL_MILESTONE,
        "authority_map_id": authority_map.get("map_id"),
        "summary": summary,
        "findings": findings,
        "safety": policy.get("safety", {}),
    }
    inventory = {
        "schema": "stegverse.site_construction_path_inventory.v1",
        "generated_at": utc_now(),
        "policy_id": policy.get("policy_id"),
        "authority_map_id": authority_map.get("map_id"),
        "paths": classified,
    }

    outputs = policy.get("outputs", {})
    write_json(root / outputs.get("report_json", "transition_discovery_reports/site-construction-plane-discovery-report.json"), report)
    write_report_md(root / outputs.get("report_md", "transition_discovery_reports/site-construction-plane-discovery-report.md"), report)
    write_json(root / outputs.get("path_inventory_json", "transition_discovery_reports/site-construction-path-inventory.json"), inventory)
    write_inventory_md(root / outputs.get("path_inventory_md", "transition_discovery_reports/site-construction-path-inventory.md"), classified)

    print(json.dumps(summary, indent=2))
    return 0 if summary.get("forbidden_paths", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
