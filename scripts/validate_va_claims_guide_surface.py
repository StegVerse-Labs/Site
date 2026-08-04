#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "va-disability-claim-guide.html"
GUIDED = ROOT / "va-claims-guided-workflow.html"
CHAT = ROOT / "va-claims-chat.html"
STATE = ROOT / "data/va-claim-assistant/chat-capability-state.json"
OUT = ROOT / "data/va-claim-assistant/guide-surface-validation.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    guide = GUIDE.read_text(encoding="utf-8")
    guided = GUIDED.read_text(encoding="utf-8")
    chat = CHAT.read_text(encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    controls = state.get("controls", {})
    errors: list[str] = []

    require("Governed VA Claims Guide" in guide, "governed guide title missing", errors)
    require('href="va-claims-guided-workflow.html"' in guide, "guided workflow link missing from guide", errors)
    require("Try the step-by-step workflow" in guide, "top workflow invitation missing", errors)
    require("SOURCE_GROUNDED_ASSISTANT" in guide, "current capability missing", errors)
    require("Private document upload disabled" in guide, "upload disabled state missing", errors)
    require("Automated filing disabled" in guide, "filing disabled state missing", errors)
    require("Every material fact reviewed and confirmed" in guide, "material fact review gate missing", errors)
    require("Every claimed condition selected by the veteran" in guide, "condition selection gate missing", errors)
    require("Authorized VA or accredited-representative transport available" in guide, "authorized transport gate missing", errors)
    require("must not submit the claim" in guide, "fail-closed filing language missing", errors)

    require("Step-by-Step VA Claims Workflow" in guided, "guided page title missing", errors)
    require("Card 1 of 6" in guided and "Card 6 of 6" in guided, "guided card range incomplete", errors)
    require("Login.gov and ID.me are secure sign-in services" in guided, "sign-in services explanation missing", errors)
    require("Blue Button" in guided and "not a physical blue button" in guided, "Blue Button plain-language explanation missing", errors)
    require("Confirm and continue" in guided, "card confirmation controls missing", errors)
    require("advance.disabled=!checked(card)" in guided, "next-card completion lock missing", errors)
    require("The next card stays locked until you confirm" in guided, "veteran-confirmation rule missing", errors)
    require("https://www.va.gov/my-health/medical-records/download" in guided, "official medical-record link missing", errors)
    require("https://www.login.gov/help/creating-an-account/creating-an-account/" in guided, "official Login.gov help link missing", errors)

    require("Walk me through the cards" in chat, "guided chat entry missing", errors)
    require("confirm every task" in chat, "chat confirmation boundary missing", errors)
    require("A statement such as “done” does not automatically complete a card" in chat, "generic done rejection missing", errors)
    require("confirm all" in chat, "explicit card completion command missing", errors)
    require("Private document upload and automated claim filing remain disabled" in chat, "chat inactive capabilities boundary missing", errors)
    require("passwords, one-time security codes" in chat, "credential disclosure warning missing", errors)

    require(state.get("current_capability") == "SOURCE_GROUNDED_ASSISTANT", "state capability mismatch", errors)
    require(controls.get("private_document_upload_enabled") is False, "private upload unexpectedly enabled", errors)
    require(controls.get("automated_filing_enabled") is False, "automated filing unexpectedly enabled", errors)
    require(controls.get("veteran_submission_authority_preserved") is True, "veteran authority not preserved", errors)
    require(controls.get("human_review_required_before_filing") is True, "human review before filing not required", errors)
    require(controls.get("fail_closed_when_evidence_or_authority_missing") is True, "fail-closed control missing", errors)

    surfaces = [GUIDE, GUIDED, CHAT]
    body = {
        "schema_version": "1.1.0",
        "state": "PASS" if not errors else "FAIL",
        "surfaces": [path.name for path in surfaces],
        "capability_state": state.get("state"),
        "current_capability": state.get("current_capability"),
        "guided_card_count": 6,
        "card_advance_requires_veteran_confirmation": True,
        "private_document_upload_enabled": controls.get("private_document_upload_enabled"),
        "automated_filing_enabled": controls.get("automated_filing_enabled"),
        "veteran_submission_authority_preserved": controls.get("veteran_submission_authority_preserved"),
        "authority_effect": False,
        "activation_effect": False,
        "surface_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in surfaces},
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
