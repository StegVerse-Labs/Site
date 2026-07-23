#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "request": ROOT / "data" / "stegmusic" / "composition-request.schema.v1.json",
    "receipt": ROOT / "data" / "stegmusic" / "composition-receipt.schema.v1.json",
}
REQUIRED = {
    "request": [
        "composition_request_id", "profile_scope", "session_intent", "cultural_scope",
        "historical_fidelity_target", "innovation_distance", "audience_and_place_scope",
        "instrument_and_tool_availability", "rights_constraints", "frozen_evidence_packet_id",
        "evidence_frozen", "composition_may_execute", "authority"
    ],
    "receipt": [
        "composition_id", "composition_request_id", "frozen_evidence_packet_id",
        "performer_role_graph", "instrument_and_tool_states", "continuity_events",
        "rights_and_originality_decision", "evaluation_results", "provenance_disclosure",
        "generated_origin_disclosed", "receipt_hash", "authority"
    ],
}

failures = []
for name, path in FILES.items():
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        continue
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        continue
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        failures.append(f"{name} schema draft mismatch")
    text = path.read_text(encoding="utf-8")
    for marker in REQUIRED[name]:
        if marker not in text:
            failures.append(f"{name} missing marker: {marker}")
    if payload.get("properties", {}).get("authority", {}).get("const") != "none":
        failures.append(f"{name} authority must be none")

request = json.loads(FILES["request"].read_text(encoding="utf-8")) if FILES["request"].exists() else {}
receipt = json.loads(FILES["receipt"].read_text(encoding="utf-8")) if FILES["receipt"].exists() else {}
if request:
    rights = request.get("properties", {}).get("rights_constraints", {}).get("properties", {})
    if rights.get("protected_expression_copying_prohibited", {}).get("const") is not True:
        failures.append("request must prohibit protected-expression copying")
    if rights.get("artist_voice_imitation_prohibited", {}).get("const") is not True:
        failures.append("request must prohibit artist voice imitation")
    gate = request.get("properties", {}).get("execution_gate", {}).get("properties", {})
    if gate.get("evidence_frozen", {}).get("const") is not True:
        failures.append("request execution gate must require frozen evidence")
if receipt:
    disclosure = receipt.get("properties", {}).get("provenance_disclosure", {}).get("properties", {})
    if disclosure.get("generated_origin_disclosed", {}).get("const") is not True:
        failures.append("receipt must require generated-origin disclosure")
    decision = receipt.get("properties", {}).get("rights_and_originality_decision", {}).get("properties", {}).get("decision", {}).get("enum", [])
    if set(decision) != {"ALLOW", "DENY", "ESCALATE"}:
        failures.append("receipt rights decision set must be ALLOW/DENY/ESCALATE")

if failures:
    print("STEGMUSIC_COMPOSITION_REQUEST_RECEIPT_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_COMPOSITION_REQUEST_RECEIPT_PASS")
print("request=evidence_rights_scope_execution_gate")
print("receipt=replay_roles_components_continuity_rights_artifacts_disclosure")
print("decisions=ALLOW_DENY_ESCALATE")
print("authority=none")
