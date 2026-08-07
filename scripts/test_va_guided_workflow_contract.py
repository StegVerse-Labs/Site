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


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = False
        self.viewport = False
        self.step_ids: list[str] = []
        self.card_ids: list[str] = []
        self.buttons: list[str] = []
        self.links: list[str] = []
        self._button = False
        self._button_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html" and data.get("lang") == "en": self.lang = True
        if tag == "meta" and data.get("name") == "viewport": self.viewport = True
        if data.get("data-step"): self.step_ids.append(str(data["data-step"]))
        if data.get("data-card"): self.card_ids.append(str(data["data-card"]))
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

    require(gp.lang and wp.lang, "both user surfaces require lang=en", errors)
    require(gp.viewport and wp.viewport, "both user surfaces require mobile viewport", errors)
    require(gp.step_ids == ["1", "2", "3", "4", "5", "6"], "primary page requires six ordered steps", errors)
    require(wp.card_ids == ["1", "2", "3", "4", "5", "6"], "walkthrough requires six ordered cards", errors)
    require(sum(1 for text in gp.buttons if text.startswith("DONE")) == 6, "primary page requires six DONE buttons", errors)
    require(sum(1 for href in gp.links if href.startswith("va-claims-guided-workflow.html?step=")) == 6, "primary page requires six step-specific help links", errors)
    require(KEY in guide and KEY in guided, "shared completion state missing", errors)
    require("localStorage.setItem" in guide and "localStorage.setItem" in guided, "completion persistence write missing", errors)
    require("localStorage.getItem" in guide and "localStorage.getItem" in guided, "completion persistence read missing", errors)
    require("classList.toggle('done'" in guide, "primary completed-card visual state missing", errors)
    require("URLSearchParams" in guided and "params.get('step')" in guided, "focused step query routing missing", errors)
    require("Return to Instruction Page" in guided, "walkthrough return control missing", errors)
    require("Continue with help me complete this" in guided, "walkthrough continued-help control missing", errors)
    require("va-claims-chat.html?guided=1" in guided, "walkthrough must route to Claims Chat help", errors)
    require("https://www.va.gov/my-health/medical-records/download" in wp.links, "official VA records link missing", errors)
    require("https://secure.login.gov/sign_up/enter_email" in wp.links, "official Login.gov path missing", errors)
    require("get('guided')==='1'" in chat, "Claims Chat guided mode missing", errors)
    require("password" in chat.lower() and "one-time" in chat.lower(), "Claims Chat credential warning missing", errors)

    receipt = {
        "schema_version": "2.1.0",
        "state": "PASS" if not errors else "FAIL",
        "goal_id": "SV-VA-DUAL-FLOW-001",
        "task_id": "SV-VA-DF-VALIDATE-001",
        "design_contract": "PRIMARY_CHECKLIST_PLUS_FOCUSED_HELP",
        "primary_steps": gp.step_ids,
        "walkthrough_steps": wp.card_ids,
        "done_buttons": sum(1 for text in gp.buttons if text.startswith("DONE")),
        "step_help_links": sum(1 for href in gp.links if href.startswith("va-claims-guided-workflow.html?step=")),
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
