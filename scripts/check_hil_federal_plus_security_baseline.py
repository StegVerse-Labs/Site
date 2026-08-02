#!/usr/bin/env python3
"""Fail-closed validator for the HIL federal-plus security profile."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data" / "hil-federal-plus-security-baseline.json"
SCHEMA = ROOT / "schemas" / "hil-federal-plus-security-baseline.schema.json"
POLICY = ROOT / "docs" / "HIL_FEDERAL_PLUS_SECURITY_BASELINE.md"
FEDERAL_FLOOR = ROOT / "data" / "hil-federal-control-floor.json"
FEDERAL_FLOOR_SCHEMA = ROOT / "schemas" / "hil-federal-control-floor.schema.json"
ALLOWED_STATES = {
    "IMPLEMENTED",
    "PARTIAL",
    "BLOCKED",
    "MISSING",
    "FAILED",
    "STALE",
    "UNVERIFIED",
    "NOT_APPLICABLE",
}
FAIL_STATES = {"MISSING", "FAILED", "STALE", "UNVERIFIED"}
EXPECTED_AUTHORITY = {
    "execution": False,
    "publication": False,
    "custody": False,
    "master_record_append": False,
    "production_activation": False,
}
EXPECTED_FLOOR_REFERENCES = {
    "NIST-SP-800-53-R5-5.2.0",
    "NIST-SP-800-218-V1.1",
    "NIST-SP-800-207",
    "CISA-ZTMM-2.0",
    "OMB-M-22-09",
}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def validate_federal_floor(failures: list[str]) -> dict:
    require(FEDERAL_FLOOR.is_file(), "missing federal control floor", failures)
    require(FEDERAL_FLOOR_SCHEMA.is_file(), "missing federal control floor schema", failures)
    if not FEDERAL_FLOOR.is_file() or not FEDERAL_FLOOR_SCHEMA.is_file():
        return {}

    floor = json.loads(FEDERAL_FLOOR.read_text(encoding="utf-8"))
    floor_schema = json.loads(FEDERAL_FLOOR_SCHEMA.read_text(encoding="utf-8"))
    require(
        floor_schema.get("$id") == "https://stegverse.org/schemas/hil-federal-control-floor-v1.json",
        "federal floor schema ID mismatch",
        failures,
    )
    require(floor.get("schema_version") == "HIL-FEDERAL-CONTROL-FLOOR-v1", "invalid federal floor schema_version", failures)
    require(floor.get("floor_id") == "HIL-FEDERAL-FLOOR-2026-08-02", "invalid federal floor_id", failures)
    require(floor.get("posture") == "MINIMUM_NOT_TARGET", "federal floor posture drift", failures)
    require(floor.get("authority_effect") == "NONE", "federal floor authority effect must remain NONE", failures)
    require(floor.get("certification_claimed") is False, "federal certification must not be claimed", failures)
    require(floor.get("production_activation_authorized") is False, "federal floor must not authorize production", failures)

    references = floor.get("references")
    require(isinstance(references, list), "federal floor references must be an array", failures)
    seen: set[str] = set()
    if isinstance(references, list):
        for reference in references:
            require(isinstance(reference, dict), "federal floor reference must be an object", failures)
            if not isinstance(reference, dict):
                continue
            reference_id = reference.get("reference_id")
            require(isinstance(reference_id, str), "invalid federal floor reference_id", failures)
            require(reference_id not in seen, f"duplicate federal floor reference: {reference_id}", failures)
            if isinstance(reference_id, str):
                seen.add(reference_id)
            require(reference.get("status") == "AUTHORITATIVE_FLOOR", f"invalid federal floor status: {reference_id}", failures)
            require(str(reference.get("url", "")).startswith("https://"), f"invalid federal floor URL: {reference_id}", failures)
            require(bool(reference.get("version")), f"missing federal floor version: {reference_id}", failures)
            require(bool(reference.get("owner")), f"missing federal floor owner: {reference_id}", failures)
            require(bool(reference.get("freshness_rule")), f"missing federal floor freshness rule: {reference_id}", failures)
    require(seen == EXPECTED_FLOOR_REFERENCES, "federal floor reference inventory drift", failures)

    above_floor = floor.get("above_floor_requirements")
    require(isinstance(above_floor, list) and len(above_floor) >= 10, "insufficient above-floor requirements", failures)
    return floor


def validate() -> dict:
    failures: list[str] = []
    require(PROFILE.is_file(), "missing security profile", failures)
    require(SCHEMA.is_file(), "missing security schema", failures)
    require(POLICY.is_file(), "missing canonical security policy", failures)
    federal_floor = validate_federal_floor(failures)
    if not PROFILE.is_file() or not SCHEMA.is_file() or not POLICY.is_file():
        return build_receipt({}, failures, federal_floor=federal_floor)

    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    policy = POLICY.read_text(encoding="utf-8")

    require(profile.get("schema_version") == "HIL-FEDERAL-PLUS-SECURITY-v1", "invalid schema_version", failures)
    require(profile.get("profile_id") == "HIL-SECURITY-BASELINE-2026-08-02", "invalid profile_id", failures)
    require(profile.get("security_posture") == "FEDERAL_REQUIREMENTS_ARE_MINIMUMS", "federal-minimum posture missing", failures)
    require(profile.get("canonical_policy") == "docs/HIL_FEDERAL_PLUS_SECURITY_BASELINE.md", "canonical policy path mismatch", failures)
    require("FEDERAL_REQUIREMENTS_ARE_MINIMUMS" in policy, "policy posture marker missing", failures)
    require("data/hil-federal-control-floor.json" in policy, "versioned federal floor missing from policy", failures)
    require(schema.get("$id") == "https://stegverse.org/schemas/hil-federal-plus-security-baseline-v1.json", "schema ID mismatch", failures)
    require(profile.get("authority") == EXPECTED_AUTHORITY, "authority must remain entirely false", failures)

    controls = profile.get("controls")
    require(isinstance(controls, list) and len(controls) >= 12, "at least 12 controls required", failures)
    seen: set[str] = set()
    nonimplemented: list[str] = []
    if isinstance(controls, list):
        for control in controls:
            require(isinstance(control, dict), "control must be an object", failures)
            if not isinstance(control, dict):
                continue
            control_id = control.get("control_id")
            require(isinstance(control_id, str) and control_id.startswith("HIL-SEC-"), "invalid control_id", failures)
            require(control_id not in seen, f"duplicate control_id: {control_id}", failures)
            seen.add(control_id)
            state = control.get("state")
            require(state in ALLOWED_STATES, f"invalid state for {control_id}", failures)
            require(isinstance(control.get("required"), bool), f"required flag missing for {control_id}", failures)
            require(bool(control.get("owner")), f"owner missing for {control_id}", failures)
            require(bool(control.get("freshness_rule")), f"freshness_rule missing for {control_id}", failures)
            require(bool(control.get("release_condition")), f"release_condition missing for {control_id}", failures)
            evidence = control.get("evidence")
            require(isinstance(evidence, list), f"evidence must be an array for {control_id}", failures)
            if isinstance(evidence, list):
                for reference in evidence:
                    require(isinstance(reference, str) and len(reference) >= 3, f"invalid evidence reference for {control_id}", failures)
                    if isinstance(reference, str) and not reference.startswith(("http://", "https://")):
                        local = ROOT / reference
                        require(local.exists(), f"unresolved local evidence for {control_id}: {reference}", failures)
            if control.get("required") is True and state != "IMPLEMENTED":
                nonimplemented.append(str(control_id))
            if control.get("required") is True and state in FAIL_STATES:
                failures.append(f"required control in fail state: {control_id}={state}")

    activation = profile.get("activation") or {}
    expected_state = "PASS" if not nonimplemented and not failures else "BLOCKED"
    require(activation.get("state") == expected_state, f"activation state must be {expected_state}", failures)
    blockers = activation.get("blockers")
    require(isinstance(blockers, list), "activation blockers must be an array", failures)
    if expected_state == "BLOCKED":
        require(bool(blockers), "blocked profile requires explicit blockers", failures)
    else:
        require(blockers == [], "passing profile must have no blockers", failures)
    require(bool(activation.get("next_executable_action")), "next executable action missing", failures)

    return build_receipt(profile, failures, nonimplemented, federal_floor)


def build_receipt(
    profile: dict,
    failures: list[str],
    nonimplemented: list[str] | None = None,
    federal_floor: dict | None = None,
) -> dict:
    floor = federal_floor or {}
    receipt = {
        "schema_version": "HIL-FEDERAL-PLUS-SECURITY-VALIDATION-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile_id": profile.get("profile_id"),
        "profile_sha256": hashlib.sha256(canonical_bytes(profile)).hexdigest() if profile else None,
        "federal_floor_id": floor.get("floor_id"),
        "federal_floor_sha256": hashlib.sha256(canonical_bytes(floor)).hexdigest() if floor else None,
        "validation_state": "PASS" if not failures else "FAIL",
        "security_activation_state": (profile.get("activation") or {}).get("state", "BLOCKED"),
        "nonimplemented_required_controls": nonimplemented or [],
        "failures": failures,
        "authority_effect": "NONE",
        "production_activation_authorized": False,
        "publication_authorized": False,
        "custody_authorized": False,
    }
    receipt["receipt_sha256"] = hashlib.sha256(canonical_bytes(receipt)).hexdigest()
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = validate()
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if receipt["validation_state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
