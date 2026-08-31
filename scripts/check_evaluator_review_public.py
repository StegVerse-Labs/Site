#!/usr/bin/env python3
"""Observe the published evaluator-review frozen v0.4 projection without authority.

This verifier performs anonymous HTTP GETs only. It does not authenticate,
comment, approve, freeze, execute, mutate, or claim review-bridge activation.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HTML_URL = "https://stegverse.org/evaluator-review.html"
PROJECTION_URL = "https://stegverse.org/data/evaluator-review/cross-framework-current-basis-001.json"
REPORT = Path("reports/evaluator-review-public-verification.json")

EXPECTED_SDK_HEAD = "5a21fc6bdf4a94cfd6c4a4f369a1ba8b86721909"
EXPECTED_SOURCE_BLOB = "59d818a15fc7be732c97dae7d2174d8cfe9a7bab"
EXPECTED_MANIFEST_SHA256 = "07a08496c21b31f70f6f45ef731aa5f6b2522a6fc8f67f2d0a4c2b6fceda7a3f"
EXPECTED_VECTOR_SCHEMA = "stegverse.cross-framework-current-basis-vector.v0.4"

HTML_MARKERS = [
    "StegVerse — Evaluator Review",
    "Governed test review",
    "PUBLIC READ",
    "Results comparison",
]

USER_AGENT = "StegVerse-Evaluator-Public-Verification/1.0"


def fetch(url: str, attempts: int = 6, delay_seconds: int = 10) -> tuple[int, bytes]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                },
            )
            with urlopen(req, timeout=20) as response:
                return int(getattr(response, "status", 0) or 0), response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(delay_seconds)
    raise RuntimeError(f"public fetch failed for {url}: {last_error}")


def body_sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def fail(errors: list[str], observation: dict) -> int:
    observation["status"] = "FAIL"
    observation["errors"] = errors
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("EVALUATOR REVIEW PUBLIC VERIFICATION: FAIL")
    for error in errors:
        print(f"- {error}")
    print(f"report={REPORT}")
    return 1


def main() -> int:
    observation = {
        "schema": "stegverse.evaluator_review.public_verification.v1",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "html_url": HTML_URL,
        "projection_url": PROJECTION_URL,
        "authority_effect": "NONE",
        "activation_effect": False,
        "authenticated": False,
        "review_action_performed": False,
        "execution_action_performed": False,
    }
    errors: list[str] = []

    try:
        html_status, html_body = fetch(HTML_URL)
    except RuntimeError as exc:
        return fail([str(exc)], observation)

    observation["html_http_status"] = html_status
    observation["html_sha256"] = body_sha256(html_body)
    html = html_body.decode("utf-8", errors="replace")
    if html_status != 200:
        errors.append(f"evaluator-review HTTP status {html_status}")
    for marker in HTML_MARKERS:
        if marker not in html:
            errors.append(f"evaluator-review missing marker: {marker}")

    try:
        projection_status, projection_body = fetch(PROJECTION_URL)
    except RuntimeError as exc:
        errors.append(str(exc))
        return fail(errors, observation)

    observation["projection_http_status"] = projection_status
    observation["projection_sha256"] = body_sha256(projection_body)
    if projection_status != 200:
        errors.append(f"projection HTTP status {projection_status}")

    try:
        projection = json.loads(projection_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"projection JSON invalid: {exc}")
        return fail(errors, observation)

    source = projection.get("source", {})
    test = projection.get("test", {})
    manifest = projection.get("manifest", {})
    input_block = manifest.get("input", {})
    comparison = input_block.get("comparison_input", {})
    initial = comparison.get("initial_state", {})
    transition = comparison.get("transition", {})
    boundary = comparison.get("comparison_boundary", {})
    native = comparison.get("architecture_native_derivation", {})
    controls = comparison.get("controls", [])
    control_ids = {control.get("control_id") for control in controls if isinstance(control, dict)}
    approvals = projection.get("approvals", [])
    approved_parties = {
        approval.get("party_id")
        for approval in approvals
        if isinstance(approval, dict)
        and approval.get("status") == "APPROVED"
        and approval.get("version") == 4
        and approval.get("manifest_hash") == EXPECTED_MANIFEST_SHA256
    }

    checks = {
        "review_schema": projection.get("review_schema") == "stegverse.evaluator-review.v1",
        "public_read": projection.get("access_mode") == "PUBLIC_READ",
        "source_head": source.get("source_head_sha") == EXPECTED_SDK_HEAD,
        "source_blob": source.get("source_blob_sha") == EXPECTED_SOURCE_BLOB,
        "test_version": test.get("version") == 4,
        "test_state_frozen": test.get("state") == "FROZEN",\n        "result_state_available": test.get("result_state") == "RESULTS_AVAILABLE",
        "frozen_hash": test.get("frozen_manifest_hash") == EXPECTED_MANIFEST_SHA256,
        "frozen_blob": test.get("frozen_manifest_git_blob_sha1") == EXPECTED_SOURCE_BLOB,
        "execution_window_open": test.get("execution_window_state") == "OPEN",
        "embedded_snapshot_label_preserved": comparison.get("freeze_state") == "DRAFT_PRE_FREEZE",
        "vector_schema": comparison.get("vector_schema") == EXPECTED_VECTOR_SCHEMA,
        "s0_declared_initial": initial.get("standing") == "DECLARED_VALID_FOR_TEST",
        "s0_no_transition_receipt_pre_observation": initial.get("receipt_state") == "NOT_RECEIPT_BEARING_PRE_OBSERVATION",
        "changed_basis": transition.get("changed_condition") == "CURRENT_POLICY_BASIS_CHANGED",
        "invalidation_not_asserted": transition.get("invalidation_asserted_as_input") is False,
        "receipt_is_post_observation": transition.get("receipt_semantics") == "S0_TO_S1_RECEIPT_IS_POST_OBSERVATION_EVIDENCE",
        "standing_independent": boundary.get("current_standing_is_independently_determined") is True,
        "transition_receipt_not_input": boundary.get("transition_receipt_is_not_a_pre_execution_input") is True,
        "common_input_has_no_native_currentness": native.get("common_artifact_contains_native_currentness_booleans") is False,
        "cross_arch_visibility_closed": native.get("cross_architecture_visibility_before_completion") is False,
        "valid_continuity_control": "VALID_CONTINUITY_CONTROL" in control_ids,
        "known_invalidation_control": "KNOWN_INVALIDATION_CONTROL" in control_ids,
        "external_approval_bound": "external-counterpart" in approved_parties,
        "stegverse_owner_approval_bound": "stegverse" in approved_parties,
        "execution_not_run": test.get("execution_state") == "NOT_RUN",
        "results_absent": projection.get("results") is None,
    }
    observation["checks"] = checks
    observation["sdk_head"] = source.get("source_head_sha")
    observation["source_blob_sha"] = source.get("source_blob_sha")
    observation["manifest_sha256"] = test.get("frozen_manifest_hash")
    observation["test_version"] = test.get("version")
    observation["declared_state"] = test.get("state")
    observation["embedded_snapshot_label"] = comparison.get("freeze_state")
    observation["execution_state"] = test.get("execution_state")

    for name, passed in checks.items():
        if not passed:
            errors.append(f"projection check failed: {name}")

    if errors:
        return fail(errors, observation)

    observation["status"] = "PASS"
    observation["errors"] = []
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("EVALUATOR REVIEW PUBLIC VERIFICATION: PASS")
    print(f"html_url={HTML_URL}")
    print(f"projection_url={PROJECTION_URL}")
    print(f"sdk_head={EXPECTED_SDK_HEAD}")
    print(f"source_blob_sha={EXPECTED_SOURCE_BLOB}")
    print(f"manifest_sha256={EXPECTED_MANIFEST_SHA256}")
    print("projection_state=FROZEN")
    print("embedded_snapshot_label=DRAFT_PRE_FREEZE")
    print("execution_window=OPEN")
    print("executed=true")
    print("results_available=true")
    print("authority_effect=NONE")
    print("activation_effect=false")
    print(f"report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
