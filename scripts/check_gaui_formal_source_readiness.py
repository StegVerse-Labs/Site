#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/gaui-formal-source-readiness.json"


def fail(reason: str) -> None:
    raise SystemExit(f"GAUI_FORMAL_SOURCE_GATE=FAIL\nreason={reason}")


def main() -> int:
    if not STATE.is_file():
        fail("missing_state")
    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data.get("source_uri") != "https://zenodo.org/records/22301698":
        fail("unexpected_source_uri")
    if data.get("linkedin_discussion_satisfies_formal_source_gate") is not False:
        fail("discussion_must_not_satisfy_formal_gate")
    if data.get("publication_authority_effect") is not False:
        fail("gate_must_not_grant_publication_authority")

    full_read = data.get("full_formal_source_independently_read") is True
    locations = data.get("exact_claim_locations_resolved") is True
    projection = data.get("public_comparative_projection_ready") is True
    state = data.get("formal_source_state")

    if not full_read or not locations:
        if state != "BLOCKED_UNRESOLVED_FORMAL_SOURCE":
            fail("unresolved_source_must_fail_closed")
        if projection:
            fail("projection_cannot_be_ready_while_source_unresolved")
    else:
        if state not in {"FORMAL_SOURCE_RESOLVED", "SOURCE_MATRIX_RECONCILED"}:
            fail("resolved_source_state_invalid")

    unresolved = data.get("unresolved_requirements")
    if not isinstance(unresolved, list):
        fail("unresolved_requirements_must_be_list")
    if not full_read and not unresolved:
        fail("blocked_gate_requires_explicit_unresolved_requirements")

    print("GAUI_FORMAL_SOURCE_GATE=PASS")
    print(f"formal_source_state={state}")
    print(f"public_comparative_projection_ready={str(projection).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
