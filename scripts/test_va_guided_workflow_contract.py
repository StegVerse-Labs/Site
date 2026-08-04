#!/usr/bin/env python3
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDED = ROOT / "va-claims-guided-workflow.html"
CHAT = ROOT / "va-claims-chat.html"
OUT = ROOT / "data/va-claim-assistant/guided-workflow-contract-validation.json"


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.cards: list[str] = []
        self.inputs = 0
        self.labels = 0
        self.buttons = 0
        self.links: list[str] = []
        self.viewport = False
        self.lang = False
        self._current_card: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html" and data.get("lang") == "en":
            self.lang = True
        if tag == "meta" and data.get("name") == "viewport":
            self.viewport = True
        if tag == "section" and data.get("data-card"):
            self.cards.append(str(data["data-card"]))
        if tag == "input" and data.get("type") == "checkbox":
            self.inputs += 1
        if tag == "label":
            self.labels += 1
        if tag == "button":
            self.buttons += 1
        if tag == "a" and data.get("href"):
            self.links.append(str(data["href"]))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    guided = GUIDED.read_text(encoding="utf-8")
    chat = CHAT.read_text(encoding="utf-8")
    parser = ContractParser()
    parser.feed(guided)
    errors: list[str] = []

    require(parser.lang, "guided page language declaration missing", errors)
    require(parser.viewport, "mobile viewport declaration missing", errors)
    require(parser.cards == ["1", "2", "3", "4", "5", "6"], "six ordered guidance cards required", errors)
    require(parser.inputs >= 18, "expected completion checkboxes are missing", errors)
    require(parser.labels >= parser.inputs, "every checkbox must be contained in or associated with a label", errors)
    require(parser.buttons >= 11, "back, next, and finish controls are incomplete", errors)
    require("@media(max-width:840px)" in guided, "mobile single-column layout contract missing", errors)
    require("button[disabled]" in guided, "visible disabled-state styling missing", errors)
    require("advance.disabled=!checked(card)" in guided, "next-card lock is not bound to all completion checks", errors)
    require("if(checked(card)&&current<cards.length-1)" in guided, "next transition does not fail closed", errors)
    require("localStorage.setItem('vaGuidedCard'" in guided, "resume-point persistence missing", errors)
    require("vaGuidedComplete" in guided, "completion persistence missing", errors)
    require("Never share your password or one-time security code" in guided, "credential warning missing", errors)
    require("will not post sensitive medical records publicly" in guided, "public-record warning missing", errors)
    require("va-claims-chat.html?guided=1&card=" in guided, "card-specific Claims Chat links missing", errors)
    require("https://www.va.gov/my-health/medical-records/download" in parser.links, "official VA records link missing", errors)
    require("https://www.login.gov/help/creating-an-account/creating-an-account/" in parser.links, "official Login.gov help link missing", errors)

    require("guided=1" in chat, "Claims Chat guided query mode missing", errors)
    require("generic" in chat.lower() and "done" in chat.lower(), "generic done rejection language missing", errors)
    require("current card" in chat.lower(), "current-card context language missing", errors)
    require("password" in chat.lower() and "one-time" in chat.lower(), "Claims Chat credential boundary missing", errors)

    state = "PASS" if not errors else "FAIL"
    receipt = {
        "schema_version": "1.0.0",
        "state": state,
        "goal_id": "SV-VA-GUIDED-CARDS-001",
        "task_id": "SV-VA-GC-008",
        "guided_surface": GUIDED.name,
        "chat_surface": CHAT.name,
        "cards_observed": parser.cards,
        "checkboxes_observed": parser.inputs,
        "labels_observed": parser.labels,
        "buttons_observed": parser.buttons,
        "mobile_viewport": parser.viewport,
        "language_declared": parser.lang,
        "authority_effect": False,
        "activation_effect": False,
        "errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if state == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
