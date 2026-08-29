#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "evaluator-review.html").read_text(encoding="utf-8")
js = (ROOT / "assets/evaluator-review.js").read_text(encoding="utf-8")
fixture = json.loads((ROOT / "data/evaluator-review/cross-framework-current-basis-001.json").read_text(encoding="utf-8"))
handoff = (ROOT / "docs/EVALUATOR_REVIEW_UI_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
contract = (ROOT / "docs/EVALUATOR_REVIEW_API_CONTRACT.md").read_text(encoding="utf-8")
task = json.loads((ROOT / "data/tasks/SITE-EVALUATOR-MANIFEST-REVIEW-575.json").read_text(encoding="utf-8"))

required_html = [
    "What are we testing?", "Test vector", "Frozen inputs", "Observable outputs",
    "Pass / fail interpretation", "Expected observation is not a decision input",
    "Evidence requirements", "Discussion / review", "Approval state", "Execution",
    "Results comparison", "View raw manifest", "Revision history",
    "Provenance / advanced details", "Request changes", "Approve this version",
    "viewport-fit=cover"
]
for token in required_html:
    assert token in html, f"missing evaluator UI token: {token}"

assert "@media(max-width:680px)" in html
assert "overflow-wrap:anywhere" in html
assert "window.StegVerseEvaluatorReviewBridge" in contract
assert "TV/TVC" in contract and "Master Records" in contract
assert "DRAFT_PRE_FREEZE" in handoff
assert task["state"] == "COMPLETE_VALIDATED_MERGED_PUBLICLY_OBSERVED"
assert "public Site route for this UI: OBSERVED" in handoff
assert fixture["review_schema"] == "stegverse.evaluator-review.v1"
assert fixture["test"]["state"] == "DRAFT"
assert fixture["test"]["execution_state"] == "NOT_RUN"
assert fixture["test"]["frozen_manifest_hash"] is None
assert fixture["approvals"] == []
assert fixture["results"] is None
assert fixture["manifest"]["input"]["input_data"]["freeze_state"] == "DRAFT_PRE_FREEZE"
assert fixture["manifest"]["input"]["input_data"]["comparison_boundary"]["expected_observation_is_not_a_decision_input"] is True

for token in ["approvalMatchesCurrent", "freezeEligibility", "exactApprovalPayload", "exactChangePayload", "authorized StegVerse review runtime"]:
    assert token in js, f"missing logic token: {token}"

assert re.search(r"disabled=!bridgeAvailable\(\"approve\"\)", html), "approval must fail closed without bridge"
assert re.search(r"disabled=!bridgeAvailable\(\"requestChanges\"\)", html), "change request must fail closed without bridge"

print("EVALUATOR_REVIEW_UI_STATIC_PASS")

assert fixture["test"]["version"] == 2
assert fixture["test"]["validation_state"] == "PASS"
assert fixture["source"]["source_blob_sha"] == "2dd0468779975d18ad53dfe400e1d2fcf83650c3"
assert fixture["manifest"]["input"]["input_data"]["vector_schema"] == "stegverse.cross-framework-current-basis-vector.v0.2"
assert fixture["manifest"]["input"]["input_data"]["transition"]["changed_condition"] == "CURRENT_POLICY_BASIS_CHANGED"
assert fixture["manifest"]["input"]["input_data"]["transition"]["invalidation_asserted_as_input"] is False
assert fixture["manifest"]["input"]["input_data"]["comparison_boundary"]["primary_vector_does_not_assert_invalidation"] is True
assert fixture["manifest"]["input"]["input_data"]["comparison_boundary"]["current_standing_is_independently_determined"] is True
control_ids = [x["control_id"] for x in fixture["manifest"]["input"]["input_data"]["controls"]]
assert control_ids == ["VALID_CONTINUITY_CONTROL", "KNOWN_INVALIDATION_CONTROL"]
assert fixture["approvals"] == [] and fixture["results"] is None
print("EVALUATOR_REVIEW_UI_V02_SYNC_PASS")
