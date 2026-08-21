#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data/va-claim-assistant/chat-capability-state.json"
PROJECTION_PATH = ROOT / "api/va-claim-assistant/runtime-projection.json"
PAGE_PATH = ROOT / "va-claims-chat.html"
BRIDGE_PATH = ROOT / "assets/va-claims-chat-runtime.js"
RECEIPT_PATH = ROOT / "data/va-claim-assistant/chat-surface-validation.json"

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
projection = json.loads(PROJECTION_PATH.read_text(encoding="utf-8"))
page = PAGE_PATH.read_text(encoding="utf-8")
bridge = BRIDGE_PATH.read_text(encoding="utf-8")

errors = []
controls = state.get("controls", {})

for key in ("private_document_upload_enabled", "automated_filing_enabled", "public_upload_enabled"):
    if controls.get(key) is not False:
        errors.append(f"{key}_must_be_false")
for key in (
    "veteran_submission_authority_preserved",
    "human_review_required_before_filing",
    "fail_closed_when_evidence_or_authority_missing",
):
    if controls.get(key) is not True:
        errors.append(f"{key}_must_be_true")
for key, value in state.get("authority", {}).items():
    if value is not False:
        errors.append(f"authority_{key}_must_be_false")

projection_active = projection.get("state") == "VERIFIED" and projection.get("active") is True
if projection_active:
    if projection.get("capability") != "COORDINATED_VA_RESOURCES_LLM":
        errors.append("active_projection_capability_mismatch")
    if not isinstance(projection.get("endpoint"), str) or not projection["endpoint"].startswith("https://"):
        errors.append("active_projection_requires_https_endpoint")
    if projection.get("custody_state") != "RECORDED":
        errors.append("active_projection_requires_custody_recorded")
    if projection.get("reconstruction_state") != "PASS":
        errors.append("active_projection_requires_reconstruction_pass")
else:
    if state.get("state") != "SOURCE_GROUNDED_ACTIVE":
        errors.append("inactive_runtime_requires_source_grounded_state")
    if state.get("current_capability") != "SOURCE_GROUNDED_ASSISTANT":
        errors.append("inactive_runtime_requires_source_grounded_capability")
    if projection.get("active") is not False:
        errors.append("blocked_projection_must_not_be_active")
    if projection.get("endpoint") is not None:
        errors.append("blocked_projection_endpoint_must_be_null")

for key in (
    "private_document_upload_active",
    "private_document_retrieval_active",
    "filing_active",
    "authority_effect",
    "activation_effect",
):
    if projection.get(key) is not False:
        errors.append(f"projection_{key}_must_be_false")

required_page_tokens = [
    "VA Claims Chat",
    "What can I help you with?",
    "Ask a VA claims question in your own words",
    "Start a disability claim",
    "What evidence do I need?",
    "Get my VA records",
    "Understand a VA decision",
    "va-claims-chat-runtime.js",
    "For your privacy",
]
for token in required_page_tokens:
    if token not in page:
        errors.append("missing_page_token:" + token)

# Public UI must stay user-facing. Runtime/governance state belongs in machine-readable
# artifacts and receipts, not in labels a veteran must interpret.
for forbidden in (
    "Current capability:",
    "SOURCE-GROUNDED PROCEDURAL HELP",
    "COORDINATED VA RESOURCES LLM",
    "Choose how to use Claims Chat",
    "Confirmation rule",
    "Document safety gate",
    "Unsupported routes remain fail-closed",
):
    if forbidden in page:
        errors.append("technical_or_internal_ui_token_present:" + forbidden)

if 'type="file"' in page.lower():
    errors.append("public_document_upload_control_must_be_absent")
if "<form" in page.lower() and "file" in page.lower():
    errors.append("filing_or_upload_form_must_not_be_exposed")

required_bridge_tokens = [
    "validActiveProjection",
    "runtime_not_verified",
    "ADMITTED_OFFICIAL_VA_ONLY",
    "private_document_context:false",
    "filing_requested:false",
    "authority_escalation_rejected",
]
for token in required_bridge_tokens:
    if token not in bridge:
        errors.append("missing_bridge_token:" + token)

state_sha = hashlib.sha256(STATE_PATH.read_bytes()).hexdigest()
projection_sha = hashlib.sha256(PROJECTION_PATH.read_bytes()).hexdigest()
page_sha = hashlib.sha256(PAGE_PATH.read_bytes()).hexdigest()
bridge_sha = hashlib.sha256(BRIDGE_PATH.read_bytes()).hexdigest()
receipt = {
    "schema_version": "3.0.0",
    "surface": "va-claims-chat.html",
    "state": "PASS" if not errors else "FAIL",
    "surface_policy": "VETERAN_FIRST_MINIMAL_UI",
    "capability_state": state.get("state"),
    "current_capability": state.get("current_capability"),
    "runtime_projection_state": projection.get("state"),
    "coordinated_llm_active": projection_active,
    "private_document_upload_enabled": controls.get("private_document_upload_enabled"),
    "automated_filing_enabled": controls.get("automated_filing_enabled"),
    "veteran_submission_authority_preserved": controls.get("veteran_submission_authority_preserved"),
    "authority_effect": False,
    "activation_effect": False,
    "state_sha256": state_sha,
    "projection_sha256": projection_sha,
    "page_sha256": page_sha,
    "bridge_sha256": bridge_sha,
    "errors": errors,
}
canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
receipt["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2, sort_keys=True))
if errors:
    raise SystemExit(1)
