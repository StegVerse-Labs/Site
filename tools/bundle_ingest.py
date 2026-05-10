#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAL_MILESTONE = "MS-012E.5 — Default Queue Mode Ingestor"


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


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(obj, sort_keys=True) + "\n")


def tree_fp(root: Path) -> str:
    skip = (
        ".git/",
        "ingestion_reports/",
        "dependency_reports/",
        "sandbox_reports/",
        "headless_cmd_reports/",
        "__pycache__/",
    )
    rows: list[str] = []
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
        f"{item.action} {item.repo_path} {item.old_sha256}->{item.new_sha256}"
        for item in decisions
        if item.action in {"created", "updated", "would_created", "would_updated"}
    ]
    return sha_b("\n".join(sorted(rows)).encode("utf-8"))


def queue_policy(policy: dict[str, Any]) -> dict[str, Any]:
    obj = policy.get("queue", {})
    return obj if isinstance(obj, dict) else {}


def qdir(policy: dict[str, Any], key: str, default: str) -> str:
    return str(queue_policy(policy).get(key, default))


def safe_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    path = Path(name)
    return not path.is_absolute() and ".." not in path.parts


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
    return any(repo_path == prefix.rstrip("/") or repo_path.startswith(prefix) for prefix in prefixes)


def inspect_bundle(bundle: Path) -> list[str]:
    with zipfile.ZipFile(bundle, "r") as archive:
        return [name for name in sorted(archive.namelist()) if safe_member(name)]


def classify_bundle(bundle: Path, *, allow_engine_mutation: bool) -> dict[str, Any]:
    paths = inspect_bundle(bundle)
    mapped = [
        ".github/workflows/" + path[len("github/workflows/"):] if path.startswith("github/workflows/") else path
        for path in paths
    ]

    if any(path.startswith(".github/workflows/") for path in mapped):
        return {
            "verdict": "PRIVILEGED_EXECUTOR_REQUIRED",
            "route": "privileged_queue",
            "bundle_class": "workflow_bundle",
            "reason": "workflow mutation requires privileged executor",
            "mapped_paths": mapped,
        }

    if "tools/bundle_ingest.py" in mapped and not allow_engine_mutation:
        return {
            "verdict": "SANDBOX_REQUIRED",
            "route": "sandbox_queue",
            "bundle_class": "ingestion_engine_mutation_bundle",
            "reason": "automatic queue mode must not apply bundles that mutate the ingestion engine",
            "mapped_paths": mapped,
        }

    if any(("secret" in path.lower() or "token" in path.lower() or "credential" in path.lower() or ".env" in path.lower()) for path in mapped):
        return {
            "verdict": "HUMAN_REVIEW_REQUIRED",
            "route": "failed_bundles",
            "bundle_class": "authority_material_bundle",
            "reason": "possible secret/authority material",
            "mapped_paths": mapped,
        }

    artifact_names = {
        "page-contract-report.json",
        "page-contract-report.md",
        "transition-replay-report.json",
        "transition-replay-report.md",
    }
    if any(Path(path).name in artifact_names for path in paths):
        return {
            "verdict": "ALLOW",
            "route": "ingest",
            "bundle_class": "artifact_bundle",
            "reason": "known report artifact bundle",
            "mapped_paths": mapped,
        }

    if len([path for path in paths if path != "README.md"]) > 5 and "bundle-manifest.json" not in paths:
        return {
            "verdict": "SANDBOX_REQUIRED",
            "route": "sandbox_queue",
            "bundle_class": "complex_unmanifested_bundle",
            "reason": "complex bundle lacks manifest",
            "mapped_paths": mapped,
        }

    return {
        "verdict": "ALLOW",
        "route": "ingest",
        "bundle_class": "ordinary_bundle",
        "reason": "ordinary bundle allowed",
        "mapped_paths": mapped,
    }


