#!/usr/bin/env python3
"""Verify Ecosystem Chat public boundary alignment.

This verifier intentionally checks text, contract, and fixture invariants only.
It does not execute site JavaScript or call external services.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT_FILES = [
    ROOT / "ecosystem-chat.html",
    ROOT / "assets" / "ecosystem-chat.js",
    ROOT / "docs" / "ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
    ROOT / "docs" / "ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
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

JSON_FIXTURES = [
    ROOT / "fixtures" / "ecosystem-chat" / "request.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "response.example.json",
    ROOT / "fixtures" / "ecosystem-chat" / "sdk-form-payload.example.json",
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

    for fixture in JSON_FIXTURES:
        load_json(fixture)

    verify_request_fixture()
    verify_response_fixture()
    verify_sdk_fixture()

    print(json.dumps({
        "ok": True,
        "checked": [str(path.relative_to(ROOT)) for path in TEXT_FILES + JSON_FIXTURES],
        "boundary": "no-shell/no-credential/authority-required/receipt-required",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
