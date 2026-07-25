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
EXPECTED_SIZE = 109210
EXPECTED_HASH = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL activation-state verification failed: {message}")


def load(path: Path) -> dict:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    state = load(STATE)
    manifest = load(MANIFEST)

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
    require(state["activation_state"] == "PRIMARY_COMPLETE_DEPLOYED_CONTROLLED_CYCLE_PENDING", "unexpected activation state")
    require(state["public_acquisition_authorized"] is False, "public acquisition must remain unauthorized")
    require(state["release_authorized"] is False, "release must remain unauthorized")
    require(state["authority_effect"] == "NONE", "activation-state observation must grant no authority")

    remaining = state["remaining_gates"]
    required_remaining = {
        "merged_gateway_deployed_with_durable_storage",
        "separate_intake_review_and_publication_credentials",
        "live_readiness_controlled_cycle_ready",
        "deployed_submission_and_receiver_receipt",
        "actual_restart_persistence_proof",
        "authenticated_accept_private",
        "append_only_publication",
        "site_import",
        "first_chained_master_record_release",
        "authorized_orchestration_submission",
    }
    require(set(remaining) == required_remaining, "remaining activation gates are incomplete or stale")

    controlled = state["controlled_cycle"]
    for key, value in controlled.items():
        if key == "orchestration_submission":
            require(value == "NOT_AUTHORIZED", "orchestration submission must remain unauthorized")
        else:
            require(value == "NOT_ESTABLISHED", f"{key} may not be marked established without evidence")

    print("HIL_ACTIVATION_STATE_VERIFICATION=PASS")
    print("HIL_PRIMARY=VERIFIED_INSTALLED")
    print("HIL_GATEWAY_IMPLEMENTATION=MERGED")
    print("HIL_DEPLOYED_CONTROLLED_CYCLE=PENDING")
    print("HIL_PUBLIC_ACQUISITION_AUTHORIZED=false")
    print("HIL_RELEASE_AUTHORIZED=false")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
