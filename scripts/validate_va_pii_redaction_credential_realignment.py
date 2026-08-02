#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/va-claim-assistant/pii-redaction-credential-realignment-contract.json"
OUT = ROOT / "data/va-claim-assistant/pii-redaction-credential-realignment-validation.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    errors: list[str] = []
    policy = data.get("policy", {})
    zones = data.get("zones", {})
    sequence = data.get("processing_sequence", [])
    prohibited = data.get("prohibited_actions", [])
    gates = data.get("release_gates", [])

    require(data.get("contract_id") == "SV-VA-PII-REALIGNMENT-001", "contract id mismatch", errors)
    require(policy.get("federal_privacy_controls_are_minimum") is True, "federal floor missing", errors)
    require(policy.get("stegverse_must_exceed_minimum") is True, "StegVerse-plus requirement missing", errors)
    require(policy.get("raw_pii_to_llm_adapter_prohibited") is True, "raw PII adapter prohibition missing", errors)
    require(policy.get("identity_reassociation_requires_verified_credentialing_handoff") is True, "credentialing handoff requirement missing", errors)
    require(policy.get("reassociation_before_credentialing_prohibited") is True, "pre-credential linkage prohibition missing", errors)
    require(policy.get("authority_effect") is False and policy.get("activation_effect") is False, "authority or activation effect must be false", errors)

    required_zones = {"credentialing_vault", "document_privacy_zone", "claims_reasoning_zone", "identity_linkage_zone"}
    require(required_zones.issubset(zones), "required privacy zones missing", errors)
    reasoning_rejected = set(zones.get("claims_reasoning_zone", {}).get("must_not_receive", []))
    for value in ("name", "social security number", "VA file number", "credential secret", "raw identity-proofing artifact"):
        require(value in reasoning_rejected, f"claims reasoning zone does not reject {value}", errors)

    require("verify no prohibited identifier remains in model-facing copy" in sequence, "model-facing leakage verification missing", errors)
    require("complete credentialing handoff through the credentialing vault" in sequence, "credentialing handoff step missing", errors)
    require("issue scoped identity-linkage receipt" in sequence, "identity linkage receipt step missing", errors)
    require("bind only the approved derived record or exact package hash to veteran identity reference" in sequence, "hash-bound identity realignment missing", errors)

    require("treat pseudonymization as anonymization" in prohibited, "pseudonymization warning missing", errors)
    require("send raw documents or direct identifiers to the LLM adapter" in prohibited, "raw document adapter prohibition missing", errors)
    require("link a document to a veteran before credentialing succeeds" in prohibited, "pre-credential linking prohibition missing", errors)

    required_gates = {
        "PII detector and redactor tests pass",
        "model-facing PII leakage tests pass",
        "credentialing handoff validation passes",
        "revocation prevents future identity linkage",
        "raw documents never leave the privacy zone",
        "custody and reconstruction pass",
        "independent privacy and security assessment retained",
        "no unresolved high or critical findings",
    }
    require(required_gates.issubset(set(gates)), "required release gates missing", errors)

    body = {
        "schema_version": "1.0.0",
        "state": "PASS" if not errors else "FAIL",
        "contract_id": data.get("contract_id"),
        "federal_floor_required": policy.get("federal_privacy_controls_are_minimum"),
        "exceeds_floor_required": policy.get("stegverse_must_exceed_minimum"),
        "raw_pii_to_adapter_prohibited": policy.get("raw_pii_to_llm_adapter_prohibited"),
        "credentialing_handoff_required": policy.get("identity_reassociation_requires_verified_credentialing_handoff"),
        "precredential_reassociation_prohibited": policy.get("reassociation_before_credentialing_prohibited"),
        "privacy_zone_count": len(zones),
        "release_gate_count": len(gates),
        "authority_effect": False,
        "activation_effect": False,
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "errors": errors,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
