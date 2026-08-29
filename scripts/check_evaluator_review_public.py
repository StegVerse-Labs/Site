#!/usr/bin/env python3
"""Observe the published evaluator-review v0.2 projection without authority.

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

EXPECTED_SDK_HEAD = "c9b8935309e69d3a6f70e4ad4ef5dd55fb8a9aac"
EXPECTED_SOURCE_BLOB = "2dd0468779975d18ad53dfe400e1d2fcf83650c3"
EXPECTED_VECTOR_SCHEMA = "stegverse.cross-framework-current-basis-vector.v0.2"

HTML_MARKERS = [
    "StegVerse — Evaluator Review",
    "Governed test review",
    "PUBLIC READ",
    "Not yet executed",
    "Approve this version",
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
    input_data = manifest.get("input", {}).get("input_data", {})
    transition = input_data.get("transition", {})
    boundary = input_data.get("comparison_boundary", {})
    controls = input_data.get("controls", [])
    control_ids = {control.get("control_id") for control in controls if isinstance(control, dict)}

    checks = {
        "review_schema": projection.get("review_schema") == "stegverse.evaluator-review.v1",
        "public_read": projection.get("access_mode") == "PUBLIC_READ",
        "source_head": source.get("source_head_sha") == EXPECTED_SDK_HEAD,
        "source_blob": source.get("source_blob_sha") == EXPECTED_SOURCE_BLOB,
        "test_version": test.get("version") == 2,
        "test_state": test.get("state") == "DRAFT",
        "freeze_state": input_data.get("freeze_state") == "DRAFT_PRE_FREEZE",
        "vector_schema": input_data.get("vector_schema") == EXPECTED_VECTOR_SCHEMA,
        "changed_basis": transition.get("changed_condition") == "CURRENT_POLICY_BASIS_CHANGED",
        "invalidation_not_asserted": transition.get("invalidation_asserted_as_input") is False,
        "standing_independent": boundary.get("current_standing_is_independently_determined") is True,
        "valid_continuity_control": "VALID_CONTINUITY_CONTROL" in control_ids,
        "known_invalidation_control": "KNOWN_INVALIDATION_CONTROL" in control_ids,
        "approvals_absent": projection.get("approvals") == [],
        "frozen_absent": test.get("frozen_manifest_hash") is None and test.get("frozen_at") is None,
        "execution_not_run": test.get("execution_state") == "NOT_RUN",
        "results_absent": projection.get("results") is None,
    }
    observation["checks"] = checks
    observation["sdk_head"] = source.get("source_head_sha")
    observation["source_blob_sha"] = source.get("source_blob_sha")
    observation["test_version"] = test.get("version")
    observation["freeze_state"] = input_data.get("freeze_state")

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
    print("draft_state=DRAFT_PRE_FREEZE")
    print("approval=false")
    print("frozen=false")
    print("executed=false")
    print("results_available=false")
    print("authority_effect=NONE")
    print("activation_effect=false")
    print(f"report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
