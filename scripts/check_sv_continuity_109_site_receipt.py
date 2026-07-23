#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_TRUE = (
    "authoritative_vs_effective_database_distinguished",
    "external_ai_returns_non_authoritative",
    "unknown_retention_preserved",
    "renderer_grants_no_authority",
    "propagation_packet_grants_no_authority",
)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_sv_continuity_109_site_receipt.py RECEIPT", file=sys.stderr)
        return 2
    receipt = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures: list[str] = []
    if receipt.get("protocol_id") != "SV-CONTINUITY-109":
        failures.append("wrong protocol_id")
    if receipt.get("destination") != "StegVerse-Labs/Site":
        failures.append("wrong destination")
    checks = receipt.get("checks", {})
    for key in REQUIRED_TRUE:
        if checks.get(key) is not True:
            failures.append(f"required check failed: {key}")
    for key, value in receipt.get("authority", {}).items():
        if value is not False:
            failures.append(f"authority must remain false: {key}")
    activation_complete = checks.get("site_activation_complete") is True
    downstream_complete = checks.get("downstream_verified_ingestion_complete") is True
    decision = receipt.get("decision")
    if decision == "PASS" and not (activation_complete and downstream_complete):
        failures.append("PASS requires Site activation and downstream verified ingestion")
    if decision not in {"PASS", "BLOCK"}:
        failures.append("decision must be PASS or BLOCK")
    if failures:
        for failure in failures:
            print(f"BLOCK: {failure}")
        return 1
    print(f"VALID: Site verification decision {decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
