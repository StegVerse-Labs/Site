#!/usr/bin/env python3
"""Validate the public economic roadmap *projection*, not upstream runtime truth.

This checker is CI-safe. It cannot create, attest or verify a Master Records receipt.
The existing authorized Publisher must authenticate every complete milestone before
it is permitted to publish this JSON.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/economy/public-release-benchmarks.v1.json"
VALID = {"NOT_VERIFIED", "UNKNOWN_NOT_AUTHENTICALLY_OBSERVED", "VERIFIED_COMPLETE", "INVALIDATED"}

def validate(data: dict) -> list[str]:
    errors = []
    if data.get("schema") != "stegverse.public-economic-roadmap/v1":
        errors.append("wrong schema")
    a = data.get("authority_boundary", {})
    for key in ("site_display_grants_completion", "source_merge_proves_runtime", "synthetic_evidence_counts"):
        if a.get(key) is not False:
            errors.append(f"{key} must be false")
    required = {
        "master_records_state_RECORDED", "reconstruction_PASS",
        "required_evidence_validation_PASS", "exact_receipt_digest_equality",
        "correct_benchmark_identity", "governed_publication_closure",
    }
    if not required.issubset(set(a.get("required_for_complete", []))):
        errors.append("missing exact completion invariants")
    stages = data.get("stages")
    if not isinstance(stages, list) or len(stages) != 6:
        errors.append("exactly six stages required")
        return errors
    lanes = data.get("stage1_execution_lanes", {})
    external = lanes.get("external_ai", {}) if isinstance(lanes, dict) else {}
    private = lanes.get("private_workspace", {}) if isinstance(lanes, dict) else {}
    if external.get("mode") != "ON_DEMAND_EPHEMERAL_STEGBROWSER" or external.get("requires_native_mykv_installation") is not False:
        errors.append("external AI lane must remain ephemeral and independent of native MyKV")
    if private.get("mode") != "NATIVE_MYKV_WORKSPACE_WITH_PRIVATE_ASSISTANT" or private.get("requires_native_mykv_installation") is not True:
        errors.append("private MyKV lane must require genuine native installation")
    stage1 = {b.get("id"): b for b in stages[0].get("benchmarks", [])}
    required_ephemeral_proof = {
        "current_authorized_ephemeral_lease", "exact_external_intr_ingress_allow",
        "real_provider_request_and_usable_response", "exact_external_intr_egress_allow",
        "usage_and_result_attribution", "terminal_ephemeral_session_destruction",
        "durable_canonical_master_records_reconstruction",
    }
    for bid in ("S1_CHATGPT", "S1_CLAUDE"):
        gate = stage1.get(bid, {})
        if gate.get("execution_mode") != "EPHEMERAL_STEGBROWSER_WITH_GOVERNED_EXTERNAL_PROVIDER" or gate.get("native_mykv_installation_prerequisite") is not False:
            errors.append(f"{bid}: must not depend on native MyKV installation")
        if not required_ephemeral_proof.issubset(set(gate.get("required_proof", []))):
            errors.append(f"{bid}: missing independent ephemeral runtime proof predicates")
    if sum(len(s.get("benchmarks", [])) for s in stages) != 16:
        errors.append("the public release contract requires exactly sixteen benchmarks")
    ids = set()
    completed_ids = set()
    for i, s in enumerate(stages, 1):
        if s.get("id") != f"S{i}":
            errors.append(f"incorrect stage identity {i}")
        benchmarks = s.get("benchmarks")
        if not isinstance(benchmarks, list) or not benchmarks:
            errors.append(f"stage {i}: missing benchmarks")
            continue
        all_complete = True
        for b in benchmarks:
            bid = b.get("id")
            if not isinstance(bid, str) or not bid.startswith(f"S{i}_") or bid in ids:
                errors.append(f"invalid or duplicate benchmark id: {bid}")
            ids.add(bid)
            status = b.get("status")
            if status not in VALID:
                errors.append(f"{bid}: invalid status")
            if status == "VERIFIED_COMPLETE":
                completed_ids.add(bid)
                if not all(isinstance(b.get(k), str) and b[k].strip() for k in ("evidence_ref", "verified_at")):
                    errors.append(f"{bid}: completed without public evidence reference/time")
                if data.get("publication_posture") != "GOVERNED_PUBLISHED":
                    errors.append(f"{bid}: completed without governed-publication posture")
            else:
                all_complete = False
        if s.get("status") == "VERIFIED_COMPLETE" and not all_complete:
            errors.append(f"stage {i}: premature completion")
        if s.get("status") not in VALID:
            errors.append(f"stage {i}: invalid status")
        if s.get("status") == "VERIFIED_COMPLETE" and i > 1:
            previous = stages[i-2]
            if previous.get("status") != "VERIFIED_COMPLETE":
                errors.append(f"stage {i}: predecessor is not complete")
    if completed_ids and not data.get("generated_at"):
        errors.append("completed milestones need authenticated projection timestamp")
    return errors

def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    errors = validate(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps({"path": str(path), "valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
