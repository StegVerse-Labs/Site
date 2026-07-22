#!/usr/bin/env python3
"""Validate reciprocal evaluation evidence references and JSONL replay chains."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/framework-evaluations"
INDEX = BASE / "index.json"
EVIDENCE = BASE / "evidence/index.json"
TEST_CASE_INDEX = BASE / "test-cases/index.json"
VALID_RESULTS = {"PASS", "PARTIAL", "FAIL", "ERROR", "REFUSE", "NOT_TESTED", "INCONCLUSIVE", "DISPUTED"}
VALID_OBSERVATIONS = {"DECLARED", "OBSERVED", "DERIVED", "RECONSTRUCTED", "DISPUTED"}


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise AssertionError(f"missing run stream: {path.relative_to(ROOT)}")
    events = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.name}:{number}: invalid JSON: {exc}") from exc
    if not events:
        raise AssertionError(f"empty run stream: {path.relative_to(ROOT)}")
    return events


def require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> int:
    registry = load_json(INDEX)
    evidence_registry = load_json(EVIDENCE)
    test_index = load_json(TEST_CASE_INDEX)

    evidence_ids = {item.get("evidence_id") for item in evidence_registry.get("evidence", [])}
    require(None not in evidence_ids, "evidence entry missing evidence_id")
    require(len(evidence_ids) == len(evidence_registry.get("evidence", [])), "duplicate evidence_id")

    test_case_ids = {item.get("test_case_id") for item in test_index.get("test_cases", [])}
    require(None not in test_case_ids, "test-case index entry missing test_case_id")

    for entry in registry.get("frameworks", []):
        record = load_json(BASE / entry["evaluation_path"])
        referenced_evidence = set(record.get("self_declaration", {}).get("evidence_refs", []))
        for determination in record.get("determinations", []):
            referenced_evidence.update(determination.get("evidence_refs", []))
        for dispute in record.get("disputes", []):
            referenced_evidence.update(dispute.get("evidence_refs", []))
        require(referenced_evidence <= evidence_ids, f"{entry['framework_id']}: unresolved evidence refs: {sorted(referenced_evidence - evidence_ids)}")

        for run in record.get("test_runs", []):
            require(run.get("test_case_id") in test_case_ids, f"{run.get('run_id')}: unknown test_case_id")
            require(run.get("result") in VALID_RESULTS, f"{run.get('run_id')}: invalid result")
            require(set(run.get("evidence_refs", [])) <= evidence_ids, f"{run.get('run_id')}: unresolved run evidence refs")
            artifacts = run.get("artifact_refs", [])
            require(len(artifacts) == 1, f"{run.get('run_id')}: exactly one canonical JSONL artifact required")
            stream_path = ROOT / artifacts[0]
            events = load_jsonl(stream_path)
            event_ids = [event.get("event_id") for event in events]
            require(all(event_ids), f"{run.get('run_id')}: event missing event_id")
            require(len(event_ids) == len(set(event_ids)), f"{run.get('run_id')}: duplicate event_id")
            require(event_ids == run.get("event_refs"), f"{run.get('run_id')}: event_refs do not preserve JSONL order")

            seen: set[str] = set()
            for position, event in enumerate(events):
                require(event.get("observation_class") in VALID_OBSERVATIONS, f"{event.get('event_id')}: invalid observation_class")
                require(event.get("authority_effect") == "NONE", f"{event.get('event_id')}: authority escalation")
                require(set(event.get("evidence_refs", [])) <= evidence_ids, f"{event.get('event_id')}: unresolved evidence refs")
                parent = event.get("parent_event_id")
                if position == 0:
                    require(parent is None, f"{event.get('event_id')}: first event must have null parent")
                else:
                    require(parent in seen, f"{event.get('event_id')}: parent must reference an earlier event")
                seen.add(event["event_id"])

            require(events[-1].get("event_type") == "evaluation_completed", f"{run.get('run_id')}: terminal event missing")
            require(events[-1].get("result") == run.get("result"), f"{run.get('run_id')}: terminal result mismatch")
            require(events[-1].get("replay_status") == run.get("replay_status"), f"{run.get('run_id')}: replay status mismatch")

    print("RECIPROCAL FRAMEWORK EVALUATION REPLAY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
