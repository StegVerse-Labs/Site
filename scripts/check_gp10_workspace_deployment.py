#!/usr/bin/env python3
"""Fail closed unless deployed GP10 pages exactly match the committed source."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = "https://stegverse-labs.github.io/Site"
PAGES = {
    "gp10-workspace.html": [
        "Content-Security-Policy",
        'content="no-referrer"',
        "assets/gp10-security.js",
        "noindex,nofollow,noarchive",
        "No execution authority",
    ],
    "gp10-workspace-examples.html": [
        "Content-Security-Policy",
        'content="no-referrer"',
        "assets/gp10-security.js",
        "noindex,nofollow,noarchive",
        "No execution authority",
    ],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "StegVerse-GP10-Deployment-Observer/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read()


def observe(base_url: str, timeout: int) -> tuple[bool, list[dict]]:
    observations: list[dict] = []
    all_match = True
    cache_buster = int(time.time())
    for name, markers in PAGES.items():
        local = (ROOT / name).read_bytes()
        url = f"{base_url.rstrip('/')}/{name}?gp10_observation={cache_buster}"
        item = {
            "page": name,
            "url": url,
            "local_sha256": sha256(local),
            "remote_sha256": None,
            "exact_match": False,
            "markers": {},
            "error": None,
        }
        try:
            remote = fetch(url, timeout)
            text = remote.decode("utf-8", errors="replace")
            item["remote_sha256"] = sha256(remote)
            item["exact_match"] = remote == local
            item["markers"] = {marker: marker in text for marker in markers}
            if not item["exact_match"] or not all(item["markers"].values()):
                all_match = False
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            item["error"] = f"{type(exc).__name__}: {exc}"
            all_match = False
        observations.append(item)
    return all_match, observations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay-seconds", type=int, default=20)
    parser.add_argument("--timeout-seconds", type=int, default=20)
    parser.add_argument("--commit", default="UNKNOWN")
    parser.add_argument("--run-id", default="UNKNOWN")
    parser.add_argument("--output", default="validation/gp10-workspace-deployment-receipt.json")
    args = parser.parse_args()

    started = datetime.now(timezone.utc).isoformat()
    final_observations: list[dict] = []
    passed = False
    used_attempt = 0

    for attempt in range(1, max(args.attempts, 1) + 1):
        used_attempt = attempt
        passed, final_observations = observe(args.base_url, args.timeout_seconds)
        if passed:
            break
        if attempt < args.attempts:
            time.sleep(max(args.delay_seconds, 0))

    receipt = {
        "receipt_type": "GP10_SITE_DEPLOYMENT_OBSERVATION",
        "schema_version": "1.0.0",
        "tested_commit": args.commit,
        "workflow_run_id": args.run_id,
        "base_url": args.base_url,
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "attempts_used": used_attempt,
        "result": "PASS" if passed else "FAILED",
        "comparison": "EXACT_REMOTE_BYTES_EQUAL_COMMITTED_SOURCE",
        "observations": final_observations,
        "execution_authority": False,
        "limitations": [
            "A matching deployment does not establish source truth, evidence custody, approval, certification, or execution authority.",
            "This receipt observes only the named static pages and committed security markers.",
        ],
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
