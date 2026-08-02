#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data/va-claim-assistant/chat-capability-state.json"
PAGE_PATH = ROOT / "va-claims-chat.html"
RECEIPT_PATH = ROOT / "data/va-claim-assistant/chat-surface-validation.json"

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
page = PAGE_PATH.read_text(encoding="utf-8")

errors = []
required_state = {
    "state": "SOURCE_GROUNDED_ACTIVE",
    "current_capability": "SOURCE_GROUNDED_ASSISTANT",
}
for key, expected in required_state.items():
    if state.get(key) != expected:
        errors.append(f"{key}_must_equal_{expected}")

controls = state.get("controls", {})
for key in ("private_document_upload_enabled", "automated_filing_enabled", "public_upload_enabled"):
    if controls.get(key) is not False:
        errors.append(f"{key}_must_be_false")
for key in ("veteran_submission_authority_preserved", "human_review_required_before_filing", "fail_closed_when_evidence_or_authority_missing"):
    if controls.get(key) is not True:
        errors.append(f"{key}_must_be_true")

for key, value in state.get("authority", {}).items():
    if value is not False:
        errors.append(f"authority_{key}_must_be_false")

required_page_tokens = [
    "Governed VA Claims Chat",
    "SOURCE_GROUNDED_ASSISTANT",
    "Upload documents — not yet active",
    "Prepare or file claim — not yet active",
    "Veteran confirms every material fact",
    "Veteran selects every claimed condition",
    "Exact, unexpired package authorization",
    "does not target or predict a percentage",
]
for token in required_page_tokens:
    if token not in page:
        errors.append("missing_page_token:" + token)

if 'type="button" disabled>Upload documents — not yet active' not in page:
    errors.append("document_upload_control_must_be_disabled")
if 'type="button" disabled>Prepare or file claim — not yet active' not in page:
    errors.append("filing_control_must_be_disabled")

state_sha = hashlib.sha256(STATE_PATH.read_bytes()).hexdigest()
page_sha = hashlib.sha256(PAGE_PATH.read_bytes()).hexdigest()
receipt = {
    "schema_version": "1.0.0",
    "surface": "va-claims-chat.html",
    "state": "PASS" if not errors else "FAIL",
    "capability_state": state.get("state"),
    "current_capability": state.get("current_capability"),
    "private_document_upload_enabled": controls.get("private_document_upload_enabled"),
    "automated_filing_enabled": controls.get("automated_filing_enabled"),
    "veteran_submission_authority_preserved": controls.get("veteran_submission_authority_preserved"),
    "authority_effect": False,
    "activation_effect": False,
    "state_sha256": state_sha,
    "page_sha256": page_sha,
    "errors": errors,
}
canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
receipt["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2, sort_keys=True))
if errors:
    raise SystemExit(1)
