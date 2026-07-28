#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "user-llm-bounded-execution-import-status.json"
IMPORT_DIR = ROOT / "data" / "user-llm-bounded-execution-receipts"
EXPECTED_ROUTES = {
    "demo_test_suite:list",
    "entity_sandbox_runner:submit",
    "hil_response_packet:submit_pdf_metadata",
}
FALSE_FIELDS = (
    "production_execution_authorized",
    "publication_authorized",
    "continuity_authorized",
    "custody_authorized",
    "master_record_release_authorized",
    "site_activation_complete",
    "activation_effect",
    "authority_effect",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    files = sorted(IMPORT_DIR.glob("*.json"))
    observed = {
        f"{item['route']}:{item['action']}"
        for item in (json.loads(path.read_text(encoding="utf-8")) for path in files)
    }
    require(data.get("schema_version") == "USER-LLM-BOUNDED-EXECUTION-IMPORT-STATUS-v1", "schema mismatch")
    require(data.get("state") == "BOUNDED_RETURNED_EXECUTION_EVIDENCE_OBSERVED", "state mismatch")
    require(data.get("imports_observed") == len(files) == 3, "import count mismatch")
    require(set(data.get("routes", [])) == EXPECTED_ROUTES == observed, "route set mismatch")
    require(data.get("source_commit") == "668ace00da5e1e3544c6a2a2166ab1435025e39b", "source commit mismatch")
    require(data.get("source_workflow_run_id") == 30358280344, "workflow run mismatch")
    require(data.get("site_import_merge_commit") == "0d2811757b4c1b987190e41f276ac40b79d0d724", "Site merge mismatch")
    for field in FALSE_FIELDS:
        require(data.get(field) is False, f"authority escalation: {field}")
    require(bool(data.get("remaining_blockers")), "remaining blockers must stay explicit")
    print("USER_LLM_BOUNDED_EXECUTION_IMPORT_STATUS=PASS imports=3 activation=false")


if __name__ == "__main__":
    main()
