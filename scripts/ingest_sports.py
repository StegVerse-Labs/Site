#!/usr/bin/env python3
"""
Universal sports data ingestion for StegVerse.

- Reads configuration from data/ingestion/sports_sources.json
- Scrapes / fetches data from primary & backup sources
- Normalizes into frontend JSON files (e.g. data/cfp/cfp-data.json)
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "ingestion" / "sports_sources.json"
CFP_OUTPUT_PATH = ROOT / "data" / "cfp" / "cfp-data.json"


def log(msg: str) -> None:
  ts = time.strftime("%Y-%m-%d %H:%M:%S")
  print(f"[{ts}] {msg}", flush=True)


def load_config() -> Dict[str, Any]:
  if not CONFIG_PATH.exists():
    raise SystemExit(f"Config not found at {CONFIG_PATH}")
  with CONFIG_PATH.open("r", encoding="utf-8") as f:
    return json.load(f)


# ---------------------------------------------------------------------------
# NCAAF CFP RANKINGS SCRAPER (PRIMARY)
# ---------------------------------------------------------------------------

def fetch_cfp_rankings_official(url: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
  """
  Scrape official CFP rankings page.

  NOTE: This is intentionally conservative and may need tuning once we see the actual HTML.
  For now, we:
    - Find all <tr> rows in the main rankings table
    - Expect columns: Rank, Team, Record, Conference (if present)
  """
  log(f"Fetching CFP rankings from official site: {url}")
  resp = requests.get(url, timeout=20)
  resp.raise_for_status()

  soup = BeautifulSoup(resp.text, "html.parser")

  # This part is heuristic and may need adjustment once you inspect the real HTML.
  tables = soup.find_all("table")
  if not tables:
    raise RuntimeError("No tables found on CFP rankings page.")

  # Pick the first non-trivial table
  table = None
  for t in tables:
    if t.find("tr") and len(t.find_all("tr")) > 5:
      table = t
      break
  if not table:
    raise RuntimeError("No suitable table found in CFP page HTML.")

  rows = table.find_all("tr")
  rankings: List[Dict[str, Any]] = []

  for tr in rows[1:]:
    cols = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
    if not cols or not cols[0].isdigit():
      continue

    try:
      seed = int(cols[0])
    except ValueError:
      continue

    team = cols[1] if len(cols) > 1 else ""
    record = cols[2] if len(cols) > 2 else ""
    conference = cols[3] if len(cols) > 3 else ""

    rankings.append(
      {
        "seed": seed,
        "team": team,
        "record": record,
        "conference": conference or "",
        "status": "in_play",
        "lock_reason": "",
        "spot_scenarios": [],
      }
    )

  if not rankings:
    raise RuntimeError("Parsed 0 CFP rankings rows from official page.")

  meta = {
    "source": "cfp_official",
    "source_label": "Official CFP Rankings",
    "fetched_at": int(time.time()),
    "url": url,
  }
  return rankings, meta


def fetch_cfp_rankings_backup() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
  """
  Placeholder for backup CFP rankings (CFBD or ncaa-api).

  This is intentionally left as a stub so the ingestion step won't crash,
  but we can wire it to a real API later.
  """
  log("Backup CFP rankings fetch not implemented yet; returning empty list.")
  return [], {
    "source": "backup_unimplemented",
    "source_label": "Backup CFP Rankings (TODO)",
    "fetched_at": int(time.time()),
    "url": "",
  }


# ---------------------------------------------------------------------------
# STANDINGS / POLLS (STUBS FOR NOW)
# ---------------------------------------------------------------------------

def fetch_ncaaf_standings(url: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
  """
  Stub for ESPN standings scraper. Implement after CFP rankings are verified.
  """
  log(f"[STUB] Would fetch NCAAF standings from {url}")
  return [], {
    "source": "espn_ncaaf_standings",
    "source_label": "ESPN NCAAF Standings (stub)",
    "fetched_at": int(time.time()),
    "url": url,
  }


def fetch_ap_poll(url: str, label: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
  """
  Stub for AP poll scraper.
  """
  log(f"[STUB] Would fetch AP poll from {url}")
  return [], {
    "source": "ap_poll_stub",
    "source_label": label,
    "fetched_at": int(time.time()),
    "url": url,
  }


def fetch_coaches_poll(url: str, label: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
  """
  Stub for Coaches poll scraper.
  """
  log(f"[STUB] Would fetch Coaches poll from {url}")
  return [], {
    "source": "coaches_poll_stub",
    "source_label": label,
    "fetched_at": int(time.time()),
    "url": url,
  }


# ---------------------------------------------------------------------------
# NCAAF 2025 PIPELINE
# ---------------------------------------------------------------------------

def build_ncaaf_2025_state(config: Dict[str, Any]) -> Dict[str, Any]:
  """
  Build the full NCAAF 2025 composite state used by the CFP frontend.
  This includes:
    - CFP rankings
    - (stub) standings
    - (stub) polls
    - games placeholder
  """
  sports = config.get("sports", {})
  ncaaf = sports.get("ncaaf", {})
  seasons = ncaaf.get("seasons", {})
  season_cfg = seasons.get("2025", {})

  # --- CFP rankings ---
  cfp_cfg = season_cfg.get("cfp_rankings", {})
  cfp_primary = cfp_cfg.get("primary", {})
  cfp_backup = cfp_cfg.get("backup", {})

  rankings: List[Dict[str, Any]] = []
  rankings_meta: Dict[str, Any] = {}

  try:
    if cfp_primary.get("type") == "scrape" and cfp_primary.get("url"):
      rankings, rankings_meta = fetch_cfp_rankings_official(cfp_primary["url"])
  except Exception as e:
    log(f"Primary CFP scrape failed: {e}")
    if cfp_backup:
      rankings, rankings_meta = fetch_cfp_rankings_backup()

  # Ensure seeds are sorted
  rankings = sorted(rankings, key=lambda r: r.get("seed", 999))

  # --- Standings (stub) ---
  standings_cfg = season_cfg.get("standings", {})
  espn_cfg = standings_cfg.get("primary", {})
  confs, conf_meta = [], {}
  if espn_cfg.get("url"):
    confs, conf_meta = fetch_ncaaf_standings(espn_cfg["url"])

  # --- Polls (stubs) ---
  polls_section = season_cfg.get("polls", {})
  polls: List[Dict[str, Any]] = []

  ap_cfg = polls_section.get("ap", {}).get("primary", {})
  if ap_cfg.get("url"):
    ap_teams, ap_meta = fetch_ap_poll(ap_cfg["url"], ap_cfg.get("label", "AP Top 25"))
    polls.append(
      {
        "name": ap_cfg.get("cache_title", "AP Top 25"),
        "source_id": "AP",
        "teams": ap_teams,
        "_meta": ap_meta,
      }
    )

  coaches_cfg = polls_section.get("coaches", {}).get("primary", {})
  if coaches_cfg.get("url"):
    c_teams, c_meta = fetch_coaches_poll(
      coaches_cfg["url"],
      coaches_cfg.get("label", "Coaches Poll")
    )
    polls.append(
      {
        "name": coaches_cfg.get("cache_title", "Coaches Poll"),
        "source_id": "COACHES",
        "teams": c_teams,
        "_meta": c_meta,
      }
    )

  # --- Games placeholder ---
  games: List[Dict[str, Any]] = []

  # --- Sources list for footer ---
  sources = [
    {
      "id": "CFP",
      "label": "College Football Playoff – Rankings",
      "url": cfp_primary.get("url", "https://collegefootballplayoff.com")
    },
    {
      "id": "AP",
      "label": "AP Top 25",
      "url": ap_cfg.get("url", "https://apnews.com")
    },
    {
      "id": "COACHES",
      "label": "Coaches Poll",
      "url": coaches_cfg.get("url", "https://sports.usatoday.com")
    },
    {
      "id": "STANDINGS",
      "label": "ESPN NCAAF Standings",
      "url": espn_cfg.get("url", "https://espn.com/college-football/standings")
    }
  ]

  now_ts = int(time.time())
  state: Dict[str, Any] = {
    "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ts)),
    "sources": sources,
    "cfp_source_id": "CFP",
    "conf_source_id": "STANDINGS",
    "rankings": rankings,
    "games": games,
    "polls": polls,
    "conferences": confs,
    "_meta": {
      "rankings_meta": rankings_meta,
      "standings_meta": conf_meta,
      "generated_at": now_ts,
      "sport": "ncaaf",
      "season": "2025"
    }
  }

  return state


def main() -> None:
  log("Starting universal sports ingestion.")
  config = load_config()

  # For now we only build NCAAF 2025.
  state = build_ncaaf_2025_state(config)

  CFP_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  with CFP_OUTPUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, sort_keys=False)
  log(f"Wrote CFP state to {CFP_OUTPUT_PATH}")

  log("Ingestion complete.")


if __name__ == "__main__":
  try:
    main()
  except Exception as exc:
    log(f"ERROR: {exc}")
    sys.exit(1)
