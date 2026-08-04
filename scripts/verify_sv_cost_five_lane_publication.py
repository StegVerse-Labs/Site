#!/usr/bin/env python3
"""Verify the deployed bounded five-lane publication and emit a durable receipt."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TARGET = os.environ.get(
    "SV_COST_PUBLIC_URL",
    "https://stegverse.org/papers/sv-cost-relational-analysis.html",
)
OUTPUT = Path(
    os.environ.get(
        "SV_COST_PUBLIC_RECEIPT",
        "papers/sv-cost-five-lane-public-verification.json",
    )
)
MARKERS = [
    "Five-Lane Cost Results for Reconstructable Governance",
    "OpenAI raw",
    "$0.006875",
    "OpenAI governed",
    "$0.006880",
    "Anthropic raw",
    "$0.010656",
    "Anthropic governed",
    "$0.007116",
    "StegVerse-only",
    "$0.000000002885",
    "universal provider economics",
    "company ROI",
    "fresh-inference equivalence",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_once(url: str) -> tuple[int, bytes, str]:
    cache_bust = urllib.parse.urlencode({"sv_cost_verify": str(int(time.time()))})
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        url + separator + cache_bust,
        headers={
            "User-Agent": "StegVerse-SV-COST-Publication-Verifier/1.0",
            "Accept": "text/html,application/xhtml+xml",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        return int(response.status), body, response.geturl()


def main() -> int:
    observed_at = utc_now()
    attempts: list[dict[str, object]] = []
    status = 0
    body = b""
    final_url = TARGET
    error = None

    for attempt in range(1, 6):
        try:
            status, body, final_url = fetch_once(TARGET)
            attempts.append({"attempt": attempt, "http_status": status, "bytes": len(body)})
            if status == 200 and body:
                break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            error = f"{type(exc).__name__}: {exc}"
            attempts.append({"attempt": attempt, "error": error})
        if attempt < 5:
            time.sleep(attempt * 3)

    text = body.decode("utf-8", errors="replace")
    marker_checks = {marker: marker in text for marker in MARKERS}
    all_markers = all(marker_checks.values())
    complete = status == 200 and all_markers

    receipt = {
        "schema_version": "1.0.0",
        "task_id": "SV-COST-FIVE-LANE-PUBLIC-BODY-VERIFY-001",
        "originating_goal": "Publish and verify SV-COST-FIVE-LANE-RESULTS-001 with bounded claims",
        "observed_at": observed_at,
        "target_url": TARGET,
        "final_url": final_url,
        "http_status": status or None,
        "response_bytes": len(body),
        "content_sha256": "sha256:" + hashlib.sha256(body).hexdigest() if body else None,
        "marker_checks": marker_checks,
        "all_required_markers_present": all_markers,
        "attempts": attempts,
        "last_error": error,
        "state": "COMPLETE" if complete else "BLOCKED_RETRY",
        "publication_claim_boundary": (
            "One bounded deterministic reconstruction operation; no universal provider economics, "
            "enterprise-wide savings, company ROI, or fresh-inference equivalence."
        ),
        "source_commit": os.environ.get("GITHUB_SHA"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "next_executable_action": (
            "Release claim and close StegVerse-Labs/Site#173"
            if complete
            else "Retry through .github/workflows/sv-cost-five-lane-public-verification.yml"
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if complete else 1


if __name__ == "__main__":
    sys.exit(main())
