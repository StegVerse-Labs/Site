#!/usr/bin/env python
"""
scripts/cfp_fetch.py

Fetches CFP data from SCW-API (CFP_API_URL) and writes:
- data/cfp-data.json   (full payload)
- data/cfp-teams.json  (team lookup map, if present)
"""

import json
import os
import sys
from pathlib import Path

import requests


def main() -> int:
    api_url = os.environ.get("CFP_API_URL", "").strip()
    if not api_url:
        print("CFP_API_URL env var is not set.", file=sys.stderr)
        return 1

    print(f"[cfp_fetch] Fetching CFP data from: {api_url}")

    try:
        resp = requests.get(api_url, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"[cfp_fetch] ERROR calling CFP API: {e}", file=sys.stderr)
        return 1

    try:
        payload = resp.json()
    except Exception as e:
        print(f"[cfp_fetch] ERROR parsing JSON: {e}", file=sys.stderr)
        return 1

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # 1) Write the full payload
    full_path = data_dir / "cfp-data.json"
    with full_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    print(f"[cfp_fetch] Wrote full payload -> {full_path}")

    # 2) Try to extract a team map for team pages
    teams = None

    # preferred key
    if isinstance(payload, dict):
        if isinstance(payload.get("teams"), dict):
            teams = payload["teams"]
        elif isinstance(payload.get("team_index"), dict):
            teams = payload["team_index"]
        # fall back: if there's a list of rankings with embedded team objects
        elif isinstance(payload.get("rankings"), list):
            tmap = {}
            for item in payload["rankings"]:
                team = item.get("team") or {}
                code = team.get("code") or team.get("id") or team.get("short_name")
                if code:
                    tmap[code] = team
            if tmap:
                teams = tmap

    if teams is not None:
        teams_path = data_dir / "cfp-teams.json"
        with teams_path.open("w", encoding="utf-8") as f:
            json.dump(teams, f, indent=2, sort_keys=True)
        print(f"[cfp_fetch] Wrote team map -> {teams_path}")
    else:
        print("[cfp_fetch] No team map found in payload; skipping cfp-teams.json")

    print("[cfp_fetch] Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
