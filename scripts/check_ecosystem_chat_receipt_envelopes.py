#!/usr/bin/env python3
"""Validate authority, execution, transition identity, and gateway preview contracts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "fixtures" / "ecosystem-chat" / "authority-receipt-envelope.example.json"
EXEC = ROOT / "fixtures" / "ecosystem-chat" / "execution-receipt-envelope.example.json"
NESTED_VALIDATORS = [
    ROOT / "scripts" / "check_ecosystem_chat_transition_identity.py",
    ROOT / "scripts" / "check_ecosystem_chat_gateway_activation.py",
]


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain an object")
    return data


def validate_common(data: dict, expected_type: str) -> int | None:
    if data.get("payload_type") != expected_type:
        return fail(f"{expected_type} payload_type drift")
    if data.get("preview_only") is not True:
        return fail(f"{expected_type} must remain preview_only")
    if data.get("live_signature") is not False:
        return fail(f"{expected_type} must not claim a live signature")
    issuer = data.get("issuer", {})
    if issuer.get("class") != "governed_backend_authority":
        return fail(f"{expected_type} issuer class drift")
    if issuer.get("verified") is not False:
        return fail(f"{expected_type} preview issuer must remain unverified")
    crypto = data.get("cryptographic_shape", {})
    if crypto.get("digest_algorithm") != "sha256":
        return fail(f"{expected_type} digest algorithm must be sha256")
    if not str(crypto.get("digest", "")).startswith("sha256:preview-"):
        return fail(f"{expected_type} digest must be clearly preview-shaped")
    for key in ("signature_algorithm", "signature", "key_id"):
        if crypto.get(key) is not None:
            return fail(f"{expected_type} {key} must remain null")
    replay = data.get("replay", {})
    for key in ("request_replayable", "decision_replayable", "input_pointers_present"):
        if replay.get(key) is not True:
            return fail(f"{expected_type} replay.{key} must be true")
    if replay.get("inputs_embedded") is not False:
        return fail(f"{expected_type} must use pointers rather than embedded inputs")
    reconstruction = data.get("reconstruction", {})
    if reconstruction.get("reconstructable") is not True:
        return fail(f"{expected_type} must remain reconstructable")
    if not isinstance(reconstruction.get("required_artifacts"), list) or not reconstruction["required_artifacts"]:
        return fail(f"{expected_type} requires reconstruction artifacts")
    supersession = data.get("supersession", {})
    if supersession.get("status") != "CURRENT_PREVIEW":
        return fail(f"{expected_type} supersession status drift")
    if supersession.get("supersedes_receipt_id") is not None or supersession.get("superseded_by_receipt_id") is not None:
        return fail(f"{expected_type} preview must not claim supersession links")
    return None


def main() -> int:
    authority = load(AUTH)
    execution = load(EXEC)

    result = validate_common(authority, "authority_receipt_envelope_preview")
    if result is not None:
        return result
    result = validate_common(execution, "execution_receipt_envelope_preview")
    if result is not None:
        return result

    auth_binding = authority.get("binding", {})
    if auth_binding.get("request_id") != "ahr_site_preview_allow_001":
        return fail("authority receipt request binding drift")
    if auth_binding.get("transition_type") != "authority_evaluation":
        return fail("authority transition type drift")
    if auth_binding.get("result") != "ALLOW":
        return fail("authority receipt must bind ALLOW")
    if auth_binding.get("scope") != ["ecosystem_chat.gateway.evaluate"]:
        return fail("authority receipt scope drift")
    if auth_binding.get("commit_time_validity") != "PASS":
        return fail("authority receipt commit-time validity must pass")

    exec_binding = execution.get("binding", {})
    if exec_binding.get("request_id") != "etr_site_preview_001":
        return fail("execution receipt request binding drift")
    if exec_binding.get("transition_type") != "execution_transition":
        return fail("execution transition type drift")
    if exec_binding.get("result") != "DRY_RUN_ONLY":
        return fail("execution receipt must bind DRY_RUN_ONLY")
    if exec_binding.get("authority_request_id") != auth_binding.get("request_id"):
        return fail("execution receipt must bind the authority request")
    if exec_binding.get("authority_result") != "ALLOW":
        return fail("execution receipt authority result must remain ALLOW")
    if exec_binding.get("commit_time_validity") != "PASS":
        return fail("execution receipt commit-time validity must pass")
    if exec_binding.get("state_change") is not False or exec_binding.get("rollback_performed") is not False:
        return fail("dry-run receipt must show no state change or rollback")
    resource_use = exec_binding.get("resource_use", {})
    if any(value not in (0, 0.0) for value in resource_use.values()):
        return fail("dry-run receipt resource use must remain zero")

    auth_required = set(authority["reconstruction"]["required_artifacts"])
    exec_required = set(execution["reconstruction"]["required_artifacts"])
    if "authority-handshake-positive-request.example.json" not in auth_required:
        return fail("authority reconstruction is missing request fixture")
    if "authority-receipt-envelope.example.json" not in exec_required:
        return fail("execution reconstruction is missing authority receipt pointer")

    for validator in NESTED_VALIDATORS:
        if not validator.exists():
            return fail(f"nested validator missing: {validator.name}")
        completed = subprocess.run(
            [sys.executable, str(validator)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(completed.stdout, end="")
        if completed.returncode != 0:
            return fail(f"nested contract failed: {validator.name}")

    print("PASS: receipt envelopes, transition identity, and governed gateway contract are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
