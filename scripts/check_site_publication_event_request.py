#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "site-publication-event-request.json"


def die(message: str) -> None:
    raise SystemExit("SITE_PUBLICATION_EVENT_REQUEST_FAIL: " + message)


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site_publication_event_request.py")], cwd=ROOT, check=True)
    value = json.loads(OUT.read_text(encoding="utf-8"))
    if value.get("schema") != "stegverse.site.publication-event-request/v1":
        die("unexpected envelope schema")
    if value.get("runtime_class") != "EVENT_EPHEMERAL":
        die("runtime class mismatch")
    if value.get("persistent_node_identity_required") is not True:
        die("persistent Node continuity is not required")
    for key in ("persistent_host_required", "always_on_receiver_required", "second_user_operated_device_required", "request_grants_execution_authority"):
        if value.get(key) is not False:
            die(f"forbidden requirement/authority enabled: {key}")
    if value.get("rendezvous_requirement") != "REQUIRED":
        die("public rendezvous must be required")
    if value.get("public_profile_observation_origin") != "INDEPENDENT_PUBLIC_HTTPS":
        die("public observation origin mismatch")
    if value.get("credential_authority") != "TV/TVC" or value.get("github_token_runtime_authority") != "NONE":
        die("credential/runtime authority mismatch")

    intent = value.get("transport_intent") or {}
    if intent.get("schema") != "stegverse.universal-intr-transport/v1" or intent.get("protocol") != "InTr":
        die("transport schema/protocol mismatch")
    if intent.get("operation_id") != "SITE_PUBLICATION_EVENT":
        die("operation mismatch")
    if intent.get("boundary_path") != ["DEVICE_SYSTEM", "STEGOS_ECOSYSTEM"]:
        die("non-adjacent or unexpected boundary path")
    semantics = intent.get("transport_semantics") or {}
    if semantics.get("event_triggered") is not True or semantics.get("always_on_receiver_required") is not False or semantics.get("second_user_device_required") is not False:
        die("event-ephemeral transport semantics mismatch")
    authority = intent.get("authority") or {}
    if authority.get("authority_transfer") is not False or authority.get("transport_grants_execution_authority") is not False or authority.get("credential_authority") != "TV/TVC":
        die("transport authority violation")

    request = value.get("materialization_request") or {}
    if request.get("schema") != "stegverse.universal-intr-materialization-request/v1":
        die("materialization schema mismatch")
    if request.get("state") != "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION":
        die("materialization state mismatch")
    if request.get("operation_id") != intent.get("operation_id") or request.get("packet_id") != intent.get("packet_id") or request.get("payload_hash") != intent.get("payload_hash"):
        die("materialization/transport binding mismatch")
    if request.get("event_triggered") is not True or request.get("always_on_receiver_required") is not False or request.get("second_user_device_required") is not False:
        die("materialization runtime semantics mismatch")
    if request.get("request_grants_execution_authority") is not False or request.get("claim_or_fence_minted") is not False or request.get("transport_grants_execution_authority") is not False or request.get("authority_transfer") is not False:
        die("materialization request grants authority")
    if request.get("downstream_owner_ref") != "StegVerse-Labs/StegOS:canonical-runtime-lane":
        die("downstream runtime owner mismatch")
    if request.get("credential_authority") != "TV/TVC" or request.get("github_token_runtime_authority") != "NONE":
        die("materialization authority mismatch")

    if value.get("artifact_manifest_sha256") != intent.get("payload_hash") or request.get("payload_hash") != intent.get("payload_hash"):
        die("artifact manifest identity not preserved")

    print("SITE_PUBLICATION_EVENT_REQUEST_CONTRACT=PASS")
    print("RUNTIME_CLASS=EVENT_EPHEMERAL")
    print("MATERIALIZATION_STATE=QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION")
    print("ALWAYS_ON_RECEIVER_REQUIRED=false")
    print("SECOND_USER_OPERATED_DEVICE_REQUIRED=false")
    print("REQUEST_GRANTS_EXECUTION_AUTHORITY=false")


if __name__ == "__main__":
    main()
