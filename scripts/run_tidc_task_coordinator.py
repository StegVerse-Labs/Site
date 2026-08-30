#!/usr/bin/env python3
"""Observe and advance repository-native TIDC tasks without halting on pending evidence."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "data" / "tidc" / "task-graph.v0.1.json"
DEFAULT_OUT = ROOT / "data" / "tidc" / "coordinator" / "latest.json"
RETURNS = ROOT / "data" / "tidc" / "blinded-coding" / "returns"
GENERATED = ROOT / "generated" / "tidc-blinded-results"
ACTIVE_SOURCE = ROOT / "data" / "tidc" / "source-work" / "active.json"
SOURCE_RECEIPTS = ROOT / "data" / "tidc" / "source-receipts"

EXPECTED_SOURCE_RECEIPTS = {
    "SRC-001": "COMP-001.json",
    "SRC-002": "COMP-002.json",
    "SRC-003": "COMP-003.json",
    "SRC-004": "NET-POLYMATH.json",
    "SRC-005": "AI-001.json",
    "SRC-006": "AI-002.json",
    "SRC-007": "AI-003.json",
    "SRC-008": "QNT.json",
    "SRC-009": "QAI-2025-JP-OSAKA.json",
}


def run_command(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "exit_status": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "status": "COMPLETE" if completed.returncode == 0 else "FAILED",
    }


def validate_publication() -> dict[str, Any]:
    return run_command([sys.executable, "scripts/check_tidc_publication.py"])


def validate_reliability() -> dict[str, Any]:
    script = ROOT / "scripts" / "check_tidc_reliability.py"
    if not script.exists():
        return {"status": "WAITING_BUILD", "reason": "scripts/check_tidc_reliability.py is absent"}
    return run_command([sys.executable, str(script.relative_to(ROOT))])


def test_agreement() -> dict[str, Any]:
    test = ROOT / "tests" / "tidc" / "test_agreement_calculator.py"
    if not test.exists():
        return {"status": "WAITING_BUILD", "reason": "tests/tidc/test_agreement_calculator.py is absent"}
    return run_command([sys.executable, str(test.relative_to(ROOT))])


def blinded_returns() -> list[Path]:
    return sorted(RETURNS.glob("*.json")) if RETURNS.exists() else []


def observe_blinded_returns() -> dict[str, Any]:
    files = blinded_returns()
    return {
        "status": "COMPLETE" if files else "WAITING_EVIDENCE",
        "count": len(files),
        "paths": [str(path.relative_to(ROOT)) for path in files],
        "continuation": "Other repository tasks continue while no return is present.",
    }


def process_blinded_returns() -> dict[str, Any]:
    files = blinded_returns()
    if not files:
        return {
            "status": "WAITING_EVIDENCE",
            "reason": "No committed blinded return exists at data/tidc/blinded-coding/returns/.",
            "continuation": "Coordinator does not halt; validators, source audit, and gate observation continue.",
        }

    GENERATED.mkdir(parents=True, exist_ok=True)
    processed: list[dict[str, Any]] = []
    overall = "COMPLETE"
    for path in files:
        base = path.stem
        commands = [
            [sys.executable, "scripts/validate_tidc_blinded_return.py", str(path.relative_to(ROOT))],
            [sys.executable, "scripts/create_tidc_blinded_return_receipt.py", str(path.relative_to(ROOT)), "--out", f"generated/tidc-blinded-results/{base}.receipt.json"],
            [sys.executable, "scripts/compare_tidc_blinded_coding.py", str(path.relative_to(ROOT)), "--json-out", f"generated/tidc-blinded-results/{base}.comparison.json", "--md-out", f"generated/tidc-blinded-results/{base}.comparison.md"],
        ]
        results = [run_command(command) for command in commands]
        if any(result["status"] != "COMPLETE" for result in results):
            overall = "FAILED"
        processed.append({"return": str(path.relative_to(ROOT)), "commands": results})
    return {"status": overall, "processed": processed}


def terminal_source_receipts() -> tuple[list[str], list[str]]:
    terminal: list[str] = []
    invalid: list[str] = []
    for work_id, filename in EXPECTED_SOURCE_RECEIPTS.items():
        path = SOURCE_RECEIPTS / filename
        if not path.exists():
            invalid.append(work_id)
            continue
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            invalid.append(work_id)
            continue
        if receipt.get("work_id") != work_id or receipt.get("status") not in {"COMPLETE", "LIMITATION_RETAINED"}:
            invalid.append(work_id)
            continue
        terminal.append(work_id)
    return terminal, invalid


def observe_source_packet() -> dict[str, Any]:
    index = ROOT / "docs" / "TIDC_SOURCE_PACKET_INDEX.md"
    if not index.exists():
        return {"status": "WAITING_BUILD", "reason": "docs/TIDC_SOURCE_PACKET_INDEX.md is absent"}

    text = index.read_text(encoding="utf-8")
    unresolved_markers = sum(text.lower().count(marker) for marker in ("gap", "missing", "unresolved", "inaccessible"))
    terminal, invalid = terminal_source_receipts()

    active = {}
    if ACTIVE_SOURCE.exists():
        try:
            active = json.loads(ACTIVE_SOURCE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            active = {}

    queue_exhausted = active.get("status") == "QUEUE_EXHAUSTED"
    index_terminal_count_declared = "source_receipts_complete_or_limited: 9" in text
    complete = (
        queue_exhausted
        and len(terminal) == len(EXPECTED_SOURCE_RECEIPTS)
        and not invalid
        and index_terminal_count_declared
    )

    return {
        "status": "COMPLETE" if complete else "IN_PROGRESS",
        "exists_at": "docs/TIDC_SOURCE_PACKET_INDEX.md",
        "terminal_source_receipts": len(terminal),
        "expected_source_receipts": len(EXPECTED_SOURCE_RECEIPTS),
        "invalid_or_missing_work_ids": invalid,
        "source_queue_exhausted": queue_exhausted,
        "unresolved_marker_count": unresolved_markers,
        "limitations_retained": unresolved_markers > 0,
        "completion_boundary": "Terminal retrieval with disclosed limitations is sufficient for archival-source gate review; unresolved limitations remain visible and are not fabricated away.",
        "continuation": (
            "Source retrieval is terminal; preserve disclosed limitations through reliability review."
            if complete
            else "Repository research sessions may resolve one source record at a time without waiting for the independent return."
        ),
    }


def advance_source_queue() -> dict[str, Any]:
    script = ROOT / "scripts" / "advance_tidc_source_queue.py"
    if not script.exists():
        return {"status": "WAITING_BUILD", "reason": "scripts/advance_tidc_source_queue.py is absent"}
    result = run_command([
        sys.executable,
        str(script.relative_to(ROOT)),
        "--out",
        str(ACTIVE_SOURCE.relative_to(ROOT)),
    ])
    if result["status"] != "COMPLETE":
        return result
    active = json.loads(ACTIVE_SOURCE.read_text(encoding="utf-8"))
    active_status = active.get("status")
    return {
        "status": "COMPLETE" if active_status == "QUEUE_EXHAUSTED" else "IN_PROGRESS",
        "active_status": active_status,
        "active_work_id": active.get("work_id"),
        "active_task": active.get("task"),
        "receipt_path": active.get("receipt_path"),
        "remaining_count": active.get("remaining_count", 0),
        "development_halted": False,
        "continuation": active.get("continuation"),
        "command_result": result,
    }


def evaluate_activation_gate(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    required = [
        "TIDC-R2-001", "TIDC-R2-002", "TIDC-R2-003",
        "TIDC-R2-005", "TIDC-R2-006", "TIDC-R2-006A",
    ]
    incomplete = [task_id for task_id in required if results.get(task_id, {}).get("status") != "COMPLETE"]
    gate_path = ROOT / "data" / "tidc" / "release-2-gate.v0.1.json"
    declared_state = None
    if gate_path.exists():
        declared_state = json.loads(gate_path.read_text(encoding="utf-8")).get("state")
    return {
        "status": "READY_TO_ACTIVATE" if not incomplete else "BLOCKED_CONTINUING",
        "declared_gate_state": declared_state,
        "incomplete_tasks": incomplete,
        "activation_permitted": not incomplete,
        "continuation": "BLOCKED_CONTINUING means activation is blocked, not development.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    handlers = {
        "validate_publication": validate_publication,
        "validate_reliability": validate_reliability,
        "test_agreement": test_agreement,
        "observe_blinded_returns": observe_blinded_returns,
        "process_blinded_returns": process_blinded_returns,
        "observe_source_packet": observe_source_packet,
        "advance_source_queue": advance_source_queue,
    }

    results: dict[str, dict[str, Any]] = {}
    for task in graph["tasks"]:
        task_id = task["task_id"]
        handler = task["handler"]
        if handler == "evaluate_activation_gate":
            results[task_id] = evaluate_activation_gate(results)
        elif handler == "write_coordinator_receipt":
            results[task_id] = {"status": "COMPLETE", "exists_at": str(args.out)}
        else:
            results[task_id] = handlers[handler]()
        results[task_id]["name"] = task["name"]
        results[task_id]["exists_at"] = task["exists_at"]

    statuses = [result["status"] for result in results.values()]
    receipt = {
        "schema": "stegverse.site.tidc.coordinator_receipt.v0.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": graph["scope"],
        "policy": graph["policy"],
        "summary": {
            "tasks": len(results),
            "complete": statuses.count("COMPLETE"),
            "in_progress": statuses.count("IN_PROGRESS"),
            "waiting_evidence": statuses.count("WAITING_EVIDENCE"),
            "waiting_build": statuses.count("WAITING_BUILD"),
            "failed": statuses.count("FAILED"),
            "activation_state": results["TIDC-R2-007"]["status"],
            "active_source_work_id": results.get("TIDC-R2-006A", {}).get("active_work_id"),
            "development_halted": False,
        },
        "tasks": results,
        "boundary": "Pending evidence blocks only dependent activation. It does not halt repository development or unrelated executable tasks.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt["summary"], sort_keys=True))

    if receipt["summary"]["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
