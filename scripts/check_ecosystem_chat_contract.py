#!/usr/bin/env python3
"""Validate the Ecosystem Chat activation surface.

This checker is intentionally static. It verifies that the public Site page,
browser-side script, gateway contract, form gateway model, activation status,
fixtures, README, workflow/iOS surfaces, and boundary task references preserve
the public-mirror and governed-task handoff contract.
"""

from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

BOUNDARY_TASK_ID = "ecosystem-chat-boundary-check-v1"
BOUNDARY_TASK_PATH = "data/headless-tasks/ecosystem-chat-boundary-check-v1.json"
BOUNDARY_SCRIPT = "scripts/check_ecosystem_chat_boundary.py"
INTERACTION_BANDS = ["intra", "inter", "research", "provider", "solver", "receipt"]

CHECKS = {
    "ecosystem-chat.html": [
        "<script src=\"assets/ecosystem-chat.js\"></script>",
        "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
        "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
        "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md",
        "id=\"sdkEntryForm\"",
        "id=\"targetEntryPoint\"",
        "id=\"requestedRoute\"",
        "id=\"receiptExpectation\"",
        "id=\"submissionPosture\"",
        "id=\"manifestPreview\"",
        "id=\"receiptPreview\"",
        "id=\"sdkFormStatus\"",
        "id=\"interactionBandMeter\"",
        "Ecosystem LLM routing bands",
        "Math solver",
        "INTRA",
        "INTER",
        "RESEARCH",
        "PROVIDER",
        "SOLVER",
        "RECEIPT",
        "Restricted admin",
        "raw_shell_allowed",
        "authority_required",
        "rate_limit_required",
        "receipt_required_for_execution",
        "interaction_profile",
        "interaction_bands",
        "math_solver_supported",
    ],
    "assets/ecosystem-chat.js": [
        "const STEGVERSE_GATEWAY_PATH = '/api/ecosystem-chat';",
        "const STEGVERSE_LOCAL_MODE = true;",
        "RESTRICTED_PATTERNS",
        "INTERACTION_BANDS",
        "calculateInteractionProfile",
        "renderInteractionBands",
        "Restricted admin",
        "buildManifest",
        "buildReceiptWindow",
        "buildSdkPayload",
        "getSubmissionCheck",
        "raw_shell_allowed: false",
        "authority_required: true",
        "rate_limit_required: true",
        "receipt_required_for_execution: true",
        "site_receipt_authority: false",
        "site_shell_authority: false",
        "site_credential_authority: false",
        "receipt=not-issued",
        "interaction_profile",
        "interaction_bands",
        "math_solver_supported",
    ],
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md": [
        "Ecosystem Chat is not a public terminal.",
        "raw_shell_allowed",
        "authority_required",
        "rate_limit_required",
        "receipt_required_for_execution",
        "SDK entry IFF rule",
        "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
        "fixtures/ecosystem-chat/request.example.json",
        "fixtures/ecosystem-chat/response.example.json",
        "Restricted administration examples",
        "Local transcript hashes are not proof receipts.",
    ],
    "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md": [
        "StegVerse-org/SDK entry point",
        "if and only if",
        "Fillable form fields",
        "Manifest window",
        "Receipt window",
        "dropdown-style controls",
        "raw_shell_allowed",
        "authority_required",
        "rate_limit_required",
        "receipt_required_for_execution",
        "fixtures/ecosystem-chat/sdk-form-payload.example.json",
        "`fields`",
        "`manifest`",
        "`receipt_window`",
    ],
    "docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md": [
        BOUNDARY_TASK_ID,
        BOUNDARY_TASK_PATH,
        BOUNDARY_SCRIPT,
        "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md",
        "no shell",
        "no credential authority",
        "authority required before execution",
        "receipt required for execution",
    ],
    "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md": [
        "SDK Entry Form is installed",
        "The Site-side activation surface is complete for pre-backend handoff.",
        "Boundary verifier",
        "Declared boundary task",
        "No-shell boundary state: installed",
        "No-credential boundary state: installed",
        "Restricted-admin routing state: installed",
        "Boundary verifier state: installed",
        "Declared task state: installed",
        "Registry state: installed",
        "Backend gateway state: not installed",
        "Authority-issued receipt state: not installed",
        "python scripts/check_ecosystem_chat_contract.py",
        "python scripts/check_ecosystem_chat_boundary.py",
    ],
    "fixtures/ecosystem-chat/request.example.json": [
        "\"execution_model\": \"allowlisted_task_request_only\"",
        "\"raw_shell_allowed\": false",
        "\"authority_required\": true",
        "\"rate_limit_required\": true",
        "\"receipt_required_for_execution\": true",
        "\"interaction_bands\"",
        "\"interaction_profile\"",
        "\"math_solver_supported\": true",
    ],
    "fixtures/ecosystem-chat/response.example.json": [
        "\"routed_module\": \"Site\"",
        "\"task_status\": \"preview_only\"",
        "\"receipt_id\": null",
        "Shell: disabled",
        "Interaction bands:",
        "Math solver:",
        "\"interaction_profile\"",
    ],
    "fixtures/ecosystem-chat/sdk-form-payload.example.json": [
        "\"fields\"",
        "\"manifest\"",
        "\"receipt_window\"",
        "\"target_entry_point\": \"StegVerse-org/SDK\"",
        "\"raw_shell_allowed\": false",
        "\"site_receipt_authority\": false",
        "\"site_shell_authority\": false",
        "\"site_credential_authority\": false",
        "\"manifest_correct_at_submission\": true",
        "\"interaction_bands\"",
        "\"interaction_profile\"",
        "\"math_solver_supported\": true",
    ],
    "fixtures/ecosystem-chat/sdk-backend-response.example.json": [
        "\"accepted\": true",
        "\"routed_module\": \"StegVerse-org/SDK\"",
        "\"receipt_id\": null",
        "\"next_action\"",
        "\"errors\": []",
    ],
    BOUNDARY_TASK_PATH: [BOUNDARY_TASK_ID, BOUNDARY_SCRIPT, "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", "ordinary_analysis", "public_surface_boundary_verification"],
    "data/headless-task-registry-v1.json": [BOUNDARY_TASK_ID, BOUNDARY_TASK_PATH, "ordinary_analysis", "active"],
    ".github/workflows/check-ecosystem-chat.yml": [
        "name: Check Ecosystem Chat Contract",
        "docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md",
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
        "[`docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md`](docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md)",
        "[`docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md`](docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md)",
        "[`fixtures/ecosystem-chat/request.example.json`](fixtures/ecosystem-chat/request.example.json)",
        "[`fixtures/ecosystem-chat/response.example.json`](fixtures/ecosystem-chat/response.example.json)",
        "[`fixtures/ecosystem-chat/sdk-form-payload.example.json`](fixtures/ecosystem-chat/sdk-form-payload.example.json)",
        "[`fixtures/ecosystem-chat/sdk-backend-response.example.json`](fixtures/ecosystem-chat/sdk-backend-response.example.json)",
        f"[`{BOUNDARY_SCRIPT}`]({BOUNDARY_SCRIPT})",
        f"[`{BOUNDARY_TASK_PATH}`]({BOUNDARY_TASK_PATH})",
        "python scripts/check_ecosystem_chat_contract.py",
        "python scripts/check_ecosystem_chat_boundary.py",
        "Ecosystem Chat     =  text-only user advancement surface, not proof authority or shell authority",
    ],
}

