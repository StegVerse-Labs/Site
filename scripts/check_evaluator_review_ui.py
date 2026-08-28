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
assert "public Site route for this UI: NOT YET OBSERVED" in handoff
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
