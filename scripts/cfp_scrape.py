#!/usr/bin/env python3
"""
CFP Phase 2 – Data Ingestion (Scraping Primary Sources)

- Scrapes CFP-style rankings + basic poll info from public sites.
- Normalizes into the cfp-data.json shape used by the frontend.
- Overwrites data/cfp-data.json in the repo.

This script is designed to be run from GitHub Actions, but can also
be run locally:

    python scripts/cfp_scrape.py

Notes:
- This is intentionally defensive; if a site layout changes, it will
  fail gracefully and keep the existing cfp-data.json file.
- All selectors are "best effort" heuristics; refine as needed
  once you see the HTML of your chosen primary source.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup  # type: ignore


# -------------------------------
# CONFIG
# -------------------------------
# You can adjust these endpoints if you decide to change sources later.
CFP_PRIMARY_URL = "https://www.espn.com/college-football/rankings"  # CFP/AP/Coaches on one page
STANDINGS_URL = "https://www.espn.com/college-football/standings"   # conference standings
USER_AGENT = "StegVerse-CFP-Scraper/1.0 (+https://stegverse.org)"


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
CFP_DATA_PATH = os.path.join(DATA_DIR, "cfp-data.json")


# -------------------------------
# Helpers
# -------------------------------
def log(msg: str) -> None:
    print(f"[cfp_scrape] {msg}", flush=True)


def fetch_html(url: str) -> Optional[str]:
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        log(f"ERROR fetching {url}: {e}")
        return None


def load_existing_data() -> Dict[str, Any]:
    if not os.path.exists(CFP_DATA_PATH):
        log("No existing cfp-data.json found; starting from empty.")
        return {}
    try:
        with open(CFP_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"ERROR reading existing cfp-data.json: {e}")
        return {}


def save_data(data: Dict[str, Any]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CFP_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
    log(f"Wrote {CFP_DATA_PATH}")


# -------------------------------
# Parsing helpers
# -------------------------------
def parse_rankings_from_espn(html: str) -> Dict[str, Any]:
    """
    Heuristic parser for ESPN rankings page.

    We aim to pull:
      - CFP Top 12
      - AP Top 25 (top few entries)
      - Coaches Poll (top few entries)

    The layout can change; this is intentionally generic.
    If parsing fails, we return partial info.
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    polls: List[Dict[str, Any]] = []
    cfp_rankings: List[Dict[str, Any]] = []

    def parse_table(table, poll_name: str) -> List[Dict[str, Any]]:
        rows = []
        tbody = table.find("tbody") or table
        for tr in tbody.find_all("tr"):
            cols = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
            if len(cols) < 3:
                continue
            # Heuristic: [rank, team, record, ...]
            try:
                rank = int(cols[0])
            except ValueError:
                continue
            team = cols[1]
            record = cols[2]
            # Conference unknown from this table; leave blank
            rows.append({
                "rank": rank,
                "team": team,
                "record": record,
                "conference": ""
            })
        return rows

    # Simple heuristic: first 3 tables correspond to CFP/AP/Coaches.
    # If this is wrong, refine later after inspecting HTML.
    for idx, table in enumerate(tables[:3]):
        name = "Unknown Poll"
        if idx == 0:
            name = "CFP Rankings"
        elif idx == 1:
            name = "AP Top 25"
        elif idx == 2:
            name = "Coaches Poll"

        teams = parse_table(table, name)
        if not teams:
            continue

        poll = {
            "name": name,
            "source_id": "1" if name == "CFP Rankings" else ("2" if name == "AP Top 25" else "3"),
            "teams": teams
        }
        polls.append(poll)

        if name == "CFP Rankings":
            # Convert poll rows to CFP Top 12 seeding model
            for t in teams[:12]:
                cfp_rankings.append({
                    "seed": t["rank"],
                    "team": t["team"],
                    "record": t["record"],
                    "conference": t.get("conference", ""),
                    "status": "in_play",
                    "lock_reason": "",
                    "spot_scenarios": []
                })

    return {"polls": polls, "rankings": cfp_rankings}