EXPECTED_IOS_MAPPING = {
    "ios_path": "iosnoperiod/github/workflows/check-ecosystem-chat.yml",
    "canonical_path": ".github/workflows/check-ecosystem-chat.yml",
    "display_path_without_leading_dot": "github/workflows/check-ecosystem-chat.yml",
    "status": "canonical_active",
}

REQUIRED_PAYLOAD_KEYS = {"fields", "manifest", "receipt_window"}
REQUIRED_FORM_KEYS = {"target_entry_point", "input_mode", "requested_route", "receipt_expectation", "submission_posture", "user_request", "declared_goal", "operator_note"}
REQUIRED_MANIFEST_KEYS = {"target_entry_point", "input_mode", "requested_route", "detected_route", "task_status", "raw_shell_allowed", "authority_required", "rate_limit_required", "receipt_required_for_execution", "restricted_admin_review_required", "interaction_profile", "interaction_bands", "math_solver_supported", "user_request", "declared_goal", "operator_note", "source_surface"}
REQUIRED_RECEIPT_WINDOW_KEYS = {"receipt_expectation", "submission_posture", "site_receipt_authority", "site_shell_authority", "site_credential_authority", "manifest_correct_at_submission", "submission_target", "execution_allowed_from_site", "authority_required_before_execution", "receipt_required_for_execution", "interaction_profile", "interaction_bands", "math_solver_supported", "correctness_errors"}
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
    failures.extend(check_gateway_request_fixture())
    failures.extend(check_gateway_response_fixture())
    failures.extend(check_sdk_payload_fixture())
    failures.extend(check_sdk_backend_response_fixture())
    failures.extend(check_boundary_task_fixture())
    if failures:
        print("Ecosystem Chat contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Ecosystem Chat contract check passed.")
    return 0


