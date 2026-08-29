#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "contract": ROOT / "data" / "stegverse-me-origin-contract.json",
    "html": ROOT / "stegos-node" / "services.html",
    "state": ROOT / "stegos-node" / "services-state.js",
    "runtime": ROOT / "stegos-node" / "services.js",
    "handoff": ROOT / "docs" / "STEGVERSE_ME_SITE_ORIGIN_MIRROR_HANDOFF.md",
    "claim": ROOT / "data" / "session-work-claims.d" / "site-stegverse-me-origin-581.json",
}

MARKERS = {
    "html": (
        "My StegVerse Services",
        'id="projection-state"',
        'id="services"',
        'data-state="ACTIVE"',
        "ACTIVE (green)",
        "REVIEW (yellow)",
        "UNAVAILABLE (red)",
        "INACTIVE (gray)",
        "./services-state.js",
        "./services.js",
    ),
    "state": (
        'ACTIVE: "GREEN"',
        'REVIEW: "YELLOW"',
        'UNAVAILABLE: "RED"',
        'INACTIVE: "GRAY"',
        'registration_verified',
        'governed_control.enabled=true',
        'authority_effect: "NONE"',
        "activation_performed: false",
    ),
    "runtime": (
        'DB_NAME = "stegos-node-v1"',
        'RECEIPTS = "receipts"',
        'receipt_number !== 1',
        'transition !== "NODE_REGISTERED"',
        'continuity_parent !== "GENESIS"',
        'credential_authority !== "TV/TVC"',
        'fetch("./kv-readiness-snapshot.json"',
        "FAIL_CLOSED",
        "runtime activation claimed: false",
    ),
    "handoff": (
        "SITE-STEGVERSE-ME-ORIGIN-581",
        "State: CLAIM_ADMISSION_IN_PROGRESS",
        "No alternate node identity",
        "No production DNS target",
        "authority",
    ),
    "claim": (
        "SITE-STEGVERSE-ME-ORIGIN-581-20260829",
        "CLAIMED_FOR_IMPLEMENTATION",
        "TV/TVC",
        '"authority_effect": false',
        '"activation_effect": false',
    ),
}

PROHIBITED = (
    "password",
    "api_key",
    "private_key",
    "github_token",
    "GITHUB_TOKEN",
    "activation_performed: true",
    '"activation_effect": true',
    '"authority_effect": true',
)


def main() -> int:
    failures: list[str] = []
    contents: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
            continue
        contents[name] = path.read_text(encoding="utf-8")

    for name, markers in MARKERS.items():
        text = contents.get(name, "")
        for marker in markers:
            if marker not in text:
                failures.append(f"{name} missing marker {marker}")

    combined = "\n".join(contents.values())
    for marker in PROHIBITED:
        if marker in combined:
            failures.append(f"prohibited authority/secret marker {marker}")

    try:
        contract = json.loads(contents.get("contract", "{}"))
        if contract.get("schema") != "stegverse.site.personal-kv-origin-contract/v1":
            failures.append("origin contract schema mismatch")
        if contract.get("dns_mutation_allowed") is not False:
            failures.append("DNS mutation must remain false")
        if contract.get("authority_effect") != "NONE" or contract.get("activation_effect") is not False:
            failures.append("origin contract authority boundary invalid")
        routes = {item.get("public_path") for item in contract.get("routes", [])}
        expected = {"/", "/n/{opaque_node}/", "/n/{opaque_node}/services.html"}
        if routes != expected:
            failures.append("canonical route set mismatch")
        if any(contract.get("authority", {}).values()):
            failures.append("domain/web origin may not own authority")
    except json.JSONDecodeError:
        failures.append("origin contract invalid JSON")

    if failures:
        print("STEGVERSE_ME_ORIGIN_SOURCE_FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("STEGVERSE_ME_ORIGIN_SOURCE_PASS")
    print("DNS_MUTATION_PERFORMED=false")
    print("AUTHORITY_EFFECT=NONE")
    print("ACTIVATION_EFFECT=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