def parse_standings_from_espn(html: str) -> List[Dict[str, Any]]:
    """
    Very generic parsing of conference standings.
    We'll look for tables that resemble standings blocks and
    group by headings that look like conference names.
    """
    soup = BeautifulSoup(html, "html.parser")
    conferences: List[Dict[str, Any]] = []

    # ESPN often uses sections with headings; we look for h2/h3 followed by a table.
    for header_tag in soup.find_all(["h2", "h3"]):
        name = header_tag.get_text(strip=True)
        table = header_tag.find_next("table")
        if not table:
            continue

        teams: List[Dict[str, Any]] = []
        tbody = table.find("tbody") or table
        for tr in tbody.find_all("tr"):
            cols = [c.get_text(strip=True) for c in tr.find_all("td")]
            if len(cols) < 3:
                continue
            # Heuristic:
            # col0: team, col1: overall, col2: conference
            team = cols[0]
            overall = cols[1]
            conf_rec = cols[2]
            pf = cols[3] if len(cols) > 3 else ""
            pa = cols[4] if len(cols) > 4 else ""
            teams.append({
                "team": team,
                "overall": overall,
                "conference_record": conf_rec,
                "pf": pf or 0,
                "pa": pa or 0,
            })
        if teams:
            conferences.append({
                "id": name.lower().replace(" ", "").replace("-", ""),
                "name": name,
                "teams": teams
            })

    return conferences


# -------------------------------
# Build combined CFP data model
# -------------------------------
def build_cfp_data() -> Dict[str, Any]:
    existing = load_existing_data()
    now_iso = datetime.now(timezone.utc).isoformat()

    # Base structure
    data: Dict[str, Any] = {
        "last_updated": now_iso,
        "sources": [
            {"id": "1", "label": "ESPN Rankings", "url": CFP_PRIMARY_URL},
            {"id": "4", "label": "ESPN Standings", "url": STANDINGS_URL},
        ],
        "cfp_source_id": "1",
        "conf_source_id": "4",
        "rankings": [],
        "games": existing.get("games", []),  # for now reuse whatever you manually defined
        "polls": [],
        "conferences": [],
    }

    # Try to reuse any custom "sources" entries the frontend already depends on.
    # We'll append our own if they are not present.
    existing_sources = {s.get("id"): s for s in existing.get("sources", []) if isinstance(s, dict)}
    for sid, source in existing_sources.items():
        if sid not in [s["id"] for s in data["sources"]]:
            data["sources"].append(source)

    # Rankings + polls
    html_rank = fetch_html(CFP_PRIMARY_URL)
    if html_rank:
        parsed = parse_rankings_from_espn(html_rank)
        if parsed.get("rankings"):
            data["rankings"] = parsed["rankings"]
        if parsed.get("polls"):
            data["polls"] = parsed["polls"]
    else:
        log("WARNING: Could not fetch rankings HTML; keeping existing rankings/polls if any.")
        if existing.get("rankings"):
            data["rankings"] = existing["rankings"]
        if existing.get("polls"):
            data["polls"] = existing["polls"]

    # Standings
    html_stand = fetch_html(STANDINGS_URL)
    if html_stand:
        conferences = parse_standings_from_espn(html_stand)
        if conferences:
            data["conferences"] = conferences
    else:
        log("WARNING: Could not fetch standings HTML; keeping existing conferences if any.")
        if existing.get("conferences"):
            data["conferences"] = existing["conferences"]

    # Ensure we at least have SOME rankings; if not, keep old.
    if not data["rankings"] and existing.get("rankings"):
        log("WARNING: No new rankings parsed; falling back to existing rankings.")
        data["rankings"] = existing["rankings"]

    if not data["polls"] and existing.get("polls"):
        data["polls"] = existing["polls"]

    if not data["conferences"] and existing.get("conferences"):
        data["conferences"] = existing["conferences"]

    return data


# -------------------------------
# Main
# -------------------------------
def main() -> int:
    log("Starting CFP scrape...")
    data = build_cfp_data()
    save_data(data)
    log("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
