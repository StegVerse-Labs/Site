#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "governed-transitions.html"
SCRIPT = ROOT / "assets" / "governed-transitions.js"
LIVE = ROOT / "assets" / "governed-transitions-live-custody.js"
DATA = ROOT / "data" / "governed-transition-index.json"
STATUS = ROOT / "data" / "governed-transition-index-import-status.json"
EXECUTOR = ROOT / "data" / "governed-executor-status.json"


def fail(message: str) -> int:
    print(f"GOVERNED TRANSITION OBSERVATORY: FAIL - {message}")
    return 1


def main() -> int:
    for path in [PAGE, SCRIPT, LIVE, DATA, STATUS, EXECUTOR]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    live = LIVE.read_text(encoding="utf-8")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    executor = json.loads(EXECUTOR.read_text(encoding="utf-8"))

    for marker in [
        "Governed Ecosystem Transitions",
        "derived public projection",
        "executor-status",
        "live-custody-status",
        "does not authorize, execute, activate executors",
        "assets/governed-transitions.js",
        "assets/governed-transitions-live-custody.js",
        "Admissible Automated Transitions",
    ]:
        if marker not in page:
            return fail(f"page missing marker: {marker}")

    for marker in [
        "data/governed-transition-index.json",
        "data/governed-transition-index-import-status.json",
        "data/governed-executor-status.json",
        "projection_type",
        "master_record_status",
        "reconstruction_status",
        "activation_receipt_id",
        "executor_state_imported",
        "hash_verified",
        "live_orchestration_feed",
        "does not grant per-transition execution",
    ]:
        if marker not in script:
            return fail(f"renderer missing marker: {marker}")

    for marker in [
        "data/ecosystem-chat-gateway.json",
        "stegverse_ecosystem_chat_last_gateway_result",
        "transition_id",
        "/api/transitions/",
        "custody_submission",
        "custody_receipt_id",
        "master_record_status",
        "master_record_ref",
        "reconstruction_status",
        "RECORDED custody contract mismatch",
        "Site does not issue the final receipt",
    ]:
        if marker not in live:
            return fail(f"live custody overlay missing marker: {marker}")

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

    if executor.get("projection_type") != "governed_executor_status":
        return fail("executor projection_type mismatch")
    if executor.get("activation", {}).get("state") != "ACTIVE":
        return fail("executor projection must show ACTIVE")
    if not executor.get("activation", {}).get("activation_receipt_id"):
        return fail("executor projection requires activation receipt")
    if executor.get("to_executor", {}).get("status") != "ACTIVE":
        return fail("native executor must be ACTIVE")
    if executor.get("from_executor", {}).get("status") != "FALLBACK_ONLY":
        return fail("bootstrap executor must be FALLBACK_ONLY")
    executor_boundary = executor.get("authority_boundary", {})
    for key in [
        "projection_grants_execution_authority",
        "projection_grants_publication_authority",
        "projection_grants_admissibility",
        "projection_is_master_records_custody",
        "activation_is_per_transition_authority",
    ]:
        if executor_boundary.get(key) is not False:
            return fail(f"executor projection boundary invalid: {key}")

    if status.get("status_type") != "governed_transition_index_import_status":
        return fail("import status_type mismatch")
    if status.get("state") == "LOCAL_FALLBACK_ACTIVE":
        if status.get("hash_verified") is not False:
            return fail("local fallback must not claim hash verification")
        if status.get("live_orchestration_feed") is not False:
            return fail("local fallback must not claim live feed")
    elif status.get("state") == "RECEIPTED_EXPORT_IMPORTED":
        if status.get("hash_verified") is not True:
            return fail("receipted import must be hash verified")
    else:
        return fail("unsupported import state")
    if status.get("executor_state_imported") is not True:
        return fail("executor state must be imported")

    print(f"GOVERNED TRANSITION OBSERVATORY: PASS ({len(records)} record(s), executor ACTIVE, live custody overlay installed, {status['state']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
