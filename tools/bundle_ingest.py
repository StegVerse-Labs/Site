#!/usr/bin/env python3
"""
StegVerse MS-012C bundle ingestion receipt boundary.

A bundle is treated as a proposed repo-state transition:
- fingerprint bundle
- normalize paths
- map dotless workflow paths
- compare file hashes
- apply only changed/missing files
- emit receipt
- append ledger
- update fingerprint index

Standard-library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class FileDecision:
    bundle_path: str
    repo_path: str | None
    action: str
    reason: str
    old_sha256: str | None
    new_sha256: str | None
    bytes: int


@dataclass
class PathMapping:
    bundle_path: str
    repo_path: str
    reason: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return sha256_bytes(path.read_bytes())


def tree_fingerprint(repo_root: Path, include_prefixes: list[str] | None = None) -> str:
    """Compute a stable fingerprint of tracked working-tree files visible to the runner.

    This intentionally skips .git and common report/cache directories.
    """
    skip_prefixes = (
        ".git/",
        "ingestion_reports/",
        "page_contract_reports/",
        "transition_replay_reports/",
        "next_transition_step_reports/",
        "__pycache__/",
    )
    rows: list[str] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        if rel.startswith(skip_prefixes):
            continue
        if include_prefixes and not any(rel.startswith(prefix) for prefix in include_prefixes):
            continue
        digest = sha256_file(path)
        rows.append(f"{digest}  {rel}")
    return sha256_bytes("\n".join(rows).encode("utf-8"))


def changed_files_fingerprint(decisions: list[FileDecision]) -> str:
    rows = []
    for d in decisions:
        if d.action in {"created", "updated", "would_created", "would_updated"}:
            rows.append(f"{d.action} {d.repo_path} {d.old_sha256}->{d.new_sha256}")
    return sha256_bytes("\n".join(sorted(rows)).encode("utf-8"))


def safe_zip_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    p = Path(name)
    if p.is_absolute():
        return False
    if any(part == ".." for part in p.parts):
        return False
    return True


def normalize_repo_path(bundle_path: str) -> tuple[str, PathMapping | None]:
    clean = bundle_path.lstrip("/")
    if clean.startswith(".github/workflows/"):
        return clean, None
    if clean.startswith("github/workflows/"):
        mapped = ".github/workflows/" + clean[len("github/workflows/"):]
        return mapped, PathMapping(
            bundle_path=clean,
            repo_path=mapped,
            reason="mapped dotless upload-safe workflow path to GitHub Actions workflow path",
        )
    return clean, None


def is_protected(repo_path: str, protected: list[str]) -> bool:
    return any(repo_path == prefix.rstrip("/") or repo_path.startswith(prefix) for prefix in protected)


def find_bundle(repo_root: Path, explicit_bundle: str | None) -> Path:
    if explicit_bundle:
        path = repo_root / explicit_bundle
        if not path.exists():
            raise SystemExit(f"Bundle not found: {path}")
        return path

    incoming = repo_root / "incoming"
    bundles = sorted(incoming.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not bundles:
        raise SystemExit("No bundle found. Commit a .zip file under incoming/ or pass --bundle.")
    return bundles[0]


def load_json_if_exists(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")


def ingest_bundle(repo_root: Path, bundle_path: Path, policy_path: Path, apply: bool) -> dict[str, Any]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    protected = list(policy.get("protected_paths", []))

    bundle_bytes = bundle_path.read_bytes()
    bundle_sha256 = sha256_bytes(bundle_bytes)
    before_tree = tree_fingerprint(repo_root)

    decisions: list[FileDecision] = []
    mappings: list[PathMapping] = []
    unsafe_count = 0

    with zipfile.ZipFile(bundle_path, "r") as zf:
        for name in sorted(zf.namelist()):
            if not safe_zip_member(name):
                unsafe_count += 1
                decisions.append(FileDecision(name, None, "skipped", "unsafe path or directory entry", None, None, 0))
                continue

            data = zf.read(name)
            new_hash = sha256_bytes(data)

            if name == "README.md":
                decisions.append(FileDecision(name, None, "skipped", "bundle root README is documentation and is not applied to repo root", None, new_hash, len(data)))
                continue

            repo_rel, mapping = normalize_repo_path(name)
            if mapping:
                mappings.append(mapping)

            old_hash = sha256_file(repo_root / repo_rel)

            if is_protected(repo_rel, protected):
                decisions.append(FileDecision(name, repo_rel, "skipped", "protected path", old_hash, new_hash, len(data)))
                continue

            if old_hash == new_hash:
                decisions.append(FileDecision(name, repo_rel, "unchanged", "target hash already matches", old_hash, new_hash, len(data)))
                continue

            action = "updated" if (repo_root / repo_rel).exists() else "created"
            if apply:
                target = repo_root / repo_rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                decisions.append(FileDecision(name, repo_rel, action, "hash differs or target missing", old_hash, new_hash, len(data)))
            else:
                decisions.append(FileDecision(name, repo_rel, "would_" + action, "dry run; hash differs or target missing", old_hash, new_hash, len(data)))

    after_tree = tree_fingerprint(repo_root)
    changed_fp = changed_files_fingerprint(decisions)

    applied = [d for d in decisions if d.action in {"created", "updated"}]
    would_apply = [d for d in decisions if d.action.startswith("would_")]
    unchanged = [d for d in decisions if d.action == "unchanged"]
    skipped = [d for d in decisions if d.action == "skipped"]

    verdict = "ALLOW"
    if unsafe_count > 0:
        verdict = "ALLOW_WITH_SKIPPED_UNSAFE_PATHS"

    receipt = {
        "generated_at": utc_now(),
        "schema": "stegverse.bundle_ingestion_receipt.v1",
        "formal_milestone": "MS-012C — Ingestion Receipt Boundary",
        "bundle_name": bundle_path.name,
        "bundle_path": str(bundle_path),
        "bundle_sha256": bundle_sha256,
        "mode": "apply" if apply else "dry_run",
        "verdict": verdict,
        "files_seen": len(decisions),
        "files_created": len([d for d in decisions if d.action == "created"]),
        "files_updated": len([d for d in decisions if d.action == "updated"]),
        "files_unchanged": len(unchanged),
        "files_skipped": len(skipped),
        "files_would_apply": len(would_apply),
        "unsafe_paths_rejected": unsafe_count,
        "path_mappings_applied": [asdict(m) for m in mappings],
        "repo_transition": {
            "before_tree_fingerprint": before_tree,
            "after_tree_fingerprint": after_tree,
            "changed_files_fingerprint": changed_fp,
        },
        "decisions": [asdict(d) for d in decisions],
    }

    outputs = policy.get("ledger_outputs", {})
    latest_path = repo_root / outputs.get("latest_receipt", "data/latest-bundle-ingestion-receipt-v1.json")
    ledger_path = repo_root / outputs.get("ledger_jsonl", "data/bundle-ingestion-ledger-v1.jsonl")
    index_path = repo_root / outputs.get("fingerprint_index", "data/bundle-fingerprint-index-v1.json")

    if apply:
        latest_path.parent.mkdir(parents=True, exist_ok=True)
        latest_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        append_jsonl(ledger_path, {
            "generated_at": receipt["generated_at"],
            "bundle_name": receipt["bundle_name"],
            "bundle_sha256": receipt["bundle_sha256"],
            "verdict": receipt["verdict"],
            "changed_files_fingerprint": changed_fp,
            "before_tree_fingerprint": before_tree,
            "after_tree_fingerprint": after_tree,
        })

        index = load_json_if_exists(index_path, {
            "schema": "stegverse.bundle_fingerprint_index.v1",
            "formal_milestone": "MS-012C — Ingestion Receipt Boundary",
            "receipts": [],
        })
        receipts = index.setdefault("receipts", [])
        receipts.append({
            "generated_at": receipt["generated_at"],
            "bundle_name": receipt["bundle_name"],
            "bundle_sha256": receipt["bundle_sha256"],
            "verdict": receipt["verdict"],
            "changed_files_fingerprint": changed_fp,
        })
        index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

    report = {
        "generated_at": receipt["generated_at"],
        "schema": "stegverse.bundle_ingestion_report.v1",
        "bundle": str(bundle_path),
        "policy": str(policy_path),
        "mode": receipt["mode"],
        "receipt": receipt,
        "summary": {
            "total_entries_seen": len(decisions),
            "applied": len(applied),
            "would_apply": len(would_apply),
            "unchanged": len(unchanged),
            "skipped": len(skipped),
            "path_mappings": len(mappings),
            "unsafe_paths_rejected": unsafe_count,
        },
    }
    return report


def write_reports(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bundle-ingestion-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out_dir / "latest-bundle-ingestion-receipt-v1.json").write_text(json.dumps(report["receipt"], indent=2), encoding="utf-8")

    lines = [
        "# Bundle Ingestion Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Mode: `{report['mode']}`",
        f"Bundle: `{report['bundle']}`",
        f"Bundle SHA-256: `{report['receipt']['bundle_sha256']}`",
        f"Verdict: `{report['receipt']['verdict']}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Repo Transition", ""])
    transition = report["receipt"]["repo_transition"]
    for key, value in transition.items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Path Mappings", ""])
    mappings = report["receipt"]["path_mappings_applied"]
    if not mappings:
        lines.append("No path mappings applied.")
    else:
        for m in mappings:
            lines.append(f"- `{m['bundle_path']}` → `{m['repo_path']}` — {m['reason']}")

    lines.extend(["", "## File Decisions", ""])
    for row in report["receipt"]["decisions"]:
        repo_path = row["repo_path"] or "(none)"
        lines.append(f"- `{row['action']}` `{row['bundle_path']}` → `{repo_path}` — {row['reason']}")

    (out_dir / "bundle-ingestion-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle", default=None)
    parser.add_argument("--policy", default="data/bundle-ingestion-policy-v1.json")
    parser.add_argument("--out-dir", default="ingestion_reports")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    bundle_path = find_bundle(repo_root, args.bundle)
    policy_path = repo_root / args.policy

    report = ingest_bundle(repo_root, bundle_path, policy_path, args.apply)
    write_reports(report, repo_root / args.out_dir)
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
