#!/usr/bin/env python3
"""Fail-closed validation for the HIL deployed controlled-cycle evidence packet."""
from __future__ import annotations

import ipaddress
import json
import re
import socket
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data" / "hil-deployed-controlled-cycle-evidence.json"
ACTIVATION = ROOT / "data" / "hil-activation-state.json"
RUNBOOK = ROOT / "docs" / "HIL_DEPLOYED_CONTROLLED_CYCLE_RUNBOOK.md"

PRIMARY_VERSION = "v1.1"
PRIMARY_HASH = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROTOCOL_VERSION = "HIL-PROTOCOL-v1.1"
PROMPT_VERSION = "HIL-PROMPT-v1.1"
PROMPT_HASH = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
PROVENANCE_SCHEMA = "HIL-RESPONSE-PROVENANCE-v1.1"
RECEIVER_RECEIPT_SCHEMA = "HIL-RECEIVER-RECEIPT-v2"
SHA256 = re.compile(r"^[a-f0-9]{64}$")
COMMIT = re.compile(r"^[a-f0-9]{40}$")


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


def globally_routable(address: str) -> bool:
    try:
        parsed = ipaddress.ip_address(address)
    except ValueError:
        return False
    return parsed.is_global


def valid_https_origin(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    if not (
        parsed.scheme == "https"
        and parsed.hostname
        and not parsed.username
        and not parsed.password
        and parsed.path in {"", "/"}
        and not parsed.query
        and not parsed.fragment
    ):
        return False

    hostname = parsed.hostname.lower().rstrip(".")
    if hostname == "localhost" or hostname.endswith(".localhost"):
        return False

    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            resolved = {
                item[4][0]
                for item in socket.getaddrinfo(hostname, parsed.port or 443, type=socket.SOCK_STREAM)
            }
        except socket.gaierror:
            return False
        return bool(resolved) and all(globally_routable(address) for address in resolved)
    return literal.is_global


def main() -> None:
    packet = load(PACKET)
    activation = load(ACTIVATION)
    runbook = RUNBOOK.read_text(encoding="utf-8")

    require(packet.get("schema_version") == "HIL-DEPLOYED-CONTROLLED-CYCLE-EVIDENCE-v1", "schema version mismatch")
    require(packet.get("experiment_id") == "HIL-2026", "experiment mismatch")
    require(packet.get("cycle_id") == "HIL-CYCLE-0001", "first controlled-cycle ID mismatch")
    require(packet.get("packet_state") in {"INCOMPLETE", "COMPLETE"}, "invalid packet state")
    require(packet.get("authority_effect") == "NONE", "evidence packet must not grant authority")

    contract = packet.get("contract")
    require(isinstance(contract, dict), "missing HIL v1.1 contract binding")
    expected_contract = {
        "primary_version": PRIMARY_VERSION,
        "primary_sha256": PRIMARY_HASH,
        "protocol_version": PROTOCOL_VERSION,
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": PROMPT_HASH,
        "provenance_schema": PROVENANCE_SCHEMA,
        "receiver_receipt_schema": RECEIVER_RECEIPT_SCHEMA,
    }
    for key, expected in expected_contract.items():
        require(contract.get(key) == expected, f"contract mismatch for {key}")

    deployment = packet["deployment"]
    require(deployment.get("repository") == "StegVerse-org/LLM-adapter", "gateway repository mismatch")
    require(deployment.get("minimum_commit") is None, "retired minimum-commit gate must remain removed")
    if established(deployment):
        require(bool(COMMIT.fullmatch(str(deployment.get("deployed_commit", "")))), "invalid deployed commit")
        require(valid_https_origin(deployment.get("base_url")), "deployment base URL must be a globally routable HTTPS origin")
        require(deployment.get("evidence_refs"), "deployment evidence references missing")

    credentials = packet["credential_separation"]
    require(credentials.get("secret_material_recorded") is False, "secret material must never be recorded")

    readiness = packet["readiness"]
    require(readiness.get("receipt_type") == "HIL-HTTPS-RECEIVER-PROBE-v1", "readiness receipt type mismatch")

    submission = packet["submission"]
    require(submission.get("receiver_receipt_type") == RECEIVER_RECEIPT_SCHEMA, "receiver receipt type mismatch")

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

    storage = packet["durable_storage"]
    if established(storage):
        require(storage.get("storage_class") == "EXTERNAL_DURABLE_SERVICE", "durable storage class mismatch")
        require(isinstance(storage.get("locator_fingerprint"), str) and storage["locator_fingerprint"], "storage fingerprint missing")
        require(storage.get("persistence_declaration_ref"), "persistence declaration evidence missing")

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
        require(readiness.get("observed_state") == "READY", "receiver readiness not READY")
        for key, expected in expected_contract.items():
            if key == "receiver_receipt_schema":
                continue
            require(readiness.get(key) == expected, f"readiness contract mismatch for {key}")
        require(valid_hash(readiness.get("receipt_sha256")), "invalid readiness receipt hash")
        require(readiness.get("evidence_ref"), "readiness evidence reference missing")

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
        require(valid_https_origin(publication.get("stable_lookup_url")), "stable lookup must use a globally routable HTTPS origin")

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
        "HIL-DEPLOYED-CONTROLLED-CYCLE-RUNBOOK-v1.1",
        "data/HIL_Canonical_Paper_v1_1.pdf",
        PRIMARY_HASH,
        PROMPT_HASH,
        "HIL-HTTPS-RECEIVER-PROBE-v1",
        RECEIVER_RECEIPT_SCHEMA,
        "actual service restart or replacement",
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
