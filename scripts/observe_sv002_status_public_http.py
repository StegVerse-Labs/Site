#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PAGE_URL = "https://stegverse.org/sv002-status/"
STATUS_URL = "https://stegverse.org/data/sv002-experiment-status.json"
PAGE_MARKERS = (
    "EXPERIMENT EFFECTS: TRANSITION-ELEMENT DERIVED",
    "Completing self-characterization does not self-promote StegVerse-002",
)
EXPECTED_EFFECT = "DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS"


def validate(page_text: str, status: dict[str, Any]) -> dict[str, bool]:
    t = status.get("principal_transition_semantics") or {}
    life = status.get("adjacent_lifecycle_goal") or {}
    return {
        "page_transition_marker": all(marker in page_text for marker in PAGE_MARKERS),
        "status_projection_non_authorizing": status.get("authority_effect") == "NONE_STATUS_ONLY",
        "authority_transfer_not_assumed": t.get("authority_transfer_assumed") is False,
        "transition_effect_resolution": t.get("authority_effect_resolution") == EXPECTED_EFFECT,
        "capability_realization_is_transition_evidence": t.get("capability_realization_is_transition_evidence") is True,
        "capability_realization_not_preclaimed": t.get("capability_realization_observed") is False,
        "transition_effect_not_yet_evaluated": t.get("transition_effect_state") == "NOT_YET_EVALUATED",
        "lifecycle_self_promotion_false": t.get("lifecycle_self_promotion") is False,
        "system_ai_active_false": life.get("system_ai_active") is False,
    }


def fetch(url: str, *, attempt: int) -> tuple[int, bytes, dict[str, str]]:
    separator = "&" if "?" in url else "?"
    target = f"{url}{separator}proof_attempt={attempt}&ts={int(time.time())}"
    req = urllib.request.Request(
        target,
        headers={
            "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "StegVerse-SV002-Status-Observer/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read()
        headers = {k.lower(): v for k, v in response.headers.items()}
        return int(response.status), body, headers


def observe(output_dir: Path, *, attempts: int = 20, delay_seconds: int = 10) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            page_code, page_body, page_headers = fetch(PAGE_URL, attempt=attempt)
            json_code, json_body, json_headers = fetch(STATUS_URL, attempt=attempt)
            page_text = page_body.decode("utf-8", "replace")
            status = json.loads(json_body)
            if not isinstance(status, dict):
                raise RuntimeError("status endpoint returned non-object JSON")
            checks = validate(page_text, status)
            passed = page_code == 200 and json_code == 200 and all(checks.values())
            receipt = {
                "schema": "stegverse.sv002-status-public-http-proof/v1",
                "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "attempt": attempt,
                "page_url": PAGE_URL,
                "status_url": STATUS_URL,
                "page_http_status": page_code,
                "status_http_status": json_code,
                "page_sha256": hashlib.sha256(page_body).hexdigest(),
                "status_sha256": hashlib.sha256(json_body).hexdigest(),
                "checks": checks,
                "result": "PASS" if passed else "FAIL",
                "authority_effect": False,
                "activation_effect": False,
                "execution_authority": False,
                "experiment_authority": False,
                "github_actions_runtime_authority": False,
            }
            (output_dir / "page.html").write_bytes(page_body)
            (output_dir / "status.json").write_bytes(json_body)
            (output_dir / "page-headers.json").write_text(json.dumps(page_headers, indent=2, sort_keys=True) + "\n")
            (output_dir / "status-headers.json").write_text(json.dumps(json_headers, indent=2, sort_keys=True) + "\n")
            (output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            if passed:
                return receipt
            last_error = f"public content did not satisfy checks on attempt {attempt}"
        except Exception as exc:
            last_error = repr(exc)
        if attempt < attempts:
            time.sleep(delay_seconds)
    fail = {
        "schema": "stegverse.sv002-status-public-http-proof/v1",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": "FAIL",
        "error": last_error,
        "authority_effect": False,
        "activation_effect": False,
        "execution_authority": False,
        "experiment_authority": False,
        "github_actions_runtime_authority": False,
    }
    (output_dir / "receipt.json").write_text(json.dumps(fail, indent=2, sort_keys=True) + "\n")
    return fail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/sv002-status-public-http"))
    parser.add_argument("--attempts", type=int, default=20)
    parser.add_argument("--delay-seconds", type=int, default=10)
    args = parser.parse_args()
    receipt = observe(args.output_dir, attempts=args.attempts, delay_seconds=args.delay_seconds)
    print("SV002_STATUS_PUBLIC_HTTP_" + receipt["result"])
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
