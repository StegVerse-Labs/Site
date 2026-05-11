#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
    if pattern.endswith("/"):
        return repo_path.startswith(pattern)
    return repo_path == pattern or repo_path.startswith(pattern.rstrip("/") + "/")


def categories_for_path(repo_path: str, authority_map: dict[str, Any]) -> list[str]:
    categories = []
    for name, meta in authority_map.get("path_categories", {}).items():
        for pattern in meta.get("patterns", []):
            if matches_pattern(repo_path, str(pattern)):
                categories.append(name)
                break
    return categories


def classify_path(repo_path: str, authority_map: dict[str, Any]) -> dict[str, Any]:
    cats = categories_for_path(repo_path, authority_map)
    meta = [authority_map.get("path_categories", {}).get(cat, {}) for cat in cats]

    if not cats:
        verdict = "UNMAPPED_PATH_CATEGORY"
        reason = "No path category currently covers this path."
    elif any(m.get("authority_class") == "forbidden_internal_surface" for m in meta):
        verdict = "FORBIDDEN_INTERNAL_SURFACE"
        reason = "Path maps to forbidden internal surface."
    elif any(m.get("human_approval_required") is True for m in meta):
        verdict = "HUMAN_APPROVAL_REQUIRED"
        reason = "At least one mapped path category requires human approval."
    elif any(m.get("sandbox_required") is True for m in meta):
        verdict = "SANDBOX_REQUIRED"
        reason = "At least one mapped path category requires sandbox review."
    elif any(m.get("routine_allowed") == "conditional" for m in meta):
        verdict = "CONDITIONAL"
        reason = "At least one mapped path category is conditionally allowed."
    else:
        verdict = "ROUTINE_ALLOWED"
        reason = "Mapped categories are routine allowed."

    return {
        "path": repo_path,
        "categories": cats,
        "authority_classes": [m.get("authority_class") for m in meta],
        "verdict": verdict,
        "reason": reason,
        "sandbox_required": any(m.get("sandbox_required") is True for m in meta),
        "human_approval_required": any(m.get("human_approval_required") is True for m in meta),
    }


def collect_paths(root: Path) -> list[str]:
    candidate_files = []
    for rel in [
        "ingestion_reports/bundle-ingestion-report.json",
        "ingestion_reports/bundle-queue-report.json",
    ]:
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
            for decision in receipt.get("decisions", []):
                if isinstance(decision, dict) and decision.get("repo_path"):
                    candidate_files.append(str(decision["repo_path"]))

    return sorted(set(candidate_files))


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Site Path Category Authority Audit",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Map: `{report.get('map_id')}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in report.get("summary", {}).items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Path Classifications", ""])
    for item in report.get("paths", []):
        lines.append(f"- `{item.get('verdict')}` `{item.get('path')}` categories=`{', '.join(item.get('categories', [])) or 'none'}` — {item.get('reason')}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--authority-map", default="data/transition-table/transition-element-action-authority-map-v1.json")
    parser.add_argument("--out-dir", default="transition_authority_reports")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    authority_map = load_json(root / args.authority_map, None)
    if not isinstance(authority_map, dict):
        raise SystemExit(f"Missing or invalid authority map: {args.authority_map}")

    paths = sorted(set(args.path or collect_paths(root)))
    classified = [classify_path(path, authority_map) for path in paths]

    summary = {
        "paths_total": len(classified),
        "routine_allowed": sum(1 for x in classified if x["verdict"] == "ROUTINE_ALLOWED"),
        "conditional": sum(1 for x in classified if x["verdict"] == "CONDITIONAL"),
        "sandbox_required": sum(1 for x in classified if x["sandbox_required"]),
        "human_approval_required": sum(1 for x in classified if x["human_approval_required"]),
        "unmapped": sum(1 for x in classified if x["verdict"] == "UNMAPPED_PATH_CATEGORY"),
        "forbidden": sum(1 for x in classified if x["verdict"] == "FORBIDDEN_INTERNAL_SURFACE"),
    }

    report = {
        "schema": "stegverse.site_path_category_authority_audit.v1",
        "generated_at": utc_now(),
        "map_id": authority_map.get("map_id"),
        "summary": summary,
        "paths": classified,
    }

    out = root / args.out_dir
    write_json(out / "site-path-category-authority-audit.json", report)
    write_markdown(out / "site-path-category-authority-audit.md", report)

    print(json.dumps(summary, indent=2))
    return 0 if summary["forbidden"] == 0 and summary["unmapped"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
