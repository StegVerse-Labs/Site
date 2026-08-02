#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / "data/fixtures/hil-semantic-transformation/canonical-semantic-receipt-event.json"


def main() -> int:
    event = json.loads(EVENT.read_text(encoding="utf-8"))
    failures: list[str] = []
    required = ["event_id", "parent_event_id", "event_type", "governed_projection", "evidence_refs", "continuity_refs"]
    for field in required:
        if not event.get(field):
            failures.append(f"missing {field}")
    if event.get("event_type") != "evidence":
        failures.append("event_type must be evidence")
    if event.get("source_record_mutated") is not False:
        failures.append("source record mutation prohibited")
    if event.get("authority_effect") is not False:
        failures.append("authority effect prohibited")
    governed = event.get("governed_projection", {})
    if governed.get("validation") != "PASS":
        failures.append("linked receipt must validate PASS")
    if governed.get("authority_effect") is not False:
        failures.append("receipt authority effect prohibited")
    unresolved = [ref for ref in event.get("evidence_refs", []) if not (ROOT / ref).exists()]
    failures.extend(f"unresolved evidence ref: {ref}" for ref in unresolved)
    print(json.dumps({"validation": "PASS" if not failures else "FAIL", "event_id": event.get("event_id"), "failures": failures}, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
