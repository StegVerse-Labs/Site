#!/usr/bin/env python
import os
import sys
import json
import time
import datetime as dt
from pathlib import Path

import requests

# ---- Config ----

CFBD_API_KEY = os.getenv("CFBD_API_KEY", "").strip()
if not CFBD_API_KEY:
    print("ERROR: CFBD_API_KEY env var is not set.", file=sys.stderr)
    sys.exit(1)

# Adjust this if your data file is somewhere else
OUTPUT_PATH = Path("data/cfp-data.json")

CFBD_RANKINGS_URL = "https://api.collegefootballdata.com/rankings"

# ---- Helpers ----

def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def fetch_rankings(year: int):
    """Fetch rankings from CFBD and return JSON."""
    headers = {
        "Authorization": f"Bearer {CFBD_API_KEY}",
        "Accept": "application/json",
    }
    params = {"year": year}
    resp = requests.get(CFBD_RANKINGS_URL, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def pick_latest_cfp_snapshot(data):
    """
    CFBD rankings payload is a list of 'weeks', each with multiple polls.
    We pick the latest (max season/week) entry that has a CFP poll.
    """
    latest = None
    latest_key = None

    for entry in data:
        season = entry.get("season")
        week = entry.get("week")
        polls = entry.get("polls", [])

        for poll in polls:
            name = poll.get("name", "")
            # Look for CFP-style poll
            upper = name.upper()
            if "CFP" in upper or "PLAYOFF" in upper:
                key = (season, entry.get("seasonType", ""), week)
                if latest_key is None or key > latest_key:
                    latest_key = key
                    latest = {
                        "season": season,
                        "seasonType": entry.get("seasonType"),
                        "week": week,
                        "poll": poll,
                    }

    return latest


def build_payload_from_snapshot(snapshot):
    """
    Turn the CFBD snapshot into the cfp-data.json structure
    expected by the frontend.
    """
    if not snapshot:
        raise RuntimeError("No CFP snapshot found in rankings data.")

    season = snapshot["season"]
    week = snapshot["week"]
    poll = snapshot["poll"]
    poll_name = poll.get("name", "CFP Rankings")
    ranks = poll.get("ranks", [])

    # Build CFP Top 12 rankings for our main table
    rankings = []
    for r in ranks:
        rank = r.get("rank")
        if rank is None or rank > 12:
            continue
        team = r.get("school") or r.get("team") or "Unknown"
        conf = r.get("conference", "")
        rankings.append({
            "seed": rank,
            "team": team,
            "record": "-",            # CFBD rankings payload doesn't include record directly
            "conference": conf or "",
            "status": "in_play",      # We could get fancy later
            "lock_reason": "",
            "spot_scenarios": []
        })

    # Build polls block (CFP + possibly AP/Coaches if present)
    polls_out = []
    for p in snapshot.get("all_polls", [poll]):
        name = p.get("name", "Unknown Poll")
        teams = []
        for r in p.get("ranks", []):
            teams.append({
                "rank": r.get("rank"),
                "team": r.get("school") or r.get("team") or "Unknown",
                "record": "-",
                "conference": r.get("conference", ""),
            })
        polls_out.append({
            "name": name,
            "source_id": "cfbd",
            "teams": teams,
        })

    payload = {
        "last_updated": now_iso(),
        "sources": [
            {
                "id": "cfbd",
                "label": "CollegeFootballData.com Rankings API",
                "url": CFBD_RANKINGS_URL,
            }
        ],
        "cfp_source_id": "cfbd",
        "conf_source_id": "cfbd",  # placeholder; we can wire standings later
        "rankings": rankings,
        "games": [],      # Phase 3: hook to CFBD games endpoint
        "polls": polls_out,
        "conferences": [] # Phase 3: hook to CFBD standings/records
    }

    return payload


def attach_all_polls(latest_snapshot, all_data):
    """
    Enrich snapshot with 'all_polls' for that same (season, seasonType, week),
    so we can include AP / Coaches etc. in our UI.
    """
    if not latest_snapshot:
        return latest_snapshot

    season = latest_snapshot["season"]
    week = latest_snapshot["week"]
    seasonType = latest_snapshot["seasonType"]

    all_polls = []
    for entry in all_data:
        if (
            entry.get("season") == season and
            entry.get("week") == week and
            entry.get("seasonType") == seasonType
        ):
            all_polls.extend(entry.get("polls", []))

    latest_snapshot["all_polls"] = all_polls
    return latest_snapshot


def main():
    year = dt.datetime.utcnow().year
    print(f"[cfp_ingest] Fetching CFBD rankings for {year}...")

    data = fetch_rankings(year)
    print(f"[cfp_ingest] Got {len(data)} ranking snapshots from CFBD.")

    snapshot = pick_latest_cfp_snapshot(data)
    if not snapshot:
        print("ERROR: No CFP poll found in CFBD rankings data.", file=sys.stderr)
        sys.exit(1)

    snapshot = attach_all_polls(snapshot, data)

    payload = build_payload_from_snapshot(snapshot)

    # Make sure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # If file exists, load previous to avoid meaningless rewrites
    old = None
    if OUTPUT_PATH.exists():
        try:
            old = json.loads(OUTPUT_PATH.read_text())
        except Exception:
            old = None

    new_text = json.dumps(payload, indent=2, sort_keys=True)

    if old is not None:
        old_text = json.dumps(old, indent=2, sort_keys=True)
        if old_text == new_text:
            print("[cfp_ingest] No change in data; not updating cfp-data.json.")
            return

    OUTPUT_PATH.write_text(new_text, encoding="utf-8")
    print(f"[cfp_ingest] Wrote updated CFP data to {OUTPUT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[cfp_ingest] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
