#!/usr/bin/env python3
"""Observe and advance RTG formalism-publication readiness without external tasks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SITE_ROOT = Path(__file__).resolve().parents[1]
TASK_STATE = SITE_ROOT / "data/formalism-publication/rtg-projection-task-state.json"
OUTPUT = SITE_ROOT / "data/formalism-publication/rtg-projection-observation.json"
IMPORT_SCHEMA = SITE_ROOT / "data/formalism-publication/rtg-publication-readiness.schema.json"
PROJECTION = SITE_ROOT / "formalisms/rtg/index.html"
MACHINE_BASE = Path("review/volume-I-integrated-v0.9.0/machine-execution")
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
    observations: dict[str, Any] = {
        "site_import_schema_present": IMPORT_SCHEMA.exists(),
        "review_only_projection_present": PROJECTION.exists(),
    }

    if not IMPORT_SCHEMA.exists():
        blockers.append("missing Site import schema: data/formalism-publication/rtg-publication-readiness.schema.json")
    if not PROJECTION.exists():
        blockers.append("missing review-only Site projection: formalisms/rtg/index.html")

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
        blockers.append(f"missing source handback schema: {source['handback_schema_path']}")

    convergence_path = rtg_root / MACHINE_BASE / "formalism-convergence-state.json"
    refresh_path = rtg_root / MACHINE_BASE / "site-projection-refresh-signal.json"
    if convergence_path.exists():
        convergence = load(convergence_path)
    else:
        convergence = {
            "state": "NOT_YET_PERSISTED",
            "next_machine_action": "RTG convergence workflow must create formalism-convergence-state.json",
            "manual_external_tasks": [],
        }
        blockers.append(f"missing RTG convergence state: {MACHINE_BASE / 'formalism-convergence-state.json'}")
    if refresh_path.exists():
        refresh = load(refresh_path)
    else:
        refresh = {
            "refresh_required": True,
            "source_state": convergence.get("state"),
            "manual_external_tasks": [],
        }
        blockers.append(f"missing RTG Site refresh signal: {MACHINE_BASE / 'site-projection-refresh-signal.json'}")
    observations["rtg_convergence"] = convergence
    observations["rtg_site_refresh_signal"] = refresh

    machine_receipts: dict[str, Any] = {}
    for issue in EXPECTED_LANES:
        relative = MACHINE_BASE / f"lane-{issue}-observation.json"
        path = rtg_root / relative
        if path.exists():
            machine_receipts[str(issue)] = load(path)
        else:
            machine_receipts[str(issue)] = {
                "state": "NOT_YET_PERSISTED",
                "path": str(relative),
                "next_machine_action": "RTG workflow must generate and commit this receipt",
            }
            blockers.append(f"missing RTG machine receipt: {relative}")

    readiness_path = rtg_root / MACHINE_BASE / "readiness-observation.json"
    if readiness_path.exists():
        readiness = load(readiness_path)
    else:
        readiness = {
            "state": "NOT_YET_PERSISTED",
            "next_machine_action": "RTG workflow must generate and commit readiness-observation.json",
        }
        blockers.append(f"missing RTG readiness receipt: {MACHINE_BASE / 'readiness-observation.json'}")
    observations["rtg_machine_readiness"] = readiness

    lane_results: dict[str, Any] = {}
    all_terminal = True
    all_accepted = True
    for issue, expected_lane in EXPECTED_LANES.items():
        relative = source["lane_handbacks"][str(issue)]
        path = rtg_root / relative
        if not path.exists():
            lane_results[str(issue)] = {
                "state": "MISSING",
                "lane_id": expected_lane,
                "path": relative,
                "machine_receipt": machine_receipts[str(issue)],
                "remaining_blockers": ["source handback is missing"],
            }
            blockers.append(f"missing issue {issue} handback: {relative}")
            all_terminal = False
            all_accepted = False
            continue
        handback = load(path)
        state = handback.get("state")
        lane_id = handback.get("lane_id")
        lane_blockers = handback.get("remaining_blockers", [])
        lane_results[str(issue)] = {
            "state": state,
            "lane_id": lane_id,
            "path": relative,
            "machine_receipt": machine_receipts[str(issue)],
            "remaining_blockers": lane_blockers,
        }
        if handback.get("issue") != issue or lane_id != expected_lane:
            blockers.append(f"issue {issue} handback identity mismatch")
        if handback.get("authority_effect") != "NONE":
            blockers.append(f"issue {issue} handback authority_effect must be NONE")
        if state not in TERMINAL_SOURCE_STATES:
            all_terminal = False
        if state != "ACCEPTED":
            all_accepted = False

    if all_accepted and readiness.get("state") == "READY_FOR_CENTRAL_ACCEPTANCE" and not blockers:
        site_state = "ACTIVATION_ELIGIBLE"
        next_action = "perform governed publication-eligibility transition and record receipt"
    elif all_terminal and not blockers:
        site_state = "READY_FOR_CENTRAL_ACCEPTANCE_REVIEW"
        next_action = "record central formalism acceptance from durable repository evidence"
    else:
        site_state = "ACTIVE_REVIEW_ONLY_WITH_MACHINE_EXECUTION"
        next_action = convergence.get(
            "next_machine_action",
            readiness.get("next_machine_action", "continue RTG machine lane execution and recompute"),
        )

    result = {
        "schema_version": "1.1.0",
        "task_id": task["task_id"],
        "source_repository": source["repository"],
        "source_branch": source["branch"],
        "site_state": site_state,
        "source_lanes": lane_results,
        "observations": observations,
        "blockers": blockers,
        "manual_external_tasks": [],
        "next_machine_action": next_action,
        "authority_effect": False,
        "activation_effect": site_state == "ACTIVE_REVIEW_ONLY_WITH_MACHINE_EXECUTION",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
