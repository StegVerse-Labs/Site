#!/usr/bin/env python3
"""Fail-closed static validator for the TIDC open research publication."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "technology-induced-discovery-clustering.html"
LEDGER = ROOT / "data" / "tidc" / "pilot-events-v0.1.json"
PRECURSORS = ROOT / "data" / "tidc" / "access-precursors-v0.1.json"
SECOND_PACKET = ROOT / "data" / "tidc" / "second-coding-packet-v0.1.json"
CODER_TEMPLATE = ROOT / "data" / "tidc" / "coder-response.template.v0.1.json"
DISAGREEMENT_TEMPLATE = ROOT / "data" / "tidc" / "disagreement-ledger.template.v0.1.json"
AGREEMENT_SCRIPT = ROOT / "scripts" / "calculate_tidc_agreement.py"
HANDOFF = ROOT / "docs" / "TIDC_OPEN_RESEARCH_HANDOFF.md"
CONSTRAINT_NOTE = ROOT / "docs" / "TIDC_CONSTRAINT_PRESSURE_HYPOTHESIS.md"
ACCESS_NOTE = ROOT / "docs" / "TIDC_QUANTUM_ACCESS_INFLECTION_TRACKING.md"
REGISTRY = ROOT / "public-registry.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TIDC_PUBLICATION_INVALID: {message}")


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"TIDC_PUBLICATION_INVALID: unreadable {path.relative_to(ROOT)}: {exc}") from exc


def main() -> None:
    required = (
        PAGE, LEDGER, PRECURSORS, SECOND_PACKET, CODER_TEMPLATE,
        DISAGREEMENT_TEMPLATE, AGREEMENT_SCRIPT, HANDOFF,
        CONSTRAINT_NOTE, ACCESS_NOTE, REGISTRY,
    )
    for path in required:
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        "PILOT · NOT CONFIRMATORY",
        "RESEARCH_NOTE",
        "Site is the public mirror, not proof authority",
        "data/tidc/pilot-events-v0.1.json",
        "docs/TIDC_OPEN_RESEARCH_HANDOFF.md",
        "docs/TIDC_CONSTRAINT_PRESSURE_HYPOTHESIS.md",
        "docs/TIDC_QUANTUM_ACCESS_INFLECTION_TRACKING.md",
        "Quantum access-layer inflection under observation",
        "Constraint-pressure extension",
        "Falsification posture",
    ):
        require(marker in page, f"page missing marker: {marker}")

    ledger = read_json(LEDGER)
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

    precursor_ledger = read_json(PRECURSORS)
    require(precursor_ledger.get("schema") == "stegverse.site.tidc.access_precursors.v0.1", "wrong precursor schema")
    require(precursor_ledger.get("research_state") == "PILOT_NOT_CONFIRMATORY", "precursor state is not fail-closed")
    precursors = precursor_ledger.get("precursors", [])
    precursor_sources = precursor_ledger.get("sources", [])
    require(len(precursors) == 1, "precursor pilot must contain exactly one case")
    require(len(precursor_sources) == 3, "precursor pilot must contain exactly three source records")

    case_ids = [case.get("case_id") for case in precursors]
    precursor_source_ids = [source.get("source_id") for source in precursor_sources]
    require(len(case_ids) == len(set(case_ids)), "duplicate precursor case_id")
    require(len(precursor_source_ids) == len(set(precursor_source_ids)), "duplicate precursor source_id")
    require(case_ids == ["QAI-2025-JP-OSAKA"], "unexpected precursor case")

    allowed_event_classes = set(precursor_ledger["coding_rules"]["event_classes"])
    allowed_precursor_orientations = set(precursor_ledger["coding_rules"]["orientations"])
    allowed_precursor_confidence = set(precursor_ledger["coding_rules"]["confidence"])
    precursor_source_id_set = set(precursor_source_ids)
    for case in precursors:
        require(case.get("event_class") in allowed_event_classes, f"invalid precursor class for {case.get('case_id')}")
        require(case.get("orientation") in allowed_precursor_orientations, f"invalid precursor orientation for {case.get('case_id')}")
        require(case.get("coding_confidence") in allowed_precursor_confidence, f"invalid precursor confidence for {case.get('case_id')}")
        require(case.get("discovery_cluster_claimed") is False, f"precursor overclaims discovery cluster for {case.get('case_id')}")
        require(case.get("pilot_discovery_ledger_changed") is False, f"precursor contaminates discovery ledger for {case.get('case_id')}")
        require(set(case.get("source_ids", [])) <= precursor_source_id_set, f"unresolved precursor source for {case.get('case_id')}")
        require(isinstance(case.get("longitudinal_measures"), list) and case["longitudinal_measures"], f"missing longitudinal measures for {case.get('case_id')}")
        require(isinstance(case.get("open_questions"), list) and case["open_questions"], f"missing precursor uncertainty for {case.get('case_id')}")

    packet = read_json(SECOND_PACKET)
    require(packet.get("schema") == "stegverse.site.tidc.second_coding_packet.v0.1", "wrong second-coding packet schema")
    require(packet.get("posture") == "BLINDED_RELIABILITY_PACKET", "second-coding packet posture invalid")
    candidates = packet.get("candidate_records", [])
    candidate_ids = [record.get("record_id") for record in candidates]
    require(len(candidates) == 11, "second-coding packet must contain 11 candidate records")
    require(set(candidate_ids) == set(event_ids + case_ids), "second-coding packet does not match pilot and precursor records")
    require("Disagreement is a research output" in packet.get("instructions", {}).get("disagreement", ""), "packet disagreement rule missing")

    coder_template = read_json(CODER_TEMPLATE)
    require(coder_template.get("schema") == "stegverse.site.tidc.coder_response.v0.1", "wrong coder response schema")
    require(coder_template.get("coder", {}).get("independence_attestation") is False, "template must require explicit independence attestation")
    require(coder_template.get("research_state") == "PILOT_NOT_CONFIRMATORY", "coder template state invalid")

    disagreement = read_json(DISAGREEMENT_TEMPLATE)
    require(disagreement.get("schema") == "stegverse.site.tidc.disagreement_ledger.v0.1", "wrong disagreement schema")
    require(disagreement.get("posture") == "RELIABILITY_OUTPUT_NOT_CONFIRMATION", "disagreement posture invalid")
    require("must not be silently removed" in disagreement.get("boundary", ""), "disagreement retention boundary missing")

    agreement_source = AGREEMENT_SCRIPT.read_text(encoding="utf-8")
    for marker in (
        "TIDC_AGREEMENT_INVALID",
        "independence_attestation",
        "RELIABILITY_OUTPUT_NOT_CONFIRMATION",
        "does not confirm the TIDC hypothesis",
    ):
        require(marker in agreement_source, f"agreement calculator missing marker: {marker}")

    registry = read_json(REGISTRY)
    claims = {claim.get("id"): claim for claim in registry.get("claims", [])}
    claim = claims.get("TIDC-OPEN-RESEARCH-001")
    require(claim is not None, "public registry claim missing")
    require(claim.get("posture") == "RESEARCH_NOTE", "registry posture must remain RESEARCH_NOTE")
    public_pages = claim.get("public_pages", [])
    for path in (
        "technology-induced-discovery-clustering.html",
        "data/tidc/pilot-events-v0.1.json",
        "data/tidc/access-precursors-v0.1.json",
        "docs/TIDC_OPEN_RESEARCH_HANDOFF.md",
        "docs/TIDC_CONSTRAINT_PRESSURE_HYPOTHESIS.md",
        "docs/TIDC_QUANTUM_ACCESS_INFLECTION_TRACKING.md",
    ):
        require(path in public_pages, f"registry missing TIDC surface: {path}")
    require("access-inflection" in claim.get("source_stage", ""), "registry source stage missing access-inflection extension")
    require("constraint-pressure" in claim.get("source_stage", ""), "registry source stage missing constraint extension")

    handoff = HANDOFF.read_text(encoding="utf-8")
    require("Release 0: research opening and seed ledger        COMPLETE" in handoff, "handoff release state missing")
    require("The gate is not whether the hypothesis appears supported." in handoff, "coding-reliability gate missing")
    require("event_ledger_changed: false" in handoff, "conceptual-only ledger boundary missing")
    require("tracked precursor != discovery event" in handoff, "precursor authority boundary missing")
    require("accessibility != admissibility" in handoff, "access governance boundary missing")

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

    access_note = ACCESS_NOTE.read_text(encoding="utf-8")
    for marker in (
        "tracked_case_id: QAI-2025-JP-OSAKA",
        "ledger_event_added: false",
        "The case does not yet demonstrate a discovery cluster.",
        "Accessibility is not admissibility.",
        "pilot_event_ledger_changed: no",
    ):
        require(marker in access_note, f"access note missing marker: {marker}")

    print("TIDC_PUBLICATION_VALID")
    print(
        f"events={len(events)} sources={len(sources)} "
        f"precursors={len(precursors)} precursor_sources={len(precursor_sources)} "
        f"coding_candidates={len(candidates)} reliability_assets=4 "
        "posture=RESEARCH_NOTE state=PILOT_NOT_CONFIRMATORY"
    )


if __name__ == "__main__":
    main()
