#!/usr/bin/env python3
"""Validate the text-only Ecosystem Chat activation surface.

This checker is intentionally static. It verifies that the public Site page,
browser-side script, gateway contract, form gateway model, SDK backend handoff,
activation status, gateway fixtures, workflow gate, iOS path mapping, and README
continue to preserve the public-mirror boundary and the gateway handoff contract.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "ecosystem-chat.html": [
        "<script src=\"assets/ecosystem-chat.js\"></script>",
        "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
        "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
        "id=\"sdkEntryForm\"",
        "id=\"targetEntryPoint\"",
        "id=\"requestedRoute\"",
        "id=\"receiptExpectation\"",
        "id=\"submissionPosture\"",
        "id=\"manifestPreview\"",
        "id=\"receiptPreview\"",
        "id=\"sdkFormStatus\"",
        "fillable fields generate text only into the manifest window and receipt window",
        "Site is a public mirror and command surface",
    ],
    "assets/ecosystem-chat.js": [
        "const STEGVERSE_GATEWAY_PATH = '/api/ecosystem-chat';",
        "const STEGVERSE_LOCAL_MODE = true;",
        "buildManifest",
        "buildReceiptWindow",
        "buildSdkPayload",
        "getSubmissionCheck",
        "site_receipt_authority: false",
        "manifest_correct_at_submission",
        "receipt=not-issued",
        "repo: 'StegVerse-Labs/Site'",
    ],
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md": [
        "The browser page must not become proof authority",
        "SDK entry IFF rule",
        "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
        "fillable form fields generate text only into the manifest window and receipt window",
        "dropdown-style controls",
        "determined correct at the time of submission",
        "fixtures/ecosystem-chat/request.example.json",
        "fixtures/ecosystem-chat/response.example.json",
    ],
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md": [
        "StegVerse-org/SDK entry point",
        "if and only if",
        "Fillable form fields",
        "Manifest window",
        "Receipt window",
        "dropdown-style controls",
        "manifest_correct_at_submission",
        "fixtures/ecosystem-chat/sdk-form-payload.example.json",
        "`fields`",
        "`manifest`",
        "`receipt_window`",
    ],
    "docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md": [
        "Live backend submission: not installed",
        "SDK backend response fixture: installed",
        "fields",
        "manifest",
        "receipt_window",
        "site_receipt_authority` is anything other than `false`",
        "fixtures/ecosystem-chat/sdk-form-payload.example.json",
        "fixtures/ecosystem-chat/sdk-backend-response.example.json",
        "accepted",
        "routed_module",
        "receipt_id",
        "next_action",
        "errors",
        "Before authority issuance, `receipt_id` must remain `null`.",
    ],
    "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md": [
        "SDK Entry Form is installed",
        "Form gateway model",
        "SDK form payload fixture",
        "Fillable fields state: installed",
        "Closed-choice dropdown state: installed",
        "Manifest window state: installed",
        "Receipt window state: installed",
        "SDK backend submission state: not installed",
        "Authority-issued receipt state: not installed",
        "Overall state: pre-backend activation",
        "python scripts/check_ecosystem_chat_contract.py",
    ],
    "fixtures/ecosystem-chat/request.example.json": [
        "\"repo\": \"StegVerse-Labs/Site\"",
        "\"goal\": \"text-only ecosystem command console\"",
    ],
    "fixtures/ecosystem-chat/response.example.json": [
        "\"routed_module\": \"Site\"",
        "\"receipt_id\": null",
    ],
    "fixtures/ecosystem-chat/sdk-form-payload.example.json": [
        "\"fields\"",
        "\"manifest\"",
        "\"receipt_window\"",
        "\"target_entry_point\": \"StegVerse-org/SDK\"",
        "\"site_receipt_authority\": false",
        "\"manifest_correct_at_submission\": true",
    ],
    "fixtures/ecosystem-chat/sdk-backend-response.example.json": [
        "\"accepted\": true",
        "\"routed_module\": \"StegVerse-org/SDK\"",
        "\"receipt_id\": null",
        "\"next_action\"",
        "\"errors\": []",
    ],
    ".github/workflows/check-ecosystem-chat.yml": [
        "name: Check Ecosystem Chat Contract",
        "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
        "docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md",
        "fixtures/ecosystem-chat/request.example.json",
        "fixtures/ecosystem-chat/response.example.json",
        "fixtures/ecosystem-chat/sdk-form-payload.example.json",
        "fixtures/ecosystem-chat/sdk-backend-response.example.json",
        "workflow_dispatch:",
        "python scripts/check_ecosystem_chat_contract.py",
    ],
    "iosnoperiod/iosnoperiod.md": [
        "iosnoperiod/github/workflows/check-ecosystem-chat.yml",
        ".github/workflows/check-ecosystem-chat.yml",
        "github/workflows/check-ecosystem-chat.yml",
        "The no-leading-dot mirror is not the active GitHub Actions workflow location.",
    ],
    "README.md": [
        "[`ecosystem-chat.html`](ecosystem-chat.html)",
        "[`assets/ecosystem-chat.js`](assets/ecosystem-chat.js)",
        "[`docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md`](docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md)",
        "[`docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md`](docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md)",
        "[`docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md`](docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md)",
        "[`fixtures/ecosystem-chat/request.example.json`](fixtures/ecosystem-chat/request.example.json)",
        "[`fixtures/ecosystem-chat/response.example.json`](fixtures/ecosystem-chat/response.example.json)",
        "[`fixtures/ecosystem-chat/sdk-form-payload.example.json`](fixtures/ecosystem-chat/sdk-form-payload.example.json)",
        "[`fixtures/ecosystem-chat/sdk-backend-response.example.json`](fixtures/ecosystem-chat/sdk-backend-response.example.json)",
        "[`iosnoperiod/iosnoperiod.md`](iosnoperiod/iosnoperiod.md)",
        "[`iosnoperiod/workflow-map.json`](iosnoperiod/workflow-map.json)",
        "Ecosystem Chat     =  text-only command surface, not proof authority",
    ],
}

EXPECTED_IOS_MAPPING = {
    "ios_path": "iosnoperiod/github/workflows/check-ecosystem-chat.yml",
    "canonical_path": ".github/workflows/check-ecosystem-chat.yml",
    "display_path_without_leading_dot": "github/workflows/check-ecosystem-chat.yml",
    "status": "canonical_active",
}

REQUIRED_PAYLOAD_KEYS = {"fields", "manifest", "receipt_window"}
REQUIRED_FORM_KEYS = {
    "target_entry_point",
    "input_mode",
    "requested_route",
    "receipt_expectation",
    "submission_posture",
    "user_request",
    "declared_goal",
    "operator_note",
}
REQUIRED_MANIFEST_KEYS = {
    "target_entry_point",
    "input_mode",
    "requested_route",
    "user_request",
    "declared_goal",
    "operator_note",
    "source_surface",
}
REQUIRED_RECEIPT_WINDOW_KEYS = {
    "receipt_expectation",
    "submission_posture",
    "site_receipt_authority",
    "manifest_correct_at_submission",
    "submission_target",
    "correctness_errors",
}
REQUIRED_BACKEND_RESPONSE_KEYS = {"accepted", "routed_module", "receipt_id", "next_action", "errors"}


def main() -> int:
    failures: list[str] = []

    for relative_path, required_fragments in CHECKS.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"missing file: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in content:
                failures.append(f"{relative_path}: missing required fragment: {fragment}")

    failures.extend(check_ios_workflow_map())
    failures.extend(check_sdk_payload_fixture())
    failures.extend(check_sdk_backend_response_fixture())

    if failures:
        print("Ecosystem Chat contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Ecosystem Chat contract check passed.")
    return 0


def check_ios_workflow_map() -> list[str]:
    path = ROOT / "iosnoperiod/workflow-map.json"
    if not path.exists():
        return ["missing file: iosnoperiod/workflow-map.json"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"iosnoperiod/workflow-map.json: invalid JSON: {error}"]

    mappings = data.get("mappings")
    if not isinstance(mappings, list):
        return ["iosnoperiod/workflow-map.json: mappings must be a list"]

    if not mappings:
        return ["iosnoperiod/workflow-map.json: mappings must not be empty"]

    first_mapping = mappings[0]
    failures: list[str] = []
    for key, expected_value in EXPECTED_IOS_MAPPING.items():
        if first_mapping.get(key) != expected_value:
            failures.append(
                "iosnoperiod/workflow-map.json: "
                f"expected {key}={expected_value!r}, got {first_mapping.get(key)!r}"
            )

    return failures


def check_sdk_payload_fixture() -> list[str]:
    path = ROOT / "fixtures/ecosystem-chat/sdk-form-payload.example.json"
    if not path.exists():
        return ["missing file: fixtures/ecosystem-chat/sdk-form-payload.example.json"]

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"fixtures/ecosystem-chat/sdk-form-payload.example.json: invalid JSON: {error}"]

    failures: list[str] = []
    if set(payload) != REQUIRED_PAYLOAD_KEYS:
        failures.append("fixtures/ecosystem-chat/sdk-form-payload.example.json: top-level keys must be fields, manifest, receipt_window")
        return failures

    sections = {
        "fields": REQUIRED_FORM_KEYS,
        "manifest": REQUIRED_MANIFEST_KEYS,
        "receipt_window": REQUIRED_RECEIPT_WINDOW_KEYS,
    }
    for section, required_keys in sections.items():
        value = payload.get(section)
        if not isinstance(value, dict):
            failures.append(f"fixtures/ecosystem-chat/sdk-form-payload.example.json: {section} must be an object")
            continue
        if set(value) != required_keys:
            failures.append(f"fixtures/ecosystem-chat/sdk-form-payload.example.json: {section} keys do not match required contract")

    manifest = payload.get("manifest", {})
    receipt_window = payload.get("receipt_window", {})
    if manifest.get("target_entry_point") != "StegVerse-org/SDK":
        failures.append("fixtures/ecosystem-chat/sdk-form-payload.example.json: manifest target_entry_point must be StegVerse-org/SDK")
    if receipt_window.get("site_receipt_authority") is not False:
        failures.append("fixtures/ecosystem-chat/sdk-form-payload.example.json: site_receipt_authority must be false")
    if not isinstance(receipt_window.get("correctness_errors"), list):
        failures.append("fixtures/ecosystem-chat/sdk-form-payload.example.json: correctness_errors must be a list")

    return failures


def check_sdk_backend_response_fixture() -> list[str]:
    path = ROOT / "fixtures/ecosystem-chat/sdk-backend-response.example.json"
    if not path.exists():
        return ["missing file: fixtures/ecosystem-chat/sdk-backend-response.example.json"]

    try:
        response = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"fixtures/ecosystem-chat/sdk-backend-response.example.json: invalid JSON: {error}"]

    failures: list[str] = []
    if set(response) != REQUIRED_BACKEND_RESPONSE_KEYS:
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: keys must be accepted, routed_module, receipt_id, next_action, errors")
    if response.get("receipt_id") is not None:
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: receipt_id must be null before backend activation")
    if not isinstance(response.get("accepted"), bool):
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: accepted must be boolean")
    if not isinstance(response.get("errors"), list):
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: errors must be a list")

    return failures


if __name__ == "__main__":
    sys.exit(main())
