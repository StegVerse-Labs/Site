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


def observe_source_packet() -> dict[str, Any]:
    index = ROOT / "docs" / "TIDC_SOURCE_PACKET_INDEX.md"
    if not index.exists():
        return {"status": "WAITING_BUILD", "reason": "docs/TIDC_SOURCE_PACKET_INDEX.md is absent"}
    text = index.read_text(encoding="utf-8")
    unresolved_markers = sum(text.lower().count(marker) for marker in ("gap", "missing", "unresolved", "inaccessible"))
    return {
        "status": "IN_PROGRESS" if unresolved_markers else "COMPLETE",
        "exists_at": "docs/TIDC_SOURCE_PACKET_INDEX.md",
        "unresolved_marker_count": unresolved_markers,
        "continuation": "Repository research sessions may resolve one source record at a time without waiting for the independent return.",
    }


def evaluate_activation_gate(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    required = ["TIDC-R2-001", "TIDC-R2-002", "TIDC-R2-003", "TIDC-R2-005", "TIDC-R2-006"]
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
        "schema": "stegverse.site.tidc.coordinator_receipt.v0.1",
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
