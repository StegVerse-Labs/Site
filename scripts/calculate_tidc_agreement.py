#!/usr/bin/env python3
"""Calculate transparent field-level agreement for TIDC coding artifacts."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SCHEMA = "stegverse.site.tidc.coder_response.v0.1"
OUTPUT_SCHEMA = "stegverse.site.tidc.disagreement_ledger.v0.1"
FIRST_PASS_ROLE = "FIRST_PASS_SNAPSHOT"
EXCLUDED_FIELDS = {
    "evidence_quotes_or_locations",
    "uncertainty_notes",
    "exclusion_reason",
}


def load(path: Path, role: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise SystemExit(f"TIDC_AGREEMENT_INVALID: {path} has unexpected schema")

    coder = data.get("coder", {})
    if role == "first":
        is_snapshot = data.get("coding_role") == FIRST_PASS_ROLE
        is_independent = coder.get("independence_attestation") is True
        if not (is_snapshot or is_independent):
            raise SystemExit(
                f"TIDC_AGREEMENT_INVALID: {path} must be an attested coding response "
                f"or a governed {FIRST_PASS_ROLE}"
            )
        if is_snapshot and coder.get("independence_attestation") is not False:
            raise SystemExit(
                f"TIDC_AGREEMENT_INVALID: {path} first-pass snapshot must not claim independence"
            )
    elif not coder.get("independence_attestation"):
        raise SystemExit(f"TIDC_AGREEMENT_INVALID: {path} lacks independence attestation")

    records = data.get("records")
    if not isinstance(records, list) or not records:
        raise SystemExit(f"TIDC_AGREEMENT_INVALID: {path} has no records")
    ids = [record.get("record_id") for record in records]
    if any(not record_id for record_id in ids) or len(ids) != len(set(ids)):
        raise SystemExit(f"TIDC_AGREEMENT_INVALID: {path} has missing or duplicate record IDs")
    return data


def by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {record["record_id"]: record for record in data["records"]}


def comparable_fields(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    return sorted((set(a) & set(b)) - EXCLUDED_FIELDS - {"record_id"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    first = load(args.first, "first")
    second = load(args.second, "second")
    first_records = by_id(first)
    second_records = by_id(second)
    shared_ids = sorted(set(first_records) & set(second_records))
    if not shared_ids:
        raise SystemExit("TIDC_AGREEMENT_INVALID: no shared record IDs")

    field_counts: dict[str, Counter[str]] = defaultdict(Counter)
    disagreements: list[dict[str, Any]] = []
    total = agreements = unresolved = 0

    for record_id in shared_ids:
        left = first_records[record_id]
        right = second_records[record_id]
        for field in comparable_fields(left, right):
            total += 1
            lv, rv = left.get(field), right.get(field)
            if lv == rv:
                agreements += 1
                field_counts[field]["agreements"] += 1
            else:
                field_counts[field]["disagreements"] += 1
                if lv in (None, "Unresolved") or rv in (None, "Unresolved"):
                    unresolved += 1
                disagreements.append({
                    "record_id": record_id,
                    "field": field,
                    "first_pass_value": lv,
                    "second_pass_value": rv,
                    "resolution_status": "Unresolved",
                    "resolution_rationale": None,
                    "source_locations": [],
                    "codebook_revision_required": False,
                })

    percent = round((agreements / total) * 100, 2) if total else None
    field_metrics = []
    for field, counts in sorted(field_counts.items()):
        field_total = counts["agreements"] + counts["disagreements"]
        field_metrics.append({
            "field": field,
            "comparisons": field_total,
            "exact_agreements": counts["agreements"],
            "disagreements": counts["disagreements"],
            "percent_agreement": round((counts["agreements"] / field_total) * 100, 2) if field_total else None,
        })

    output = {
        "schema": OUTPUT_SCHEMA,
        "research_state": "PILOT_NOT_CONFIRMATORY",
        "posture": "RELIABILITY_OUTPUT_NOT_CONFIRMATION",
        "comparison": {
            "first_pass_id": first["coder"]["coder_id"],
            "first_pass_role": first.get("coding_role", "INDEPENDENT_CODER_RESPONSE"),
            "second_pass_id": second["coder"]["coder_id"],
            "second_pass_independence_attested": True,
            "generated_at": None,
        },
        "summary": {
            "records_compared": len(shared_ids),
            "fields_compared": total,
            "exact_agreements": agreements,
            "disagreements": len(disagreements),
            "unresolved": unresolved,
            "percent_agreement": percent,
        },
        "field_metrics": field_metrics,
        "record_disagreements": disagreements,
        "boundary": "Agreement measures coding reproducibility; it does not confirm the TIDC hypothesis.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"TIDC_AGREEMENT_WRITTEN records={len(shared_ids)} fields={total} agreement={percent}")


if __name__ == "__main__":
    main()
