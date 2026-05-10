#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAL_MILESTONE = "MS-012I — Site Ephemeral Sandbox Protocols"


@dataclass
class MemberFinding:
    path: str
    action: str
    reason: str
    size_bytes: int | None = None
    sha256: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return sha_bytes(path.read_bytes())


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


def safe_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    p = Path(name)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    if name == ".git" or name.startswith(".git/"):
        return False
    return True


def is_marker(path: Path, policy: dict[str, Any]) -> bool:
    return path.name in set(policy.get("marker_files", [".gitkeep", "README.md"]))


def inspect_zip(bundle: Path) -> tuple[list[str], list[MemberFinding], dict[str, bytes]]:
    findings: list[MemberFinding] = []
    safe_payload: dict[str, bytes] = {}
    members: list[str] = []

    with zipfile.ZipFile(bundle, "r") as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            name = info.filename
            members.append(name)

            if name.endswith("/"):
                findings.append(MemberFinding(name, "ignored", "directory entry"))
                continue

            if not safe_member(name):
                findings.append(MemberFinding(name, "rejected", "unsafe path"))
                continue

            data = archive.read(name)
            digest = sha_bytes(data)
            findings.append(MemberFinding(name, "accepted_for_review", "safe member", len(data), digest))
            safe_payload[name] = data

    return members, findings, safe_payload


def contains_workflow_material(paths: list[str]) -> bool:
    mapped = [
        ".github/workflows/" + p[len("github/workflows/"):] if p.startswith("github/workflows/") else p
        for p in paths
    ]
    return any(p.startswith(".github/workflows/") for p in mapped)


def contains_ingestor_mutation(paths: list[str]) -> bool:
    return "tools/bundle_ingest.py" in paths


def has_manifest(paths: list[str]) -> bool:
    return "bundle-manifest.json" in paths or "bundle_manifest.json" in paths


def build_manifest(bundle: Path, payload_paths: list[str], classification: str) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "schema": "stegverse.bundle_manifest.v1",
        "bundle_id": f"{bundle.stem}.sandbox-candidate",
        "formal_milestone": FORMAL_MILESTONE,
        "source_bundle": bundle.name,
        "classification": classification,
        "purpose": "Sandbox-generated candidate bundle. Must pass through normal ingestion before any live repo changes are applied.",
        "files": [
            {
                "path": path,
                "role": "sandbox_preserved_member"
            }
            for path in sorted(payload_paths)
            if path not in {"README.md", "bundle-manifest.json", "bundle_manifest.json"}
        ],
        "safety": {
            "generated_by_ephemeral_sandbox": True,
            "requires_ingestion_reentry": True,
            "does_not_contain_workflow_files": not contains_workflow_material(payload_paths),
            "does_not_mutate_ingestion_engine": not contains_ingestor_mutation(payload_paths),
        }
    }


