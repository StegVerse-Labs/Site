#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
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


@dataclass
class PathMapping:
    bundle_path: str
    repo_path: str
    reason: str


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha_b(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_f(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return sha_b(path.read_bytes())


def load(path: Path, default: Any = None) -> Any:
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


def tree_fp(root: Path) -> str:
    skip = (".git/", "ingestion_reports/", "dependency_reports/", "sandbox_reports/", "__pycache__/")
    rows = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(skip):
            continue
        rows.append(f"{sha_f(path)}  {rel}")
    return sha_b("\n".join(rows).encode("utf-8"))


def changed_fp(decisions: list[FileDecision]) -> str:
    rows = [
        f"{d.action} {d.repo_path} {d.old_sha256}->{d.new_sha256}"
        for d in decisions
        if d.action in {"created", "updated", "would_created", "would_updated"}
    ]
    return sha_b("\n".join(sorted(rows)).encode("utf-8"))


def safe_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    p = Path(name)
    return not p.is_absolute() and ".." not in p.parts


def artifact_mapping(name: str, policy: dict[str, Any]) -> PathMapping | None:
    clean = name.lstrip("/")
    for item in policy.get("artifact_file_mappings", []):
        if clean == item.get("bundle_path"):
            return PathMapping(clean, str(item["repo_path"]), str(item.get("reason", "known artifact report routed")))
    return None


def normalize_path(name: str, policy: dict[str, Any]) -> tuple[str, PathMapping | None]:
    clean = name.lstrip("/")
    artifact = artifact_mapping(clean, policy)
    if artifact:
        return artifact.repo_path, artifact
    if clean.startswith("github/workflows/"):
        mapped = ".github/workflows/" + clean[len("github/workflows/"):]
        return mapped, PathMapping(clean, mapped, "mapped dotless upload-safe workflow path to GitHub Actions workflow path")
    return clean, None


def protected(repo_path: str, prefixes: list[str]) -> bool:
    return any(repo_path == p.rstrip("/") or repo_path.startswith(p) for p in prefixes)


def inspect_bundle(bundle: Path) -> list[str]:
    with zipfile.ZipFile(bundle, "r") as zf:
        return [name for name in sorted(zf.namelist()) if safe_member(name)]


def classify_bundle(bundle: Path) -> dict[str, Any]:
    paths = inspect_bundle(bundle)
    mapped = [
        ".github/workflows/" + p[len("github/workflows/"):] if p.startswith("github/workflows/") else p
        for p in paths
    ]
    if any(p.startswith(".github/workflows/") for p in mapped):
        return {"verdict": "PRIVILEGED_EXECUTOR_REQUIRED", "route": "privileged_queue", "bundle_class": "workflow_bundle", "reason": "workflow mutation requires privileged executor", "mapped_paths": mapped}
    if any(("secret" in p.lower() or "token" in p.lower() or "credential" in p.lower() or ".env" in p.lower()) for p in mapped):
        return {"verdict": "HUMAN_REVIEW_REQUIRED", "route": "failed_bundles", "bundle_class": "authority_material_bundle", "reason": "possible secret/authority material", "mapped_paths": mapped}
    artifact_names = {"page-contract-report.json", "page-contract-report.md", "transition-replay-report.json", "transition-replay-report.md"}
    if any(Path(p).name in artifact_names for p in paths):
        return {"verdict": "ALLOW", "route": "ingest", "bundle_class": "artifact_bundle", "reason": "known report artifact bundle", "mapped_paths": mapped}
    if len([p for p in paths if p != "README.md"]) > 5 and "bundle-manifest.json" not in paths:
        return {"verdict": "SANDBOX_REQUIRED", "route": "sandbox_queue", "bundle_class": "complex_unmanifested_bundle", "reason": "complex bundle lacks manifest", "mapped_paths": mapped}
    return {"verdict": "ALLOW", "route": "ingest", "bundle_class": "ordinary_bundle", "reason": "ordinary bundle allowed", "mapped_paths": mapped}


def copy_with_receipt(root: Path, source: Path, route_dir: str, receipt: dict[str, Any], suffix: str, remove_original: bool = False) -> None:
    target_dir = root / route_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = target_dir / source.name
    if source.resolve() != copied.resolve():
        shutil.copy2(source, copied)

    base = target_dir / f"{source.stem}.{suffix}"
    base.with_suffix(".json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    md = [
        f"# Incoming {suffix.replace('-', ' ').title()} Receipt",
        "",
        f"File: `{source.name}`",
        f"Verdict: `{receipt.get('verdict')}`",
        f"Route: `{receipt.get('route')}`",
        f"Reason: {receipt.get('reason')}",
        f"SHA-256: `{receipt.get('bundle_sha256') or receipt.get('file_sha256')}`",
        "",
    ]
    if receipt.get("repo_transition"):
        md.extend([
            "## Repo Transition",
            "",
            f"- `before_tree_fingerprint`: `{receipt['repo_transition'].get('before_tree_fingerprint')}`",
            f"- `after_tree_fingerprint`: `{receipt['repo_transition'].get('after_tree_fingerprint')}`",
            f"- `changed_files_fingerprint`: `{receipt['repo_transition'].get('changed_files_fingerprint')}`",
            "",
        ])
    base.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")

    if remove_original and source.exists() and source.resolve() != copied.resolve():
        source.unlink()


def installed_receipt_from_ingestion(source: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": now(),
        "schema": "stegverse.installed_bundle_receipt.v1",
        "formal_milestone": "MS-012E.3 — Installed Bundle Archive",
        "bundle_name": source.name,
        "bundle_path": str(source),
        "bundle_sha256": receipt.get("bundle_sha256"),
        "verdict": "INSTALLED_BUNDLE_ARCHIVED",
        "route": "installed_bundles",
        "reason": "Bundle was successfully ingested with ALLOW and archived as an installed transition object.",
        "source_ingestion_receipt": receipt,
        "repo_transition": receipt.get("repo_transition", {}),
        "files_created": receipt.get("files_created"),
        "files_updated": receipt.get("files_updated"),
        "files_unchanged": receipt.get("files_unchanged"),
        "files_skipped": receipt.get("files_skipped"),
    }


def archive_installed_bundle(root: Path, source: Path, policy: dict[str, Any], receipt: dict[str, Any]) -> None:
    if not policy.get("queue", {}).get("archive_installed_bundles", True):
        return
    installed_receipt = installed_receipt_from_ingestion(source, receipt)
    copy_with_receipt(
        root,
        source,
        policy.get("queue", {}).get("installed_dir", "installed_bundles"),
        installed_receipt,
        "installed",
        remove_original=bool(policy.get("queue", {}).get("delete_original_after_install_archive", False)),
    )


def seen_status(root: Path, file_sha: str, policy: dict[str, Any]) -> str | None:
    installed_dir = root / policy.get("queue", {}).get("installed_dir", "installed_bundles")
    for receipt_path in installed_dir.glob("*.json"):
        obj = load(receipt_path, {}) or {}
        if obj.get("bundle_sha256") == file_sha or obj.get("file_sha256") == file_sha:
            return "already_installed"

    index_path = root / policy.get("ledger_outputs", {}).get("fingerprint_index", "data/bundle-fingerprint-index-v1.json")
    index = load(index_path, {"receipts": []}) or {"receipts": []}
    for item in index.get("receipts", []):
        if item.get("bundle_sha256") == file_sha and item.get("verdict") == "ALLOW":
            return "already_applied"

    for folder_name, status in [
        (policy.get("queue", {}).get("failed_dir", "failed_bundles"), "already_failed"),
        (policy.get("queue", {}).get("privileged_dir", "privileged_queue"), "already_privileged_routed"),
        (policy.get("queue", {}).get("sandbox_dir", "sandbox_queue"), "already_sandbox_routed"),
    ]:
        folder = root / folder_name
        for receipt_path in folder.glob("*.json"):
            obj = load(receipt_path, {}) or {}
            if obj.get("bundle_sha256") == file_sha or obj.get("file_sha256") == file_sha:
                return status
    return None


def stale_receipt(path: Path, reason: str, seen_state: str | None = None) -> dict[str, Any]:
    digest = sha_f(path)
    return {
        "generated_at": now(),
        "schema": "stegverse.stale_incoming_receipt.v1",
        "formal_milestone": "MS-012E.3 — Installed Bundle Archive",
        "incoming_path": str(path),
        "file_name": path.name,
        "file_sha256": digest,
        "bundle_sha256": digest,
        "verdict": "STALE_INCOMING_QUARANTINED",
        "route": "failed_bundles",
        "seen_state": seen_state,
        "reason": reason,
    }


def quarantine_stale(root: Path, path: Path, policy: dict[str, Any], reason: str, seen_state: str | None = None) -> dict[str, Any]:
    receipt = stale_receipt(path, reason, seen_state)
    copy_with_receipt(
        root,
        path,
        policy.get("queue", {}).get("failed_dir", "failed_bundles"),
        receipt,
        "stale",
        remove_original=bool(policy.get("queue", {}).get("delete_original_after_quarantine", False)),
    )
    return receipt


def ingest_one(root: Path, bundle: Path, policy_path: Path, apply: bool, retry_failed: bool = False) -> dict[str, Any]:
    policy = load(policy_path, {})
    bundle_sha = sha_f(bundle) or ""

    seen = None if retry_failed else seen_status(root, bundle_sha, policy)
    if seen:
        receipt = stale_receipt(
            bundle,
            f"Incoming bundle is already seen as {seen}; quarantined as stale queue debris instead of being silently skipped.",
            seen,
        )
        if apply and policy.get("queue", {}).get("quarantine_already_seen_incoming", True):
            copy_with_receipt(root, bundle, policy.get("queue", {}).get("failed_dir", "failed_bundles"), receipt, "stale", remove_original=bool(policy.get("queue", {}).get("delete_original_after_quarantine", False)))
        return {
            "generated_at": receipt["generated_at"],
            "schema": "stegverse.bundle_ingestion_report.v1",
            "bundle": str(bundle),
            "mode": "apply" if apply else "dry_run",
            "receipt": receipt,
            "summary": {"applied": 0, "stale_quarantined": 1 if apply else 0, "seen_state": seen},
        }

    gate = classify_bundle(bundle)
    base = {
        "generated_at": now(),
        "schema": "stegverse.bundle_ingestion_receipt.v1",
        "formal_milestone": "MS-012E.3 — Installed Bundle Archive",
        "bundle_name": bundle.name,
        "bundle_path": str(bundle),
        "bundle_sha256": bundle_sha,
        "mode": "apply" if apply else "dry_run",
        "bundle_class": gate["bundle_class"],
        "verdict": gate["verdict"],
        "route": gate["route"],
        "reason": gate["reason"],
        "mapped_paths": gate["mapped_paths"],
    }

    if gate["verdict"] == "PRIVILEGED_EXECUTOR_REQUIRED":
        receipt = {**base, "decisions": []}
        if apply:
            copy_with_receipt(root, bundle, policy.get("queue", {}).get("privileged_dir", "privileged_queue"), receipt, "privileged-task")
        return {"generated_at": receipt["generated_at"], "schema": "stegverse.bundle_ingestion_report.v1", "bundle": str(bundle), "mode": receipt["mode"], "receipt": receipt, "summary": {"applied": 0, "routed_privileged": 1}}

    if gate["verdict"] in {"SANDBOX_REQUIRED", "HUMAN_REVIEW_REQUIRED", "FAIL_CLOSED"}:
        receipt = {**base, "decisions": []}
        route = policy.get("queue", {}).get("sandbox_dir", "sandbox_queue") if gate["verdict"] == "SANDBOX_REQUIRED" else policy.get("queue", {}).get("failed_dir", "failed_bundles")
        if apply:
            copy_with_receipt(root, bundle, route, receipt, "failure")
        return {"generated_at": receipt["generated_at"], "schema": "stegverse.bundle_ingestion_report.v1", "bundle": str(bundle), "mode": receipt["mode"], "receipt": receipt, "summary": {"applied": 0, "routed": route}}

    before = tree_fp(root)
    decisions: list[FileDecision] = []
    mappings: list[PathMapping] = []
    unsafe_count = 0

    with zipfile.ZipFile(bundle, "r") as zf:
        for name in sorted(zf.namelist()):
            if not safe_member(name):
                unsafe_count += 1
                decisions.append(FileDecision(name, None, "skipped", "unsafe path or directory entry", None, None, 0))
                continue
            data = zf.read(name)
            new_hash = sha_b(data)
            if name == "README.md":
                decisions.append(FileDecision(name, None, "skipped", "bundle root README is documentation and is not applied to repo root", None, new_hash, len(data)))
                continue
            repo_rel, mapping = normalize_path(name, policy)
            if mapping:
                mappings.append(mapping)
            old_hash = sha_f(root / repo_rel)
            if protected(repo_rel, list(policy.get("protected_paths", []))):
                decisions.append(FileDecision(name, repo_rel, "skipped", "protected path", old_hash, new_hash, len(data)))
                continue
            if old_hash == new_hash:
                decisions.append(FileDecision(name, repo_rel, "unchanged", "target hash already matches", old_hash, new_hash, len(data)))
                continue
            action = "updated" if (root / repo_rel).exists() else "created"
            if apply:
                target = root / repo_rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                decisions.append(FileDecision(name, repo_rel, action, "hash differs or target missing", old_hash, new_hash, len(data)))
            else:
                decisions.append(FileDecision(name, repo_rel, "would_" + action, "dry run; hash differs or target missing", old_hash, new_hash, len(data)))

    after = tree_fp(root)
    changed = changed_fp(decisions)
    receipt = {
        **base,
        "verdict": "ALLOW",
        "route": "ingest",
        "files_seen": len(decisions),
        "files_created": len([d for d in decisions if d.action == "created"]),
        "files_updated": len([d for d in decisions if d.action == "updated"]),
        "files_unchanged": len([d for d in decisions if d.action == "unchanged"]),
        "files_skipped": len([d for d in decisions if d.action == "skipped"]),
        "unsafe_paths_rejected": unsafe_count,
        "path_mappings_applied": [asdict(m) for m in mappings],
        "repo_transition": {
            "before_tree_fingerprint": before,
            "after_tree_fingerprint": after,
            "changed_files_fingerprint": changed,
        },
        "decisions": [asdict(d) for d in decisions],
    }

    if apply:
        outputs = policy.get("ledger_outputs", {})
        latest = root / outputs.get("latest_receipt", "data/latest-bundle-ingestion-receipt-v1.json")
        ledger = root / outputs.get("ledger_jsonl", "data/bundle-ingestion-ledger-v1.jsonl")
        index_path = root / outputs.get("fingerprint_index", "data/bundle-fingerprint-index-v1.json")
        latest.parent.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        append_jsonl(ledger, {
            "generated_at": receipt["generated_at"],
            "formal_milestone": receipt["formal_milestone"],
            "bundle_name": receipt["bundle_name"],
            "bundle_sha256": receipt["bundle_sha256"],
            "bundle_class": receipt["bundle_class"],
            "verdict": receipt["verdict"],
            "changed_files_fingerprint": changed,
        })
        index = load(index_path, {"schema": "stegverse.bundle_fingerprint_index.v1", "receipts": []}) or {"receipts": []}
        index.setdefault("receipts", []).append({
            "generated_at": receipt["generated_at"],
            "formal_milestone": receipt["formal_milestone"],
            "bundle_name": receipt["bundle_name"],
            "bundle_sha256": receipt["bundle_sha256"],
            "bundle_class": receipt["bundle_class"],
            "verdict": receipt["verdict"],
            "changed_files_fingerprint": changed,
        })
        index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
        archive_installed_bundle(root, bundle, policy, receipt)

    return {
        "generated_at": receipt["generated_at"],
        "schema": "stegverse.bundle_ingestion_report.v1",
        "bundle": str(bundle),
        "policy": str(policy_path),
        "mode": receipt["mode"],
        "receipt": receipt,
        "summary": {
            "total_entries_seen": len(decisions),
            "applied": len([d for d in decisions if d.action in {"created", "updated"}]),
            "unchanged": len([d for d in decisions if d.action == "unchanged"]),
            "skipped": len([d for d in decisions if d.action == "skipped"]),
            "path_mappings": len(mappings),
            "unsafe_paths_rejected": unsafe_count,
            "installed_archived": 1 if apply and policy.get("queue", {}).get("archive_installed_bundles", True) else 0,
        },
    }


def write_report(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bundle-ingestion-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out_dir / "latest-bundle-ingestion-receipt-v1.json").write_text(json.dumps(report["receipt"], indent=2), encoding="utf-8")
    receipt = report["receipt"]
    lines = [
        "# Bundle Ingestion Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Mode: `{report['mode']}`",
        f"Bundle: `{report['bundle']}`",
        f"Verdict: `{receipt['verdict']}`",
        f"Route: `{receipt.get('route')}`",
        f"Bundle class: `{receipt.get('bundle_class', receipt.get('schema'))}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in report.get("summary", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    if "decisions" in receipt:
        lines.extend(["", "## File Decisions", ""])
        for row in receipt.get("decisions", []):
            lines.append(f"- `{row.get('action')}` `{row.get('bundle_path')}` → `{row.get('repo_path')}` — {row.get('reason')}")
    (out_dir / "bundle-ingestion-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_queue(root: Path, policy_path: Path, apply: bool, retry_failed: bool) -> dict[str, Any]:
    policy = load(policy_path, {})
    incoming = root / policy.get("queue", {}).get("incoming_dir", "incoming")
    reports = []
    stale_receipts = []
    entries = sorted(incoming.iterdir(), key=lambda p: p.name) if incoming.exists() else []
    for path in entries:
        if path.is_dir():
            continue
        if path.suffix.lower() != ".zip":
            if policy.get("queue", {}).get("stale_non_zip_files", True):
                receipt = quarantine_stale(root, path, policy, "Non-ZIP file in incoming/ cannot be ingested as a bundle.")
                stale_receipts.append(receipt)
            continue
        try:
            reports.append(ingest_one(root, path, policy_path, apply, retry_failed))
        except zipfile.BadZipFile:
            receipt = quarantine_stale(root, path, policy, "Invalid ZIP file in incoming/.")
            reports.append({"generated_at": receipt["generated_at"], "schema": "stegverse.bundle_ingestion_report.v1", "bundle": str(path), "mode": "apply" if apply else "dry_run", "receipt": receipt, "summary": {"stale_quarantined": 1 if apply else 0}})
        except Exception as exc:
            receipt = {
                "generated_at": now(),
                "schema": "stegverse.bundle_ingestion_receipt.v1",
                "formal_milestone": "MS-012E.3 — Installed Bundle Archive",
                "bundle_name": path.name,
                "bundle_path": str(path),
                "bundle_sha256": sha_f(path),
                "verdict": "FAIL_CLOSED",
                "route": "failed_bundles",
                "reason": f"Unhandled ingestion exception: {exc}",
                "decisions": [],
            }
            if apply:
                copy_with_receipt(root, path, policy.get("queue", {}).get("failed_dir", "failed_bundles"), receipt, "failure")
            reports.append({"generated_at": receipt["generated_at"], "schema": "stegverse.bundle_ingestion_report.v1", "bundle": str(path), "mode": "apply" if apply else "dry_run", "receipt": receipt, "summary": {"failed": 1}})
    return {"generated_at": now(), "schema": "stegverse.bundle_queue_report.v1", "bundles_seen": len(reports), "stale_files_seen": len(stale_receipts), "reports": reports, "stale_receipts": stale_receipts}


def write_queue_report(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bundle-queue-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Bundle Queue Report", "", f"Generated: `{report['generated_at']}`", f"Bundles seen: `{report['bundles_seen']}`", f"Stale files seen: `{report.get('stale_files_seen', 0)}`", "", "## Results", ""]
    for item in report.get("reports", []):
        receipt = item["receipt"]
        lines.append(f"- `{receipt.get('bundle_name') or receipt.get('file_name')}` → `{receipt.get('verdict')}` / `{receipt.get('route')}` — {receipt.get('reason')}")
    for receipt in report.get("stale_receipts", []):
        lines.append(f"- `{receipt.get('file_name')}` → `{receipt.get('verdict')}` / `{receipt.get('route')}` — {receipt.get('reason')}")
    (out_dir / "bundle-queue-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_bundle(root: Path, explicit: str | None) -> Path:
    if explicit:
        path = root / explicit
        if not path.exists():
            raise SystemExit(f"Bundle not found: {path}")
        return path
    bundles = sorted((root / "incoming").glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not bundles:
        raise SystemExit("No bundle found. Commit a .zip file under incoming/ or pass --bundle.")
    return bundles[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle")
    parser.add_argument("--policy", default="data/bundle-ingestion-policy-v1.json")
    parser.add_argument("--out-dir", default="ingestion_reports")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--process-queue", action="store_true")
    parser.add_argument("--retry-failed", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy_path = root / args.policy
    out_dir = root / args.out_dir

    if args.process_queue:
        queue_report = process_queue(root, policy_path, args.apply, args.retry_failed)
        write_queue_report(queue_report, out_dir)
        if queue_report["reports"]:
            write_report(queue_report["reports"][-1], out_dir)
        print(json.dumps({"bundles_seen": queue_report["bundles_seen"], "stale_files_seen": queue_report.get("stale_files_seen", 0)}, indent=2))
        return 0

    report = ingest_one(root, find_bundle(root, args.bundle), policy_path, args.apply, args.retry_failed)
    write_report(report, out_dir)
    print(json.dumps(report.get("summary", {}), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
