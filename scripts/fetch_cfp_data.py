#!/usr/bin/env python
"""
Fetch CFP-related data by scraping primary sources and write it to data/cfp-data.json.

This is Phase 2 "plumbing": the script is structured so you can improve the
HTML scraping later without changing the overall flow or the GitHub Action.

Right now:
- It tries to scrape rankings / standings / games, but if scraping fails,
  it will fall back to any existing cfp-data.json and update only timestamps.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import httpx


# ---------------------------
# Config
# ---------------------------

# You can tweak these later as you refine scraping logic
CFP_RANKINGS_URL = os.getenv(
    "CFP_RANKINGS_URL",
    "https://collegefootballplayoff.com/sports/football/rankings"  # example; may need adjustment
)
STANDINGS_URL = os.getenv(
    "CFP_STANDINGS_URL",
    "https://www.espn.com/college-football/standings"  # example
)
SCOREBOARD_URL = os.getenv(
    "CFP_SCOREBOARD_URL",
    "https://www.espn.com/college-football/scoreboard"  # example
)

# Output path (relative to repo root)
OUTPUT_PATH = Path("data/cfp-data.json")


# ---------------------------
# Helpers
# ---------------------------

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def safe_get_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def fetch_html(url: str) -> str:
    """
    Basic HTML fetch with httpx. No heavy parsing here yet.
    """
    print(f"[fetch] GET {url}")
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.text


# ---------------------------
# Scraping stubs (to be refined)
# ---------------------------

def scrape_cfp_rankings(html: str) -> List[Dict[str, Any]]:
    """
    TODO: Implement real scraping of the CFP rankings page.

    For now returns an empty list so the pipeline is wired and safe.
    You can later:
      - Inspect the HTML
      - Add proper parsing (e.g. regex or a small HTML parser)
    """
    # Placeholder: structure is correct, content is empty.
    rankings: List[Dict[str, Any]] = []
    # Example of the expected shape for each entry:
    # rankings.append({
    #     "seed": 1,
    #     "team": "Example Team",
    #     "record": "12-0",
    #     "conference": "Big Ten",
    #     "status": "locked",  # "locked" | "in_play" | "eliminated"
    #     "lock_reason": "CFP #1",
    #     "spot_scenarios": [
    #         {"team": "Example Team", "path": "Already locked"}
    #     ],
    # })
    return rankings


def scrape_standings(html: str) -> List[Dict[str, Any]]:
    """
    TODO: Implement real scraping of conference standings from ESPN (or similar).

    For now returns an empty list with the correct shape.
    """
    conferences: List[Dict[str, Any]] = []
    # Example structure:
    # conferences = [
    #     {
    #         "id": "big12",
    #         "name": "Big 12",
    #         "teams": [
    #             {
    #                 "team": "Texas Tech",
    #                 "overall": "11-1",
    #                 "conference_record": "8-1",
    #                 "pf": 420,
    #                 "pa": 260,
    #             },
    #         ],
    #     }
    # ]
    return conferences


def scrape_games(html: str) -> List[Dict[str, Any]]:
    """
    TODO: Implement real scraping of games / scoreboard.

    For now returns an empty list with the correct shape.
    """
    games: List[Dict[str, Any]] = []
    # Example structure:
    # games = [
    #     {
    #         "id": "ttu-byu",
    #         "home": "Texas Tech",
    #         "away": "BYU",
    #         "home_score": 38,
#             "away_score": 21,
    #         "status": "Final",
    #         "kickoff": "2025-12-06T17:00:00Z",
    #         "conference": "Big 12",
    #         "note": "Big 12 Championship Game",
    #     }
    # ]
    return games


def build_sources_block() -> List[Dict[str, Any]]:
    """
    Keep this aligned with sources used in cfp.html; you can tweak as needed.
    """
    return [
        {"id": "1", "label": "College Football Playoff", "url": "https://collegefootballplayoff.com"},
        {"id": "2", "label": "AP Top 25", "url": "https://apnews.com"},
        {"id": "3", "label": "Coaches Poll", "url": "https://sports.usatoday.com"},
        {"id": "4", "label": "ESPN Standings", "url": "https://www.espn.com/college-football/standings"},
    ]


def build_polls_stub() -> List[Dict[str, Any]]:
    """
    Placeholder polls – you can later scrape AP / Coaches polls here.
    """
    polls: List[Dict[str, Any]] = []
    # Example structure:
    # polls = [
    #     {
    #         "name": "CFP Rankings",
    #         "source_id": "1",
    #         "teams": [
    #             {"rank": 1, "team": "Ohio State", "record": "12-0", "conference": "Big Ten"},
    #         ],
    #     }
    # ]
    return polls


# ---------------------------
# Main assembly
# ---------------------------

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]  # from scripts/ -> repo root
    out_path = repo_root / OUTPUT_PATH

    existing = safe_get_json(out_path)
    print(f"[info] Existing cfp-data.json present: {bool(existing)}")

    rankings: List[Dict[str, Any]] = []
    conferences: List[Dict[str, Any]] = []
    games: List[Dict[str, Any]] = []

    # Try scraping rankings
    try:
        html = fetch_html(CFP_RANKINGS_URL)
        rankings = scrape_cfp_rankings(html)
        print(f"[ok] rankings scraped: {len(rankings)} entries")
    except Exception as e:
        print(f"[warn] rankings scrape failed: {e!r}")

    # Try scraping standings
    try:
        html = fetch_html(STANDINGS_URL)
        conferences = scrape_standings(html)
        print(f"[ok] conferences scraped: {len(conferences)} entries")
    except Exception as e:
        print(f"[warn] standings scrape failed: {e!r}")

    # Try scraping games / scoreboard
    try:
        html = fetch_html(SCOREBOARD_URL)
        games = scrape_games(html)
        print(f"[ok] games scraped: {len(games)} entries")
    except Exception as e:
        print(f"[warn] scoreboard scrape failed: {e!r}")

    # If scraping gave us nothing, keep existing data to avoid wiping page
    if not rankings and "rankings" in existing:
        print("[info] Using existing rankings (scrape empty)")
        rankings = existing.get("rankings", [])

    if not conferences and "conferences" in existing:
        print("[info] Using existing conferences (scrape empty)")
        conferences = existing.get("conferences", [])

    if not games and "games" in existing:
        print("[info] Using existing games (scrape empty)")
        games = existing.get("games", [])

    data: Dict[str, Any] = {
        "last_updated": now_iso(),
        "sources": build_sources_block(),
        "cfp_source_id": "1",
        "conf_source_id": "4",
        "rankings": rankings,
        "polls": build_polls_stub() if "polls" not in existing else existing["polls"],
        "conferences": conferences,
        "games": games,
    }

    # Merge in any extra fields from existing file (so we don't lose custom bits)
    for key, value in existing.items():
        if key not in data:
            data[key] = value

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2, sort_keys=False), encoding="utf-8")
    print(f"[done] wrote {out_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
