#!/usr/bin/env python3
"""
StegVerse upload-safe bundle ingestion engine.

Purpose:
- Stop manual file-by-file comparison.
- Ingest a zip bundle committed under incoming/.
- Compare target files by SHA-256.
- Apply only missing/changed files.
- Map dotless workflow paths from github/workflows/ to .github/workflows/.

Standard-library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return sha256_bytes(path.read_bytes())


def safe_zip_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    path = Path(name)
    if path.is_absolute():
        return False
    if any(part == ".." for part in path.parts):
        return False
    return True


def normalize_repo_path(bundle_path: str) -> str:
    clean = bundle_path.lstrip("/")
    if clean.startswith(".github/workflows/"):
        return clean
    if clean.startswith("github/workflows/"):
        return ".github/workflows/" + clean[len("github/workflows/"):]
    return clean


def is_protected(repo_path: str, protected_prefixes: list[str]) -> bool:
    return any(repo_path == prefix.rstrip("/") or repo_path.startswith(prefix) for prefix in protected_prefixes)


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


def load_manifest(zf: zipfile.ZipFile) -> dict[str, Any] | None:
    for candidate in ("bundle-manifest.json", "manifest.json", "data/bundle-manifest.json"):
        if candidate in zf.namelist():
            try:
                return json.loads(zf.read(candidate).decode("utf-8"))
            except Exception:
                return None
    return None


def ingest_bundle(repo_root: Path, bundle_path: Path, apply: bool, policy_path: Path) -> dict[str, Any]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    protected = list(policy.get("protected_paths", []))

    decisions: list[FileDecision] = []
    with zipfile.ZipFile(bundle_path, "r") as zf:
        manifest = load_manifest(zf)
        names = sorted(zf.namelist())

        for name in names:
            if not safe_zip_member(name):
                decisions.append(FileDecision(name, None, "skipped", "unsafe or directory entry", None, None, 0))
                continue

            # Do not ingest README from the bundle as a repo replacement unless explicitly nested elsewhere.
            # It is usually human guidance for the uploaded bundle, not target repo content.
            if name == "README.md":
                data = zf.read(name)
                decisions.append(FileDecision(name, None, "skipped", "bundle README is not applied to repo root", None, sha256_bytes(data), len(data)))
                continue

            repo_rel = normalize_repo_path(name)
            if is_protected(repo_rel, protected):
                data = zf.read(name)
                decisions.append(FileDecision(name, repo_rel, "skipped", "protected path", sha256_file(repo_root / repo_rel), sha256_bytes(data), len(data)))
                continue

            data = zf.read(name)
            target = repo_root / repo_rel
            old_hash = sha256_file(target)
            new_hash = sha256_bytes(data)

            if old_hash == new_hash:
                decisions.append(FileDecision(name, repo_rel, "unchanged", "target hash already matches", old_hash, new_hash, len(data)))
                continue

            action = "updated" if target.exists() else "created"
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)

            decisions.append(FileDecision(name, repo_rel, action if apply else "would_" + action, "hash differs or target missing", old_hash, new_hash, len(data)))

    applied = [d for d in decisions if d.action in {"created", "updated"}]
    skipped = [d for d in decisions if d.action == "skipped"]
    unchanged = [d for d in decisions if d.action == "unchanged"]
    would_apply = [d for d in decisions if d.action.startswith("would_")]

    return {
        "generated_at": utc_now(),
        "schema": "stegverse.bundle_ingestion_report.v1",
        "bundle": str(bundle_path),
        "policy": str(policy_path),
        "mode": "apply" if apply else "dry_run",
        "manifest_seen": manifest is not None,
        "summary": {
            "total_entries_seen": len(decisions),
            "applied": len(applied),
            "would_apply": len(would_apply),
            "unchanged": len(unchanged),
            "skipped": len(skipped)
        },
        "decisions": [asdict(d) for d in decisions]
    }


def write_reports(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bundle-ingestion-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Bundle Ingestion Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Bundle: `{report['bundle']}`",
        f"Mode: `{report['mode']}`",
        f"Manifest seen: `{str(report['manifest_seen']).lower()}`",
        "",
        "## Summary",
        "",
    ]

    for key, value in report["summary"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Decisions", ""])
    for row in report["decisions"]:
        repo_path = row["repo_path"] or "(none)"
        lines.append(f"- `{row['action']}` `{row['bundle_path']}` → `{repo_path}` — {row['reason']}")

    (out_dir / "bundle-ingestion-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest an upload-safe bundle into the repository.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle", default=None, help="Path to bundle relative to repo root. Defaults to newest incoming/*.zip.")
    parser.add_argument("--policy", default="data/bundle-ingestion-policy-v1.json")
    parser.add_argument("--out-dir", default="ingestion_reports")
    parser.add_argument("--apply", action="store_true", help="Apply changes. Without this flag, dry-run only.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    policy_path = repo_root / args.policy
    bundle_path = find_bundle(repo_root, args.bundle)

    report = ingest_bundle(repo_root, bundle_path, args.apply, policy_path)
    write_reports(report, repo_root / args.out_dir)

    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
