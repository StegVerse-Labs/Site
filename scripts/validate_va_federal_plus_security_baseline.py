#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/va-claim-assistant/federal-plus-security-baseline.json"
OUT = ROOT / "data/va-claim-assistant/federal-plus-security-baseline-validation.json"

REQUIRED_FAMILIES = {"AC","AT","AU","CA","CM","CP","IA","IR","MA","MP","PE","PL","PM","PS","PT","RA","SA","SC","SI","SR"}
REQUIRED_PLUS = {"identity","data_protection","execution","provenance_and_custody","filing","monitoring_and_response","privacy"}


def main() -> int:
    doc = json.loads(SRC.read_text(encoding="utf-8"))
    errors: list[str] = []
    policy = doc.get("policy", {})
    floor = doc.get("federal_floor", {})
    plus = doc.get("stegverse_plus_controls", {})

    if policy.get("federal_requirements_are_minimum") is not True:
        errors.append("federal floor not mandatory")
    if policy.get("stegverse_must_exceed_minimum") is not True:
        errors.append("exceed-minimum policy missing")
    if policy.get("compliance_claim_requires_independent_evidence") is not True:
        errors.append("independent evidence gate missing")
    if policy.get("authority_effect") is not False or policy.get("activation_effect") is not False:
        errors.append("contract improperly grants authority or activation")

    families = set(floor.get("nist_sp_800_53", {}).get("required_families", []))
    if families != REQUIRED_FAMILIES:
        errors.append("NIST control families incomplete")
    if floor.get("nist_sp_800_63", {}).get("phishing_resistant_authentication_required_for_privileged_and_filing_actions") is not True:
        errors.append("phishing-resistant authentication missing")
    zt = floor.get("zero_trust", {})
    for key in ("explicit_verification", "least_privilege", "assume_breach", "service_to_service_identity"):
        if zt.get(key) is not True:
            errors.append(f"zero trust control missing: {key}")
    if floor.get("fedramp_assurance", {}).get("automated_continuous_evidence_required") is not True:
        errors.append("continuous assurance missing")

    if set(plus) != REQUIRED_PLUS:
        errors.append("StegVerse-plus control domains incomplete")
    if doc.get("prohibited_claims") != ["FedRAMP authorized", "FISMA compliant", "NIST compliant", "VA approved", "federal compliant"]:
        errors.append("prohibited compliance claims changed")
    if len(doc.get("activation_gates", [])) < 12:
        errors.append("activation gates incomplete")

    body = {
        "schema_version": "1.0.0",
        "baseline_id": doc.get("baseline_id"),
        "state": "PASS" if not errors else "FAIL",
        "federal_floor_required": policy.get("federal_requirements_are_minimum"),
        "exceeds_floor_required": policy.get("stegverse_must_exceed_minimum"),
        "control_family_count": len(families),
        "plus_domain_count": len(plus),
        "phishing_resistant_authentication_required": floor.get("nist_sp_800_63", {}).get("phishing_resistant_authentication_required_for_privileged_and_filing_actions"),
        "continuous_assurance_required": floor.get("fedramp_assurance", {}).get("automated_continuous_evidence_required"),
        "compliance_claim_requires_independent_evidence": policy.get("compliance_claim_requires_independent_evidence"),
        "authority_effect": False,
        "activation_effect": False,
        "contract_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "errors": errors,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
