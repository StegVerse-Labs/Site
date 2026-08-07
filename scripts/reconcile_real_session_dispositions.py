#!/usr/bin/env python3
"""Admit repository-grounded dispositions and scan for real MERGE_REQUIRED candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "session-orchestration-registry.json"
EVIDENCE_DIR = ROOT / "data" / "session-disposition-evidence"
RECEIPT_DIR = ROOT / "data" / "session-disposition-receipts"
SCAN_REPORT = ROOT / "data" / "session-merge-required-candidate-scan.json"
SEARCH_DIRS = [
    ROOT / "data" / "session-consolidations",
    ROOT / "data" / "session-consolidation-receipts",
    ROOT / "data" / "session-goal-inventories",
]


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry_at_commit(commit: str) -> dict[str, Any]:
    if not commit or any(char.isspace() for char in commit):
        raise ValueError("baseline_registry_commit must be a non-empty git ref without whitespace")
    result = subprocess.run(
        ["git", "show", f"{commit}:{REGISTRY.relative_to(ROOT)}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    value = json.loads(result.stdout)
    if not isinstance(value, dict) or not isinstance(value.get("sessions"), list):
        raise ValueError("baseline registry is malformed")
    return value


def find_session(registry: dict[str, Any], session_id: str) -> dict[str, Any]:
    matches = [row for row in registry.get("sessions", []) if isinstance(row, dict) and row.get("session_id") == session_id]
    if len(matches) != 1:
        raise ValueError(f"session lookup must resolve exactly once: {session_id} ({len(matches)})")
    return matches[0]


def verify_supersession(registry: dict[str, Any], evidence: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if evidence.get("requested_posture") != "SUPERSEDED":
        raise ValueError("evidence requested_posture must be SUPERSEDED")
    source = find_session(registry, str(evidence.get("session_id")))
    successor = find_session(registry, str(evidence.get("successor_session_id")))
    conditions = evidence.get("required_source_conditions", {})
    if source.get("active_task_ownership") is not conditions.get("source_active_task_ownership"):
        raise ValueError("source active_task_ownership condition not met")
    if source.get("unique_unmerged_state") is not conditions.get("source_unique_unmerged_state"):
        raise ValueError("source unique_unmerged_state condition not met")
    needle = conditions.get("source_reason_contains")
    if not isinstance(needle, str) or needle not in str(source.get("reason", "")):
        raise ValueError("source reason does not establish declared supersession")
    if successor.get("task_id") != evidence.get("successor_task_id"):
        raise ValueError("successor task does not match evidence")
    if successor.get("posture") != conditions.get("successor_posture"):
        raise ValueError("successor posture condition not met")
    if successor.get("active_task_ownership") is not conditions.get("successor_active_task_ownership"):
        raise ValueError("successor active ownership condition not met")
    if source.get("session_id") == successor.get("session_id"):
        raise ValueError("source and successor cannot be the same session")
    return source, successor


def apply_supersession(
    registry: dict[str, Any],
    evidence: dict[str, Any],
    baseline_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source, successor = verify_supersession(registry, evidence)
    if baseline_registry is None:
        baseline_registry = json.loads(json.dumps(registry))
    baseline_source = find_session(baseline_registry, str(evidence.get("session_id")))
    if baseline_source.get("posture") == "SUPERSEDED":
        raise ValueError("baseline registry must predate supersession admission")
    conditions = evidence.get("required_source_conditions", {})
    if baseline_source.get("active_task_ownership") is not conditions.get("source_active_task_ownership"):
        raise ValueError("baseline source active ownership condition not met")
    if baseline_source.get("unique_unmerged_state") is not conditions.get("source_unique_unmerged_state"):
        raise ValueError("baseline source unique state condition not met")
    needle = conditions.get("source_reason_contains")
    if not isinstance(needle, str) or needle not in str(baseline_source.get("reason", "")):
        raise ValueError("baseline source reason does not establish supersession")

    before = json.loads(json.dumps(baseline_source))
    evidence_hash = sha256(evidence)
    source["posture"] = "SUPERSEDED"
    source["safe_to_archive"] = False
    source["active_task_ownership"] = False
    source["unique_unmerged_state"] = False
    source["disposition_evidence"] = str(
        (EVIDENCE_DIR / f"{evidence['evidence_id']}.json").relative_to(ROOT)
    )
    source["disposition_evidence_sha256"] = evidence_hash
    source["superseded_by_session_id"] = successor.get("session_id")
    source["superseded_by_task_id"] = successor.get("task_id")
    source["superseded_by_owner"] = evidence.get("successor_owner")
    after = json.loads(json.dumps(source))
    before_hash = sha256(before)
    after_hash = sha256(after)
    if before_hash == after_hash:
        raise ValueError("disposition transition must change the source-state hash")
    receipt = {
        "schema_version": "1.1.0",
        "receipt_type": "hash_bound_session_disposition",
        "evidence_id": evidence.get("evidence_id"),
        "session_id": source.get("session_id"),
        "task_id": source.get("task_id"),
        "disposition": "SUPERSEDED",
        "admission_status": "ADMITTED",
        "source_registry": str(REGISTRY.relative_to(ROOT)),
        "baseline_registry_commit": evidence.get("baseline_registry_commit"),
        "evidence_path": source["disposition_evidence"],
        "evidence_sha256": evidence_hash,
        "before_sha256": before_hash,
        "after_sha256": after_hash,
        "successor": {
            "session_id": successor.get("session_id"),
            "task_id": successor.get("task_id"),
            "posture": successor.get("posture"),
            "active_task_ownership": successor.get("active_task_ownership"),
            "owner": evidence.get("successor_owner"),
        },
        "archive_candidate": False,
        "ui_archive_action_performed": False,
        "nonclaims": evidence.get("nonclaims", []),
    }
    receipt["receipt_sha256"] = sha256(receipt)
    return receipt


def candidate_reason(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    reasons: list[str] = []
    if value.get("posture") == "MERGE_REQUIRED":
        reasons.append("posture=MERGE_REQUIRED")
    if value.get("unique_unmerged_state") is True:
        reasons.append("unique_unmerged_state=true")
    remaining = value.get("unique_chat_only_requirements_remaining")
    if isinstance(remaining, int) and remaining > 0:
        reasons.append(f"unique_chat_only_requirements_remaining={remaining}")
    consolidation = value.get("session_consolidation")
    if isinstance(consolidation, dict):
        nested = consolidation.get("unique_chat_only_requirements_remaining")
        if isinstance(nested, int) and nested > 0:
            reasons.append(f"session_consolidation.unique_chat_only_requirements_remaining={nested}")
    return reasons


def scan_merge_required(registry: dict[str, Any]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for row in registry.get("sessions", []):
        reasons = candidate_reason(row)
        if reasons:
            candidates.append({
                "source": str(REGISTRY.relative_to(ROOT)),
                "session_id": row.get("session_id") if isinstance(row, dict) else None,
                "reasons": reasons,
                "source_sha256": sha256(row),
            })
    scanned_files = 0
    for directory in SEARCH_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            scanned_files += 1
            try:
                value = load_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            reasons = candidate_reason(value)
            if reasons:
                candidates.append({
                    "source": str(path.relative_to(ROOT)),
                    "session_id": value.get("session_id") if isinstance(value, dict) else None,
                    "reasons": reasons,
                    "source_sha256": sha256(value),
                })
    state = "REVIEW_REQUIRED_REAL_CANDIDATE_FOUND" if candidates else "BLOCKED_NO_REAL_CANDIDATE"
    report = {
        "schema_version": "1.0.0",
        "report_type": "real_merge_required_candidate_scan",
        "state": state,
        "registry": str(REGISTRY.relative_to(ROOT)),
        "search_directories": [str(path.relative_to(ROOT)) for path in SEARCH_DIRS],
        "scanned_files": scanned_files,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "archive_rejection_established": bool(candidates),
        "fabricated_state": False,
        "next_action": (
            "review the real candidate, preserve its unique state, and validate MERGE_REQUIRED archival rejection"
            if candidates
            else "retain this blocker until a repository-grounded session declares unique unmerged state; do not manufacture a candidate"
        ),
    }
    report["report_sha256"] = sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry = load_json(REGISTRY)
    evidence_paths = sorted(EVIDENCE_DIR.glob("*.json")) if EVIDENCE_DIR.exists() else []
    if not evidence_paths:
        raise SystemExit("no disposition evidence files found")
    receipts: list[dict[str, Any]] = []
    for path in evidence_paths:
        evidence = load_json(path)
        if evidence.get("requested_posture") == "SUPERSEDED":
            baseline_commit = evidence.get("baseline_registry_commit")
            if not isinstance(baseline_commit, str) or not baseline_commit:
                raise SystemExit(f"missing baseline_registry_commit in {path.relative_to(ROOT)}")
            baseline_registry = load_registry_at_commit(baseline_commit)
            receipt = apply_supersession(registry, evidence, baseline_registry)
            receipts.append(receipt)
            receipt_path = RECEIPT_DIR / f"{evidence['evidence_id']}.receipt.json"
            if args.check:
                if not receipt_path.exists() or load_json(receipt_path) != receipt:
                    print(f"SESSION_DISPOSITION_RECEIPT_STALE:{receipt_path.relative_to(ROOT)}")
                    return 1
            else:
                RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
                receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    scan = scan_merge_required(registry)
    if args.check:
        if not SCAN_REPORT.exists() or load_json(SCAN_REPORT) != scan:
            print("SESSION_MERGE_REQUIRED_SCAN_STALE")
            return 1
    else:
        SCAN_REPORT.write_text(json.dumps(scan, indent=2) + "\n", encoding="utf-8")
        if args.apply:
            REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"SESSION_REAL_DISPOSITION_PASS:receipts={len(receipts)}:merge_scan={scan['state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
