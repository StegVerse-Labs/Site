#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
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

    # Primary instruction page: all steps visible, persistent status, two actions.
    require("VA Claims Guide" in guide, "plain-language guide title missing", errors)
    require(len(re.findall(r'data-step="[1-6]"', guide)) == 6, "primary instruction page must expose six ordered steps", errors)
    require(guide.count("DONE") >= 6, "each primary step requires a DONE control", errors)
    require(guide.count("Help me with this") >= 6, "each primary step requires a Help me with this control", errors)
    require("va-claims-guided-workflow.html?step=" in guide, "step-addressable walkthrough links missing", errors)
    require("vaClaimsProgress" in guide, "shared progress storage key missing from primary page", errors)
    require("classList.toggle('complete'" in guide or "classList.toggle(\"complete\"" in guide, "completed-card dimming state missing", errors)
    require("Reset progress" in guide, "progress reset control missing", errors)
    require("Nothing is filed or submitted for you" in guide, "veteran-control boundary missing", errors)

    # Focused walkthrough: one selected step, return path, and continued help path.
    require("VA Claims Step-by-Step" in guided, "focused walkthrough title missing", errors)
    require(len(re.findall(r'data-card="[1-6]"', guided)) == 6, "focused walkthrough must contain six addressable step cards", errors)
    require("URLSearchParams" in guided and "step" in guided, "walkthrough query-step routing missing", errors)
    require("vaClaimsProgress" in guided, "shared progress storage key missing from walkthrough", errors)
    require("Return to Instruction Page" in guided, "return-to-instruction control missing", errors)
    require("Continue with help me complete this" in guided, "continued-help control missing", errors)
    require("va-claims-chat.html?guided=1" in guided, "step-specific Claims Chat continuation missing", errors)
    require("https://www.va.gov/my-health/medical-records/download" in guided, "official VA records link missing", errors)
    require("https://www.login.gov/help/creating-an-account/creating-an-account/" in guided, "official Login.gov help link missing", errors)

    # Chat remains a separate help surface with credential and authority boundaries.
    require("guided=1" in chat, "Claims Chat guided query mode missing", errors)
    require("password" in chat.lower() and "one-time" in chat.lower(), "Claims Chat credential boundary missing", errors)

    # Existing capability controls remain fail-closed even though they are not displayed as user-facing jargon.
    require(state.get("current_capability") == "SOURCE_GROUNDED_ASSISTANT", "state capability mismatch", errors)
    require(controls.get("private_document_upload_enabled") is False, "private upload unexpectedly enabled", errors)
    require(controls.get("automated_filing_enabled") is False, "automated filing unexpectedly enabled", errors)
    require(controls.get("veteran_submission_authority_preserved") is True, "veteran authority not preserved", errors)
    require(controls.get("human_review_required_before_filing") is True, "human review before filing not required", errors)
    require(controls.get("fail_closed_when_evidence_or_authority_missing") is True, "fail-closed control missing", errors)

    surfaces = [GUIDE, GUIDED, CHAT]
    body = {
        "schema_version": "2.0.0",
        "state": "PASS" if not errors else "FAIL",
        "design_contract": "PRIMARY_CHECKLIST_PLUS_FOCUSED_HELP",
        "surfaces": [path.name for path in surfaces],
        "primary_steps": 6,
        "focused_steps": 6,
        "shared_progress_key": "vaClaimsProgress",
        "capability_state": state.get("state"),
        "current_capability": state.get("current_capability"),
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
