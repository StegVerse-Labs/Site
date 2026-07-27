#!/usr/bin/env python3
"""Validate a TIDC blinded second-coder JSON return without external dependencies."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PACKET_ID = "BCP-2026-07-27-01"
EXPECTED_IDS = [f"BCP-E{i:02d}" for i in range(1, 11)]
DEPENDENCY = {"Necessary", "Material", "Supportive", "Incidental", "Unresolved"}
ORIENTATION = {"Self-capability", "External", "Mixed", "Unresolved"}
ORIGIN = {"Inherited problem", "Newly formulated by technology", "Mixed", "Unresolved"}
CONFIDENCE = {"High", "Medium", "Low", "Insufficient"}
DATE_FIELDS = (
    "candidate_generation_date",
    "verification_date",
    "publication_date",
    "acceptance_date",
    "recognition_date",
)
RECORD_KEYS = {
    "blind_event_id", "technology_dependency", "orientation", "problem_origin_type",
    *DATE_FIELDS, "coding_confidence", "evidence_rationale", "uncertainties",
    "needs_source_expansion",
}
TOP_KEYS = {"packet_id", "coder_independence_statement", "records", "cross_record_notes"}
INDEPENDENCE_KEYS = {"did_not_inspect_existing_tidc_material", "used_only_supplied_evidence", "notes"}
NOTE_KEYS = {"ambiguous_definitions", "records_that_should_be_split", "possible_systematic_biases_in_packet", "other_notes"}


def fail(message: str) -> None:
    raise SystemExit(f"TIDC_BLINDED_RETURN_INVALID: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_exact_keys(obj: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(obj)
    require(actual == expected, f"{label} keys differ; missing={sorted(expected-actual)} extra={sorted(actual-expected)}")


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing return file: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    require(isinstance(data, dict), "top-level value must be an object")
    return data


def validate(data: dict[str, Any]) -> None:
    require_exact_keys(data, TOP_KEYS, "top-level")
    require(data["packet_id"] == PACKET_ID, "wrong packet_id")

    independence = data["coder_independence_statement"]
    require(isinstance(independence, dict), "coder_independence_statement must be an object")
    require_exact_keys(independence, INDEPENDENCE_KEYS, "coder_independence_statement")
    require(independence["did_not_inspect_existing_tidc_material"] is True, "independence statement not affirmed")
    require(independence["used_only_supplied_evidence"] is True, "supplied-evidence-only statement not affirmed")
    require(isinstance(independence["notes"], str), "independence notes must be a string")

    records = data["records"]
    require(isinstance(records, list), "records must be an array")
    require(len(records) == 10, "records must contain exactly 10 entries")
    ids: list[str] = []
    for index, record in enumerate(records, 1):
        require(isinstance(record, dict), f"record {index} must be an object")
        require_exact_keys(record, RECORD_KEYS, f"record {index}")
        event_id = record["blind_event_id"]
        require(isinstance(event_id, str), f"record {index} blind_event_id must be a string")
        ids.append(event_id)
        require(record["technology_dependency"] in DEPENDENCY, f"{event_id}: invalid technology_dependency")
        require(record["orientation"] in ORIENTATION, f"{event_id}: invalid orientation")
        require(record["problem_origin_type"] in ORIGIN, f"{event_id}: invalid problem_origin_type")
        require(record["coding_confidence"] in CONFIDENCE, f"{event_id}: invalid coding_confidence")
        for field in DATE_FIELDS:
            value = record[field]
            require(value is None or isinstance(value, str), f"{event_id}: {field} must be string or null")
        require(isinstance(record["evidence_rationale"], str) and record["evidence_rationale"].strip(), f"{event_id}: empty evidence_rationale")
        uncertainties = record["uncertainties"]
        require(isinstance(uncertainties, list) and uncertainties, f"{event_id}: uncertainties must be non-empty")
        require(all(isinstance(item, str) and item.strip() for item in uncertainties), f"{event_id}: invalid uncertainty entry")
        require(isinstance(record["needs_source_expansion"], bool), f"{event_id}: needs_source_expansion must be boolean")

    require(ids == EXPECTED_IDS, f"records must be ordered exactly {EXPECTED_IDS}; received {ids}")
    require(len(ids) == len(set(ids)), "duplicate blind_event_id")

    notes = data["cross_record_notes"]
    require(isinstance(notes, dict), "cross_record_notes must be an object")
    require_exact_keys(notes, NOTE_KEYS, "cross_record_notes")
    for key, value in notes.items():
        require(isinstance(value, list), f"cross_record_notes.{key} must be an array")
        require(all(isinstance(item, str) for item in value), f"cross_record_notes.{key} contains non-string value")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("return_json", type=Path)
    args = parser.parse_args()
    data = load(args.return_json)
    validate(data)
    print("TIDC_BLINDED_RETURN_VALID")
    print(f"packet_id={PACKET_ID} records=10 independence=affirmed")


if __name__ == "__main__":
    main()
