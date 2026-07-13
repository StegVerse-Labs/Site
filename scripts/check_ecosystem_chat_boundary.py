#!/usr/bin/env python3
"""Verify Ecosystem Chat public boundary, single-entry UX, transition intents, continuation panel, and preview telemetry alignment."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UX_STATUS_PATH = ROOT / "docs" / "ECOSYSTEM_CHAT_UX_STATUS.md"
INTENT_CATALOG_PATH = ROOT / "data" / "ecosystem-chat-transition-intents.json"
TASK_PATH = ROOT / "data" / "headless-tasks" / "ecosystem-chat-boundary-check-v1.json"
REGISTRY_PATH = ROOT / "data" / "headless-task-registry-v1.json"
JSON_FIXTURES = [ROOT / "fixtures" / "ecosystem-chat" / "request.example.json", ROOT / "fixtures" / "ecosystem-chat" / "response.example.json", ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json", INTENT_CATALOG_PATH]
TEXT_FILES = [ROOT / "README.md", ROOT / "ecosystem-chat.html", ROOT / "assets" / "ecosystem-chat.js", ROOT / "docs" / "ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md", ROOT / "docs" / "ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md", ROOT / "docs" / "ECOSYSTEM_CHAT_BOUNDARY_CHECK.md", ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", UX_STATUS_PATH]
INTERACTION_BANDS = ["intra", "inter", "research", "provider", "solver", "receipt"]
TRANSITION_INTENTS = ["explain", "demonstrate", "compare", "research", "build", "replay", "runtime", "formalism", "sdk", "implementation", "solver"]
REQUIRED_TEXT = ["raw_shell_allowed", "authority_required", "rate_limit_required", "receipt_required_for_execution", "Restricted admin"]
REQUIRED_BOUNDARY_TEXT = ["shell", "credential", "receipt", "authority"]
REQUIRED_PAGE_LINKS = ["docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md", "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md", "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md"]
REQUIRED_README_REFERENCES = ["docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md", "scripts/check_ecosystem_chat_boundary.py", "scripts/check_ecosystem_chat_contract.py", "data/headless-tasks/ecosystem-chat-boundary-check-v1.json", "data/headless-task-registry-v1.json", "python scripts/check_ecosystem_chat_contract.py", "python scripts/check_ecosystem_chat_boundary.py"]
REQUIRED_TASK_INPUTS = ["README.md", "ecosystem-chat.html", "assets/ecosystem-chat.js", "data/ecosystem-chat-transition-intents.json", "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md", "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md", "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md", "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", "docs/ECOSYSTEM_CHAT_UX_STATUS.md", "fixtures/ecosystem-chat/request.example.json", "fixtures/ecosystem-chat/response.example.json", "fixtures/ecosystem-chat/sdk-form-payload.example.json", "scripts/check_ecosystem_chat_boundary.py", "scripts/check_ecosystem_chat_contract.py", "data/headless-tasks/ecosystem-chat-boundary-check-v1.json", "data/headless-task-registry-v1.json"]
REQUIRED_ACTIVATION_STATUS_TEXT = ["No-shell boundary state: installed", "No-credential boundary state: installed", "Restricted-admin routing state: installed", "Boundary verifier state: installed", "Declared task state: installed", "Registry state: installed", "Contract check state: installed and aligned with boundary task", "scripts/check_ecosystem_chat_contract.py\n  -> confirms", "scripts/check_ecosystem_chat_boundary.py\n  -> confirms", "data/headless-tasks/ecosystem-chat-boundary-check-v1.json\n  -> declares", "data/headless-task-registry-v1.json\n  -> keeps ecosystem-chat-boundary-check-v1 active.", "Backend gateway state: not installed", "Authority-issued receipt state: not installed"]
REQUIRED_UX_STATUS_TEXT = ["UX contract: single-primary-governed-chat-preview-entry", "Primary: Try the governed chat preview -> #console", "Secondary: How the boundary works -> #how-it-works", "multi-entry console", "task launcher", "repo control panel", "python scripts/run_site_task.py validate"]
REQUIRED_SINGLE_ENTRY_TEXT = ["Try the governed chat preview", "How the boundary works", "Technical preview details", "This page has one public purpose", "It is a governed chat preview, not a shell, not a repo control panel, not a proof issuer, and not the full product."]
FORBIDDEN_PRIMARY_ENTRY_TEXT = ["Open SDK form", "Open console", "View guardrails", "Gateway contract target"]


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(path: Path, needles: list[str]) -> None:
    body = read_text(path)
    missing = [needle for needle in needles if needle not in body]
    if missing:
        raise AssertionError(f"{path.relative_to(ROOT)} missing required text: {', '.join(missing)}")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def verify_single_entry_ux() -> None:
    page = read_text(ROOT / "ecosystem-chat.html")
    missing = [text for text in REQUIRED_SINGLE_ENTRY_TEXT if text not in page]
    if missing:
        raise AssertionError(f"ecosystem-chat.html missing single-entry UX text: {', '.join(missing)}")
    forbidden = [text for text in FORBIDDEN_PRIMARY_ENTRY_TEXT if text in page]
    if forbidden:
        raise AssertionError(f"ecosystem-chat.html restored old competing primary entry text: {', '.join(forbidden)}")
    primary_buttons = re.findall(r'<(?:a|button)\b[^>]*class="[^"]*\bsv-btn-primary\b[^"]*"', page)
    if len(primary_buttons) != 2:
        raise AssertionError("ecosystem-chat.html must keep exactly two primary actions: hero entry and chat submit")
    hero_start = page.find('<div class="sv-hero">')
    boundary_start = page.find('<div class="sv-boundary">', hero_start)
    if hero_start < 0 or boundary_start < 0:
        raise AssertionError("ecosystem-chat.html missing hero/boundary structure")
    hero = page[hero_start:boundary_start]
    hero_buttons = re.findall(r'<a\b[^>]*class="[^"]*\bsv-btn\b[^"]*"', hero)
    if len(hero_buttons) != 2 or 'href="#console"' not in hero or 'href="#how-it-works"' not in hero:
        raise AssertionError("ecosystem-chat.html hero must point only to chat preview and boundary explanation")
    if '<details class="simple-card" id="technical-details">' not in page:
        raise AssertionError("ecosystem-chat.html must keep SDK/gateway details collapsible")


def verify_interaction_band_surface() -> None:
    page = read_text(ROOT / "ecosystem-chat.html")
    script = read_text(ROOT / "assets" / "ecosystem-chat.js")
    for needle in ["Ecosystem LLM routing bands", "Math solver", "INTRA", "INTER", "RESEARCH", "PROVIDER", "SOLVER", "RECEIPT", 'id="interactionBandMeter"']:
        if needle not in page:
            raise AssertionError(f"ecosystem-chat.html missing interaction-band surface text: {needle}")
    for needle in ["INTERACTION_BANDS", "calculateInteractionProfile", "renderInteractionBands", "interaction_profile", "interaction_bands", "math_solver_supported"]:
        if needle not in script:
            raise AssertionError(f"assets/ecosystem-chat.js missing telemetry code: {needle}")
    for band in INTERACTION_BANDS:
        if f'"{band}"' not in page and f"'{band}'" not in script:
            raise AssertionError(f"interaction band {band!r} missing from page/script")
        if f'"{band}"' not in script and f"'{band}'" not in script:
            raise AssertionError(f"interaction band {band!r} missing from JavaScript classifier")


def verify_transition_intent_engine() -> None:
    catalog = load_json(INTENT_CATALOG_PATH)
    if catalog.get("schema") != "stegverse.site.transition_intents.v0.1":
        raise AssertionError("transition intent catalog schema drift")
    if catalog.get("mode") != "local_preview_only" or catalog.get("authority") != "none":
        raise AssertionError("transition intent catalog must remain local_preview_only with authority none")
    intents = catalog.get("intents")
    if not isinstance(intents, list):
        raise AssertionError("transition intent catalog must declare intents list")
    ids = [intent.get("id") for intent in intents if isinstance(intent, dict)]
    missing = [intent for intent in TRANSITION_INTENTS if intent not in ids]
    if missing:
        raise AssertionError("transition intent catalog missing ids: " + ", ".join(missing))
    script = read_text(ROOT / "assets" / "ecosystem-chat.js")
    for needle in ["TRANSITION_INTENTS", "classifyTransitionIntent", "transition_intent", "transition_destination", "Suggested transition:", "Transition boundary:"]:
        if needle not in script:
            raise AssertionError(f"assets/ecosystem-chat.js missing transition intent code: {needle}")
    for intent in TRANSITION_INTENTS:
        if f"id: '{intent}'" not in script:
            raise AssertionError(f"assets/ecosystem-chat.js missing transition intent {intent!r}")


def verify_continuation_panel() -> None:
    page = read_text(ROOT / "ecosystem-chat.html")
    script = read_text(ROOT / "assets" / "ecosystem-chat.js")
    for needle in ['id="continuationPanel"', 'id="continuationSummary"', 'id="continuationGrid"', "Continue to…"]:
        if needle not in page:
            raise AssertionError(f"ecosystem-chat.html missing continuation-panel surface: {needle}")
    for needle in ["renderContinuationPanel", "transition_destination", "continuation", "item.destination", "link.href"]:
        if needle not in script:
            raise AssertionError(f"assets/ecosystem-chat.js missing continuation-panel behavior: {needle}")


def verify_json_fixtures() -> None:
    for path in JSON_FIXTURES:
        data = load_json(path)
        if not data:
            raise AssertionError(f"{path.relative_to(ROOT)} must not be empty")


def verify_text_contracts() -> None:
    for path in TEXT_FILES:
        read_text(path)
    require_text(ROOT / "ecosystem-chat.html", REQUIRED_TEXT + REQUIRED_BOUNDARY_TEXT + REQUIRED_PAGE_LINKS)
    require_text(ROOT / "README.md", REQUIRED_README_REFERENCES)
    require_text(ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", REQUIRED_ACTIVATION_STATUS_TEXT)
    require_text(UX_STATUS_PATH, REQUIRED_UX_STATUS_TEXT)


def verify_task_contract() -> None:
    task = load_json(TASK_PATH)
    registry = load_json(REGISTRY_PATH)
    if task.get("task_id") != "ecosystem-chat-boundary-check-v1":
        raise AssertionError("unexpected ecosystem chat task id")
    if task.get("manual_actions_required") is not False:
        raise AssertionError("ecosystem chat task must require no manual actions")
    inputs = task.get("expected_inputs")
    if not isinstance(inputs, list):
        raise AssertionError("ecosystem chat task expected_inputs must be a list")
    missing = [entry for entry in REQUIRED_TASK_INPUTS if entry not in inputs]
    if missing:
        raise AssertionError("ecosystem chat task missing expected_inputs: " + ", ".join(missing))
    tasks = registry.get("tasks")
    if not isinstance(tasks, list):
        raise AssertionError("headless task registry tasks must be a list")
    entry = next((item for item in tasks if isinstance(item, dict) and item.get("task_id") == "ecosystem-chat-boundary-check-v1"), None)
    if entry is None or entry.get("status") != "active":
        raise AssertionError("ecosystem chat boundary task must remain active in registry")


def main() -> int:
    verify_single_entry_ux()
    verify_interaction_band_surface()
    verify_transition_intent_engine()
    verify_continuation_panel()
    verify_json_fixtures()
    verify_text_contracts()
    verify_task_contract()
    print("ECOSYSTEM_CHAT_BOUNDARY_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
