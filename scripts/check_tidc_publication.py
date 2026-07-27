#!/usr/bin/env python3
"""Fail-closed static validator for the TIDC open research publication."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "technology-induced-discovery-clustering.html"
LEDGER = ROOT / "data" / "tidc" / "pilot-events-v0.1.json"
HANDOFF = ROOT / "docs" / "TIDC_OPEN_RESEARCH_HANDOFF.md"
CONSTRAINT_NOTE = ROOT / "docs" / "TIDC_CONSTRAINT_PRESSURE_HYPOTHESIS.md"
REGISTRY = ROOT / "public-registry.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TIDC_PUBLICATION_INVALID: {message}")


def main() -> None:
    for path in (PAGE, LEDGER, HANDOFF, CONSTRAINT_NOTE, REGISTRY):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        "PILOT · NOT CONFIRMATORY",
        "RESEARCH_NOTE",
        "Site is the public mirror, not proof authority",
        "data/tidc/pilot-events-v0.1.json",
        "docs/TIDC_OPEN_RESEARCH_HANDOFF.md",
        "docs/TIDC_CONSTRAINT_PRESSURE_HYPOTHESIS.md",
        "Constraint-pressure extension",
        "architectural efficiency != governed execution",
        "Falsification posture",
    ):
        require(marker in page, f"page missing marker: {marker}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    require(ledger.get("schema") == "stegverse.site.tidc.pilot_events.v0.1", "wrong ledger schema")
    require(ledger.get("research_state") == "PILOT_NOT_CONFIRMATORY", "research state is not fail-closed")
    events = ledger.get("events", [])
    sources = ledger.get("sources", [])
    require(len(events) == 10, "pilot must contain exactly 10 seed events")
    require(len(sources) == 10, "pilot must contain exactly 10 source records")

    event_ids = [event.get("event_id") for event in events]
    source_ids = [source.get("source_id") for source in sources]
    require(len(event_ids) == len(set(event_ids)), "duplicate event_id")
    require(len(source_ids) == len(set(source_ids)), "duplicate source_id")

    allowed_dependency = set(ledger["coding_rules"]["dependency_classes"])
    allowed_orientation = set(ledger["coding_rules"]["orientations"])
    allowed_confidence = set(ledger["coding_rules"]["confidence"])
    source_id_set = set(source_ids)
    for event in events:
        require(event.get("dependency_class") in allowed_dependency, f"invalid dependency class for {event.get('event_id')}")
        require(event.get("orientation") in allowed_orientation, f"invalid orientation for {event.get('event_id')}")
        require(event.get("coding_confidence") in allowed_confidence, f"invalid confidence for {event.get('event_id')}")
        require(event.get("source_id") in source_id_set, f"unresolved source for {event.get('event_id')}")
        require(isinstance(event.get("open_questions"), list) and event["open_questions"], f"missing uncertainty for {event.get('event_id')}")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    claims = {claim.get("id"): claim for claim in registry.get("claims", [])}
    claim = claims.get("TIDC-OPEN-RESEARCH-001")
    require(claim is not None, "public registry claim missing")
    require(claim.get("posture") == "RESEARCH_NOTE", "registry posture must remain RESEARCH_NOTE")
    public_pages = claim.get("public_pages", [])
    for path in (
        "technology-induced-discovery-clustering.html",
        "data/tidc/pilot-events-v0.1.json",
        "docs/TIDC_OPEN_RESEARCH_HANDOFF.md",
        "docs/TIDC_CONSTRAINT_PRESSURE_HYPOTHESIS.md",
    ):
        require(path in public_pages, f"registry missing TIDC surface: {path}")
    require("constraint-pressure" in claim.get("source_stage", ""), "registry source stage missing conceptual extension")

    handoff = HANDOFF.read_text(encoding="utf-8")
    require("Release 0: research opening and seed ledger        COMPLETE" in handoff, "handoff release state missing")
    require("The gate is not whether the hypothesis appears supported." in handoff, "coding-reliability gate missing")
    require("event_ledger_changed: false" in handoff, "conceptual-only ledger boundary missing")
    require("architectural efficiency != governed execution" in handoff, "governance boundary missing")

    note = CONSTRAINT_NOTE.read_text(encoding="utf-8")
    for marker in (
        "research_state: CONCEPTUAL_HYPOTHESIS",
        "confirmatory_status: NOT_TESTED",
        "β1 > 0",
        "β2 < 0",
        "National labels must not be used as substitutes for laboratory-level evidence.",
        "Efficiency changes the economics of capability. It does not by itself establish trustworthy execution.",
    ):
        require(marker in note, f"constraint note missing marker: {marker}")

    print("TIDC_PUBLICATION_VALID")
    print(
        f"events={len(events)} sources={len(sources)} "
        "posture=RESEARCH_NOTE state=PILOT_NOT_CONFIRMATORY "
        "constraint_pressure=CONCEPTUAL_HYPOTHESIS"
    )


if __name__ == "__main__":
    main()
