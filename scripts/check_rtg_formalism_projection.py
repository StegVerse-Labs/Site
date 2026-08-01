#!/usr/bin/env python3
"""Observe RTG formalism-publication readiness without external/manual tasks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SITE_ROOT = Path(__file__).resolve().parents[1]
TASK_STATE = SITE_ROOT / "data/formalism-publication/rtg-projection-task-state.json"
OUTPUT = SITE_ROOT / "data/formalism-publication/rtg-projection-observation.json"
EXPECTED_LANES = {
    3: "hosted-deterministic-rendering",
    4: "predecessor-and-statement-integration",
    5: "corpus-proof-and-artifact-closure",
}
TERMINAL_SOURCE_STATES = {"COMPLETE_AWAITING_ACCEPTANCE", "ACCEPTED"}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rtg-root", default="../RTG")
    args = parser.parse_args()

    rtg_root = Path(args.rtg_root).resolve()
    task = load(TASK_STATE)
    source = task["source"]
    blockers: list[str] = []
    observations: dict[str, Any] = {}

    manifest_path = rtg_root / source["manifest_path"]
    schema_path = rtg_root / source["handback_schema_path"]
    if not manifest_path.exists():
        blockers.append(f"missing source manifest: {source['manifest_path']}")
        manifest: dict[str, Any] = {}
    else:
        manifest = load(manifest_path)
        observations["manifest_state"] = manifest.get("state")
        observations["activation_eligible"] = manifest.get("activation_eligible")
        observations["authority_effect"] = manifest.get("authority_effect")
        if manifest.get("activation_eligible") is not False:
            blockers.append("source activation_eligible must remain false before accepted readiness")
        if manifest.get("authority_effect") != "NONE":
            blockers.append("source authority_effect must remain NONE")

    if not schema_path.exists():
        blockers.append(f"missing handback schema: {source['handback_schema_path']}")

    lane_results: dict[str, Any] = {}
    all_terminal = True
    for issue, expected_lane in EXPECTED_LANES.items():
        relative = source["lane_handbacks"][str(issue)]
        path = rtg_root / relative
        if not path.exists():
            lane_results[str(issue)] = {"state": "MISSING", "path": relative}
            blockers.append(f"missing issue {issue} handback: {relative}")
            all_terminal = False
            continue
        handback = load(path)
        state = handback.get("state")
        lane_id = handback.get("lane_id")
        lane_results[str(issue)] = {
            "state": state,
            "lane_id": lane_id,
            "path": relative,
            "remaining_blockers": handback.get("remaining_blockers", []),
        }
        if handback.get("issue") != issue or lane_id != expected_lane:
            blockers.append(f"issue {issue} handback identity mismatch")
        if handback.get("authority_effect") != "NONE":
            blockers.append(f"issue {issue} handback authority_effect must be NONE")
        if state not in TERMINAL_SOURCE_STATES:
            all_terminal = False

    site_state = (
        "READY_TO_BUILD_IMPORT_SCHEMA"
        if all_terminal and not blockers
        else "OBSERVING_SOURCE_WITH_RECORDED_BLOCKERS"
    )
    result = {
        "schema_version": "1.0.0",
        "task_id": task["task_id"],
        "source_repository": source["repository"],
        "source_branch": source["branch"],
        "site_state": site_state,
        "source_lanes": lane_results,
        "observations": observations,
        "blockers": blockers,
        "manual_external_tasks": [],
        "next_machine_action": (
            "build and validate the Site import schema"
            if site_state == "READY_TO_BUILD_IMPORT_SCHEMA"
            else "continue scheduled source observation and preserve exact blockers"
        ),
        "authority_effect": false,
        "activation_effect": false
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
