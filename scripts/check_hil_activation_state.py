#!/usr/bin/env python3
"""Validate HIL activation gates without converting missing evidence into success."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "hil-activation-state.json"
MANIFEST = ROOT / "data" / "hil-experiment.json"
PRIMARY = ROOT / "data" / "hil-primary-v0.5-review.pdf.b64"
READINESS = ROOT / "data" / "hil-readiness" / "HIL-LIVE-READINESS-OBSERVATION-v2-run-30173147748.json"
EXPECTED_SIZE = 109210
EXPECTED_HASH = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
EXPECTED_RECEIPT_HASH = "d320ea8d0f9f293fb19a1cf04ec3239b2d13d4836e99637cfed496d3c07eba36"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL activation-state verification failed: {message}")


def load(path: Path) -> dict:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    state = load(STATE)
    manifest = load(MANIFEST)
    readiness = load(READINESS)

    encoded = "".join(PRIMARY.read_text(encoding="ascii").split())
    payload = base64.b64decode(encoded, validate=True)
    require(len(payload) == EXPECTED_SIZE, "Primary decoded size mismatch")
    require(hashlib.sha256(payload).hexdigest() == EXPECTED_HASH, "Primary decoded hash mismatch")
    require(payload.startswith(b"%PDF-"), "Primary lacks PDF signature")

    primary = state["primary"]
    require(primary["state"] == "VERIFIED_INSTALLED", "Primary state is not verified installed")
    require(primary["custody_recovery_complete"] is True, "custody recovery not complete")
    require(primary["size_bytes"] == EXPECTED_SIZE, "activation-state Primary size mismatch")
    require(primary["sha256"] == EXPECTED_HASH, "activation-state Primary hash mismatch")
    require(manifest["primary_document"]["artifact_state"] == "VERIFIED", "manifest Primary state mismatch")
    require(manifest["primary_document"]["sha256"] == EXPECTED_HASH, "manifest Primary hash mismatch")

    require(state["gateway"]["implementation_state"] == "MERGED", "gateway merge not recorded")
    require(
        state["activation_state"] == "BOUNDED_CONTROLLED_CYCLE_READY_EXTERNAL_DEPLOYMENT_AND_EXECUTION_PENDING",
        "unexpected activation state",
    )
    require(state["public_acquisition_authorized"] is False, "public acquisition must remain unauthorized")
    require(state["release_authorized"] is False, "release must remain unauthorized")
    require(state["authority_effect"] == "NONE", "activation-state observation must grant no authority")

    require(readiness["schema_version"] == "HIL-LIVE-READINESS-OBSERVATION-v2", "readiness schema mismatch")
    require(readiness["observation_sha256"] == EXPECTED_RECEIPT_HASH, "readiness receipt hash mismatch")
    require(readiness["observed_state"] == "CONTROLLED_CYCLE_READY", "bounded readiness not established")
    require(readiness["observation_scope"] == "GITHUB_HOSTED_EPHEMERAL_DEPLOYMENT_PROOF", "readiness scope mismatch")
    require(readiness["credential_separation_verified"] is True, "credential separation not established")
    require(readiness["durable_path_reused_across_process_restart"] is True, "restart path reuse not established")
    require(readiness["external_production_deployment_claimed"] is False, "invalid production claim")
    require(readiness["authority_granted"] is False, "invalid authority claim")

    required_remaining = {
        "external_production_gateway_deployed_with_durable_storage",
        "deployed_submission_and_receiver_receipt",
        "exact_response_byte_and_provenance_persistence_across_restart",
        "authenticated_accept_private",
        "append_only_publication_execution",
        "stable_public_lookup",
        "first_chained_master_record_release",
        "authorized_orchestration_submission",
    }
    require(set(state["remaining_gates"]) == required_remaining, "remaining activation gates are incomplete or stale")

    controlled = state["controlled_cycle"]
    require(controlled["actual_restart"] == "ESTABLISHED_FOR_BOUNDED_GATEWAY_PROCESS", "bounded restart not recorded")
    require(controlled["site_import"] == "BOUNDED_READINESS_RECEIPT_IMPORTED", "receipt import not recorded")
    require(
        controlled["append_only_publication"] == "READINESS_ESTABLISHED_EXECUTION_NOT_ESTABLISHED",
        "publication readiness boundary mismatch",
    )
    for key in (
        "deployed_submission",
        "receiver_receipt",
        "exact_byte_persistence",
        "provenance_manifest_persistence",
        "accept_private",
        "private_review_receipt",
        "stable_public_lookup",
        "master_record_release",
    ):
        require(controlled[key] == "NOT_ESTABLISHED", f"{key} may not be marked established without evidence")
    require(controlled["orchestration_submission"] == "NOT_AUTHORIZED", "orchestration submission must remain unauthorized")

    print("HIL_ACTIVATION_STATE_VERIFICATION=PASS")
    print("HIL_PRIMARY=VERIFIED_INSTALLED")
    print("HIL_BOUNDED_CONTROLLED_CYCLE=READY")
    print("HIL_EXTERNAL_PRODUCTION_DEPLOYMENT=NOT_ESTABLISHED")
    print("HIL_PUBLIC_ACQUISITION_AUTHORIZED=false")
    print("HIL_RELEASE_AUTHORIZED=false")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
