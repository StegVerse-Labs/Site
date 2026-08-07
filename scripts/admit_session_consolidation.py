#!/usr/bin/env python3
"""Admit an approved session-consolidation receipt into the canonical registry."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data" / "session-orchestration-registry.json"
DEFAULT_REPORT = ROOT / "session_registry_intake.report.json"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def validate_receipt(receipt: dict[str, Any], receipt_path: Path) -> list[str]:
    failures: list[str] = []
    required = {
        "session_id",
        "task_id",
        "repository",
        "posture",
        "active_task_ownership",
        "unique_unmerged_state",
        "safe_to_archive",
        "conflicting_active_owner",
        "successor_execution_source",
        "material_state_locations",
        "required_before_archive",
        "reason",
    }
    missing = sorted(required - receipt.keys())
    if missing:
        failures.append("missing receipt fields: " + ", ".join(missing))
        return failures
    if receipt.get("posture") != "ARCHIVABLE":
        failures.append("registry intake requires an ARCHIVABLE consolidation receipt")
    if receipt.get("active_task_ownership") is not False:
        failures.append("receipt still owns active work")
    if receipt.get("unique_unmerged_state") is not False:
        failures.append("receipt still contains unique unmerged state")
    if receipt.get("safe_to_archive") is not True:
        failures.append("receipt is not safe_to_archive=true")
    if receipt.get("conflicting_active_owner") is not False:
        failures.append("receipt declares a conflicting active owner")
    if receipt.get("required_before_archive"):
        failures.append("receipt has unresolved required_before_archive actions")

    successor = receipt.get("successor_execution_source")
    if not isinstance(successor, str) or not successor:
        failures.append("receipt lacks successor_execution_source")
    elif not (ROOT / successor).exists():
        failures.append(f"successor execution source does not resolve: {successor}")

    locations = receipt.get("material_state_locations")
    if not isinstance(locations, list) or not locations:
        failures.append("receipt lacks material_state_locations")
    else:
        for location in locations:
            if not isinstance(location, str) or not location:
                failures.append("material_state_locations must contain non-empty strings")
                continue
            if location == str(receipt_path.relative_to(ROOT)):
                continue
            candidate = ROOT / location
            if not candidate.exists():
                failures.append(f"material state location does not resolve: {location}")
    return failures


def build_entry(receipt: dict[str, Any], receipt_path: Path) -> dict[str, Any]:
    inventory_paths = [
        value
        for value in receipt.get("material_state_locations", [])
        if isinstance(value, str) and "session-goal-inventories/" in value
    ]
    authority_checked = [
        receipt.get("canonical_handoff", "docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md"),
        str(receipt_path.relative_to(ROOT)),
        *inventory_paths,
    ]
    entry: dict[str, Any] = {
        "session_id": receipt["session_id"],
        "repository": receipt["repository"],
        "task_id": receipt["task_id"],
        "posture": receipt["posture"],
        "claim_state": receipt.get("claim_state", "MERGED_INTO_CANONICAL_WORKSTREAM"),
        "claimant": "repository-native registry intake",
        "claim_created_at": os.getenv("GITHUB_RUN_STARTED_AT", "repository-native"),
        "claim_release_condition": "registry admission and retained retirement validation PASS",
        "authority_checked": list(dict.fromkeys(authority_checked)),
        "current_commit": os.getenv("GITHUB_SHA", "repository-native"),
        "active_task_ownership": receipt["active_task_ownership"],
        "unique_unmerged_state": receipt["unique_unmerged_state"],
        "safe_to_archive": receipt["safe_to_archive"],
        "conflicting_active_owner": receipt["conflicting_active_owner"],
        "successor_execution_source": receipt["successor_execution_source"],
        "material_state_locations": receipt["material_state_locations"],
        "completed_or_transferred": receipt.get("completed_or_transferred", []),
        "collision_boundaries": receipt.get("collision_boundaries", []),
        "required_before_archive": receipt["required_before_archive"],
        "reason": receipt["reason"],
    }
    return entry


def admit(registry: dict[str, Any], receipt: dict[str, Any], receipt_path: Path) -> tuple[str, list[str]]:
    failures = validate_receipt(receipt, receipt_path)
    sessions = registry.get("sessions")
    if not isinstance(sessions, list):
        failures.append("registry sessions is not a list")
        return "REJECTED", failures

    same_session = [row for row in sessions if isinstance(row, dict) and row.get("session_id") == receipt.get("session_id")]
    if same_session:
        matching = [row for row in same_session if row.get("task_id") == receipt.get("task_id")]
        if matching and all(
            row.get("posture") == receipt.get("posture")
            and row.get("safe_to_archive") == receipt.get("safe_to_archive")
            and row.get("active_task_ownership") == receipt.get("active_task_ownership")
            and row.get("unique_unmerged_state") == receipt.get("unique_unmerged_state")
            for row in matching
        ):
            return "ALREADY_ADMITTED", failures
        failures.append("session_id already exists with a conflicting registry disposition")

    task_key = (receipt.get("repository"), receipt.get("task_id"))
    current_owners = [
        row.get("session_id")
        for row in sessions
        if isinstance(row, dict)
        and (row.get("repository"), row.get("task_id")) == task_key
        and row.get("posture") == "CURRENT"
        and row.get("active_task_ownership") is True
    ]
    if current_owners:
        failures.append("task has a CURRENT active owner: " + ", ".join(map(str, current_owners)))

    if failures:
        return "REJECTED", failures
    sessions.append(build_entry(receipt, receipt_path))
    return "ADMITTED", []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True, help="Repository-relative consolidation receipt path")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY.relative_to(ROOT)))
    parser.add_argument("--report", default=str(DEFAULT_REPORT.relative_to(ROOT)))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    receipt_path = ROOT / args.receipt
    registry_path = ROOT / args.registry
    report_path = ROOT / args.report
    failures: list[str] = []
    action = "REJECTED"
    try:
        receipt = load_json(receipt_path)
        registry = load_json(registry_path)
        action, failures = admit(registry, receipt, receipt_path)
        if args.apply and action == "ADMITTED" and not failures:
            registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    except ValueError as exc:
        failures.append(str(exc))

    report = {
        "schema_version": "1.0.0",
        "status_type": "session_registry_intake_report",
        "status": "PASS" if not failures and action in {"ADMITTED", "ALREADY_ADMITTED"} else "FAIL",
        "action": action,
        "receipt": args.receipt,
        "registry": args.registry,
        "applied": bool(args.apply and action == "ADMITTED" and not failures),
        "failures": failures,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"SESSION_REGISTRY_INTAKE_{report['status']}:{action}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
