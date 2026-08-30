#!/usr/bin/env python3
"""Fail-closed validator for TIDC negative-control candidate collection."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/tidc/negative-controls/negative-control-design-v0.1.json"
TASK = ROOT / "data/tasks/tidc-negative-controls-001.json"
EXPECTED = {
    "NC-CLASS-001": ROOT / "data/tidc/negative-controls/technology-present-no-output/QAI-2025-JP-OSAKA.json",
    "NC-CLASS-002": ROOT / "data/tidc/negative-controls/pre-access-placebos/QNT-001-vs-QAI-2025-JP-OSAKA.json",
    "NC-CLASS-003": ROOT / "data/tidc/negative-controls/supportive-not-necessary/AI-002-LLVM-integration.json",
}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(msg: str):
    raise SystemExit(f"TIDC_NEGATIVE_CONTROLS_INVALID: {msg}")

def main() -> None:
    design = load(DESIGN)
    task = load(TASK)
    if design.get("schema") != "stegverse.site.tidc.negative_control_design.v0.1":
        fail("wrong design schema")
    if task.get("task_id") != "TIDC-NEGATIVE-CONTROLS-001":
        fail("wrong task id")
    if task.get("authority_effect") != "NONE":
        fail("task authority boundary invalid")
    classes = {row.get("id"): row for row in design.get("control_classes", [])}
    if set(classes) != set(EXPECTED):
        fail("canonical control classes changed")

    seen = []
    for class_id, path in EXPECTED.items():
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")
        row = load(path)
        if row.get("schema") != "stegverse.site.tidc.negative_control_candidate.v0.1":
            fail(f"wrong candidate schema: {path.name}")
        if row.get("control_class_id") != class_id:
            fail(f"class mismatch: {path.name}")
        if row.get("seed_ledger_changed") is not False:
            fail(f"seed ledger boundary missing: {path.name}")
        if row.get("discovery_event_added") is not False:
            fail(f"candidate promoted to discovery event: {path.name}")
        if row.get("authority_effect") != "NONE":
            fail(f"authority escalation: {path.name}")
        if not row.get("control_statement") or not row.get("falsification_use"):
            fail(f"control semantics incomplete: {path.name}")
        seen.append(row["candidate_id"])

    temporal = load(EXPECTED["NC-CLASS-002"])
    if temporal.get("chronology_check", {}).get("outcome_publication_precedes_access") is not True:
        fail("temporal placebo direction not explicit")
    if temporal.get("chronology_check", {}).get("causal_attribution_allowed") is not False:
        fail("temporal placebo does not fail closed")

    dependency = load(EXPECTED["NC-CLASS-003"])
    if dependency.get("dependency_classification", {}).get("for_candidate_generation") != "SUPPORTIVE_OR_POST_GENERATION_NOT_NECESSARY":
        fail("dependency control classification missing")

    access = load(EXPECTED["NC-CLASS-001"])
    if access.get("evidence", {}).get("discovery_cluster_claimed") is not False:
        fail("access control overclaims discovery cluster")

    print("TIDC_NEGATIVE_CONTROLS_VALID")
    print(f"classes={len(EXPECTED)} candidates={len(seen)}")
    print("seed_ledger_changed=false")
    print("authority_effect=NONE")

if __name__ == "__main__":
    main()
