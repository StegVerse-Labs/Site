#!/usr/bin/env python3
"""Compare the issued TIDC blinded return with the seed coding and preserve disagreement."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "tidc" / "pilot-events-v0.1.json"
BLIND_TO_EVENT = {f"BCP-E{i:02d}": event_id for i, event_id in enumerate([
    "COMP-001", "COMP-002", "COMP-003", "NET-001", "NET-002",
    "AI-001", "AI-002", "AI-003", "QNT-001", "QNT-002",
], 1)}
FIELDS = (
    "technology_dependency",
    "orientation",
    "problem_origin_type",
    "candidate_generation_date",
    "verification_date",
    "publication_date",
    "acceptance_date",
    "recognition_date",
    "coding_confidence",
)
SEED_FIELD_MAP = {
    "technology_dependency": "dependency_class",
    "orientation": "orientation",
    "problem_origin_type": "problem_origin_type",
    "candidate_generation_date": "candidate_generation_date",
    "verification_date": "verification_date",
    "publication_date": "publication_date",
    "acceptance_date": "acceptance_date",
    "recognition_date": "recognition_date",
    "coding_confidence": "coding_confidence",
}


def fail(message: str) -> None:
    raise SystemExit(f"TIDC_CODING_COMPARISON_INVALID: {message}")


def load_json(path: Path) -> Any:
    if not path.exists():
        fail(f"missing {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}")


def normalize_date(value: Any) -> Any:
    if value is None:
        return None
    if not isinstance(value, str):
        return value
    return value.strip()


def compare(seed_ledger: dict[str, Any], blind_return: dict[str, Any]) -> dict[str, Any]:
    seed_by_id = {event["event_id"]: event for event in seed_ledger.get("events", [])}
    blind_records = blind_return.get("records", [])
    if len(blind_records) != 10:
        fail("blinded return must contain exactly 10 records")

    comparisons: list[dict[str, Any]] = []
    field_totals = Counter()
    field_agreements = Counter()

    for blind in blind_records:
        blind_id = blind.get("blind_event_id")
        if blind_id not in BLIND_TO_EVENT:
            fail(f"unknown blind_event_id: {blind_id}")
        event_id = BLIND_TO_EVENT[blind_id]
        seed = seed_by_id.get(event_id)
        if seed is None:
            fail(f"seed event missing: {event_id}")

        field_results: dict[str, Any] = {}
        for field in FIELDS:
            seed_value = seed.get(SEED_FIELD_MAP[field])
            blind_value = blind.get(field)
            if "date" in field:
                seed_value = normalize_date(seed_value)
                blind_value = normalize_date(blind_value)
            agreed = seed_value == blind_value
            field_totals[field] += 1
            field_agreements[field] += int(agreed)
            field_results[field] = {
                "seed": seed_value,
                "blind": blind_value,
                "agreement": agreed,
            }

        comparisons.append({
            "blind_event_id": blind_id,
            "event_id": event_id,
            "event_name": seed.get("event_name"),
            "field_results": field_results,
            "blind_rationale": blind.get("evidence_rationale"),
            "blind_uncertainties": blind.get("uncertainties"),
            "blind_needs_source_expansion": blind.get("needs_source_expansion"),
        })

    per_field = {}
    for field in FIELDS:
        total = field_totals[field]
        agreements = field_agreements[field]
        per_field[field] = {
            "agreements": agreements,
            "total": total,
            "percent_agreement": round(100 * agreements / total, 2) if total else None,
        }

    classification_fields = ("technology_dependency", "orientation", "problem_origin_type", "coding_confidence")
    date_fields = tuple(field for field in FIELDS if "date" in field)
    class_agree = sum(field_agreements[field] for field in classification_fields)
    class_total = sum(field_totals[field] for field in classification_fields)
    date_agree = sum(field_agreements[field] for field in date_fields)
    date_total = sum(field_totals[field] for field in date_fields)
    all_agree = sum(field_agreements.values())
    all_total = sum(field_totals.values())

    return {
        "schema": "stegverse.site.tidc.blinded_coding_comparison.v0.1",
        "packet_id": blind_return.get("packet_id"),
        "comparison_posture": "DESCRIPTIVE_NOT_VALIDATION",
        "agreement_summary": {
            "all_fields": {"agreements": all_agree, "total": all_total, "percent_agreement": round(100 * all_agree / all_total, 2)},
            "classification_fields": {"agreements": class_agree, "total": class_total, "percent_agreement": round(100 * class_agree / class_total, 2)},
            "date_fields": {"agreements": date_agree, "total": date_total, "percent_agreement": round(100 * date_agree / date_total, 2)},
            "per_field": per_field,
        },
        "comparisons": comparisons,
        "blind_cross_record_notes": blind_return.get("cross_record_notes"),
        "interpretation_boundary": [
            "Raw percent agreement is descriptive and is not proof of coding reliability.",
            "A single AI second coder is not an independent human replication.",
            "Disagreements must be retained and adjudicated transparently rather than overwritten.",
            "Chance-corrected reliability requires sufficient category variation and an appropriate preregistered statistic.",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["agreement_summary"]
    lines = [
        f"# TIDC Blinded Coding Comparison — {result['packet_id']}",
        "",
        "## Posture",
        "",
        "```text",
        "comparison_posture: DESCRIPTIVE_NOT_VALIDATION",
        "second_coder_type: blinded AI",
        "human_replication: not established",
        "disagreements_preserved: true",
        "```",
        "",
        "## Agreement summary",
        "",
        f"- All compared fields: {summary['all_fields']['agreements']}/{summary['all_fields']['total']} ({summary['all_fields']['percent_agreement']}%)",
        f"- Classification fields: {summary['classification_fields']['agreements']}/{summary['classification_fields']['total']} ({summary['classification_fields']['percent_agreement']}%)",
        f"- Date fields: {summary['date_fields']['agreements']}/{summary['date_fields']['total']} ({summary['date_fields']['percent_agreement']}%)",
        "",
        "## Per-field agreement",
        "",
        "| Field | Agreement |",
        "|---|---:|",
    ]
    for field, stats in summary["per_field"].items():
        lines.append(f"| `{field}` | {stats['agreements']}/{stats['total']} ({stats['percent_agreement']}%) |")

    lines.extend(["", "## Disagreements", ""])
    disagreement_count = 0
    for item in result["comparisons"]:
        differing = [(field, values) for field, values in item["field_results"].items() if not values["agreement"]]
        if not differing:
            continue
        disagreement_count += len(differing)
        lines.append(f"### {item['blind_event_id']} / {item['event_id']} — {item['event_name']}")
        lines.append("")
        for field, values in differing:
            lines.append(f"- `{field}`: seed=`{values['seed']}`; blind=`{values['blind']}`")
        lines.append("")
        lines.append(f"Blind rationale: {item['blind_rationale']}")
        lines.append("")
        lines.append("Blind uncertainties:")
        for uncertainty in item.get("blind_uncertainties") or []:
            lines.append(f"- {uncertainty}")
        lines.append("")

    if disagreement_count == 0:
        lines.append("No field-level disagreements were observed. This does not establish independence or validity.")
        lines.append("")

    lines.extend([
        "## Interpretation boundary",
        "",
    ])
    for boundary in result["interpretation_boundary"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("blind_return", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--md-out", type=Path, required=True)
    args = parser.parse_args()

    seed = load_json(LEDGER)
    blind = load_json(args.blind_return)
    result = compare(seed, blind)

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.md_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.md_out.write_text(render_markdown(result), encoding="utf-8")
    print("TIDC_BLINDED_COMPARISON_COMPLETE")
    print(f"json={args.json_out} markdown={args.md_out}")


if __name__ == "__main__":
    main()
