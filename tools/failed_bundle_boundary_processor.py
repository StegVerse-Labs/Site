#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict, Counter
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
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def sha_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stem_key(path: Path) -> str:
    name = path.name
    for suffix in [
        ".stale.json", ".stale.md",
        ".installed.json", ".installed.md",
        ".sandbox.json", ".sandbox.md",
        ".failed.json", ".failed.md",
        ".json", ".md", ".zip"
    ]:
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return path.stem


def read_text_limited(path: Path, limit: int = 20000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    if path.suffix.lower() == ".zip":
        return path.name
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return path.name


def group_failed(folder: Path) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = defaultdict(list)
    if not folder.exists():
        return {}
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.name != "README.md":
            groups[stem_key(path)].append(path)
    return dict(groups)


def classify_group(key: str, files: list[Path], policy: dict[str, Any]) -> tuple[str, str, str]:
    combined = "\n".join([key] + [p.name for p in files] + [read_text_limited(p) for p in files]).lower()
    for rule in policy.get("classification_rules", []):
        for needle in rule.get("contains_any", []):
            if str(needle).lower() in combined:
                return str(rule.get("class")), str(rule.get("route")), str(rule.get("reason"))
    return "unknown", str(policy.get("routes", {}).get("unknown", "failed_bundles")), "no rule matched; evidence remains in failed_bundles"


def copy_group(files: list[Path], dest_dir: Path) -> list[str]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for src in files:
        dest = dest_dir / src.name
        if src.resolve() == dest.resolve():
            copied.append(dest.as_posix())
            continue
        shutil.copy2(src, dest)
        copied.append(dest.as_posix())
    return copied


def write_receipt(dest_dir: Path, key: str, classification: str, reason: str, route: str, files: list[Path], applied: bool) -> tuple[str, str]:
    receipt = {
        "generated_at": utc_now(),
        "schema": "stegverse.failed_bundle_boundary_receipt.v1",
        "bundle_group": key,
        "classification": classification,
        "reason": reason,
        "route": route,
        "applied": applied,
        "source_files": [
            {
                "path": p.as_posix(),
                "sha256": sha_file(p),
                "size_bytes": p.stat().st_size if p.exists() else None
            }
            for p in files
        ],
        "safety": {
            "deleted_source": False,
            "direct_install": False,
            "workflow_mutation": False
        }
    }
    json_path = dest_dir / f"{key}.boundary.json"
    md_path = dest_dir / f"{key}.boundary.md"
    write_json(json_path, receipt)
    lines = [
        "# Failed Bundle Boundary Receipt",
        "",
        f"Generated: `{receipt['generated_at']}`",
        f"Bundle group: `{key}`",
        f"Classification: `{classification}`",
        f"Route: `{route}`",
        f"Applied: `{applied}`",
        "",
        "## Reason",
        "",
        reason,
        "",
        "## Source Files",
        ""
    ]
    for item in receipt["source_files"]:
        lines.append(f"- `{item['path']}` sha256=`{item['sha256']}`")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path.as_posix(), md_path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/transition-table/failed-bundle-boundary-policy-v1.json")
    parser.add_argument("--out-dir", default="transition_discovery_reports")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, None)
    if not isinstance(policy, dict):
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    source_dir = root / str(policy.get("source_dir", "failed_bundles"))
    groups = group_failed(source_dir)

    results = []
    for key, files in groups.items():
        classification, route, reason = classify_group(key, files, policy)
        dest_dir = root / route
        copied = []
        receipt_paths = []
        if args.apply and route != "failed_bundles":
            copied = copy_group(files, dest_dir)
            receipt_paths = list(write_receipt(dest_dir, key, classification, reason, route, files, True))
        else:
            receipt_paths = list(write_receipt(root / args.out_dir, key, classification, reason, route, files, False))

        results.append({
            "bundle_group": key,
            "classification": classification,
            "route": route,
            "reason": reason,
            "applied": bool(args.apply and route != "failed_bundles"),
            "source_files": [p.as_posix() for p in files],
            "copied_files": copied,
            "receipt_paths": receipt_paths
        })

    counts = Counter(item["classification"] for item in results)
    route_counts = Counter(item["route"] for item in results)
    report = {
        "generated_at": utc_now(),
        "schema": "stegverse.failed_bundle_boundary_report.v1",
        "policy_id": policy.get("policy_id"),
        "applied": args.apply,
        "summary": {
            "groups_total": len(results),
            "classification_counts": dict(sorted(counts.items())),
            "route_counts": dict(sorted(route_counts.items()))
        },
        "results": results
    }

    out_dir = root / args.out_dir
    write_json(out_dir / "failed-bundle-boundary-report.json", report)

    md = [
        "# Failed Bundle Boundary Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Applied: `{args.apply}`",
        "",
        "## Summary",
        "",
        f"- groups_total: `{len(results)}`",
        ""
    ]
    for k, v in sorted(counts.items()):
        md.append(f"- `{k}`: `{v}`")
    md.extend(["", "## Routes", ""])
    for k, v in sorted(route_counts.items()):
        md.append(f"- `{k}`: `{v}`")
    md.extend(["", "## Results", ""])
    for item in results:
        md.append(f"- `{item['classification']}` `{item['bundle_group']}` → `{item['route']}` — {item['reason']}")
    (out_dir / "failed-bundle-boundary-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
