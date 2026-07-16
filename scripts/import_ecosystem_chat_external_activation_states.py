#!/usr/bin/env python3
"""Import durable Ecosystem Chat activation states from their owner repositories.

The import is network-tolerant and fail-closed. Missing external evidence remains pending;
it never becomes a successful gate and never requires a user to download or copy artifacts.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DESTINATION_OUTPUT = DATA / "ecosystem-chat-destination-activation-state.external.json"
CUSTODY_OUTPUT = DATA / "ecosystem-chat-custody-activation-state.external.json"
STATUS_OUTPUT = DATA / "ecosystem-chat-external-activation-import-status.json"
DESTINATION_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-destination-activation-state.json"
CUSTODY_API_URL = "https://api.github.com/repos/master-records/orchestration/contents/reports/ecosystem-chat-custody-activation-state.json?ref=main"


def canonical_sha256(value: dict[str, Any]) -> str:
    binding = dict(value)
    binding.pop("state_sha256", None)
    encoded = json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate(value: Any, record_type: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("external activation state must be a JSON object")
    if value.get("record_type") != record_type:
        raise ValueError(f"unexpected record_type: {value.get('record_type')}")
    if value.get("manual_user_action_required") is not False:
        raise ValueError("external activation state must explicitly eliminate manual user action")
    expected = value.get("state_sha256")
    actual = canonical_sha256(value)
    if not expected or expected != actual:
        raise ValueError("external activation state hash mismatch")
    if not isinstance(value.get("gates"), dict):
        raise ValueError("external activation state gates must be an object")
    return value


def fetch_json(url: str, *, token: str | None = None, github_contents: bool = False) -> dict[str, Any]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "StegVerse-Site-Activation-Importer/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        value = json.loads(response.read().decode("utf-8"))
    if github_contents:
        if not isinstance(value, dict) or value.get("encoding") != "base64" or not value.get("content"):
            raise ValueError("GitHub contents response did not include base64 content")
        decoded = base64.b64decode(value["content"]).decode("utf-8")
        value = json.loads(decoded)
    return value


def preserve_or_write(path: Path, value: dict[str, Any] | None) -> bool:
    if value is None:
        return path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> int:
    token = os.getenv("STEGVERSE_REPO_SYNC_TOKEN", "").strip() or None
    errors: dict[str, str] = {}
    destination: dict[str, Any] | None = None
    custody: dict[str, Any] | None = None

    try:
        destination = validate(
            fetch_json(DESTINATION_URL),
            "ecosystem_chat_destination_activation_state",
        )
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError) as exc:
        errors["destination"] = str(exc)

    if token:
        try:
            custody = validate(
                fetch_json(CUSTODY_API_URL, token=token, github_contents=True),
                "ecosystem_chat_custody_activation_state",
            )
        except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError) as exc:
            errors["custody"] = str(exc)
    else:
        errors["custody"] = "STEGVERSE_REPO_SYNC_TOKEN not available; retained prior checked-in state if present"

    destination_present = preserve_or_write(DESTINATION_OUTPUT, destination)
    custody_present = preserve_or_write(CUSTODY_OUTPUT, custody)
    state = "VERIFIED_EXTERNAL_STATES_IMPORTED" if destination is not None and custody is not None else "EXTERNAL_STATES_PARTIAL_OR_STALE"
    status = {
        "schema_version": "1.0.0",
        "record_type": "ecosystem_chat_external_activation_import_status",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": state,
        "manual_user_action_required": False,
        "destination": {
            "freshly_imported": destination is not None,
            "checked_in_state_present": destination_present,
            "sha256": canonical_sha256(destination) if destination else None,
            "source": DESTINATION_URL,
        },
        "custody": {
            "freshly_imported": custody is not None,
            "checked_in_state_present": custody_present,
            "sha256": canonical_sha256(custody) if custody else None,
            "source": "master-records/orchestration:reports/ecosystem-chat-custody-activation-state.json",
        },
        "errors": errors,
        "authority_boundary": {
            "import_grants_deployment_authority": False,
            "import_grants_mutation_authority": False,
            "import_grants_custody_authority": False,
            "import_grants_release_authority": False,
        },
    }
    DATA.mkdir(parents=True, exist_ok=True)
    STATUS_OUTPUT.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"ECOSYSTEM CHAT EXTERNAL ACTIVATION IMPORT: {state}")
    print(f"Destination state present: {destination_present}")
    print(f"Custody state present: {custody_present}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
