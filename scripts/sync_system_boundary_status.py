#!/usr/bin/env python3
"""Mirror the canonical SDK system-boundary status without manual copying.

The consumer accepts status-only packets and never converts verification into
execution authority, custody, admissibility, deployment, or release authority.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any, Mapping

SOURCE = "https://raw.githubusercontent.com/StegVerse-org/StegVerse-SDK/main/evidence/system-boundary-downstream-status.v0.1.json"
OUTPUT = Path(__file__).resolve().parents[1] / "data/governance/system-boundary-status.v0.1.json"
TARGET = "StegVerse-Labs/Site"

REQUIRED_FALSE = (
    "production_binding_enabled",
    "release_authorized",
    "execution_authority_granted",
    "custody_transferred",
    "admissibility_determined",
)


def validate_packet(packet: Mapping[str, Any]) -> None:
    if packet.get("schema_version") != "stegverse.system_boundary.downstream_status.v0.1":
        raise ValueError("unsupported system-boundary downstream status schema")
    if packet.get("status_only") is not True:
        raise ValueError("system-boundary packet must remain status-only")
    if TARGET not in packet.get("targets", []):
        raise ValueError("Site is not an authorized status target")
    for key in REQUIRED_FALSE:
        if packet.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    state = packet.get("activation_state")
    verified = packet.get("verified")
    propagation = packet.get("downstream_propagation_allowed")
    if state == "VERIFIED":
        if verified is not True or propagation is not True:
            raise ValueError("VERIFIED requires verified and propagation flags")
    elif verified is not False or propagation is not False:
        raise ValueError("non-VERIFIED status cannot propagate as verified")


def fetch_packet() -> dict[str, Any]:
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "StegVerse-Site-status-sync"})
    with urllib.request.urlopen(request, timeout=30) as response:
        packet = json.load(response)
    validate_packet(packet)
    return packet


def write_packet(packet: Mapping[str, Any]) -> bool:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(packet, indent=2, sort_keys=True) + "\n"
    if OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == rendered:
        return False
    OUTPUT.write_text(rendered, encoding="utf-8")
    return True


if __name__ == "__main__":
    changed = write_packet(fetch_packet())
    print("System-boundary status updated." if changed else "System-boundary status unchanged.")