def emit_receipt_files(target_dir: Path, stem: str, receipt: dict[str, Any]) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    write_json(target_dir / f"{stem}.json", receipt)

    lines = [
        f"# {stem.replace('-', ' ').title()} Receipt",
        "",
        f"File: `{receipt.get('bundle_name') or receipt.get('file_name')}`",
        f"Verdict: `{receipt.get('verdict')}`",
        f"Route: `{receipt.get('route')}`",
        f"Reason: {receipt.get('reason')}",
    ]

    digest = receipt.get("bundle_sha256") or receipt.get("file_sha256")
    if digest:
        lines.append(f"SHA-256: `{digest}`")

    if receipt.get("repo_transition"):
        transition = receipt["repo_transition"]
        lines.extend([
            "",
            "## Repo Transition",
            "",
            f"- `before_tree_fingerprint`: `{transition.get('before_tree_fingerprint')}`",
            f"- `after_tree_fingerprint`: `{transition.get('after_tree_fingerprint')}`",
            f"- `changed_files_fingerprint`: `{transition.get('changed_files_fingerprint')}`",
            "",
        ])

    (target_dir / f"{stem}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def route_bundle(
    root: Path,
    source: Path,
    route_dir: str,
    receipt: dict[str, Any],
    suffix: str,
    *,
    remove_original: bool,
) -> Path:
    target_dir = root / route_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = target_dir / source.name

    if source.exists() and source.resolve() != copied.resolve():
        shutil.copy2(source, copied)

    emit_receipt_files(target_dir, f"{source.stem}.{suffix}", receipt)

    if remove_original and source.exists() and source.resolve() != copied.resolve():
        source.unlink()

    return copied


def installed_receipt_from_ingestion(source: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": now(),
        "schema": "stegverse.installed_bundle_receipt.v1",
        "formal_milestone": FORMAL_MILESTONE,
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


def archive_installed_bundle(
    root: Path,
    source: Path,
    policy: dict[str, Any],
    receipt: dict[str, Any],
    *,
    remove_original: bool,
) -> None:
    if not queue_policy(policy).get("archive_installed_bundles", True):
        return

    route_bundle(
        root,
        source,
        qdir(policy, "installed_dir", "installed_bundles"),
        installed_receipt_from_ingestion(source, receipt),
        "installed",
        remove_original=remove_original,
    )


def seen_status(root: Path, file_sha: str, policy: dict[str, Any]) -> str | None:
    installed_dir = root / qdir(policy, "installed_dir", "installed_bundles")
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
        (qdir(policy, "failed_dir", "failed_bundles"), "already_failed"),
        (qdir(policy, "privileged_dir", "privileged_queue"), "already_privileged_routed"),
        (qdir(policy, "sandbox_dir", "sandbox_queue"), "already_sandbox_routed"),
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
        "formal_milestone": FORMAL_MILESTONE,
        "incoming_path": str(path),
        "file_name": path.name,
        "file_sha256": digest,
        "bundle_sha256": digest,
        "verdict": "STALE_INCOMING_QUARANTINED",
        "route": "failed_bundles",
        "seen_state": seen_state,
        "reason": reason,
    }


def quarantine_stale(
    root: Path,
    path: Path,
    policy: dict[str, Any],
    reason: str,
    seen_state: str | None = None,
    *,
    remove_original: bool,
) -> dict[str, Any]:
    receipt = stale_receipt(path, reason, seen_state)
    route_bundle(
        root,
        path,
        qdir(policy, "failed_dir", "failed_bundles"),
        receipt,
        "stale",
        remove_original=remove_original,
    )
    return receipt


