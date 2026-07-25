#!/usr/bin/env python3
"""Fail-closed validation for the HIL deployed controlled-cycle evidence packet."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data" / "hil-deployed-controlled-cycle-evidence.json"
ACTIVATION = ROOT / "data" / "hil-activation-state.json"
RUNBOOK = ROOT / "docs" / "HIL_DEPLOYED_CONTROLLED_CYCLE_RUNBOOK.md"

PRIMARY_HASH = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
PROMPT_HASH = "0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922"
MINIMUM_COMMIT = "b2e612dd74d311e0cbe66cd1c1d4758bff129fd4"
SHA256 = re.compile(r"^[a-f0-9]{64}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL deployed-cycle evidence verification failed: {message}")


def load(path: Path) -> dict:
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def established(section: dict) -> bool:
    return section.get("state") == "ESTABLISHED"


def valid_hash(value: object) -> bool:
    return isinstance(value, str) and bool(SHA256.fullmatch(value))


def main() -> None:
    packet = load(PACKET)
    activation = load(ACTIVATION)
    runbook = RUNBOOK.read_text(encoding="utf-8")

    require(packet.get("schema_version") == "HIL-DEPLOYED-CONTROLLED-CYCLE-EVIDENCE-v1", "schema version mismatch")
    require(packet.get("experiment_id") == "HIL-2026", "experiment mismatch")
    require(packet.get("cycle_id") == "HIL-CYCLE-0001", "first controlled-cycle ID mismatch")
    require(packet.get("packet_state") in {"INCOMPLETE", "COMPLETE"}, "invalid packet state")
    require(packet.get("authority_effect") == "NONE", "evidence packet must not grant authority")

    deployment = packet["deployment"]
    require(deployment.get("repository") == "StegVerse-org/LLM-adapter", "gateway repository mismatch")
    require(deployment.get("minimum_commit") == MINIMUM_COMMIT, "minimum gateway commit mismatch")

    credentials = packet["credential_separation"]
    require(credentials.get("secret_material_recorded") is False, "secret material must never be recorded")

    readiness = packet["readiness"]
    require(readiness.get("receipt_type") == "HIL-LIVE-READINESS-OBSERVATION-v2", "readiness receipt type mismatch")

    submission = packet["submission"]
    require(submission.get("receiver_receipt_type") == "HIL-RECEIVER-RECEIPT-v2", "receiver receipt type mismatch")

    review = packet["private_review"]
    require(review.get("receipt_type") == "HIL-PRIVATE-REVIEW-RECEIPT-v1", "private-review receipt type mismatch")

    publication = packet["publication"]
    require(publication.get("publication_record_type") == "HIL-PUBLICATION-RECORD-v1", "publication record type mismatch")

    master = packet["master_record"]
    require(master.get("release_type") == "HIL-MASTER-RECORD-RELEASE-v1", "Master Record release type mismatch")

    require(packet["orchestration"].get("state") in {"NOT_AUTHORIZED", "AUTHORIZED", "SUBMITTED"}, "invalid orchestration state")

    sections = [
        deployment,
        packet["durable_storage"],
        credentials,
        readiness,
        submission,
        packet["restart"],
        packet["post_restart_persistence"],
        review,
        publication,
        packet["site_import"],
        master,
    ]
    all_established = all(established(section) for section in sections)

    if established(credentials):
        fingerprints = [
            credentials.get("intake_fingerprint"),
            credentials.get("private_review_fingerprint"),
            credentials.get("publication_fingerprint"),
        ]
        require(all(isinstance(value, str) and value for value in fingerprints), "credential fingerprints missing")
        require(len(set(fingerprints)) == 3, "credential fingerprints must be distinct")
        require(credentials.get("distinct") is True, "credential separation flag must be true")

    if established(readiness):
        require(readiness.get("observed_state") == "CONTROLLED_CYCLE_READY", "readiness not controlled-cycle ready")
        require(readiness.get("primary_sha256") == PRIMARY_HASH, "readiness Primary hash mismatch")
        require(readiness.get("prompt_sha256") == PROMPT_HASH, "readiness prompt hash mismatch")
        require(valid_hash(readiness.get("receipt_sha256")), "invalid readiness receipt hash")

    if established(submission):
        require(isinstance(submission.get("submission_id"), str) and submission["submission_id"], "submission ID missing")
        require(valid_hash(submission.get("response_sha256")), "invalid response hash")
        require(valid_hash(submission.get("provenance_manifest_sha256")), "invalid provenance hash")
        require(valid_hash(submission.get("receiver_receipt_sha256")), "invalid receiver receipt hash")

    persistence = packet["post_restart_persistence"]
    if established(persistence):
        require(packet["restart"].get("state") == "ESTABLISHED", "persistence cannot precede restart evidence")
        require(persistence.get("submission_id_unchanged") is True, "submission identity changed after restart")
        require(persistence.get("response_hash_matches") is True, "response bytes failed post-restart verification")
        require(persistence.get("provenance_hash_matches") is True, "provenance failed post-restart verification")

    if established(review):
        require(review.get("decision") == "ACCEPT_PRIVATE", "first controlled cycle must record ACCEPT_PRIVATE")
        require(review.get("write_once_verified") is True, "write-once private review not verified")
        require(valid_hash(review.get("receipt_sha256")), "invalid private-review receipt hash")

    if established(publication):
        require(isinstance(publication.get("response_id"), str) and re.fullmatch(r"HIL-RESP-[A-Z0-9-]+", publication["response_id"]), "invalid response ID")
        require(valid_hash(publication.get("publication_record_sha256")), "invalid publication record hash")
        require(publication.get("append_only_verified") is True, "append-only publication not verified")

    if established(master):
        require(valid_hash(master.get("release_sha256")), "invalid Master Record release hash")

    if packet.get("packet_state") == "COMPLETE":
        require(all_established, "packet marked complete before every evidence section is established")
        require(packet["public_acquisition"].get("authorized") is False or packet["public_acquisition"].get("authorization_ref"), "public acquisition authorization lacks reference")
    else:
        require(packet["public_acquisition"].get("authorized") is False, "incomplete packet cannot authorize public acquisition")

    require(activation.get("public_acquisition_authorized") is False, "activation ledger currently must remain fail-closed")
    require(activation.get("release_authorized") is False, "release must remain unauthorized")

    for marker in (
        "actual service restart",
        "HIL-LIVE-READINESS-OBSERVATION-v2",
        "HIL-RECEIVER-RECEIPT-v2",
        "HIL-PRIVATE-REVIEW-RECEIPT-v1",
        "HIL-PUBLICATION-RECORD-v1",
        "HIL-MASTER-RECORD-RELEASE-v1",
        "complete evidence packet != automatic public activation",
    ):
        require(marker in runbook, f"runbook missing marker: {marker}")

    print("HIL_DEPLOYED_CONTROLLED_CYCLE_EVIDENCE=PASS")
    print(f"HIL_EVIDENCE_PACKET_STATE={packet['packet_state']}")
    print(f"HIL_ALL_LIVE_SECTIONS_ESTABLISHED={str(all_established).lower()}")
    print("HIL_PUBLIC_ACQUISITION_AUTHORIZED=false")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