def load_json(relative_path: str) -> tuple[dict | None, list[str]]:
    path = ROOT / relative_path
    if not path.exists():
        return None, [f"missing file: {relative_path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, [f"{relative_path}: invalid JSON: {error}"]
    if not isinstance(data, dict):
        return None, [f"{relative_path}: must be a JSON object"]
    return data, []


def check_ios_workflow_map() -> list[str]:
    data, failures = load_json("iosnoperiod/workflow-map.json")
    if failures:
        return failures
    mappings = data.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        return ["iosnoperiod/workflow-map.json: mappings must be a non-empty list"]
    return [
        "iosnoperiod/workflow-map.json: " f"expected {key}={expected_value!r}, got {mappings[0].get(key)!r}"
        for key, expected_value in EXPECTED_IOS_MAPPING.items()
        if mappings[0].get(key) != expected_value
    ]


def require_interaction_contract(data: dict, label: str) -> list[str]:
    failures = []
    if data.get("interaction_bands") != INTERACTION_BANDS:
        failures.append(f"{label}: interaction_bands must be {INTERACTION_BANDS!r}")
    profile = data.get("interaction_profile")
    if not isinstance(profile, dict):
        failures.append(f"{label}: interaction_profile must be an object")
    else:
        for band in INTERACTION_BANDS:
            value = profile.get(band)
            if not isinstance(value, int) or value < 0 or value > 100:
                failures.append(f"{label}: interaction_profile.{band} must be integer 0..100")
        for band in profile:
            if band not in INTERACTION_BANDS:
                failures.append(f"{label}: unknown interaction band {band!r}")
    if data.get("math_solver_supported") is not True:
        failures.append(f"{label}: math_solver_supported must be true")
    return failures


def check_gateway_request_fixture() -> list[str]:
    data, failures = load_json("fixtures/ecosystem-chat/request.example.json")
    if failures:
        return failures
    expected = {"execution_model": "allowlisted_task_request_only", "raw_shell_allowed": False, "authority_required": True, "rate_limit_required": True, "receipt_required_for_execution": True}
    failures = [f"fixtures/ecosystem-chat/request.example.json: expected {key}={value!r}" for key, value in expected.items() if data.get(key) != value]
    failures.extend(require_interaction_contract(data, "fixtures/ecosystem-chat/request.example.json"))
    return failures


def check_gateway_response_fixture() -> list[str]:
    data, failures = load_json("fixtures/ecosystem-chat/response.example.json")
    if failures:
        return failures
    if data.get("routed_module") != "Site":
        failures.append("fixtures/ecosystem-chat/response.example.json: routed_module must be Site")
    if data.get("task_status") != "preview_only":
        failures.append("fixtures/ecosystem-chat/response.example.json: task_status must be preview_only")
    if data.get("receipt_id") is not None:
        failures.append("fixtures/ecosystem-chat/response.example.json: receipt_id must be null")
    profile_wrapper = {"interaction_bands": INTERACTION_BANDS, "interaction_profile": data.get("interaction_profile"), "math_solver_supported": True}
    failures.extend(require_interaction_contract(profile_wrapper, "fixtures/ecosystem-chat/response.example.json"))
    return failures


def check_sdk_payload_fixture() -> list[str]:
    payload, failures = load_json("fixtures/ecosystem-chat/sdk-form-payload.example.json")
    if failures:
        return failures
    failures = []
    if set(payload) != REQUIRED_PAYLOAD_KEYS:
        return ["fixtures/ecosystem-chat/sdk-form-payload.example.json: top-level keys must be fields, manifest, receipt_window"]
    sections = {"fields": REQUIRED_FORM_KEYS, "manifest": REQUIRED_MANIFEST_KEYS, "receipt_window": REQUIRED_RECEIPT_WINDOW_KEYS}
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
    for key in ["raw_shell_allowed", "site_receipt_authority", "site_shell_authority", "site_credential_authority"]:
        section = manifest if key == "raw_shell_allowed" else receipt_window
        if section.get(key) is not False:
            failures.append(f"fixtures/ecosystem-chat/sdk-form-payload.example.json: {key} must be false")
    if manifest.get("authority_required") is not True:
        failures.append("fixtures/ecosystem-chat/sdk-form-payload.example.json: manifest authority_required must be true")
    if not isinstance(receipt_window.get("correctness_errors"), list):
        failures.append("fixtures/ecosystem-chat/sdk-form-payload.example.json: correctness_errors must be a list")
    failures.extend(require_interaction_contract(manifest, "fixtures/ecosystem-chat/sdk-form-payload.example.json manifest"))
    failures.extend(require_interaction_contract(receipt_window, "fixtures/ecosystem-chat/sdk-form-payload.example.json receipt_window"))
    return failures


def check_sdk_backend_response_fixture() -> list[str]:
    response, failures = load_json("fixtures/ecosystem-chat/sdk-backend-response.example.json")
    if failures:
        return failures
    failures = []
    if set(response) != REQUIRED_BACKEND_RESPONSE_KEYS:
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: keys must be accepted, routed_module, receipt_id, next_action, errors")
    if response.get("receipt_id") is not None:
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: receipt_id must be null before backend activation")
    if not isinstance(response.get("accepted"), bool):
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: accepted must be boolean")
    if not isinstance(response.get("errors"), list):
        failures.append("fixtures/ecosystem-chat/sdk-backend-response.example.json: errors must be a list")
    return failures


def check_boundary_task_fixture() -> list[str]:
    task, failures = load_json(BOUNDARY_TASK_PATH)
    if failures:
        return failures
    checks = []
    if task.get("task_id") != BOUNDARY_TASK_ID:
        checks.append(f"{BOUNDARY_TASK_PATH}: task_id drift")
    if task.get("command") != ["python", BOUNDARY_SCRIPT]:
        checks.append(f"{BOUNDARY_TASK_PATH}: command drift")
    if task.get("authority_class") != "ordinary_analysis":
        checks.append(f"{BOUNDARY_TASK_PATH}: authority_class must remain ordinary_analysis")
    expected_inputs = task.get("expected_inputs")
    if not isinstance(expected_inputs, list):
        checks.append(f"{BOUNDARY_TASK_PATH}: expected_inputs must be a list")
    else:
        for required_input in ["docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md", "scripts/check_ecosystem_chat_contract.py"]:
            if required_input not in expected_inputs:
                checks.append(f"{BOUNDARY_TASK_PATH}: expected_inputs must include {required_input}")
    return checks


if __name__ == "__main__":
    raise SystemExit(main())
