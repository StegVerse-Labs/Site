#!/usr/bin/env python3
"""Project persisted runtime verification evidence into live autonomy telemetry."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "autonomy"
STATUS_PATH = DATA / "live-status.json"
EVIDENCE_PATH = DATA / "runtime-verification-evidence.json"
SITE = "StegVerse-Labs/Site"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    status = load(STATUS_PATH)
    evidence = load(EVIDENCE_PATH)
    state = str(evidence.get("state", "FAIL")).upper()
    if state not in {"PASS", "FAIL"}:
        raise ValueError("runtime evidence state must be PASS or FAIL")

    required = int(evidence.get("required_checks", 0))
    passed = int(evidence.get("passed_required_checks", 0))
    failed_ids = [str(value) for value in evidence.get("failed_required_check_ids", [])]
    generated_at = str(evidence.get("generated_at", ""))
    if required <= 0 or not generated_at:
        raise ValueError("runtime evidence lacks required check count or timestamp")

    graph = status.setdefault("task_graph", {})
    nodes = [node for node in graph.setdefault("nodes", []) if node.get("id") != "site-runtime-verification"]
    node_status = "COMPLETE" if state == "PASS" and passed == required else "BLOCKED_BY_RUNTIME_EVIDENCE"
    result = (
        f"All {required} required runtime checks passed, including both mobile flows."
        if node_status == "COMPLETE"
        else f"{passed} of {required} required runtime checks passed; failed checks: {', '.join(failed_ids) or 'unknown'}."
    )
    nodes.append({
        "id": "site-runtime-verification",
        "title": "Verify public Site runtime",
        "status": node_status,
        "result": result,
        "owner": SITE,
        "updated_at": generated_at,
        "depends_on": ["site-runtime-check-spec"],
        "evidence_path": "data/autonomy/runtime-verification-evidence.json"
    })
    graph["nodes"] = nodes

    edges = graph.setdefault("edges", [])
    edge = {"from": "site-runtime-check-spec", "to": "site-runtime-verification", "type": "sequence"}
    if not any(item.get("from") == edge["from"] and item.get("to") == edge["to"] and item.get("type") == edge["type"] for item in edges):
        edges.append(edge)

    corrective = [item for item in status.setdefault("corrective_actions", []) if item.get("id") != "runtime-verification-failure"]
    if node_status != "COMPLETE":
        corrective.append({
            "id": "runtime-verification-failure",
            "action": "Repair failed public Site runtime checks",
            "status": "MACHINE_ACTION_REQUIRED",
            "reason": result,
            "evidence_path": "data/autonomy/runtime-verification-evidence.json"
        })
    status["corrective_actions"] = corrective
    status["runtime_verification"] = {
        "state": state,
        "required_checks": required,
        "passed_required_checks": passed,
        "failed_required_check_ids": failed_ids,
        "evidence_generated_at": generated_at,
        "evidence_path": "data/autonomy/runtime-verification-evidence.json",
        "completion_authority": False,
        "release_authority": False,
        "admissibility_authority": False
    }
    write(STATUS_PATH, status)
    print(f"runtime evidence bound to live telemetry: {state} {passed}/{required}")


if __name__ == "__main__":
    main()
