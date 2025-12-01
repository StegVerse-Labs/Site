#!/usr/bin/env python3
"""
CFP Phase 2 – Data Ingestion Script

- Scrapes the latest CFP Top 25 rankings from the official CFP site
- Updates data/cfp-data.json (preserving non-ranking sections where possible)
- Designed to run in GitHub Actions on a schedule or manual trigger

NOTE:
- HTML structure of collegefootballplayoff.com may change.
- If parsing breaks, adjust the CSS selectors in `_parse_cfp_rankings`.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup

# ---------------------------
# Config
# ---------------------------

# Path to your JSON file in the repo
CFP_DATA_PATH = os.environ.get("CFP_DATA_PATH", "data/cfp-data.json")

# Primary source: official CFP site
# You may need to adjust year or path if the structure changes.
CFP_RANKINGS_URL = os.environ.get(
    "CFP_RANKINGS_URL",
    "https://collegefootballplayoff.com/rankings.aspx"  # fallback generic
)

USER_AGENT = (
    "Mozilla/5.0 (compatible; StegVerse-CFP-Bot/1.0; +https://stegverse.org)"
)


# ---------------------------
# Helpers
# ---------------------------

def _load_existing_data(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Could not load existing {path}: {e}", file=sys.stderr)
        return {}


def _save_data(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
    os.replace(tmp_path, path)


def _fetch_html(url: str) -> str:
    print(f"[INFO] Fetching CFP rankings from {url}")
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
    resp.raise_for_status()
    return resp.text


def _parse_cfp_rankings(html: str) -> List[Dict[str, Any]]:
    """
    Attempt to parse CFP Top 25 from the official site.
    This uses best-guess CSS selectors and MAY need adjustment
    once we confirm the actual HTML.

    Returns a list of:
      { "seed": int, "team": str, "record": str, "conference": str, "status": "in_play"/"locked"/"eliminated" }
    """
    soup = BeautifulSoup(html, "html.parser")

    # You will likely need to inspect the HTML and adjust this.
    # We try some common table patterns:
    table = None
    for candidate in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in candidate.find_all("th")]
        if any("rank" in h for h in headers) and any("team" in h for h in headers):
            table = candidate
            break

    if not table:
        print("[WARN] Could not find rankings table in HTML; returning empty list.", file=sys.stderr)
        return []

    rankings: List[Dict[str, Any]] = []
    for row in table.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in row.find_all("td")]
        if len(cells) < 2:
            continue
        # Heuristic: [rank, team, record, ...]
        try:
            seed = int(cells[0].split()[0])
        except Exception:
            continue

        team_name = cells[1]
        record = ""
        conference = ""
        # Try to guess record and conference from remaining cells
        if len(cells) >= 3:
            record = cells[2]
        if len(cells) >= 4:
            conference = cells[3]

        rankings.append({
            "seed": seed,
            "team": team_name,
            "record": record,
            "conference": conference,
            "status": "in_play",      # default; front-end can refine
            "lock_reason": ""
        })

    # Only keep top 12 for our primary view
    rankings = [r for r in rankings if r["seed"] <= 12]

    print(f"[INFO] Parsed {len(rankings)} CFP rankings rows (top 12).")
    return rankings


def _update_rankings(existing: Dict[str, Any], new_rankings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge new rankings into existing cfp-data.json structure.
    - Overwrites `rankings`
    - Updates `last_updated`
    - Preserves `sources`, `polls`, `conferences`, `games` if present
    """
    data = dict(existing) if isinstance(existing, dict) else {}

    data["rankings"] = new_rankings
    data["last_updated"] = datetime.now(timezone.utc).isoformat()

    # Ensure sources have an entry for CFP if not present
    sources = data.get("sources", [])
    if not any(s.get("id") == "1" for s in sources):
        sources.append({
            "id": "1",
            "label": "College Football Playoff",
            "url": CFP_RANKINGS_URL
        })
    data["sources"] = sources
    data["cfp_source_id"] = "1"

    # Ensure conf_source_id at least exists (front-end expects it)
    if "conf_source_id" not in data:
        data["conf_source_id"] = "4"

    return data


# ---------------------------
# Main
# ---------------------------

def main() -> int:
    print(f"[INFO] Loading existing data from {CFP_DATA_PATH}")
    existing = _load_existing_data(CFP_DATA_PATH)

    try:
        html = _fetch_html(CFP_RANKINGS_URL)
        rankings = _parse_cfp_rankings(html)
    except Exception as e:
        print(f"[ERROR] Failed to fetch/parse CFP rankings: {e}", file=sys.stderr)
        return 1

    if not rankings:
        print("[ERROR] No rankings parsed; aborting update.", file=sys.stderr)
        return 1

    updated = _update_rankings(existing, rankings)

    _save_data(CFP_DATA_PATH, updated)
    print(f"[INFO] Updated {CFP_DATA_PATH} with latest CFP rankings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