def ingest_one(
    root: Path,
    bundle: Path,
    policy_path: Path,
    apply: bool,
    retry_failed: bool = False,
    *,
    remove_source_after_route: bool,
    allow_engine_mutation: bool,
) -> dict[str, Any]:
    policy = load(policy_path, {}) or {}
    bundle_sha = sha_f(bundle) or ""

    seen = None if retry_failed else seen_status(root, bundle_sha, policy)
    if seen:
        receipt = stale_receipt(
            bundle,
            f"Incoming bundle is already seen as {seen}; quarantined as stale queue debris instead of being silently skipped.",
            seen,
        )
        if apply and queue_policy(policy).get("quarantine_already_seen_incoming", True):
            route_bundle(
                root,
                bundle,
                qdir(policy, "failed_dir", "failed_bundles"),
                receipt,
                "stale",
                remove_original=remove_source_after_route,
            )

        return {
            "generated_at": receipt["generated_at"],
            "schema": "stegverse.bundle_ingestion_report.v1",
            "bundle": str(bundle),
            "mode": "apply" if apply else "dry_run",
            "receipt": receipt,
            "summary": {
                "applied": 0,
                "stale_quarantined": 1 if apply else 0,
                "seen_state": seen,
                "source_removed_from_incoming": 1 if apply and remove_source_after_route else 0,
            },
        }

    gate = classify_bundle(bundle, allow_engine_mutation=allow_engine_mutation)
    base = {
        "generated_at": now(),
        "schema": "stegverse.bundle_ingestion_receipt.v1",
        "formal_milestone": FORMAL_MILESTONE,
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
            route_bundle(
                root,
                bundle,
                qdir(policy, "privileged_dir", "privileged_queue"),
                receipt,
                "privileged-task",
                remove_original=remove_source_after_route,
            )
        return {
            "generated_at": receipt["generated_at"],
            "schema": "stegverse.bundle_ingestion_report.v1",
            "bundle": str(bundle),
            "mode": receipt["mode"],
            "receipt": receipt,
            "summary": {
                "applied": 0,
                "routed_privileged": 1,
                "source_removed_from_incoming": 1 if apply and remove_source_after_route else 0,
            },
        }

    if gate["verdict"] in {"SANDBOX_REQUIRED", "HUMAN_REVIEW_REQUIRED", "FAIL_CLOSED"}:
        receipt = {**base, "decisions": []}
        route = qdir(policy, "sandbox_dir", "sandbox_queue") if gate["verdict"] == "SANDBOX_REQUIRED" else qdir(policy, "failed_dir", "failed_bundles")
        if apply:
            route_bundle(
                root,
                bundle,
                route,
                receipt,
                "failure",
                remove_original=remove_source_after_route,
            )
        return {
            "generated_at": receipt["generated_at"],
            "schema": "stegverse.bundle_ingestion_report.v1",
            "bundle": str(bundle),
            "mode": receipt["mode"],
            "receipt": receipt,
            "summary": {
                "applied": 0,
                "routed": route,
                "source_removed_from_incoming": 1 if apply and remove_source_after_route else 0,
            },
        }

    before = tree_fp(root)
    decisions: list[FileDecision] = []
    mappings: list[PathMapping] = []
    unsafe_count = 0

    with zipfile.ZipFile(bundle, "r") as archive:
        for name in sorted(archive.namelist()):
            if not safe_member(name):
                unsafe_count += 1
                decisions.append(FileDecision(name, None, "skipped", "unsafe path or directory entry", None, None, 0))
                continue

            data = archive.read(name)
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
        "files_created": len([item for item in decisions if item.action == "created"]),
        "files_updated": len([item for item in decisions if item.action == "updated"]),
        "files_unchanged": len([item for item in decisions if item.action == "unchanged"]),
        "files_skipped": len([item for item in decisions if item.action == "skipped"]),
        "unsafe_paths_rejected": unsafe_count,
        "path_mappings_applied": [asdict(item) for item in mappings],
        "repo_transition": {
            "before_tree_fingerprint": before,
            "after_tree_fingerprint": after,
            "changed_files_fingerprint": changed,
        },
        "decisions": [asdict(item) for item in decisions],
    }

    if apply:
        outputs = policy.get("ledger_outputs", {})
        latest = root / outputs.get("latest_receipt", "data/latest-bundle-ingestion-receipt-v1.json")
        ledger = root / outputs.get("ledger_jsonl", "data/bundle-ingestion-ledger-v1.jsonl")
        index_path = root / outputs.get("fingerprint_index", "data/bundle-fingerprint-index-v1.json")

        write_json(latest, receipt)
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
        write_json(index_path, index)

        archive_installed_bundle(
            root,
            bundle,
            policy,
            receipt,
            remove_original=remove_source_after_route,
        )

    return {
        "generated_at": receipt["generated_at"],
        "schema": "stegverse.bundle_ingestion_report.v1",
        "bundle": str(bundle),
        "policy": str(policy_path),
        "mode": receipt["mode"],
        "receipt": receipt,
        "summary": {
            "total_entries_seen": len(decisions),
            "applied": len([item for item in decisions if item.action in {"created", "updated"}]),
            "unchanged": len([item for item in decisions if item.action == "unchanged"]),
            "skipped": len([item for item in decisions if item.action == "skipped"]),
            "path_mappings": len(mappings),
            "unsafe_paths_rejected": unsafe_count,
            "installed_archived": 1 if apply and queue_policy(policy).get("archive_installed_bundles", True) else 0,
            "source_removed_from_incoming": 1 if apply and remove_source_after_route else 0,
        },
    }


