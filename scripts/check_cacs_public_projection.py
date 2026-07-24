#!/usr/bin/env python3
"""Validate valid and invalid CACS public projection contracts."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/cacs-public-projection.fixture.json"
INVALID_PACKETS = {
    ROOT / "data/cacs-public-projection-invalid-duplicate.fixture.json": "claim appears in multiple projection classes",
    ROOT / "data/cacs-public-projection-invalid-withdrawn-current.fixture.json": "current claim must be active",
    ROOT / "data/cacs-public-projection-invalid-stale-unqualified.fixture.json": "stale history requires explicit stale or expired qualification",
    ROOT / "data/cacs-public-projection-invalid-unsupported-current.fixture.json": "current claim must be bounded support",
}
PAGE = ROOT / "cacs-claims.html"
SCRIPT = ROOT / "assets/cacs-claims.js"
REQUIRED = {
    "projection_id", "standard", "generated_at", "active_claim",
    "historical_claims", "suppressed_claims", "qualification_rules",
    "authority_effect", "hash",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail("projection packet root must be an object")
    return value


def validate_packet(packet: dict[str, Any]) -> None:
    if set(packet) != REQUIRED:
        fail("projection packet shape is not closed")
    if packet["authority_effect"] != "NONE":
        fail("authority_effect must be NONE")

    active = packet["active_claim"]
    if active.get("public_label") != "CURRENT_BOUNDED_CLAIM":
        fail("active claim label invalid")
    if active.get("lifecycle_state") != "active":
        fail("current claim must be active")
    if active.get("correspondence_status") not in {"supported", "partially_supported"}:
        fail("current claim must be bounded support")
    if active.get("evidence_dimensions", {}).get("scope_correspondent") != "ESTABLISHED":
        fail("current claim must be scope correspondent")
    if not active.get("not_established") or not active.get("qualification"):
        fail("current claim requires non-claims and qualifications")

    historical_claims = packet["historical_claims"]
    suppressed_claims = packet["suppressed_claims"]
    historical = {entry["public_label"] for entry in historical_claims}
    suppressed = {entry["public_label"] for entry in suppressed_claims}
    if not {"SUPERSEDED_HISTORY", "STALE_HISTORY"} <= historical:
        fail("historical lifecycle labels incomplete")
    if not {"WITHDRAWN_SUPPRESSED", "OVERSTATED_QUARANTINED"} <= suppressed:
        fail("suppression labels incomplete")

    for entry in historical_claims:
        if entry.get("public_label") == "STALE_HISTORY":
            text = " ".join((str(entry.get("reason", "")), *map(str, packet["qualification_rules"]))).lower()
            if not any(marker in text for marker in ("stale", "expired", "expiration")):
                fail("stale history requires explicit stale or expired qualification")

    ids = [active["claim_id"]]
    ids += [entry["claim_id"] for entry in historical_claims]
    ids += [entry["claim_id"] for entry in suppressed_claims]
    if len(ids) != len(set(ids)):
        fail("claim appears in multiple projection classes")


def validate_surfaces() -> None:
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    for marker in ("human-view", "raw-view", "CURRENT_BOUNDED_CLAIM", "data/cacs-public-projection.fixture.json"):
        if marker not in page:
            fail(f"page marker missing: {marker}")
    for marker in ("active_claim", "historical_claims", "suppressed_claims", "JSON.stringify"):
        if marker not in script:
            fail(f"renderer marker missing: {marker}")


def main() -> int:
    try:
        validate_packet(load(PACKET))
        validate_surfaces()
        rejected = 0
        for path, expected_error in INVALID_PACKETS.items():
            try:
                validate_packet(load(path))
            except ValueError as exc:
                if expected_error not in str(exc):
                    fail(f"{path.name}: wrong rejection reason: {exc}")
                rejected += 1
            else:
                fail(f"{path.name}: invalid packet was accepted")
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"CACS_PUBLIC_PROJECTION_FAIL: {exc}")
        return 1

    print(
        "CACS_PUBLIC_PROJECTION_PASS: valid active, historical, suppressed, human, and raw projections verified; "
        f"{rejected} invalid projection vectors rejected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
