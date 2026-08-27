#!/usr/bin/env python3
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "governance-observatory-v0.1.0-public-observation.json"
BASE_URL = "https://stegverse.org/governance-observatory.html"
EXPECTED = [
    "Versioned release",
    "v0.1.0",
    "Release record",
    "377486341",
    "Historical snapshot",
]

def main() -> int:
    sha = os.environ.get("GITHUB_SHA", "unknown")
    query = urllib.parse.urlencode({"verify_sha": sha})
    url = f"{BASE_URL}?{query}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "StegVerse-Site-public-verifier/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    observed_at = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "record_type": "site_governance_observatory_public_observation",
        "source_sha": sha,
        "public_url": BASE_URL,
        "request_url": url,
        "observed_at": observed_at,
        "expected_markers": EXPECTED,
        "status": "FAIL_CLOSED",
        "http_status": None,
        "missing_markers": EXPECTED,
        "authority_effect": False,
        "activation_effect": False,
    }
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            result["http_status"] = getattr(resp, "status", None)
            missing = [marker for marker in EXPECTED if marker not in body]
            result["missing_markers"] = missing
            result["status"] = "PASS" if not missing else "STALE_OR_INCOMPLETE_PUBLIC_CONTENT"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
