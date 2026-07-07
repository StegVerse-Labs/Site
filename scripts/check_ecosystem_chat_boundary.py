#!/usr/bin/env python3
"""Verify Ecosystem Chat public boundary and single-entry UX alignment."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT_FILES = [
    ROOT / "README.md",
    ROOT / "ecosystem-chat.html",
    ROOT / "assets" / "ecosystem-chat.js",
    ROOT / "docs" / "ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVATION_STATUS.md",
]

REQUIRED_TEXT = [
    "raw_shell_allowed",
    "authority_required",
    "rate_limit_required",
    "receipt_required_for_execution",
    "Restricted admin",
]

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
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md",
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

REQUIRED_SINGLE_ENTRY_TEXT = [
    "Try the governed chat preview",
    "How the boundary works",
    "Technical preview details",
    "This page has one public purpose",
    "It is a governed chat preview, not a shell, not a repo control panel, not a proof issuer, and not the full product.",
]

FORBIDDEN_PRIMARY_ENTRY_TEXT = [
    "Open SDK form",
    "Open console",
    "View guardrails",
    "Gateway contract target",
]

JSON_FIXTURES = [
    ROOT / "fixtures" / "ecosystem-chat" / "request.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "response.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json",
]

TASK_PATH = ROOT / "data" / "headless-tasks" / "ecosystem-chat-boundary-check-v1.json"
REGISTRY_PATH = ROOT / "data" / "headless-task-registry-v1.json"


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


def verify_page_links() -> None:
    page = read_text(ROOT / "ecosystem-chat.html")
    missing = [link for link in REQUIRED_PAGE_LINKS if link not in page]
    if missing:
        raise AssertionError(f"ecosystem-chat.html missing public links: {', '.join(missing)}")


def hero_region(page: str) -> str:
    hero_start = page.find('<div class="sv-hero">')
    if hero_start < 0:
        raise AssertionError("ecosystem-chat.html missing sv-hero section")
    boundary_start = page.find('<div class="sv-boundary">', hero_start)
    if boundary_start < 0:
        raise AssertionError("ecosystem-chat.html missing sv-boundary section after hero")
    return page[hero_start:boundary_start]


def verify_single_entry_ux() -> None:
    page = read_text(ROOT / "ecosystem-chat.html")
    missing = [text for text in REQUIRED_SINGLE_ENTRY_TEXT if text not in page]
    if missing:
        raise AssertionError(f"ecosystem-chat.html missing single-entry UX text: {', '.join(missing)}")

    forbidden = [text for text in FORBIDDEN_PRIMARY_ENTRY_TEXT if text in page]
    if forbidden:
        raise AssertionError(f"ecosystem-chat.html restored old competing primary entry text: {', '.join(forbidden)}")

    primary_buttons = re.findall(r'class="sv-btn sv-btn-primary"', page)
    if len(primary_buttons) != 2:
        raise AssertionError(f"ecosystem-chat.html expected exactly 2 primary buttons: hero chat entry and chat submit; found {len(primary_buttons)}")

    if '<details class="simple-card" id="technical-details">' not in page:
        raise AssertionError("ecosystem-chat.html must keep SDK/gateway details in collapsible technical section")

    hero = hero_region(page)
    if hero.count('sv-btn') != 2:
        raise AssertionError("ecosystem-chat.html hero must have exactly one primary action and one secondary boundary action")
    if 'href="#console"' not in hero or 'href="#how-it-works"' not in hero:
        raise AssertionError("ecosystem-chat.html hero actions must point only to chat preview and boundary explanation")


def verify_readme_references() -> None:
    readme = read_text(ROOT / "README.md")
    missing = [ref for ref in REQUIRED_README_REFERENCES if ref not in readme]
    if missing:
        raise AssertionError(f"README.md missing references: {', '.join(missing)}")


def verify_activation_status() -> None:
    require_text(ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", REQUIRED_ACTIVATION_STATUS_TEXT)


def verify_declared_task() -> None:
    task = load_json(TASK_PATH)
    if task.get("task_id") != "ecosystem-chat-boundary-check-v1":
        raise AssertionError("task id drift")
    if task.get("authority_class") != "ordinary_analysis":
        raise AssertionError("task authority class drift")
    if task.get("command") != ["python", "scripts/check_ecosystem_chat_boundary.py"]:
        raise AssertionError("task command drift")
    expected_inputs = task.get("expected_inputs")
    if not isinstance(expected_inputs, list):
        raise AssertionError("task expected_inputs must be a list")
    missing = [path for path in REQUIRED_TASK_INPUTS if path not in expected_inputs]
    if missing:
        raise AssertionError(f"task missing expected inputs: {', '.join(missing)}")


def verify_registry_entry() -> None:
    registry = load_json(REGISTRY_PATH)
    tasks = registry.get("tasks")
    if not isinstance(tasks, list):
        raise AssertionError("registry tasks must be a list")
    matches = [task for task in tasks if task.get("task_id") == "ecosystem-chat-boundary-check-v1"]
    if len(matches) != 1:
        raise AssertionError("registry must contain exactly one ecosystem-chat-boundary-check-v1 entry")
    entry = matches[0]
    expected = {
        "task_path": "data/headless-tasks/ecosystem-chat-boundary-check-v1.json",
        "class": "public_surface_boundary_verification",
        "authority_class": "ordinary_analysis",
        "status": "active",
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            raise AssertionError(f"registry entry expected {key}={value!r}")


def verify_request_fixture() -> None:
    data = load_json(ROOT / "fixtures" / "ecosystem-chat" / "request.example.json")
    expected = {
        "execution_model": "allowlisted_task_request_only",
        "raw_shell_allowed": False,
        "authority_required": True,
        "rate_limit_required": True,
        "receipt_required_for_execution": True,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise AssertionError(f"request.example.json expected {key}={value!r}")


def verify_response_fixture() -> None:
    data = load_json(ROOT / "fixtures" / "ecosystem-chat" / "response.example.json")
    if data.get("task_status") != "preview_only":
        raise AssertionError("response.example.json must declare task_status=preview_only")
    if data.get("receipt_id") is not None:
        raise AssertionError("response.example.json must keep receipt_id null")
    response = str(data.get("response", ""))
    for needle in ["Shell: disabled", "Authority:"]:
        if needle not in response:
            raise AssertionError(f"response.example.json response missing {needle!r}")


def verify_sdk_fixture() -> None:
    data = load_json(ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json")
    manifest = data.get("manifest")
    receipt_window = data.get("receipt_window")
    if not isinstance(manifest, dict):
        raise AssertionError("sdk manifest must be an object")
    if not isinstance(receipt_window, dict):
        raise AssertionError("sdk receipt_window must be an object")
    for key, value in {
        "raw_shell_allowed": False,
        "authority_required": True,
        "rate_limit_required": True,
        "receipt_required_for_execution": True,
        "restricted_admin_review_required": False,
    }.items():
        if manifest.get(key) != value:
            raise AssertionError(f"sdk manifest expected {key}={value!r}")
    for key, value in {
        "site_receipt_authority": False,
        "site_shell_authority": False,
        "site_credential_authority": False,
        "execution_allowed_from_site": False,
        "authority_required_before_execution": True,
        "receipt_required_for_execution": True,
    }.items():
        if receipt_window.get(key) != value:
            raise AssertionError(f"sdk receipt_window expected {key}={value!r}")


def main() -> int:
    for path in TEXT_FILES:
        require_text(path, REQUIRED_TEXT)
        require_text(path, REQUIRED_BOUNDARY_TEXT)

    verify_page_links()
    verify_single_entry_ux()
    verify_readme_references()
    verify_activation_status()
    verify_declared_task()
    verify_registry_entry()

    for fixture in JSON_FIXTURES:
        load_json(fixture)

    verify_request_fixture()
    verify_response_fixture()
    verify_sdk_fixture()

    print(json.dumps({
        "ok": True,
        "checked": [str(path.relative_to(ROOT)) for path in TEXT_FILES + JSON_FIXTURES + [TASK_PATH, REGISTRY_PATH]],
        "required_page_links": REQUIRED_PAGE_LINKS,
        "required_readme_references": REQUIRED_README_REFERENCES,
        "required_task_inputs": REQUIRED_TASK_INPUTS,
        "boundary": "no-shell/no-credential/authority-required/receipt-required",
        "ux_contract": "single-primary-governed-chat-preview-entry",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
