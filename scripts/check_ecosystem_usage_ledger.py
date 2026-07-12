#!/usr/bin/env python3
"""Validate the public cross-entry usage ledger surface."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise SystemExit(f"ECOSYSTEM_USAGE_LEDGER_FAIL: missing {label}: {marker}")


def main() -> int:
    html = (ROOT / "ecosystem-usage.html").read_text(encoding="utf-8")
    script = (ROOT / "assets/ecosystem-usage-ledger.js").read_text(encoding="utf-8")
    roles = json.loads((ROOT / "data/entry-point-roles.json").read_text(encoding="utf-8"))
    fixture = json.loads((ROOT / "data/usage-session-fixture.json").read_text(encoding="utf-8"))

    for marker in (
        "Ecosystem Usage Ledger",
        "Entry-point roles",
        "Session summary",
        "Transition timeline",
        "usage display is not authority",
        "assets/ecosystem-usage-ledger.js",
    ):
        require(html, marker, "page marker")

    for marker in (
        "stegverse.transitionUsageEvents.v1",
        "metric_owner}::${event.measurement_id}",
        "mixed session identities are not allowed",
        "Usage prepend",
        "CONFIGURED",
        "UNAVAILABLE",
        "does not alter provider output or transition hashes",
    ):
        require(script, marker, "renderer invariant")

    ids = {item["entry_point_id"] for item in roles.get("entry_points", [])}
    if ids != {"sdk", "llm_adapter", "ecosystem_chat"}:
        raise SystemExit(f"ECOSYSTEM_USAGE_LEDGER_FAIL: unexpected role ids {sorted(ids)}")

    session_id = fixture.get("session_id")
    events = fixture.get("events", [])
    if not session_id or not events:
        raise SystemExit("ECOSYSTEM_USAGE_LEDGER_FAIL: fixture requires session and events")

    seen: set[tuple[str, str]] = set()
    owners: set[str] = set()
    for event in events:
        if event.get("session_id") != session_id:
            raise SystemExit("ECOSYSTEM_USAGE_LEDGER_FAIL: fixture mixes sessions")
        key = (str(event.get("metric_owner")), str(event.get("measurement_id")))
        if key in seen:
            raise SystemExit(f"ECOSYSTEM_USAGE_LEDGER_FAIL: duplicate measurement {key}")
        seen.add(key)
        owners.add(key[0])
        for name, metric in event.get("metrics", {}).items():
            evidence = metric.get("evidence_class")
            if evidence not in {"MEASURED", "CONFIGURED", "DERIVED", "UNAVAILABLE"}:
                raise SystemExit(f"ECOSYSTEM_USAGE_LEDGER_FAIL: invalid evidence for {name}")
            if evidence == "UNAVAILABLE" and metric.get("value") is not None:
                raise SystemExit(f"ECOSYSTEM_USAGE_LEDGER_FAIL: unavailable {name} has value")

    required_owners = {"ecosystem_chat", "sdk", "llm_adapter", "core-node-runtime-demo"}
    if not required_owners.issubset(owners):
        raise SystemExit(f"ECOSYSTEM_USAGE_LEDGER_FAIL: missing owners {sorted(required_owners - owners)}")

    print("ECOSYSTEM_USAGE_LEDGER_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
