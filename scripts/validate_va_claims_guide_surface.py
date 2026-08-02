#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "va-disability-claim-guide.html"
STATE = ROOT / "data/va-claim-assistant/chat-capability-state.json"
OUT = ROOT / "data/va-claim-assistant/guide-surface-validation.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    controls = state.get("controls", {})
    errors: list[str] = []

    require("Governed VA Claims Guide" in page, "governed guide title missing", errors)
    require('href="va-claims-chat.html"' in page, "native claims chat link missing", errors)
    require("SOURCE_GROUNDED_ASSISTANT" in page, "current capability missing", errors)
    require("Private document upload disabled" in page, "upload disabled state missing", errors)
    require("Automated filing disabled" in page, "filing disabled state missing", errors)
    require("Submission authority remains with the veteran" in page, "veteran authority statement missing", errors)
    require("Every material fact reviewed and confirmed" in page, "material fact review gate missing", errors)
    require("Every claimed condition selected by the veteran" in page, "condition selection gate missing", errors)
    require("Exact package hash generated" in page, "exact package hash gate missing", errors)
    require("Authorized VA or accredited-representative transport available" in page, "authorized transport gate missing", errors)
    require("must not submit the claim" in page, "fail-closed filing language missing", errors)
    require("ChatGPT file uploads" not in page, "legacy ChatGPT upload framing remains", errors)

    require(state.get("current_capability") == "SOURCE_GROUNDED_ASSISTANT", "state capability mismatch", errors)
    require(controls.get("private_document_upload_enabled") is False, "private upload unexpectedly enabled", errors)
    require(controls.get("automated_filing_enabled") is False, "automated filing unexpectedly enabled", errors)
    require(controls.get("veteran_submission_authority_preserved") is True, "veteran authority not preserved", errors)
    require(controls.get("human_review_required_before_filing") is True, "human review before filing not required", errors)
    require(controls.get("fail_closed_when_evidence_or_authority_missing") is True, "fail-closed control missing", errors)

    body = {
        "schema_version": "1.0.1",
        "state": "PASS" if not errors else "FAIL",
        "surface": PAGE.name,
        "capability_state": state.get("state"),
        "current_capability": state.get("current_capability"),
        "private_document_upload_enabled": controls.get("private_document_upload_enabled"),
        "automated_filing_enabled": controls.get("automated_filing_enabled"),
        "veteran_submission_authority_preserved": controls.get("veteran_submission_authority_preserved"),
        "human_review_required_before_filing": controls.get("human_review_required_before_filing"),
        "fail_closed_when_evidence_or_authority_missing": controls.get("fail_closed_when_evidence_or_authority_missing"),
        "authority_effect": False,
        "activation_effect": False,
        "page_sha256": hashlib.sha256(PAGE.read_bytes()).hexdigest(),
        "state_sha256": hashlib.sha256(STATE.read_bytes()).hexdigest(),
        "errors": errors,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
