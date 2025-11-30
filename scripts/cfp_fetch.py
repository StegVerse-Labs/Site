#!/usr/bin/env python3
"""
CFP data fetcher for StegVerse-Labs/Site.

- Reads CFP_API_URL from GitHub Actions secrets / env.
- Calls {CFP_API_URL}/api/cfp.
- If the endpoint is missing (404) or any error occurs, it logs a warning
  and exits with code 0 so the workflow stays green and existing JSON files
  are left untouched.
- When a real API is available, it will write any returned blobs into:

  data/cfp-2025.json
  data/cfp-data.json
  data/cfp-teams.json
  data/cfp-tickets.json
  data/ncaaf-2025.json
"""

import os
import sys
import json
from pathlib import Path

import requests


def main() -> int:
    base = os.getenv("CFP_API_URL", "").strip()
    if not base:
        print("[cfp_fetch] CFP_API_URL not set; skipping (no changes).")
        return 0

    base = base.rstrip("/")
    url = f"{base}/api/cfp"
    print(f"[cfp_fetch] Fetching CFP data from: {url}")

    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 404:
            print("[cfp_fetch] WARNING: /api/cfp not found on SCW-API yet; "
                  "leaving existing CFP data as-is.")
            return 0
        resp.raise_for_status()
        payload = resp.json()
    except Exception as e:
        print(f"[cfp_fetch] WARNING: could not fetch CFP data: {e}")
        print("[cfp_fetch] Leaving existing CFP data as-is.")
        return 0

    # Where our JSON lives in this repo
    root = Path(__file__).resolve().parents[1] / "data"

    mapping = {
        "cfp_2025": "cfp-2025.json",
        "cfp_data": "cfp-data.json",
        "cfp_teams": "cfp-teams.json",
        "cfp_tickets": "cfp-tickets.json",
        "ncaaf_2025": "ncaaf-2025.json",
    }

    changed = False
    for key, filename in mapping.items():
        if key not in payload:
            continue
        target = root / filename
        new_content = json.dumps(payload[key], indent=2, sort_keys=True)
        old_content = ""
        if target.exists():
            try:
                old_content = target.read_text()
            except Exception:
                old_content = ""

        if old_content.strip() != new_content.strip():
            target.write_text(new_content + "\n")
            changed = True
            print(f"[cfp_fetch] Updated {filename}")

    if not changed:
        print("[cfp_fetch] No changes detected in CFP data.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
