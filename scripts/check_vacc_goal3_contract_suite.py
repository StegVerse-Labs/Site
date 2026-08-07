#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "va-claim-assistant"
FIXTURE = BASE / "fixtures" / "vacc-goal3-contract-suite.json"
SCHEMAS = [
    "provenance-workload.schema.json",
    "claimant-submission-binding.schema.json",
    "redirect-retrieval.schema.json",
    "sanitized-document-derivative.schema.json",
    "evidence-criteria-mapping.schema.json",
]
ACTOR_CLASSES = {
    "veteran_self_service", "accredited_vso", "accredited_agent",
    "accredited_attorney", "government_service_office", "nonprofit",
    "commercial_provider", "unknown",
}
SCENARIOS = {"SUPPORTED", "PARTIALLY_SUPPORTED", "CONFLICTING", "UNSUPPORTED"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_false_effects(record: dict) -> None:
    assert record.get("authority_effect") is False
    assert record.get("activation_effect") is False


def main() -> int:
    schemas = {name: load(BASE / name) for name in SCHEMAS}
    fixture = load(FIXTURE)

    for name, schema in schemas.items():
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", name
        assert schema.get("type") == "object", name
        props = schema.get("properties", {})
        assert props.get("authority_effect", {}).get("const") is False, name
        assert props.get("activation_effect", {}).get("const") is False, name

    provenance = fixture["provenance"]
    assert_false_effects(provenance)
    assert provenance["actor"]["actor_class"] in ACTOR_CLASSES
    assert provenance["privacy"]["contains_direct_pii"] is False
    assert provenance["privacy"]["award_percentage_optimization_allowed"] is False
    assert 0 <= provenance["workload"]["citation_coverage_ratio"] <= 1
    assert provenance["artifact"]["vacc_generation_event_ref"]
    assert provenance["artifact"]["source_hash_refs"]
    assert provenance["actor"]["appointed_representative_ref"] != provenance["artifact"]["vacc_generation_event_ref"]

    binding = fixture["claimant_binding"]
    assert_false_effects(binding)
    assert binding["certification"]["veteran_affirmative_action"] is True
    assert binding["certification"]["exact_packet_hash_bound"] is True
    assert binding["decorative_identity_stamp_is_proof"] is False
    assert binding["veteran_submission_authority_preserved"] is True
    assert binding["production_fields_verified"] is False
    assert binding["submission"]["state"] == "NOT_AUTHORIZED"
    assert binding["submission"]["va_transaction_id"] is None

    retrieval = fixture["redirect_retrieval"]
    assert_false_effects(retrieval)
    assert retrieval["authoritative_source"]["source_url"].startswith("https://www.va.gov/")
    assert retrieval["retrieval"]["transport_path"] == "SOURCE_TO_VETERAN_DEVICE"
    assert retrieval["privacy"]["source_credentials_retained"] is False
    assert retrieval["privacy"]["source_document_bytes_retained"] is False
    assert retrieval["privacy"]["private_retrieval_control_publicly_active"] is False

    derivative = fixture["sanitized_derivative"]
    assert_false_effects(derivative)
    assert derivative["original"]["sha256"] == derivative["derivative"]["derived_from_sha256"]
    assert derivative["original"]["sha256"] != derivative["derivative"]["sha256"]
    controls = derivative["identifier_controls"]
    assert controls["direct_identifiers_removed_or_tokenized"] >= controls["direct_identifiers_detected"]
    assert controls["source_credentials_present"] is False
    assert controls["identity_proofing_artifacts_present"] is False
    assert controls["leakage_state"] == "PASS"
    assert all(derivative["evidence_posture"].values())

    mappings = fixture["evidence_mappings"]
    assert {m["scenario_id"] for m in mappings} == SCENARIOS
    for mapping in mappings:
        assert_false_effects(mapping)
        facts = {fact["fact_id"] for fact in mapping["record_facts"]}
        criteria = {criterion["criterion_id"] for criterion in mapping["official_criteria"]}
        assert facts
        assert criteria
        assert set(mapping["mapping"]["fact_refs"]).issubset(facts)
        assert set(mapping["mapping"]["supported_criterion_ids"]).issubset(criteria)
        assert set(mapping["mapping"]["unsupported_criterion_ids"]).issubset(criteria)
        assert mapping["claim_language"]["unsupported_assertions"] == []
        assert set(mapping["claim_language"]["fact_refs"]).issubset(facts)
        assert mapping["claim_language"]["requires_veteran_confirmation"] is True
        optimization = mapping["optimization"]
        assert optimization == {
            "desired_percentage_targeting": False,
            "unsupported_symptom_coaching": False,
            "unfavorable_evidence_suppression": False,
        }
        assert all(c["authority_ref"] == "OFFICIAL-VA-AUTHORITY-FIXTURE" for c in mapping["official_criteria"])

    result = {
        "state": "PASS",
        "contracts": SCHEMAS,
        "contract_count": len(SCHEMAS),
        "issues_covered": [179, 180, 181, 182, 183, 184],
        "mapping_scenarios": sorted(SCENARIOS),
        "public_upload_enabled": False,
        "private_retrieval_enabled": False,
        "submission_enabled": False,
        "production_va_fields_verified": False,
        "authority_effect": False,
        "activation_effect": False,
        "fixture_sha256": sha256(FIXTURE),
        "schema_sha256": {name: sha256(BASE / name) for name in SCHEMAS},
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
