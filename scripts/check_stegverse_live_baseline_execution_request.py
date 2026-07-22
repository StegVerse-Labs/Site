#!/usr/bin/env python3
"""Validate the governed StegVerse live-baseline execution request."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "data/framework-evaluations/stegverse-live-baseline-execution-request.json"
READINESS = ROOT / "data/framework-evaluations/stegverse-live-baseline-readiness.json"
NO_AUTHORITY = {
    "comparison": False,
    "admissibility": False,
    "certification": False,
    "execution": False,
    "custody": False,
    "parentage": False,
}


def require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def load(path: Path) -> dict:
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    request = load(REQUEST)
    readiness = load(READINESS)

    require(request.get("schema_version") == "1.0.0", "unsupported request schema")
    require(request.get("framework_id") == "stegverse", "framework_id mismatch")
    require(request.get("test_case_id") == readiness.get("test_case_id"), "test_case_id mismatch")
    require(request.get("requested_transition") == readiness.get("next_transition", {}).get("name"), "requested transition mismatch")
    require(request.get("authority") == NO_AUTHORITY, "request authority boundary changed")

    requester = request.get("requested_by") or {}
    require(requester.get("execution_authority") is False, "Site requester cannot claim execution authority")
    require(requester.get("custody_authority") is False, "Site requester cannot claim custody authority")

    target = request.get("execution_target") or {}
    require(target.get("runtime_owner") == "StegVerse-org/LLM-adapter", "unexpected runtime owner")
    require(target.get("site_is_execution_target") is False, "Site cannot be execution target")

    require(len(request.get("required_precommit_inputs") or []) >= 6, "precommit input contract incomplete")
    require(len(request.get("required_execution_outputs") or []) >= 8, "execution output contract incomplete")
    require(len(request.get("prohibited_inferences") or []) >= 5, "prohibited inference boundary incomplete")

    dispatch = request.get("dispatch") or {}
    readiness_state = readiness.get("state")
    if readiness_state == "BLOCKED":
        require(request.get("request_state") == "PENDING_PREREQUISITES", "blocked readiness requires pending request")
        require(dispatch.get("authorized") is False, "blocked readiness cannot authorize dispatch")
        require(dispatch.get("dispatch_id") is None, "blocked request cannot have dispatch_id")
        require(dispatch.get("dispatched_at") is None, "blocked request cannot have dispatched_at")
        require(dispatch.get("authorization_receipt_ref") is None, "blocked request cannot claim authorization receipt")
        require(dispatch.get("blocked_by_readiness_id") == readiness.get("readiness_id"), "readiness binding mismatch")
    else:
        require(request.get("request_state") in {"READY_FOR_AUTHORIZATION", "AUTHORIZED", "DISPATCHED", "COMPLETED"}, "invalid advanced request state")

    print(f"STEGVERSE LIVE BASELINE EXECUTION REQUEST: {request.get('request_state')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
