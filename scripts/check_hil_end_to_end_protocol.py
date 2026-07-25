#!/usr/bin/env python3
"""Validate the HIL operational protocol and its manifest binding."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "hil-experiment.json"
PROTOCOL = ROOT / "docs" / "HIL_END_TO_END_PROTOCOL.md"

EXPECTED_SPEC_VERSION = "HIL-END-TO-END-PROTOCOL-v1.0"
EXPECTED_SPEC_PATH = "docs/HIL_END_TO_END_PROTOCOL.md"
EXPECTED_PRIMARY_SHA256 = (
    "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
)

REQUIRED_PROTOCOL_MARKERS = (
    "## Document ownership",
    "## Canonical Primary identity",
    "## Participant and model procedure",
    "## Provenance construction",
    "## Intake readiness",
    "## Governed submission",
    "## Private review",
    "## Append-only publication",
    "## Site projection",
    "## Master Record release",
    "## Deployed controlled-cycle proof",
    "## Failure and recovery rules",
    "## Authority boundaries",
    "## Completion criterion",
    "HIL-RECEIVER-RECEIPT-v2",
    "HIL-PRIVATE-REVIEW-RECEIPT-v1",
    "HIL-PUBLICATION-RECORD-v1",
    "HIL-MASTER-RECORD-RELEASE-v1",
    "CONTROLLED_CYCLE_READY",
)

REQUIRED_ACTIVATION_REQUIREMENTS = {
    "exact_primary_installed_and_hash_verified",
    "merged_gateway_deployed_with_durable_storage",
    "separate_intake_review_and_publication_credentials",
    "live_readiness_controlled_cycle_ready",
    "deployed_submission_and_receiver_receipt",
    "actual_restart_persistence_proof",
    "authenticated_accept_private",
    "append_only_publication",
    "site_import",
    "first_chained_master_record_release",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL end-to-end protocol validation failed: {message}")


def main() -> None:
    require(MANIFEST.is_file(), f"missing {MANIFEST.relative_to(ROOT)}")
    require(PROTOCOL.is_file(), f"missing {PROTOCOL.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    protocol_text = PROTOCOL.read_text(encoding="utf-8")

    primary = manifest.get("primary_document", {})
    protocol = manifest.get("protocol", {})

    require(
        primary.get("sha256") == EXPECTED_PRIMARY_SHA256,
        "canonical Primary SHA-256 changed",
    )
    require(
        primary.get("sole_technical_specification") is False,
        "Primary must not be declared the sole technical specification",
    )
    require(
        protocol.get("end_to_end_spec_version") == EXPECTED_SPEC_VERSION,
        "manifest end-to-end protocol version mismatch",
    )
    require(
        protocol.get("end_to_end_spec_path") == EXPECTED_SPEC_PATH,
        "manifest end-to-end protocol path mismatch",
    )

    documentation_model = protocol.get("documentation_model", {})
    for owner in (
        "primary_owns",
        "manifest_and_schemas_own",
        "gateway_owns",
        "end_to_end_spec_owns",
        "handoff_owns",
    ):
        require(bool(documentation_model.get(owner)), f"missing documentation owner: {owner}")

    activation_requirements = set(manifest.get("activation_requirements", []))
    require(
        REQUIRED_ACTIVATION_REQUIREMENTS.issubset(activation_requirements),
        "manifest activation requirements are incomplete",
    )

    for marker in REQUIRED_PROTOCOL_MARKERS:
        require(marker in protocol_text, f"missing protocol marker: {marker}")

    require(
        "The Primary must not be represented as the sole technical specification"
        in protocol_text,
        "missing Primary scope boundary",
    )
    require(
        "CI and in-process test clients do not substitute for an actual deployed restart"
        in protocol_text,
        "missing deployed restart evidence boundary",
    )

    print("HIL end-to-end protocol validation: PASS")


if __name__ == "__main__":
    main()