def create_candidate_zip(root: Path, bundle: Path, payload: dict[str, bytes], policy: dict[str, Any]) -> Path:
    incoming = root / policy["directories"].get("incoming", "incoming")
    incoming.mkdir(parents=True, exist_ok=True)

    suffix = policy.get("repair_rules", {}).get("candidate_suffix", ".sandbox-candidate")
    candidate = incoming / f"{bundle.stem}{suffix}.zip"

    payload_paths = sorted(payload.keys())
    manifest = build_manifest(bundle, payload_paths, "repair_candidate_created")

    with zipfile.ZipFile(candidate, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("bundle-manifest.json", json.dumps(manifest, indent=2).encode("utf-8"))
        for name in payload_paths:
            if name in {"bundle-manifest.json", "bundle_manifest.json"}:
                continue
            if name == "README.md":
                continue
            archive.writestr(name, payload[name])

    return candidate


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Ephemeral Sandbox Report",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Bundle: `{report.get('bundle_name')}`",
        f"Verdict: `{report.get('verdict')}`",
        f"Classification: `{report.get('classification')}`",
        f"Reason: {report.get('reason')}",
        "",
        "## Candidate",
        "",
        f"- `candidate_created`: `{report.get('candidate_created')}`",
        f"- `candidate_path`: `{report.get('candidate_path')}`",
        "",
        "## Findings",
        "",
    ]

    for finding in report.get("member_findings", []):
        lines.append(f"- `{finding.get('action')}` `{finding.get('path')}` — {finding.get('reason')}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def archive_original(root: Path, bundle: Path, report: dict[str, Any], policy: dict[str, Any], apply: bool) -> None:
    if not apply:
        return

    reviewed = root / policy["directories"].get("sandbox_reviewed", "sandbox_reviewed")
    reviewed.mkdir(parents=True, exist_ok=True)

    target = reviewed / bundle.name
    if bundle.exists() and bundle.resolve() != target.resolve():
        shutil.move(str(bundle), str(target))

    receipt_base = reviewed / f"{bundle.stem}.sandbox"
    write_json(receipt_base.with_suffix(".sandbox.json"), report)

    lines = [
        "# Sandbox Reviewed Bundle Receipt",
        "",
        f"Bundle: `{bundle.name}`",
        f"Verdict: `{report.get('verdict')}`",
        f"Classification: `{report.get('classification')}`",
        f"Reason: {report.get('reason')}",
        f"Candidate: `{report.get('candidate_path')}`",
        "",
    ]
    receipt_base.with_suffix(".sandbox.md").write_text("\n".join(lines), encoding="utf-8")


def review_bundle(root: Path, bundle: Path, policy: dict[str, Any], apply: bool) -> dict[str, Any]:
    report_base = {
        "generated_at": utc_now(),
        "schema": "stegverse.ephemeral_sandbox_report.v1",
        "formal_milestone": FORMAL_MILESTONE,
        "bundle_name": bundle.name,
        "bundle_path": str(bundle),
        "bundle_sha256": sha_file(bundle),
        "mode": "apply" if apply else "dry_run",
    }

    try:
        with tempfile.TemporaryDirectory(prefix="stegverse_site_sandbox_") as tmp:
            tmp_path = Path(tmp)
            with zipfile.ZipFile(bundle, "r") as archive:
                archive.extractall(tmp_path)

            members, findings, payload = inspect_zip(bundle)

    except zipfile.BadZipFile:
        return {
            **report_base,
            "verdict": "FAIL_CLOSED",
            "classification": "invalid_zip",
            "reason": "Bundle is not a valid ZIP.",
            "candidate_created": False,
            "candidate_path": None,
            "member_findings": [],
        }

    safe_paths = sorted(payload.keys())
    rejected = [f for f in findings if f.action == "rejected"]

    if rejected:
        return {
            **report_base,
            "verdict": "DENY",
            "classification": "unrepairable",
            "reason": "Unsafe paths were present; sandbox refuses to emit a candidate.",
            "candidate_created": False,
            "candidate_path": None,
            "member_findings": [asdict(item) for item in findings],
        }

    if contains_workflow_material(safe_paths):
        return {
            **report_base,
            "verdict": "HOLD",
            "classification": "privileged_review_required",
            "reason": "Workflow material requires privileged review, not ordinary sandbox repair.",
            "candidate_created": False,
            "candidate_path": None,
            "member_findings": [asdict(item) for item in findings],
        }

    if contains_ingestor_mutation(safe_paths):
        return {
            **report_base,
            "verdict": "HOLD",
            "classification": "manual_review_required",
            "reason": "Bundle mutates tools/bundle_ingest.py; sandbox will not emit an automatic repair candidate.",
            "candidate_created": False,
            "candidate_path": None,
            "member_findings": [asdict(item) for item in findings],
        }

    if not safe_paths:
        return {
            **report_base,
            "verdict": "DENY",
            "classification": "unrepairable",
            "reason": "No safe payload members were found.",
            "candidate_created": False,
            "candidate_path": None,
            "member_findings": [asdict(item) for item in findings],
        }

    if has_manifest(safe_paths):
        return {
            **report_base,
            "verdict": "HOLD",
            "classification": "manual_review_required",
            "reason": "Bundle already has a manifest; sandbox did not infer a repair.",
            "candidate_created": False,
            "candidate_path": None,
            "member_findings": [asdict(item) for item in findings],
        }

    candidate_path = None
    if apply:
        candidate_path = create_candidate_zip(root, bundle, payload, policy)

    return {
        **report_base,
        "verdict": "ALLOW_REENTRY",
        "classification": "repair_candidate_created",
        "reason": "Sandbox added a bundle manifest and emitted a candidate ZIP back into incoming.",
        "candidate_created": bool(apply),
        "candidate_path": str(candidate_path) if candidate_path else None,
        "member_findings": [asdict(item) for item in findings],
    }


def process_queue(root: Path, policy: dict[str, Any], apply: bool) -> dict[str, Any]:
    sandbox_queue = root / policy["directories"].get("sandbox_queue", "sandbox_queue")
    reports_dir = root / policy["directories"].get("sandbox_reports", "sandbox_reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    reports = []
    entries = sorted(sandbox_queue.glob("*.zip")) if sandbox_queue.exists() else []

    for bundle in entries:
        report = review_bundle(root, bundle, policy, apply)
        reports.append(report)

        report_json = reports_dir / f"{bundle.stem}.sandbox-report.json"
        report_md = reports_dir / f"{bundle.stem}.sandbox-report.md"
        write_json(report_json, report)
        write_markdown(report_md, report)

        archive_original(root, bundle, report, policy, apply)

    queue_report = {
        "generated_at": utc_now(),
        "schema": "stegverse.ephemeral_sandbox_queue_report.v1",
        "formal_milestone": FORMAL_MILESTONE,
        "mode": "apply" if apply else "dry_run",
        "bundles_seen": len(entries),
        "reports": reports,
        "safety": policy.get("safety", {}),
    }

    write_json(reports_dir / "ephemeral-sandbox-queue-report.json", queue_report)
    write_queue_markdown(reports_dir / "ephemeral-sandbox-queue-report.md", queue_report)
    return queue_report


def write_queue_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Ephemeral Sandbox Queue Report",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Mode: `{report.get('mode')}`",
        f"Bundles seen: `{report.get('bundles_seen')}`",
        "",
        "## Results",
        "",
    ]
    for item in report.get("reports", []):
        lines.append(
            f"- `{item.get('bundle_name')}` → `{item.get('verdict')}` / `{item.get('classification')}` — {item.get('reason')}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/sandbox/ephemeral-sandbox-policy-v1.json")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, {})
    if not policy:
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    report = process_queue(root, policy, args.apply)
    print(json.dumps({
        "bundles_seen": report["bundles_seen"],
        "mode": report["mode"],
        "reports": [
            {
                "bundle": item.get("bundle_name"),
                "verdict": item.get("verdict"),
                "classification": item.get("classification"),
                "candidate_path": item.get("candidate_path"),
            }
            for item in report["reports"]
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
