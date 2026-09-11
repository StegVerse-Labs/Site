#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "INTERLOCK_INTR_CONNECTION_GUIDE.md"
PAGE = ROOT / "interlock-intr-connections.html"
EXAMPLE = ROOT / "fixtures" / "interlock-intr" / "response-packet.example.json"
README = ROOT / "README.md"


def die(message: str) -> None:
    raise SystemExit(f"INTERLOCK_INTR_CONNECTION_DOCS_FAIL: {message}")


def require_text(text: str, marker: str, where: str) -> None:
    if marker not in text:
        die(f"missing {marker!r} in {where}")


def main() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    page = PAGE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    for marker in (
        "response packet submitted",
        "stegverse.universal-intr-transport/v1",
        "stegverse.universal-intr-materialization-request/v1",
        "stegos.node_intr_outbox_entry.v1",
        "stegos.node_intr_materialization_trigger.v1",
        "PACKET_ACCEPTED",
        "OUTBOX_STAGED",
        "CONNECTION_INITIATED",
        "INGRESS_ADMITTED",
        "AWAITING_DOWNSTREAM_RECEIPT",
        "CONNECTION_ESTABLISHED",
        "BLOCKED_PROFILE_UNAVAILABLE",
        "TV/TVC",
        "Heartbeat authority = NONE_CARRIER_ONLY",
        "HIL as the reference implementation",
    ):
        require_text(guide, marker, "guide")

    for marker in (
        "A response packet starts the connection-initiation sequence",
        "Probe /intr/profile",
        "READY_FOR_PROFILE_ADAPTER_CONNECTION_INITIATION",
        "BLOCKED_PROFILE_UNAVAILABLE",
        "response packet != Node/Interlock identity",
        "ingress admitted != downstream transition executed",
        "credential authority = TV/TVC",
        "Site = documentation / projection / initiation surface only",
        "humans-as-interoperability-layer.html#submit",
    ):
        require_text(page, marker, "page")

    if "PACKET_ACCEPTED</strong><p>Exact packet/artifact retained and hash-bound." not in page:
        die("PACKET_ACCEPTED semantics changed")
    if "CONNECTION_ESTABLISHED</strong><p>Profile-required downstream/relationship evidence" not in page:
        die("CONNECTION_ESTABLISHED must require downstream evidence")
    if "packet accepted = connection established" in guide.lower() or "packet accepted means connection established" in guide.lower():
        die("guide collapses packet acceptance into connection establishment")

    if example.get("schema") != "stegverse.site.interlock-intr-response-packet-handoff/v1":
        die("example schema mismatch")
    if example.get("requested_connection_state") != "INITIATE":
        die("example must represent initiation request")
    payload_hash = example.get("payload_sha256")
    if not isinstance(payload_hash, str) or not payload_hash.startswith("sha256:") or len(payload_hash) != 71:
        die("example payload_sha256 invalid")
    authority = example.get("authority") or {}
    for key in (
        "packet_grants_governance_authority",
        "packet_grants_execution_authority",
        "packet_grants_credential_authority",
        "packet_grants_node_identity",
        "packet_grants_interlock_identity",
    ):
        if authority.get(key) is not False:
            die(f"example authority boundary invalid: {key}")
    if authority.get("credential_authority") != "TV/TVC":
        die("example credential authority mismatch")
    if authority.get("heartbeat_authority_effect") != "NONE_CARRIER_ONLY":
        die("example heartbeat boundary mismatch")
    if authority.get("authority_effect") != "NONE_HANDOFF_ONLY":
        die("example handoff authority effect mismatch")

    require_text(readme, "interlock-intr-connections.html", "README")
    require_text(readme, "INTERLOCK_INTR_CONNECTION_GUIDE.md", "README")

    print("INTERLOCK_INTR_CONNECTION_DOCS_PASS")


if __name__ == "__main__":
    main()
