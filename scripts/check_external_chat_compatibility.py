#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "external-chat.html"
CLIENT = ROOT / "assets" / "external-chat.js"
EXAMPLE = ROOT / "data" / "external-chat-example.json"


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT COMPATIBILITY: FAIL - {message}")
    return 1


def main() -> int:
    for path in [PAGE, CLIENT, EXAMPLE]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    for marker in [
        "External Chat",
        "compatibility evidence only",
        "does not certify",
        "assets/external-chat.js",
        "admissibility-wiki/external-frameworks",
    ]:
        if marker not in page:
            return fail(f"page missing marker: {marker}")

    for marker in [
        "/api/external-framework-compatibility",
        "compatibility_evidence_only",
        "compatibility_result_is_authority",
        "submission_retained",
        "wiki_record_created",
        "No result or receipt was claimed",
    ]:
        if marker not in client:
            return fail(f"client missing marker: {marker}")

    required = [
        "framework_id",
        "framework_name",
        "source_references",
        "input_artifact_type",
        "output_artifact_type",
        "actor_or_authority_model",
        "evidence_model",
        "policy_or_rule_model",
        "delegation_model",
        "decision_or_result_model",
        "receipt_or_trace_model",
        "reconstruction_model",
        "fail_closed_conditions",
    ]
    missing = [field for field in required if field not in example]
    if missing:
        return fail("example missing fields: " + ", ".join(missing))
    for key in [
        "execution_authority_claim",
        "commit_time_authority_claim",
        "certification_claim",
        "equivalence_claim",
    ]:
        if example.get(key) is not False:
            return fail(f"example boundary must be false: {key}")

    print("EXTERNAL CHAT COMPATIBILITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
