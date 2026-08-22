#!/usr/bin/env python3
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "va-disability-claim-guide.html"
GUIDED = ROOT / "va-claims-guided-workflow.html"
CHAT = ROOT / "va-claims-chat.html"
OUT = ROOT / "data/va-claim-assistant/guided-workflow-contract-validation.json"
KEY = "vaClaimsStepStateV1"
FALLBACK = "https://www.va.gov/disability/file-disability-claim-form-21-526ez/veteran-information"


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = False
        self.viewport = False
        self.step_ids: list[str] = []
        self.card_ids: list[str] = []
        self.buttons: list[str] = []
        self.links: list[str] = []
        self.help_targets: list[str] = []
        self._button = False
        self._button_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html" and data.get("lang") == "en": self.lang = True
        if tag == "meta" and data.get("name") == "viewport": self.viewport = True
        if data.get("data-step"): self.step_ids.append(str(data["data-step"]))
        if data.get("data-card"): self.card_ids.append(str(data["data-card"]))
        if data.get("data-help-target"): self.help_targets.append(str(data["data-help-target"]))
        if tag == "a" and data.get("href"): self.links.append(str(data["href"]))
        if tag == "button": self._button, self._button_text = True, []

    def handle_data(self, data: str) -> None:
        if self._button: self._button_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "button" and self._button:
            self.buttons.append(" ".join("".join(self._button_text).split()))
            self._button = False


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition: errors.append(message)


