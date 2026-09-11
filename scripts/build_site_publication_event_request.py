#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / "build" / "site-publication-artifact"
MANIFEST = ARTIFACT_ROOT / "manifest.json"
OPERATION_ID = "SITE_PUBLICATION_EVENT"
SOURCE_SUBSYSTEM = "Site:PublicationControl"
DESTINATION_SUBSYSTEM = "StegOS:SitePublicationRuntime"
DOWNSTREAM_OWNER_REF = "StegVerse-Labs/StegOS:canonical-runtime-lane"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_uri_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_uri_value(value: Any) -> str:
    return sha256_uri_bytes(canonical_json(value).encode("utf-8"))


def boundary_path(source: str, destination: str) -> list[str]:
    boundaries = ["SKAP_VAULT", "KV", "DEVICE_SYSTEM", "STEGOS_ECOSYSTEM", "EXTERNAL_SYSTEM"]
    start = boundaries.index(source)
    stop = boundaries.index(destination)
    if start <= stop:
        return boundaries[start : stop + 1]
    return list(reversed(boundaries[stop : start + 1]))


def build_intent(payload_hash: str) -> dict[str, Any]:
    path = boundary_path("DEVICE_SYSTEM", "STEGOS_ECOSYSTEM")
    basis = {
        "operation_id": OPERATION_ID,
        "payload_hash": payload_hash,
        "source_boundary": "DEVICE_SYSTEM",
        "source_subsystem": SOURCE_SUBSYSTEM,
        "destination_boundary": "STEGOS_ECOSYSTEM",
        "destination_subsystem": DESTINATION_SUBSYSTEM,
        "boundary_path": path,
    }
    return {
        "schema": "stegverse.universal-intr-transport/v1",
        "protocol": "InTr",
        "operation_id": OPERATION_ID,
        "packet_id": "INTR-" + hashlib.sha256(canonical_json(basis).encode("utf-8")).hexdigest()[:24],
        "payload_hash": payload_hash,
        "prior_transport_receipt_hash": None,
        "source": {"boundary": "DEVICE_SYSTEM", "subsystem": SOURCE_SUBSYSTEM},
        "destination": {"boundary": "STEGOS_ECOSYSTEM", "subsystem": DESTINATION_SUBSYSTEM},
        "boundary_path": path,
        "interlock_required": True,
        "transport_semantics": {
            "event_triggered": True,
            "always_on_receiver_required": False,
            "second_user_device_required": False,
            "receiver_unavailable_disposition": "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
            "exact_packet_transport_retry_allowed": True,
            "blind_consequence_retry_allowed": False,
        },
        "authority": {
            "authority_transfer": False,
            "transport_grants_execution_authority": False,
            "credential_authority": "TV/TVC",
        },
        "receipt_chain": {
            "required": True,
            "receipt_schema": "stegverse.intr.hop_receipt/v1",
            "payload_plaintext_in_receipts": False,
            "prior_hash_required_after_first_hop": True,
        },
    }


def build_materialization(intent: dict[str, Any], payload_ref: str) -> dict[str, Any]:
    intent_hash = sha256_uri_value(intent)
    identity_basis = {
        "transport_intent_hash": intent_hash,
        "operation_id": intent["operation_id"],
        "packet_id": intent["packet_id"],
        "payload_hash": intent["payload_hash"],
        "destination": intent["destination"],
    }
    body = {
        "schema": "stegverse.universal-intr-materialization-request/v1",
        "materialization_id": "INTR-MAT-" + hashlib.sha256(canonical_json(identity_basis).encode("utf-8")).hexdigest()[:24],
        "state": "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
        "transport_schema": "stegverse.universal-intr-transport/v1",
        "transport_protocol": "InTr",
        "transport_intent_hash": intent_hash,
        "operation_id": intent["operation_id"],
        "packet_id": intent["packet_id"],
        "payload_hash": intent["payload_hash"],
        "payload_ref": payload_ref,
        "destination": intent["destination"],
        "boundary_path": intent["boundary_path"],
        "downstream_owner_ref": DOWNSTREAM_OWNER_REF,
        "event_triggered": True,
        "always_on_receiver_required": False,
        "second_user_device_required": False,
        "receiver_unavailable_disposition": "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
        "exact_packet_transport_retry_allowed": True,
        "blind_consequence_retry_allowed": False,
        "interlock_required": True,
        "request_grants_execution_authority": False,
        "claim_or_fence_minted": False,
        "transport_grants_execution_authority": False,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "authority_transfer": False,
        "authority_effect": "NONE_REQUEST_ONLY",
    }
    return {**body, "request_hash": sha256_uri_value(body)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="build/site-publication-event-request.json")
    args = parser.parse_args()

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "materialize_site_publication_artifact.py"), "--output", "build/site-publication-artifact"],
        cwd=ROOT,
        check=True,
    )
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema") != "stegverse.site.static_publication_artifact.v1":
        raise SystemExit("SITE_PUBLICATION_EVENT_REQUEST_FAIL: unexpected artifact manifest schema")
    if manifest.get("format") != "STEGVERSE_SITE_STATIC_PUBLICATION_V1":
        raise SystemExit("SITE_PUBLICATION_EVENT_REQUEST_FAIL: unexpected artifact format")
    manifest_bytes = MANIFEST.read_bytes()
    manifest_sha = sha256_uri_bytes(manifest_bytes)
    payload_ref = "artifact://site-publication-manifest/" + manifest_sha.removeprefix("sha256:")
    intent = build_intent(manifest_sha)
    request = build_materialization(intent, payload_ref)
    envelope = {
        "schema": "stegverse.site.publication-event-request/v1",
        "goal_id": "SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION",
        "cosv_id": "50000000102000",
        "runtime_class": "EVENT_EPHEMERAL",
        "persistent_node_identity_required": True,
        "persistent_host_required": False,
        "always_on_receiver_required": False,
        "second_user_operated_device_required": False,
        "rendezvous_requirement": "REQUIRED",
        "public_profile_observation_origin": "INDEPENDENT_PUBLIC_HTTPS",
        "artifact_manifest_path": "build/site-publication-artifact/manifest.json",
        "artifact_manifest_sha256": manifest_sha,
        "transport_intent": intent,
        "materialization_request": request,
        "request_grants_execution_authority": False,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "authority_effect": "NONE_REQUEST_ONLY",
    }
    output = (ROOT / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if json.loads(output.read_text(encoding="utf-8")) != envelope:
        raise SystemExit("SITE_PUBLICATION_EVENT_REQUEST_FAIL: output readback mismatch")
    print(f"SITE_PUBLICATION_EVENT_REQUEST=PASS output={output.relative_to(ROOT)}")
    print(f"ARTIFACT_MANIFEST_SHA256={manifest_sha}")
    print(f"PACKET_ID={intent['packet_id']}")
    print(f"MATERIALIZATION_ID={request['materialization_id']}")
    print("RUNTIME_CLASS=EVENT_EPHEMERAL")
    print("PERSISTENT_HOST_REQUIRED=false")
    print("ALWAYS_ON_RECEIVER_REQUIRED=false")


if __name__ == "__main__":
    main()
