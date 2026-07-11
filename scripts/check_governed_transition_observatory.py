#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "governed-transitions.html"
SCRIPT = ROOT / "assets" / "governed-transitions.js"
DATA = ROOT / "data" / "governed-transition-index.json"


def fail(message: str) -> int:
    print(f"GOVERNED TRANSITION OBSERVATORY: FAIL - {message}")
    return 1


def main() -> int:
    for path in [PAGE, SCRIPT, DATA]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    data = json.loads(DATA.read_text(encoding="utf-8"))

    for marker in [
        "Governed Ecosystem Transitions",
        "derived public projection",
        "assets/governed-transitions.js",
        "Admissible Automated Transitions",
    ]:
        if marker not in page:
            return fail(f"page missing marker: {marker}")

    for marker in [
        "data/governed-transition-index.json",
        "projection_type",
        "master_record_status",
        "reconstruction_status",
    ]:
        if marker not in script:
            return fail(f"renderer missing marker: {marker}")

    if data.get("schema_version") != "1.0.0":
        return fail("schema_version must be 1.0.0")
    if data.get("projection_type") != "governed_transition_index":
        return fail("projection_type mismatch")
    records = data.get("records")
    if not isinstance(records, list) or not records:
        return fail("records must be a non-empty list")

    seen: set[tuple[str, str]] = set()
    for record in records:
        identity = (record.get("transition_id"), record.get("run_id"))
        if not all(identity):
            return fail("record missing transition/run identity")
        if identity in seen:
            return fail(f"duplicate identity: {identity}")
        seen.add(identity)
        if record.get("site_visibility") == "HIDDEN":
            return fail("hidden record included in public projection")
        if record.get("master_record_status") == "RECORDED" and not record.get("relationships", {}).get("master_record_ref"):
            return fail("RECORDED requires master_record_ref")

    boundary = data.get("authority_boundary", "")
    for phrase in ["derived projection", "does not grant admissibility", "Master-Records custody"]:
        if phrase not in boundary:
            return fail(f"authority boundary missing: {phrase}")

    print(f"GOVERNED TRANSITION OBSERVATORY: PASS ({len(records)} record(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
