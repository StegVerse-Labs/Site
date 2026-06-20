#!/usr/bin/env python3
"""Validate the text-only Ecosystem Chat activation surface.

This checker is intentionally static. It verifies that the public Site page,
browser-side script, gateway contract, activation status, gateway fixtures,
workflow gate, iOS path mapping, and README continue to preserve the
public-mirror boundary and the gateway handoff contract.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "ecosystem-chat.html": [
        "<script src=\"assets/ecosystem-chat.js\"></script>",
        "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
        "POST /api/ecosystem-chat",
        "Site is a public mirror and command surface",
        "receipt_id",
    ],
    "assets/ecosystem-chat.js": [
        "const STEGVERSE_GATEWAY_PATH = '/api/ecosystem-chat';",
        "const STEGVERSE_LOCAL_MODE = true;",
        "Gateway request failed; fail-closed to local classification.",
        "receipt=not-issued",
        "repo: 'StegVerse-Labs/Site'",
    ],
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md": [
        "The browser page must not become proof authority",
        "POST /api/ecosystem-chat",
        "receipt_id",
        "Local transcript hashes are not proof receipts.",
        "Only the appropriate governed backend authority may issue a proof receipt.",
        "fixtures/ecosystem-chat/request.example.json",
        "fixtures/ecosystem-chat/response.example.json",
    ],
    "docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md": [
        "Backend gateway state: not installed",
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
    ".github/workflows/check-ecosystem-chat.yml": [
        "name: Check Ecosystem Chat Contract",
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
        "[`fixtures/ecosystem-chat/request.example.json`](fixtures/ecosystem-chat/request.example.json)",
        "[`fixtures/ecosystem-chat/response.example.json`](fixtures/ecosystem-chat/response.example.json)",
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


if __name__ == "__main__":
    sys.exit(main())
