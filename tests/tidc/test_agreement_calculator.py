#!/usr/bin/env python3
"""Self-contained checks for the TIDC reliability agreement calculator."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALCULATOR = ROOT / "scripts" / "calculate_tidc_agreement.py"
FIRST_PASS = ROOT / "data" / "tidc" / "coder-response.first-pass.v0.1.json"


def synthetic_response(attested: bool) -> dict:
    return {
        "schema": "stegverse.site.tidc.coder_response.v0.1",
        "packet_schema": "stegverse.site.tidc.second_coding_packet.v0.1",
        "research_state": "PILOT_NOT_CONFIRMATORY",
        "coder": {
            "coder_id": "SYNTHETIC-TEST-CODER",
            "independence_attestation": attested,
            "completed_at": "2026-07-27",
            "source_access_limitations": ["Synthetic test fixture; not research evidence."],
        },
        "records": [
            {
                "record_id": "COMP-001",
                "record_kind": "discovery_event",
                "technology_wave": "Classical computer",
                "mechanism": "Computer-assisted proof / finite case checking",
                "field": "Graph theory",
                "candidate_generation_date": "1976",
                "verification_date": None,
                "public_disclosure_date": None,
                "publication_date": "1977",
                "acceptance_date": None,
                "recognition_date": None,
                "dependency_class": "Material",
                "orientation": "External",
                "problem_origin_type": "Inherited problem",
                "effective_access": "Unresolved",
                "constraint_posture": "Not measured",
                "efficiency_claim": "Unresolved",
                "acceptance_posture": "Peer reviewed",
                "coding_confidence": "Medium",
                "evidence_quotes_or_locations": ["synthetic"],
                "uncertainty_notes": ["synthetic"],
                "exclusion_recommended": False,
                "exclusion_reason": None,
            }
        ],
        "submission_boundary": "Synthetic test fixture only; not a validated research result.",
    }


def run(response: dict, output: Path) -> subprocess.CompletedProcess[str]:
    response_path = output.with_suffix(".response.json")
    response_path.write_text(json.dumps(response), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(CALCULATOR), str(FIRST_PASS), str(response_path), "--output", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    if not CALCULATOR.exists() or not FIRST_PASS.exists():
        raise SystemExit("TIDC_TEST_INVALID: calculator or first-pass snapshot missing")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        rejected = run(synthetic_response(False), tmp_path / "rejected.json")
        if rejected.returncode == 0 or "lacks independence attestation" not in rejected.stderr + rejected.stdout:
            raise SystemExit("TIDC_TEST_FAILED: unattested second response was not rejected")

        output = tmp_path / "agreement.json"
        accepted = run(synthetic_response(True), output)
        if accepted.returncode != 0:
            raise SystemExit(f"TIDC_TEST_FAILED: attested fixture rejected: {accepted.stderr}")
        data = json.loads(output.read_text(encoding="utf-8"))
        if data.get("posture") != "RELIABILITY_OUTPUT_NOT_CONFIRMATION":
            raise SystemExit("TIDC_TEST_FAILED: reliability posture missing")
        disagreements = data.get("record_disagreements", [])
        if not any(item.get("field") == "dependency_class" for item in disagreements):
            raise SystemExit("TIDC_TEST_FAILED: expected dependency disagreement not emitted")
        if data.get("comparison", {}).get("first_pass_role") != "FIRST_PASS_SNAPSHOT":
            raise SystemExit("TIDC_TEST_FAILED: first-pass snapshot role not preserved")

    print("TIDC_AGREEMENT_TESTS_VALID")


if __name__ == "__main__":
    main()
