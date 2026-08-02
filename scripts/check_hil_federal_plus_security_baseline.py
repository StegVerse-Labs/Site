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


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def validate() -> dict:
    failures: list[str] = []
    require(PROFILE.is_file(), "missing security profile", failures)
    require(SCHEMA.is_file(), "missing security schema", failures)
    require(POLICY.is_file(), "missing canonical security policy", failures)
    if failures:
        return build_receipt({}, failures)

    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    policy = POLICY.read_text(encoding="utf-8")

    require(profile.get("schema_version") == "HIL-FEDERAL-PLUS-SECURITY-v1", "invalid schema_version", failures)
    require(profile.get("profile_id") == "HIL-SECURITY-BASELINE-2026-08-02", "invalid profile_id", failures)
    require(profile.get("security_posture") == "FEDERAL_REQUIREMENTS_ARE_MINIMUMS", "federal-minimum posture missing", failures)
    require(profile.get("canonical_policy") == "docs/HIL_FEDERAL_PLUS_SECURITY_BASELINE.md", "canonical policy path mismatch", failures)
    require("FEDERAL_REQUIREMENTS_ARE_MINIMUMS" in policy, "policy posture marker missing", failures)
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

    return build_receipt(profile, failures, nonimplemented)


def build_receipt(profile: dict, failures: list[str], nonimplemented: list[str] | None = None) -> dict:
    receipt = {
        "schema_version": "HIL-FEDERAL-PLUS-SECURITY-VALIDATION-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile_id": profile.get("profile_id"),
        "profile_sha256": hashlib.sha256(canonical_bytes(profile)).hexdigest() if profile else None,
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
