#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "evaluator-review.html").read_text(encoding="utf-8")
js = (ROOT / "assets/evaluator-review.js").read_text(encoding="utf-8")
fixture = json.loads((ROOT / "data/evaluator-review/cross-framework-current-basis-001.json").read_text(encoding="utf-8"))
handoff = (ROOT / "docs/EVALUATOR_REVIEW_UI_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
intr_handoff = (ROOT / "docs/EVALUATOR_REVIEW_INTR_CONNECTOR_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
runtime_handoff = (ROOT / "docs/EVALUATOR_RUNTIME_PROJECTION_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
contract = (ROOT / "docs/EVALUATOR_REVIEW_API_CONTRACT.md").read_text(encoding="utf-8")

required_html = [
    "What are we testing?", "Test vector", "Frozen inputs", "Observable outputs",
    "Pass / fail interpretation", "Expected observation is not a decision input",
    "Evidence requirements", "Discussion / review", "Approval state", "Execution",
    "Results comparison", "View raw manifest", "Revision history",
    "Provenance / advanced details", "Request changes", "Approve this version",
    "Manifest / Receipt Report", "Ingress receipt", "Egress receipt",
    "viewport-fit=cover"
]
for token in required_html:
    assert token in html, f"missing evaluator UI token: {token}"

assert "@media(max-width:680px)" in html
assert "overflow-wrap:anywhere" in html
assert "window.StegVerseInterlockConnector" in contract
assert "Interlock Connector" in contract and "InTr" in contract
assert "TV/TVC" in contract and "Master Records" in contract
assert "DRAFT_PRE_FREEZE" in handoff
assert "PUBLICLY_OBSERVED" in handoff
assert "SITE-EVALUATOR-REVIEW-INTR-CONNECTOR-634-20260829" in intr_handoff
assert "live InTr browser->runtime receipt: NOT OBSERVED" in intr_handoff
assert "SITE-EVALUATOR-RUNTIME-PROJECTION-660" in runtime_handoff
assert "SV002_PUBLIC_OBSERVE" in runtime_handoff
assert fixture["review_schema"] == "stegverse.evaluator-review.v1"
assert fixture["test"]["state"] == "FROZEN"
assert fixture["test"]["execution_state"] == "EXECUTED"
assert fixture["test"]["frozen_manifest_hash"] == "07a08496c21b31f70f6f45ef731aa5f6b2522a6fc8f67f2d0a4c2b6fceda7a3f"
assert len(fixture["approvals"]) == 2
assert fixture["results"]["overall"] == "AWAITING_COUNTERPART"
assert fixture["manifest"]["input"]["comparison_input"]["freeze_state"] == "DRAFT_PRE_FREEZE"
assert fixture["manifest"]["input"]["comparison_input"]["comparison_boundary"]["expected_observation_is_not_a_decision_input"] is True

for token in [
    "approvalMatchesCurrent", "freezeEligibility", "exactApprovalPayload", "exactChangePayload",
    "StegVerseInterlockConnector", "buildInterlockRequest", "validateIntrReceipt",
    "stegverse.intr.hop_receipt/v1", "authority transfer prohibited",
    "StegVerseInterlockConnectorReady"
]:
    assert token in js, f"missing logic token: {token}"

assert "StegVerseEvaluatorReviewBridge" not in js, "legacy evaluator transport bridge must not remain in runtime JS"
assert re.search(r"disabled=!bridgeAvailable\(\"approve\"\)", html), "approval must fail closed without connector"
assert re.search(r"disabled=!bridgeAvailable\(\"requestChanges\"\)", html), "change request must fail closed without connector"

print("EVALUATOR_REVIEW_UI_STATIC_PASS")

assert fixture["test"]["version"] == 4
assert fixture["test"]["validation_state"] == "PASS"
assert fixture["source"]["source_blob_sha"] == "59d818a15fc7be732c97dae7d2174d8cfe9a7bab"
assert fixture["manifest"]["input"]["comparison_input"]["vector_schema"] == "stegverse.cross-framework-current-basis-vector.v0.4"
assert fixture["manifest"]["input"]["comparison_input"]["transition"]["changed_condition"] == "CURRENT_POLICY_BASIS_CHANGED"
assert fixture["manifest"]["input"]["comparison_input"]["transition"]["invalidation_asserted_as_input"] is False
assert fixture["manifest"]["input"]["comparison_input"]["comparison_boundary"]["primary_vector_does_not_assert_invalidation"] is True
assert fixture["manifest"]["input"]["comparison_input"]["comparison_boundary"]["current_standing_is_independently_determined"] is True
control_ids = [x["control_id"] for x in fixture["manifest"]["input"]["comparison_input"]["controls"]]
assert control_ids == ["VALID_CONTINUITY_CONTROL", "KNOWN_INVALIDATION_CONTROL"]
assert {x["party_id"] for x in fixture["approvals"]} == {"stegverse", "external-counterpart"}
assert fixture["executions"]["stegverse"]["status"] == "COMPLETE"
assert fixture["executions"]["stegverse"]["result"] == "DENY"
assert fixture["executions"]["stegverse"]["reason"] == "execution.authority_stale"
assert fixture["executions"]["counterpart"]["status"] == "NOT_RUN"
assert fixture["results"]["semantic_comparison_state"] == "PARTIAL_STEGVERSE_COMPLETE"
assert fixture["manifest"]["input"]["comparison_input"]["initial_state"]["receipt_state"] == "NOT_RECEIPT_BEARING_PRE_OBSERVATION"
assert fixture["manifest"]["input"]["comparison_input"]["transition"]["receipt_semantics"] == "S0_TO_S1_RECEIPT_IS_POST_OBSERVATION_EVIDENCE"
assert fixture["manifest"]["input"]["comparison_input"]["architecture_native_derivation"]["common_artifact_contains_native_currentness_booleans"] is False
assert fixture["manifest"]["input"]["comparison_input"]["comparison_boundary"]["transition_receipt_is_not_a_pre_execution_input"] is True
print("EVALUATOR_REVIEW_UI_V04_FROZEN_SYNC_PASS")

assert "transport_receipts" in contract
assert "ingress" in contract and "egress" in contract
assert "stegverse.evaluator_review.manifest_receipt_report.v1" in contract
assert "buildManifestReceiptReport" in js
assert "transport_receipts" in js
assert "ingressReceipt" in html and "egressReceipt" in html
print("EVALUATOR_REVIEW_MANIFEST_RECEIPT_REPORT_PASS")

connector = (ROOT / "assets/evaluator-intr-connector.js").read_text(encoding="utf-8")
projection = json.loads((ROOT / "data/evaluator-review/runtime-projection.json").read_text(encoding="utf-8"))
assert "x-stegverse-transport" in connector
assert "x-stegverse-payload-sha256" in connector
assert "credentials:\"omit\"" in connector
assert "__STEGVERSE_EVALUATOR_INTR_CONFIG__" in connector
assert "data/evaluator-review/runtime-projection.json" in connector
assert "StegVerseInterlockConnectorReady" in connector
assert "route_observation_digest" in connector
assert "SV002_PUBLIC_OBSERVE" in connector
assert "sv002_observe_endpoint" in connector
assert projection["schema"] == "stegverse.site.evaluator_intr_runtime_projection/v1"
assert projection["state"] == "BLOCKED" and projection["active"] is False
assert projection["endpoint"] is None and projection["readiness_endpoint"] is None
assert projection["authority_effect"] is False and projection["activation_effect"] is False
assert "assets/evaluator-intr-connector.js" in html
print("EVALUATOR_REVIEW_INTR_CONNECTOR_PASS")

assert fixture["executions"]["stegverse"]["manifest_receipt_id"] == "MR-C554125F385C65B7AA8303C10F076AD471CF864CF1DB2CC472FF771D8260F796"
assert fixture["executions"]["stegverse"]["transition_receipt_hash"] == "91410d8539e8225a6de77e6f299afafb5d813572c4fc2292a351ca56c0bc7c18"
print("EVALUATOR_REVIEW_V04_RESULT_PROJECTION_PASS")
