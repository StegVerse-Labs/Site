#!/usr/bin/env python3
"""Verify Ecosystem Chat public boundary alignment.

This verifier intentionally checks text, contract, and fixture invariants only.
It does not execute site JavaScript or call external services.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "ecosystem-chat-boundary-check-v1"
TASK_PATH = f"data/headless-tasks/{TASK_ID}.json"
VERIFIER_COMMAND = ["python", "scripts/check_ecosystem_chat_boundary.py"]

TEXT_FILES = [
    ROOT / "README.md",
    ROOT / "ecosystem-chat.html",
    ROOT / "assets" / "ecosystem-chat.js",
    ROOT / "docs" / "ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
]

REQUIRED_TEXT = [
    "raw_shell_allowed",
    "authority_required",
    "rate_limit_required",
    "receipt_required_for_execution",
    "Restricted admin",
]

REQUIRED_BOUNDARY_TEXT = [
    "shell",
    "credential",
    "receipt",
    "authority",
]

REQUIRED_PAGE_LINKS = [
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
]

REQUIRED_README_REFERENCES = [
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    "scripts/check_ecosystem_chat_boundary.py",
    TASK_PATH,
    "data/headless-task-registry-v1.json",
    "python scripts/check_ecosystem_chat_boundary.py",
]

JSON_FIXTURES = [
    ROOT / "fixtures" / "ecosystem-chat" / "request.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "response.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json",
]

EXPECTED_TASK_INPUTS = [
    "README.md",
    "ecosystem-chat.html",
    "assets/ecosystem-chat.js",
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
    "fixtures/ecosystem-chat/request.example.json",
    "fixtures/ecosystem-chat/response.example.json",
    "fixtures/ecosystem-chat/sdk-form-payload.example.json",
    "scripts/check_ecosystem_chat_boundary.py",
    TASK_PATH,
    "data/headless-task-registry-v1.json",
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(path: Path, needles: list[str]) -> None:
    body = read_text(path)
    missing = [needle for needle in needles if needle not in body]
    if missing:
        rel = path.relative_to(ROOT)
        raise AssertionError(f"{rel} missing required boundary text: {', '.join(missing)}")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing required fixture: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def verify_page_links() -> None:
    page = read_text(ROOT / "ecosystem-chat.html")
    missing = [link for link in REQUIRED_PAGE_LINKS if link not in page]
    if missing:
        raise AssertionError(f"ecosystem-chat.html missing required public links: {', '.join(missing)}")


def verify_readme_references() -> None:
    readme = read_text(ROOT / "README.md")
    missing = [ref for ref in REQUIRED_README_REFERENCES if ref not in readme]
    if missing:
        raise AssertionError(f"README.md missing required Ecosystem Chat boundary references: {', '.join(missing)}")


def verify_declared_task() -> None:
    task = load_json(ROOT / TASK_PATH)
    if task.get("task_id") != TASK_ID:
        raise AssertionError(f"{TASK_PATH} must declare task_id={TASK_ID}")
    if task.get("command") != VERIFIER_COMMAND:
        raise AssertionError(f"{TASK_PATH} must run {VERIFIER_COMMAND!r}")
    if task.get("authority_class") != "ordinary_analysis":
        raise AssertionError(f"{TASK_PATH} must remain ordinary_analysis")

    expected_inputs = task.get("expected_inputs")
    if not isinstance(expected_inputs, list):
        raise AssertionError(f"{TASK_PATH} expected_inputs must be a list")
    missing = [item for item in EXPECTED_TASK_INPUTS if item not in expected_inputs]
    if missing:
        raise AssertionError(f"{TASK_PATH} missing expected_inputs: {', '.join(missing)}")


def verify_task_registry() -> None:
    registry = load_json(ROOT / "data" / "headless-task-registry-v1.json")
    tasks = registry.get("tasks")
    if not isinstance(tasks, list):
        raise AssertionError("data/headless-task-registry-v1.json tasks must be a list")
    matches = [task for task in tasks if task.get("task_id") == TASK_ID]
    if len(matches) != 1:
        raise AssertionError(f"registry must contain exactly one {TASK_ID} entry")
    entry = matches[0]
    if entry.get("task_path") != TASK_PATH:
        raise AssertionError(f"registry {TASK_ID} task_path must be {TASK_PATH}")
    if entry.get("status") != "active":
        raise AssertionError(f"registry {TASK_ID} status must be active")
    if entry.get("authority_class") != "ordinary_analysis":
        raise AssertionError(f"registry {TASK_ID} authority_class must be ordinary_analysis")


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
        raise AssertionError("sdk-form-payload.example.json manifest must be an object")
    if not isinstance(receipt_window, dict):
        raise AssertionError("sdk-form-payload.example.json receipt_window must be an object")

    manifest_expected = {
        "raw_shell_allowed": False,
        "authority_required": True,
        "rate_limit_required": True,
        "receipt_required_for_execution": True,
        "restricted_admin_review_required": False,
    }
    for key, value in manifest_expected.items():
        if manifest.get(key) != value:
            raise AssertionError(f"sdk manifest expected {key}={value!r}")

    receipt_expected = {
        "site_receipt_authority": False,
        "site_shell_authority": False,
        "site_credential_authority": False,
        "execution_allowed_from_site": False,
        "authority_required_before_execution": True,
        "receipt_required_for_execution": True,
    }
    for key, value in receipt_expected.items():
        if receipt_window.get(key) != value:
            raise AssertionError(f"sdk receipt_window expected {key}={value!r}")


def main() -> int:
    for path in TEXT_FILES:
        require_text(path, REQUIRED_TEXT)
        require_text(path, REQUIRED_BOUNDARY_TEXT)

    verify_page_links()
    verify_readme_references()
    verify_declared_task()
    verify_task_registry()

    for fixture in JSON_FIXTURES:
        load_json(fixture)

    verify_request_fixture()
    verify_response_fixture()
    verify_sdk_fixture()

    print(json.dumps({
        "ok": True,
        "checked": [str(path.relative_to(ROOT)) for path in TEXT_FILES + JSON_FIXTURES] + [TASK_PATH, "data/headless-task-registry-v1.json"],
        "required_page_links": REQUIRED_PAGE_LINKS,
        "required_readme_references": REQUIRED_README_REFERENCES,
        "declared_task": TASK_ID,
        "boundary": "no-shell/no-credential/authority-required/receipt-required",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
