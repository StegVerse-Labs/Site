#!/usr/bin/env python3
"""Verify Conectrr source evidence remains distinct from downstream evaluation."""
from __future__ import annotations
import copy, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "conectrr-independent-evaluation.fixture.json"


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    source = payload["source_event"]
    downstream = payload["downstream_event"]
    original = copy.deepcopy(source)
    errors: list[str] = []

    if source["event_id"] == downstream["event_id"]:
        errors.append("events must have distinct stable identifiers")
    if downstream.get("parent_event_id") != source.get("event_id"):
        errors.append("downstream parent reference does not resolve to source event")
    if source.get("event_id") not in downstream.get("evidence_refs", []):
        errors.append("downstream decision does not cite source evidence event")
    projection = downstream.get("governed_projection", {})
    if projection.get("agreement_with_source") is not False:
        errors.append("fixture does not prove preserved disagreement")
    if projection.get("source_mutation_permitted") is not False:
        errors.append("source mutation boundary is not fail-closed")
    if projection.get("authority_effect") != "none":
        errors.append("fixture improperly grants authority")
    if source != original:
        errors.append("source record changed during downstream evaluation")

    event_stream = [source, downstream]
    json_export = json.dumps({"events": event_stream}, sort_keys=True)
    jsonl_export = "\n".join(json.dumps(event, sort_keys=True) for event in event_stream) + "\n"
    if len(json.loads(json_export)["events"]) != 2:
        errors.append("JSON export does not preserve both events")
    if len([line for line in jsonl_export.splitlines() if line]) != 2:
        errors.append("JSONL export does not preserve both events")

    if errors:
        print("CONECTRR_INDEPENDENT_EVALUATION_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONECTRR_INDEPENDENT_EVALUATION_CHECK=PASS")
    print("source_event=evidence")
    print("downstream_event=decision")
    print("agreement_with_source=false")
    print("source_mutation=false")
    print("exports=json,jsonl")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
