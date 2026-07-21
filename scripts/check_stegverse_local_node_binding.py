#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/ecosystem-chat-live-binding.js"


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    required = (
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "/api/stegverse-node",
        "stegverse.node.endpoint-advertisement.v1",
        "advertisement_sha256",
        "crypto.subtle.digest('SHA-256'",
        "health_bound !== true",
        "authority_granted !== false",
        "publication_authority !== false",
        "execution_authority !== false",
        "verified_local_stegverse_node_not_found",
        "external_host_dependency: false",
        "source=stegverse_local_node",
    )
    for fragment in required:
        if fragment not in text:
            raise SystemExit(f"missing local-node binding fragment: {fragment}")

    forbidden = (
        "onrender.com",
        "renderSubdomainPolicy",
        "GATEWAY_BASE_URL = 'https://",
    )
    for fragment in forbidden:
        if fragment in text:
            raise SystemExit(f"external-host binding remains: {fragment}")

    print("STEGVERSE LOCAL NODE BINDING: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