def main() -> int:
    guide = GUIDE.read_text(encoding="utf-8")
    guided = GUIDED.read_text(encoding="utf-8")
    chat = CHAT.read_text(encoding="utf-8")
    gp = SurfaceParser(); gp.feed(guide)
    wp = SurfaceParser(); wp.feed(guided)
    errors: list[str] = []

    help_links = sum(1 for href in gp.links if href.startswith("va-claims-guided-workflow.html?step="))

    require(gp.lang and wp.lang, "both user surfaces require lang=en", errors)
    require(gp.viewport and wp.viewport, "both user surfaces require mobile viewport", errors)
    require(gp.step_ids == ["1", "2", "3", "4", "5", "6"], "primary page requires six ordered steps", errors)
    require(wp.card_ids == ["1", "2", "3", "4", "5", "6"], "walkthrough requires six ordered cards", errors)
    require(sum(1 for text in gp.buttons if text.startswith("DONE")) == 6, "primary page requires six DONE buttons", errors)
    require(help_links >= 4, "primary page requires focused walkthrough help links", errors)
    require(gp.help_targets == ["step-1-help"], "step 1 requires inline expandable readiness help", errors)
    require(KEY in guide and KEY in guided, "shared completion state missing", errors)
    require("localStorage.setItem" in guide and "localStorage.setItem" in guided, "completion persistence write missing", errors)
    require("localStorage.getItem" in guide and "localStorage.getItem" in guided, "completion persistence read missing", errors)
    require("classList.toggle('done'" in guide, "primary completed-card visual state missing", errors)
    require("const requirements={" in guide and "function ready(step)" in guide, "per-step completion gate missing", errors)
    require('id="step-1-email"' in guide and 'id="step-1-phone"' in guide and 'id="step-1-id"' in guide, "step 1 three-item readiness gate missing", errors)
    require('id="step-2-account-created"' in guide and 'id="step-2-va-login-success"' in guide, "step 2 confirmations missing", errors)
    require('id="step-3-reached-download"' in guide, "step 3 page-arrival confirmation missing", errors)
    require('id="step-4-downloaded"' in guide, "step 4 download confirmation missing", errors)
    require('id="step-5-found-file"' in guide, "step 5 file-location confirmation missing", errors)
    require('id="step-6-packet-ready"' in guide and 'id="step-6-submitted"' in guide, "step 6 final packet/submission confirmations missing", errors)
    require(FALLBACK in gp.links, "primary VA.gov 21-526EZ fallback link missing", errors)
    require("URLSearchParams" in guided and "params.get('step')" in guided, "focused step query routing missing", errors)
    require("Return to Instruction Page" in guided, "walkthrough return control missing", errors)
    require("Continue with help me complete this" in guided, "walkthrough continued-help control missing", errors)
    require("va-claims-chat.html?guided=1" in guided, "walkthrough must route to Claims Chat help", errors)
    require("https://www.va.gov/sign-in/" in wp.links, "official VA.gov sign-in path missing", errors)
    require("https://www.va.gov/my-health/medical-records/download" in wp.links, "official VA records link missing", errors)
    require("https://mobile.va.gov/app/va-health-and-benefits" in wp.links, "official VA app path missing", errors)
    require(FALLBACK in wp.links, "walkthrough VA.gov 21-526EZ fallback link missing", errors)

    # The compatibility/deep-work chat intentionally moved to the veteran-first
    # minimal conversational contract on 2026-08-21. Validate that contract rather
    # than the superseded query/card presentation markers.
    require("What can I help you with?" in chat, "Claims Chat veteran-first primary prompt missing", errors)
    require("Ask a VA claims question in your own words" in chat, "Claims Chat ordinary-language guidance missing", errors)
    require(chat.count("data-prompt=") >= 4, "Claims Chat common one-tap starting points missing", errors)
    require('id="question"' in chat and 'placeholder="Ask a VA claims question' in chat, "Claims Chat free-text composer missing", errors)
    require("one step at a time" in chat.lower(), "Claims Chat step-by-step help contract missing", errors)
    require("don’t enter passwords, security codes, Social Security numbers, or full medical records here" in chat, "Claims Chat plain-language privacy warning missing", errors)
    require("const cards=[" in chat and chat.count("{title:") >= 6, "Claims Chat bounded six-step deep-work support missing", errors)
    require("vaClaimsChatCard" in chat, "Claims Chat local guided-progress continuity missing", errors)
    require("VAClaimsRuntimeBridge" in chat, "Claims Chat governed runtime bridge hook missing", errors)
    require("function localAnswer" in chat, "Claims Chat bounded local fallback missing", errors)
    require("https://www.va.gov/sign-in/" in chat, "Claims Chat official VA.gov sign-in path missing", errors)
    require("https://www.va.gov/my-health/medical-records/download" in chat, "Claims Chat official VA records path missing", errors)
    require("official VA.gov disability claim form" in chat, "Claims Chat final VA.gov submission fallback guidance missing", errors)
    require("Never share your password or one-time security code" in chat, "Claims Chat credential warning missing", errors)

    receipt = {
        "schema_version": "2.5.0",
        "state": "PASS" if not errors else "FAIL",
        "goal_id": "SV-VA-DUAL-FLOW-001",
        "task_id": "SV-VA-DF-VALIDATE-001",
        "design_contract": "SIX_STEP_GUIDE_WITH_VETERAN_FIRST_MINIMAL_CONVERSATIONAL_CHAT",
        "primary_steps": gp.step_ids,
        "walkthrough_steps": wp.card_ids,
        "done_buttons": sum(1 for text in gp.buttons if text.startswith("DONE")),
        "step_help_links": help_links,
        "inline_help_targets": gp.help_targets,
        "step_done_requirements": {
            "1": ["email", "smartphone_browser", "government_photo_id"],
            "2": ["account_created_or_confirmed", "va_login_success"],
            "3": ["reached_medical_record_download_page"],
            "4": ["all_time_all_records_pdf_or_txt_downloaded"],
            "5": ["downloaded_file_located"],
            "6": ["final_claim_packet_ready", "va_submission_confirmed"],
        },
        "fallback_submission_url": FALLBACK,
        "fallback_active_until_authorized_connected_submission": True,
        "shared_progress_key": KEY,
        "mobile_viewport": gp.viewport and wp.viewport,
        "language_declared": gp.lang and wp.lang,
        "authority_effect": False,
        "activation_effect": False,
        "errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
