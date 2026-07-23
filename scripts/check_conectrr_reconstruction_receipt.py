#!/usr/bin/env python3
"""Validate reconstruction of distinct Conectrr source and StegVerse decision records."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "conectrr-reconstruction-receipt.fixture.json"
EVENTS = ROOT / "data" / "conectrr-independent-evaluation.fixture.json"


def main() -> int:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    events = json.loads(EVENTS.read_text(encoding="utf-8"))
    source = events["source_event"]
    downstream = events["downstream_event"]
    reconstruction = receipt.get("reconstruction", {})
    errors: list[str] = []

    if receipt.get("source_event_id") != source.get("event_id"):
        errors.append("receipt source_event_id does not match source event")
    if receipt.get("downstream_event_id") != downstream.get("event_id"):
        errors.append("receipt downstream_event_id does not match downstream event")
    if receipt.get("ordering") != [source.get("event_id"), downstream.get("event_id")]:
        errors.append("receipt ordering does not preserve source-before-decision chronology")
    if downstream.get("parent_event_id") != source.get("event_id"):
        errors.append("downstream parent reference does not resolve")
    if source.get("event_id") not in downstream.get("evidence_refs", []):
        errors.append("downstream evidence reference does not resolve")
    if receipt.get("source_hash") != source.get("governed_projection", {}).get("source_hash"):
        errors.append("receipt source hash does not match imported source record")
    if not isinstance(receipt.get("source_bytes_hash"), str) or not receipt["source_bytes_hash"].startswith("sha256:"):
        errors.append("source byte hash is missing or malformed")
    if source.get("event_id") == downstream.get("event_id"):
        errors.append("source and downstream records are not distinct")
    if reconstruction.get("agreement_with_source") is not False:
        errors.append("receipt does not preserve downstream disagreement")
    for field in ("source_record_reconstructed", "downstream_record_reconstructed", "references_resolved", "source_unchanged", "records_distinct"):
        if reconstruction.get(field) is not True:
            errors.append(f"reconstruction field not true: {field}")
    if receipt.get("authority_effect") != "none":
        errors.append("reconstruction receipt improperly grants authority")

    if errors:
        print("CONECTRR_RECONSTRUCTION_RECEIPT_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONECTRR_RECONSTRUCTION_RECEIPT_CHECK=PASS")
    print("source_reconstructed=true")
    print("downstream_reconstructed=true")
    print("records_distinct=true")
    print("disagreement_preserved=true")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