def write_report(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "bundle-ingestion-report.json", report)
    write_json(out_dir / "latest-bundle-ingestion-receipt-v1.json", report["receipt"])

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
    policy = load(policy_path, {}) or {}
    incoming = root / qdir(policy, "incoming_dir", "incoming")

    reports: list[dict[str, Any]] = []
    stale_receipts: list[dict[str, Any]] = []

    entries = sorted(incoming.iterdir(), key=lambda path: path.name) if incoming.exists() else []

    for path in entries:
        if path.is_dir():
            continue

        if path.suffix.lower() != ".zip":
            if queue_policy(policy).get("stale_non_zip_files", True):
                receipt = quarantine_stale(
                    root,
                    path,
                    policy,
                    "Non-ZIP file in incoming/ cannot be ingested as a bundle.",
                    remove_original=apply,
                )
                stale_receipts.append(receipt)
            continue

        try:
            reports.append(
                ingest_one(
                    root,
                    path,
                    policy_path,
                    apply,
                    retry_failed,
                    remove_source_after_route=apply,
                    allow_engine_mutation=False,
                )
            )
        except zipfile.BadZipFile:
            receipt = quarantine_stale(
                root,
                path,
                policy,
                "Invalid ZIP file in incoming/.",
                remove_original=apply,
            )
            reports.append({
                "generated_at": receipt["generated_at"],
                "schema": "stegverse.bundle_ingestion_report.v1",
                "bundle": str(path),
                "mode": "apply" if apply else "dry_run",
                "receipt": receipt,
                "summary": {
                    "stale_quarantined": 1 if apply else 0,
                    "source_removed_from_incoming": 1 if apply else 0,
                },
            })
        except Exception as exc:
            receipt = {
                "generated_at": now(),
                "schema": "stegverse.bundle_ingestion_receipt.v1",
                "formal_milestone": FORMAL_MILESTONE,
                "bundle_name": path.name,
                "bundle_path": str(path),
                "bundle_sha256": sha_f(path),
                "verdict": "FAIL_CLOSED",
                "route": "failed_bundles",
                "reason": f"Unhandled ingestion exception: {exc}",
                "decisions": [],
            }
            if apply:
                route_bundle(
                    root,
                    path,
                    qdir(policy, "failed_dir", "failed_bundles"),
                    receipt,
                    "failure",
                    remove_original=True,
                )
            reports.append({
                "generated_at": receipt["generated_at"],
                "schema": "stegverse.bundle_ingestion_report.v1",
                "bundle": str(path),
                "mode": "apply" if apply else "dry_run",
                "receipt": receipt,
                "summary": {
                    "failed": 1,
                    "source_removed_from_incoming": 1 if apply else 0,
                },
            })

    return {
        "generated_at": now(),
        "schema": "stegverse.bundle_queue_report.v1",
        "formal_milestone": FORMAL_MILESTONE,
        "mode": "apply" if apply else "dry_run",
        "bundles_seen": len(reports),
        "stale_files_seen": len(stale_receipts),
        "reports": reports,
        "stale_receipts": stale_receipts,
    }


def write_queue_report(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "bundle-queue-report.json", report)

    lines = [
        "# Bundle Queue Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Milestone: `{report.get('formal_milestone')}`",
        f"Mode: `{report.get('mode')}`",
        f"Bundles seen: `{report['bundles_seen']}`",
        f"Stale files seen: `{report.get('stale_files_seen', 0)}`",
        "",
        "## Results",
        "",
    ]

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
    raise SystemExit("No explicit bundle supplied; default execution mode is queue processing.")


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

    if args.bundle:
        report = ingest_one(
            root,
            find_bundle(root, args.bundle),
            policy_path,
            args.apply,
            args.retry_failed,
            remove_source_after_route=args.apply,
            allow_engine_mutation=True,
        )
        write_report(report, out_dir)
        print(json.dumps(report.get("summary", {}), indent=2))
        return 0

    queue_report = process_queue(root, policy_path, args.apply, args.retry_failed)
    write_queue_report(queue_report, out_dir)
    if queue_report["reports"]:
        write_report(queue_report["reports"][-1], out_dir)

    print(json.dumps({
        "default_queue_mode": True,
        "bundles_seen": queue_report["bundles_seen"],
        "stale_files_seen": queue_report.get("stale_files_seen", 0),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
