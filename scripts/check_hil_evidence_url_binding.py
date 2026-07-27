#!/usr/bin/env python3
"""Fail closed unless deployed HIL evidence uses public, origin-bound HTTPS URLs."""
from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data" / "hil-deployed-controlled-cycle-evidence.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL evidence URL binding verification failed: {message}")


def public_hostname(hostname: str | None) -> bool:
    if not hostname:
        return False
    normalized = hostname.rstrip(".").lower()
    if normalized == "localhost" or normalized.endswith(".localhost"):
        return False
    try:
        address = ipaddress.ip_address(normalized)
    except ValueError:
        return True
    return address.is_global and not address.is_multicast


def clean_https_origin(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return bool(
        parsed.scheme == "https"
        and public_hostname(parsed.hostname)
        and not parsed.username
        and not parsed.password
        and parsed.path in {"", "/"}
        and not parsed.query
        and not parsed.fragment
    )


def clean_https_lookup(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return bool(
        parsed.scheme == "https"
        and public_hostname(parsed.hostname)
        and not parsed.username
        and not parsed.password
        and parsed.path.startswith("/")
        and parsed.path not in {"", "/"}
        and not parsed.query
        and not parsed.fragment
    )


def origin(value: str) -> tuple[str, str, int]:
    parsed = urlparse(value)
    return parsed.scheme, parsed.hostname or "", parsed.port or 443


def main() -> None:
    require(PACKET.is_file(), f"missing {PACKET.relative_to(ROOT)}")
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    require(isinstance(packet, dict), "evidence packet must contain an object")

    deployment = packet.get("deployment")
    publication = packet.get("publication")
    require(isinstance(deployment, dict), "deployment section missing")
    require(isinstance(publication, dict), "publication section missing")

    deployment_established = deployment.get("state") == "ESTABLISHED"
    publication_established = publication.get("state") == "ESTABLISHED"

    if deployment_established:
        require(clean_https_origin(deployment.get("base_url")), "deployment base URL must be a clean public HTTPS origin")

    if publication_established:
        require(deployment_established, "publication cannot precede deployment evidence")
        lookup = publication.get("stable_lookup_url")
        require(clean_https_lookup(lookup), "stable lookup must be a clean public HTTPS URL with a non-root path")
        require(origin(deployment["base_url"]) == origin(lookup), "stable lookup origin must match deployed receiver origin")

    print("HIL_EVIDENCE_URL_BINDING=PASS")
    print(f"HIL_DEPLOYMENT_URL_ESTABLISHED={str(deployment_established).lower()}")
    print(f"HIL_PUBLICATION_URL_ESTABLISHED={str(publication_established).lower()}")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
