#!/usr/bin/env python3
"""Validate HIL activation gates without converting missing evidence into success.

The activation-state record still preserves the earlier recovered v0.5 primary as
historical custody evidence. The experiment manifest has since advanced to the
canonical v1.1 paper. This validator checks both facts explicitly instead of
requiring the current manifest to describe the historical recovered artifact.
"""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "hil-activation-state.json"
MANIFEST = ROOT / "data" / "hil-experiment.json"
LEGACY_PRIMARY = ROOT / "data" / "hil-primary-v0.5-review.pdf.b64"
CANONICAL_PRIMARY = ROOT / "data" / "HIL_Canonical_Paper_v1_1.pdf"
LEGACY_EXPECTED_SIZE = 109210
LEGACY_EXPECTED_HASH = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
CANONICAL_EXPECTED_SIZE = 87271
CANONICAL_EXPECTED_HASH = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL activation-state verification failed: {message}")


def load(path: Path) -> dict:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    state = load(STATE)
    manifest = load(MANIFEST)

    encoded = "".join(LEGACY_PRIMARY.read_text(encoding="ascii").split())
    legacy_payload = base64.b64decode(encoded, validate=True)
    require(len(legacy_payload) == LEGACY_EXPECTED_SIZE, "historical Primary decoded size mismatch")
    require(
        hashlib.sha256(legacy_payload).hexdigest() == LEGACY_EXPECTED_HASH,
        "historical Primary decoded hash mismatch",
    )
    require(legacy_payload.startswith(b"%PDF-"), "historical Primary lacks PDF signature")

    primary = state["primary"]
    require(primary["state"] == "VERIFIED_INSTALLED", "historical Primary state is not verified installed")
    require(primary["custody_recovery_complete"] is True, "historical Primary custody recovery not complete")
    require(primary["artifact_path"] == "data/hil-primary-v0.5-review.pdf.b64", "historical Primary path mismatch")
    require(primary["size_bytes"] == LEGACY_EXPECTED_SIZE, "activation-state historical Primary size mismatch")
    require(primary["sha256"] == LEGACY_EXPECTED_HASH, "activation-state historical Primary hash mismatch")

    canonical = CANONICAL_PRIMARY.read_bytes()
    require(len(canonical) == CANONICAL_EXPECTED_SIZE, "canonical v1.1 Primary size mismatch")
    require(hashlib.sha256(canonical).hexdigest() == CANONICAL_EXPECTED_HASH, "canonical v1.1 Primary hash mismatch")
    require(canonical.startswith(b"%PDF-"), "canonical v1.1 Primary lacks PDF signature")

    manifest_primary = manifest["primary_document"]
    require(manifest["schema_version"] == "HIL-EXPERIMENT-v1.1", "unexpected experiment manifest schema")
    require(manifest_primary["version"] == "v1.1", "manifest Primary version mismatch")
    require(manifest_primary["artifact_path"] == "data/HIL_Canonical_Paper_v1_1.pdf", "manifest Primary path mismatch")
    require(manifest_primary["size_bytes"] == CANONICAL_EXPECTED_SIZE, "manifest Primary size mismatch")
    require(manifest_primary["sha256"] == CANONICAL_EXPECTED_HASH, "manifest Primary hash mismatch")
    require(
        manifest_primary["artifact_state"] == "INSTALLED_PENDING_AUTOMATED_HASH_VERIFICATION",
        "manifest Primary state mismatch",
    )
    require(manifest_primary["canonical_state"] == "CANONICAL_EXPERIMENT_INPUT_V1_1", "manifest canonical state mismatch")

    require(state["gateway"]["implementation_state"] == "MERGED", "gateway merge not recorded")
    require(
        state["activation_state"] == "PORTABLE_RUNTIME_VALIDATED_DEPLOYED_CONTROLLED_CYCLE_PENDING",
        "unexpected activation state",
    )
    require(state["public_acquisition_authorized"] is False, "public acquisition must remain unauthorized")
    require(state["release_authorized"] is False, "release must remain unauthorized")
    require(state["authority_effect"] == "NONE", "activation-state observation must grant no authority")

    remaining = state["remaining_gates"]
    required_remaining = {
        "validated_gateway_deployed_with_durable_storage",
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
    print("HIL_HISTORICAL_PRIMARY=VERIFIED_INSTALLED")
    print("HIL_CANONICAL_PRIMARY_V1_1=HASH_VERIFIED")
    print("HIL_GATEWAY_IMPLEMENTATION=MERGED")
    print("HIL_DEPLOYED_CONTROLLED_CYCLE=PENDING")
    print("HIL_PUBLIC_ACQUISITION_AUTHORIZED=false")
    print("HIL_RELEASE_AUTHORIZED=false")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
