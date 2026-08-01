#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data/fixtures/hil-semantic-transformation/bounded-conversation.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    source = data["source"]
    output = data["output"]
    observed: list[str] = []

    if source["claim_class"] == "hypothesis" and output["claim_class"] == "conclusion":
        observed.append("hypothesis_to_conclusion")
    if output["confidence"] > source["confidence"]:
        observed.append("confidence_inflation")
    if set(source["constraints"]) - set(output["constraints"]):
        observed.append("constraint_removal")
    if source["boundary"] != output["boundary"]:
        observed.append("campaign_boundary_reduction")

    expected = data["expected_transformations"]
    failures = sorted(set(expected) ^ set(observed))
    receipt = {
        "receipt_type": "HIL_SEMANTIC_TRANSFORMATION",
        "fixture_id": data["fixture_id"],
        "source_record_id": source["record_id"],
        "output_record_id": output["record_id"],
        "source_claim_class": source["claim_class"],
        "output_claim_class": output["claim_class"],
        "source_confidence": source["confidence"],
        "output_confidence": output["confidence"],
        "transformation_classes": observed,
        "constraints_removed": sorted(set(source["constraints"]) - set(output["constraints"])),
        "authority_effect": False,
        "validation": "PASS" if not failures else "FAIL",
        "failures": failures
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
