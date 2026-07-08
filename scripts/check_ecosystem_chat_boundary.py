#!/usr/bin/env python3
"""Verify Ecosystem Chat public boundary, single-entry UX, transition intents, and preview telemetry alignment."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UX_STATUS_PATH = ROOT / "docs" / "ECOSYSTEM_CHAT_UX_STATUS.md"
INTENT_CATALOG_PATH = ROOT / "data" / "ecosystem-chat-transition-intents.json"
TASK_PATH = ROOT / "data" / "headless-tasks" / "ecosystem-chat-boundary-check-v1.json"
REGISTRY_PATH = ROOT / "data" / "headless-task-registry-v1.json"
JSON_FIXTURES = [
    ROOT / "fixtures" / "ecosystem-chat" / "request.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "response.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json",
    INTENT_CATALOG_PATH,
]
TEXT_FILES = [
    ROOT / "README.md",
    ROOT / "ecosystem-chat.html",
    ROOT / "assets" / "ecosystem-chat.js",
    ROOT / "docs" / "ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVATION_STATUS.md",
    UX_STATUS_PATH,
]

INTERACTION_BANDS = ["intra", "inter", "research", "provider", "solver", "receipt"]
TRANSITION_INTENTS = ["explain", "demonstrate", "compare", "research", "build", "replay", "runtime", "formalism", "sdk", "implementation", "solver"]
REQUIRED_TEXT = ["raw_shell_allowed", "authority_required", "rate_limit_required", "receipt_required_for_execution", "Restricted admin"]
REQUIRED_BOUNDARY_TEXT = ["shell", "credential", "receipt", "authority"]
REQUIRED_PAGE_LINKS = [
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
]
REQUIRED_README_REFERENCES = [
    "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md",
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    "scripts/check_ecosystem_chat_boundary.py",
    "scripts/check_ecosystem_chat_contract.py",
    "data/headless-tasks/ecosystem-chat-boundary-check-v1.json",
    "data/headless-task-registry-v1.json",
    "python scripts/check_ecosystem_chat_contract.py",
    "python scripts/check_ecosystem_chat_boundary.py",
]
REQUIRED_TASK_INPUTS = [
    "README.md",
    "ecosystem-chat.html",
    "assets/ecosystem-chat.js",
    "data/ecosystem-chat-transition-intents.json",
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md",
    "docs/ECOSYSTEM_CHAT_UX_STATUS.md",
    "fixtures/ecosystem-chat/request.example.json",
    "fixtures/ecosystem-chat/response.example.json",
    "fixtures/ecosystem-chat/sdk-form-payload.example.json",
    "scripts/check_ecosystem_chat_boundary.py",
    "scripts/check_ecosystem_chat_contract.py",
    "data/headless-tasks/ecosystem-chat-boundary-check-v1.json",
    "data/headless-task-registry-v1.json",
]
REQUIRED_ACTIVATION_STATUS_TEXT = [
    "No-shell boundary state: installed",
    "No-credential boundary state: installed",
    "Restricted-admin routing state: installed",
    "Boundary verifier state: installed",
    "Declared task state: installed",
    "Registry state: installed",
    "Contract check state: installed and aligned with boundary task",
    "scripts/check_ecosystem_chat_contract.py\n  -> confirms",
    "scripts/check_ecosystem_chat_boundary.py\n  -> confirms",
    "data/headless-tasks/ecosystem-chat-boundary-check-v1.json\n  -> declares",
    "data/headless-task-registry-v1.json\n  -> keeps ecosystem-chat-boundary-check-v1 active.",
    "Backend gateway state: not installed",
    "Authority-issued receipt state: not installed",
]
REQUIRED_UX_STATUS_TEXT = [
    "UX contract: single-primary-governed-chat-preview-entry",
    "Primary: Try the governed chat preview -> #console",
    "Secondary: How the boundary works -> #how-it-works",
    "multi-entry console",
    "task launcher",
    "repo control panel",
    "python scripts/run_site_task.py validate",
]
REQUIRED_SINGLE_ENTRY_TEXT = [
    "Try the governed chat preview",
    "How the boundary works",
    "Technical preview details",
    "This page has one public purpose",
    "It is a governed chat preview, not a shell, not a repo control panel, not a proof issuer, and not the full product.",
]
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
    if len(re.findall(r'class="sv-btn sv-btn-primary"', page)) != 2:
        raise AssertionError("ecosystem-chat.html must keep exactly two primary buttons: hero entry and chat submit")
    hero_start = page.find('<div class="sv-hero">')
    boundary_start = page.find('<div class="sv-boundary">', hero_start)
    if hero_start < 0 or boundary_start < 0:
        raise AssertionError("ecosystem-chat.html missing hero/boundary structure")
    hero = page[hero_start:boundary_start]
    if hero.count('sv-btn') != 2 or 'href="#console"' not in hero or 'href="#how-it-works"' not in hero:
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


def verify_docs_and_tasks() -> None:
    for link in REQUIRED_PAGE_LINKS:
        if link not in read_text(ROOT / "ecosystem-chat.html"):
            raise AssertionError(f"ecosystem-chat.html missing public link: {link}")
    missing_readme = [ref for ref in REQUIRED_README_REFERENCES if ref not in read_text(ROOT / "README.md")]
    if missing_readme:
        raise AssertionError(f"README.md missing references: {', '.join(missing_readme)}")
    require_text(ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", REQUIRED_ACTIVATION_STATUS_TEXT)
    require_text(UX_STATUS_PATH, REQUIRED_UX_STATUS_TEXT)
    task = load_json(TASK_PATH)
    if task.get("task_id") != "ecosystem-chat-boundary-check-v1" or task.get("authority_class") != "ordinary_analysis":
        raise AssertionError("ecosystem-chat boundary task metadata drift")
    if task.get("command") != ["python", "scripts/check_ecosystem_chat_boundary.py"]:
        raise AssertionError("ecosystem-chat boundary task command drift")
    inputs = task.get("expected_inputs")
    if not isinstance(inputs, list):
        raise AssertionError("task expected_inputs must be a list")
    missing_inputs = [path for path in REQUIRED_TASK_INPUTS if path not in inputs]
    if missing_inputs:
        raise AssertionError(f"task missing expected inputs: {', '.join(missing_inputs)}")
    registry = load_json(REGISTRY_PATH)
    matches = [entry for entry in registry.get("tasks", []) if entry.get("task_id") == "ecosystem-chat-boundary-check-v1"]
    if len(matches) != 1:
        raise AssertionError("registry must contain exactly one ecosystem-chat-boundary-check-v1 entry")
    for key, value in {"task_path": "data/headless-tasks/ecosystem-chat-boundary-check-v1.json", "class": "public_surface_boundary_verification", "authority_class": "ordinary_analysis", "status": "active"}.items():
        if matches[0].get(key) != value:
            raise AssertionError(f"registry entry expected {key}={value!r}")


def require_interaction_contract(data: dict, path: str) -> None:
    if data.get("interaction_bands") != INTERACTION_BANDS:
        raise AssertionError(f"{path} must declare interaction_bands={INTERACTION_BANDS!r}")
    profile = data.get("interaction_profile")
    if not isinstance(profile, dict):
        raise AssertionError(f"{path} must declare interaction_profile object")
    for band in INTERACTION_BANDS:
        value = profile.get(band)
        if not isinstance(value, int) or value < 0 or value > 100:
            raise AssertionError(f"{path} interaction_profile {band!r} must be integer 0..100")
    unknown = [band for band in profile if band not in INTERACTION_BANDS]
    if unknown:
        raise AssertionError(f"{path} interaction_profile contains unknown bands: {', '.join(unknown)}")
    if data.get("math_solver_supported") is not True:
        raise AssertionError(f"{path} must declare math_solver_supported=true")


def require_transition_contract(data: dict, path: str) -> None:
    if data.get("transition_intent") not in TRANSITION_INTENTS:
        raise AssertionError(f"{path} must declare known transition_intent")
    if not isinstance(data.get("transition_destination"), str) or not data.get("transition_destination"):
        raise AssertionError(f"{path} must declare transition_destination")


def verify_fixtures() -> None:
    for fixture in JSON_FIXTURES:
        load_json(fixture)
    request = load_json(ROOT / "fixtures" / "ecosystem-chat" / "request.example.json")
    for key, value in {"execution_model": "allowlisted_task_request_only", "raw_shell_allowed": False, "authority_required": True, "rate_limit_required": True, "receipt_required_for_execution": True}.items():
        if request.get(key) != value:
            raise AssertionError(f"request.example.json expected {key}={value!r}")
    require_interaction_contract(request, "request.example.json")
    require_transition_contract(request, "request.example.json")
    response = load_json(ROOT / "fixtures" / "ecosystem-chat" / "response.example.json")
    if response.get("task_status") != "preview_only" or response.get("receipt_id") is not None:
        raise AssertionError("response.example.json must remain preview_only with null receipt_id")
    for needle in ["Shell: disabled", "Authority:", "Interaction bands:", "Math solver:", "Transition intent:", "Suggested transition:"]:
        if needle not in str(response.get("response", "")):
            raise AssertionError(f"response.example.json response missing {needle!r}")
    profile = {"interaction_profile": response.get("interaction_profile"), "interaction_bands": INTERACTION_BANDS, "math_solver_supported": True, "transition_intent": response.get("transition_intent"), "transition_destination": response.get("transition_destination")}
    require_interaction_contract(profile, "response.example.json")
    require_transition_contract(profile, "response.example.json")
    sdk = load_json(ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json")
    manifest = sdk.get("manifest")
    receipt_window = sdk.get("receipt_window")
    if not isinstance(manifest, dict) or not isinstance(receipt_window, dict):
        raise AssertionError("sdk fixture must declare manifest and receipt_window objects")
    for key, value in {"raw_shell_allowed": False, "authority_required": True, "rate_limit_required": True, "receipt_required_for_execution": True, "restricted_admin_review_required": False}.items():
        if manifest.get(key) != value:
            raise AssertionError(f"sdk manifest expected {key}={value!r}")
    require_interaction_contract(manifest, "sdk-form-payload.example.json manifest")
    require_transition_contract(manifest, "sdk-form-payload.example.json manifest")
    for key, value in {"site_receipt_authority": False, "site_shell_authority": False, "site_credential_authority": False, "execution_allowed_from_site": False, "authority_required_before_execution": True, "receipt_required_for_execution": True}.items():
        if receipt_window.get(key) != value:
            raise AssertionError(f"sdk receipt_window expected {key}={value!r}")
    require_interaction_contract(receipt_window, "sdk-form-payload.example.json receipt_window")
    require_transition_contract(receipt_window, "sdk-form-payload.example.json receipt_window")


def main() -> int:
    for path in TEXT_FILES:
        require_text(path, REQUIRED_TEXT)
        require_text(path, REQUIRED_BOUNDARY_TEXT)
    verify_single_entry_ux()
    verify_interaction_band_surface()
    verify_transition_intent_engine()
    verify_docs_and_tasks()
    verify_fixtures()
    print(json.dumps({
        "ok": True,
        "checked": [str(path.relative_to(ROOT)) for path in TEXT_FILES + JSON_FIXTURES + [TASK_PATH, REGISTRY_PATH]],
        "boundary": "no-shell/no-credential/authority-required/receipt-required",
        "ux_contract": "single-primary-governed-chat-preview-entry",
        "transition_intents": TRANSITION_INTENTS,
        "interaction_bands": INTERACTION_BANDS,
        "math_solver_supported": True,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
