#!/usr/bin/env python3
"""Fail-closed validator for TIDC Release 2 reliability assets."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tidc"
DOCS = ROOT / "docs"

SECOND_PACKET = DATA / "second-coding-packet-v0.1.json"
FIRST_PASS = DATA / "coder-response.first-pass.v0.1.json"
CODER_TEMPLATE = DATA / "coder-response.template.v0.1.json"
DISAGREEMENT_TEMPLATE = DATA / "disagreement-ledger.template.v0.1.json"
AGREEMENT_SCRIPT = ROOT / "scripts" / "calculate_tidc_agreement.py"
AGREEMENT_TEST = ROOT / "tests" / "tidc" / "test_agreement_calculator.py"
EXECUTION_STATUS = DOCS / "TIDC_RELIABILITY_EXECUTION_STATUS.md"
CODER_INSTRUCTIONS = DOCS / "TIDC_INDEPENDENT_CODER_INSTRUCTIONS.md"

EXPECTED_IDS = [
    "COMP-001", "COMP-002", "COMP-003", "NET-001", "NET-002",
    "AI-001", "AI-002", "AI-003", "QNT-001", "QNT-002",
    "QAI-2025-JP-OSAKA",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TIDC_RELIABILITY_INVALID: {message}")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"TIDC_RELIABILITY_INVALID: unreadable {path.relative_to(ROOT)}: {exc}") from exc


def main() -> None:
    for path in (
        SECOND_PACKET, FIRST_PASS, CODER_TEMPLATE, DISAGREEMENT_TEMPLATE,
        AGREEMENT_SCRIPT, AGREEMENT_TEST, EXECUTION_STATUS, CODER_INSTRUCTIONS,
    ):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    packet = load(SECOND_PACKET)
    require(packet.get("schema") == "stegverse.site.tidc.second_coding_packet.v0.1", "wrong packet schema")
    require(packet.get("posture") == "BLINDED_RELIABILITY_PACKET", "packet posture must remain blinded")
    packet_ids = [item.get("record_id") for item in packet.get("candidate_records", [])]
    require(packet_ids == EXPECTED_IDS, "packet record order or membership changed")
    require("Disagreement is a research output" in packet.get("instructions", {}).get("disagreement", ""), "disagreement rule missing")

    first = load(FIRST_PASS)
    require(first.get("schema") == "stegverse.site.tidc.coder_response.v0.1", "wrong first-pass schema")
    require(first.get("coding_role") == "FIRST_PASS_SNAPSHOT", "first-pass role missing")
    require(first.get("coder", {}).get("independence_attestation") is False, "first-pass snapshot must not claim independence")
    first_ids = [item.get("record_id") for item in first.get("records", [])]
    require(first_ids == EXPECTED_IDS, "first-pass records do not align with blinded packet")
    require("not independent coding" in first.get("submission_boundary", ""), "first-pass non-independence boundary missing")

    template = load(CODER_TEMPLATE)
    require(template.get("schema") == "stegverse.site.tidc.coder_response.v0.1", "wrong coder template schema")
    require(template.get("coder", {}).get("independence_attestation") is False, "blank template must fail closed")
    require(len(template.get("records", [])) == 1, "coder template must contain exactly one blank record object")

    disagreement = load(DISAGREEMENT_TEMPLATE)
    require(disagreement.get("schema") == "stegverse.site.tidc.disagreement_ledger.v0.1", "wrong disagreement schema")
    require(disagreement.get("posture") == "RELIABILITY_OUTPUT_NOT_CONFIRMATION", "wrong disagreement posture")
    require("must not be silently removed" in disagreement.get("boundary", ""), "disagreement retention boundary missing")

    calculator = AGREEMENT_SCRIPT.read_text(encoding="utf-8")
    for marker in (
        "FIRST_PASS_SNAPSHOT",
        "first-pass snapshot must not claim independence",
        "lacks independence attestation",
        "Agreement measures coding reproducibility; it does not confirm the TIDC hypothesis.",
    ):
        require(marker in calculator, f"calculator marker missing: {marker}")

    test_source = AGREEMENT_TEST.read_text(encoding="utf-8")
    for marker in (
        "unattested second response was not rejected",
        "expected dependency disagreement not emitted",
        "first-pass snapshot role not preserved",
    ):
        require(marker in test_source, f"agreement test marker missing: {marker}")

    instructions = CODER_INSTRUCTIONS.read_text(encoding="utf-8")
    for marker in (
        "Return exactly one JSON object",
        "Do not include Markdown fences",
        "independence_attestation",
        "Do not inspect the first-pass snapshot",
        "Disagreement is a valid result",
    ):
        require(marker in instructions, f"coder instruction marker missing: {marker}")

    status = EXECUTION_STATUS.read_text(encoding="utf-8")
    require("first-pass snapshot != independent coding" in status, "execution boundary missing")
    require("synthetic test != reliability evidence" in status, "test-evidence boundary missing")

    print("TIDC_RELIABILITY_VALID")
    print("records=11 first_pass=governed_snapshot independent_response=pending release_2=blocked")


if __name__ == "__main__":
    main()
