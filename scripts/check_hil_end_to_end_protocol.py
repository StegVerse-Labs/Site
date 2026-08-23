#!/usr/bin/env python3
"""Validate the current HIL end-to-end protocol and manifest binding."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "hil-experiment.json"
PROTOCOL = ROOT / "docs" / "HIL_END_TO_END_PROTOCOL.md"

EXPECTED_PRIMARY_FILENAME = "HIL_Canonical_Paper_v1_1.pdf"
EXPECTED_PRIMARY_VERSION = "v1.1"
EXPECTED_PRIMARY_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
EXPECTED_PRIMARY_PATH = "data/HIL_Canonical_Paper_v1_1.pdf"
EXPECTED_PROTOCOL_VERSION = "HIL-PROTOCOL-v1.1"
EXPECTED_PROMPT_VERSION = "HIL-PROMPT-v1.1"
EXPECTED_PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
EXPECTED_PROVENANCE_VERSION = "HIL-RESPONSE-PROVENANCE-v1.1"

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
    "exact_v1_1_pdf_hash_verified",
    "gateway_v1_1_primary_and_prompt_hashes_deployed",
    "separate_intake_review_and_publication_credentials",
    "deployed_submission_and_receiver_receipt",
    "restart_persistence_proof",
    "authenticated_private_review",
    "append_only_publication",
    "site_import",
    "first_chained_master_record_release",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL end-to-end protocol validation failed: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    require(MANIFEST.is_file(), f"missing {MANIFEST.relative_to(ROOT)}")
    require(PROTOCOL.is_file(), f"missing {PROTOCOL.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    protocol_text = PROTOCOL.read_text(encoding="utf-8")

    primary = manifest.get("primary_document", {})
    protocol = manifest.get("protocol", {})

    require(primary.get("filename") == EXPECTED_PRIMARY_FILENAME, "canonical Primary filename mismatch")
    require(primary.get("version") == EXPECTED_PRIMARY_VERSION, "canonical Primary version mismatch")
    require(primary.get("sha256") == EXPECTED_PRIMARY_SHA256, "canonical Primary SHA-256 mismatch")
    require(primary.get("artifact_path") == EXPECTED_PRIMARY_PATH, "canonical Primary artifact path mismatch")
    require(primary.get("sole_technical_specification") is False, "Primary must not be declared the sole technical specification")

    primary_path = ROOT / EXPECTED_PRIMARY_PATH
    require(primary_path.is_file(), f"missing canonical Primary artifact: {EXPECTED_PRIMARY_PATH}")
    require(sha256_file(primary_path) == EXPECTED_PRIMARY_SHA256, "canonical Primary repository bytes do not match manifest SHA-256")

    require(protocol.get("version") == EXPECTED_PROTOCOL_VERSION, "manifest protocol version mismatch")
    require(protocol.get("prompt_version") == EXPECTED_PROMPT_VERSION, "manifest prompt version mismatch")
    require(protocol.get("prompt_sha256") == EXPECTED_PROMPT_SHA256, "manifest prompt SHA-256 mismatch")

    documentation_model = protocol.get("documentation_model", {})
    for owner in ("primary_owns", "manifest_and_schemas_own", "gateway_owns", "handoff_owns"):
        require(bool(documentation_model.get(owner)), f"missing documentation owner: {owner}")

    activation_requirements = set(manifest.get("activation_requirements", []))
    require(REQUIRED_ACTIVATION_REQUIREMENTS.issubset(activation_requirements), "manifest activation requirements are incomplete")

    for marker in REQUIRED_PROTOCOL_MARKERS:
        require(marker in protocol_text, f"missing protocol marker: {marker}")

    for marker in (
        EXPECTED_PRIMARY_FILENAME,
        EXPECTED_PRIMARY_VERSION,
        EXPECTED_PRIMARY_SHA256,
        EXPECTED_PRIMARY_PATH,
        EXPECTED_PROTOCOL_VERSION,
        EXPECTED_PROVENANCE_VERSION,
    ):
        require(marker in protocol_text, f"protocol does not bind current canonical identity: {marker}")

    require("52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946" not in protocol_text, "superseded v0.5 Primary SHA remains in protocol")
    require("Humans_as_the_Interoperability_Layer_Primary_Review_Candidate_v0_5.pdf" not in protocol_text, "superseded v0.5 Primary filename remains in protocol")
    require("The Primary must not be represented as the sole technical specification" in protocol_text, "missing Primary scope boundary")
    require("CI and in-process test clients do not substitute for an actual deployed restart" in protocol_text, "missing deployed restart evidence boundary")

    print("HIL end-to-end protocol validation: PASS")
    print(f"HIL_PRIMARY_VERSION={EXPECTED_PRIMARY_VERSION}")
    print(f"HIL_PRIMARY_SHA256={EXPECTED_PRIMARY_SHA256}")
    print("HIL_RUNTIME_AUTHORITY_EFFECT=NONE")


if __name__ == "__main__":
    main()
