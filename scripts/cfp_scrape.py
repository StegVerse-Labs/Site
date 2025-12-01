#!/usr/bin/env python3
"""
cfp_scrape.py

Config-driven scraper for CFP rankings (and future polls/standings).

- Reads Site/data/cfp_sources.json
- Tries enabled sources for "rankings" in priority order
- Uses the first source that returns valid data
- Writes normalized rankings into Site/data/cfp-data.json

For now we focus on CFP rankings; polls/standings can be wired in later
using the same pattern.

Expected output JSON shape (cfp-data.json):

{
  "year": 2025,
  "source_id": "cfp_official_html",
  "source_title": "College Football Playoff — Official Rankings",
  "generated_at": "2025-11-30T01:23:45Z",
  "rankings": [
    {
      "rank": 1,
      "team": "Ohio State",
      "record": "12-0",
      "conf": "Big Ten"
    },
    ...
  ]
}
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CONFIG_PATH = DATA_DIR / "cfp_sources.json"
OUTPUT_PATH = DATA_DIR / "cfp-data.json"


def log(msg: str) -> None:
    """Simple stderr logger so GitHub Actions shows messages nicely."""
    sys.stderr.write(f"[cfp_scrape] {msg}\n")
    sys.stderr.flush()


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def select_sources(cfg: Dict[str, Any], section: str) -> List[Dict[str, Any]]:
    """Return enabled sources for a section (e.g. 'rankings') sorted by priority."""
    sec = cfg.get(section, {})
    sources = sec.get("sources", [])
    enabled = [s for s in sources if s.get("enabled", True)]
    return sorted(enabled, key=lambda s: int(s.get("priority", 100)))


def http_get(url: str, timeout: int = 20) -> requests.Response:
    log(f"GET {url}")
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp


# ---------- PARSERS ----------

def parse_rankings_from_official_html(html: str, max_teams: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Very generic HTML parser for the official CFP rankings page.

    We try to find the first table that looks like rankings (has 'Rank' in header),
    then pull Rank, Team, Record and Conference if available.

    NOTE: This may need tweaking once we see the exact HTML, but it's
    intentionally defensive and should at least not crash.
    """
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")
    if not tables:
        raise ValueError("No tables found on CFP official page.")

    rankings: List[Dict[str, Any]] = []

    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        header_line = " | ".join(h.lower() for h in headers)

        if "rank" not in header_line or "team" not in header_line:
            continue  # not our table

        # Figure out column indices
        try:
            rank_idx = next(i for i, h in enumerate(headers) if "rank" in h.lower())
        except StopIteration:
            rank_idx = None

        try:
            team_idx = next(i for i, h in enumerate(headers) if "team" in h.lower() or "school" in h.lower())
        except StopIteration:
            team_idx = None

        record_idx = None
        conf_idx = None

        for i, h in enumerate(headers):
            low = h.lower()
            if record_idx is None and ("record" in low or "overall" in low):
                record_idx = i
            if conf_idx is None and ("conf" in low or "conference" in low):
                conf_idx = i

        if team_idx is None or rank_idx is None:
            # Not a usable table; continue searching
            continue

        for row in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if not cells:
                continue

            # Guard against short rows
            rank = None
            team = None
            record = ""
            conf = ""

            if rank_idx is not None and rank_idx < len(cells):
                rank_str = cells[rank_idx].strip("# ")
                if rank_str.isdigit():
                    rank = int(rank_str)
            if team_idx is not None and team_idx < len(cells):
                team = cells[team_idx]

            if record_idx is not None and record_idx < len(cells):
                record = cells[record_idx]
            if conf_idx is not None and conf_idx < len(cells):
                conf = cells[conf_idx]

            if rank is None or not team:
                continue

            rankings.append(
                {
                    "rank": rank,
                    "team": team,
                    "record": record,
                    "conf": conf,
                }
            )

        break  # we handled the first matching rankings table

    if not rankings:
        raise ValueError("No rankings rows parsed from CFP official HTML.")

    rankings.sort(key=lambda r: r["rank"])
    if max_teams:
        rankings = rankings[:max_teams]
    return rankings


def parse_rankings_from_ncaa_json(data: Any, max_teams: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Parser for the henrygd NCAA API format.

    We expect something like:
    [
      { "rank": 1, "school": "Ohio State", "record": "12-0", "conference": "Big Ten", ... },
      ...
    ]
    """
    if not isinstance(data, list):
        raise ValueError("NCAA API JSON is not a list.")

    rankings: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue

        rank = item.get("rank")
        team = item.get("school") or item.get("team")
        record = item.get("record") or ""
        conf = item.get("conference") or item.get("conf") or ""

        if not isinstance(rank, int) or not team:
            continue

        rankings.append(
            {
                "rank": rank,
                "team": str(team),
                "record": str(record),
                "conf": str(conf),
            }
        )

    if not rankings:
        raise ValueError("No rankings parsed from NCAA API JSON.")

    rankings.sort(key=lambda r: r["rank"])
    if max_teams:
        rankings = rankings[:max_teams]
    return rankings


# ---------- SECTION DRIVERS ----------

def fetch_rankings(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Try rankings sources in order, return the first successful normalized payload."""
    year = cfg.get("meta", {}).get("year", 2025)
    sources = select_sources(cfg, "rankings")

    if not sources:
        raise RuntimeError("No enabled rankings sources in config.")

    last_error: Optional[Exception] = None

    for src in sources:
        src_id = src.get("id")
        url = src.get("url")
        src_type = src.get("type")
        max_teams = src.get("max_teams")
        title = src.get("title", src_id)

        try:
            log(f"Trying rankings source '{src_id}' ({src_type})")

            if src_type == "html_table":
                resp = http_get(url)
                rankings = parse_rankings_from_official_html(resp.text, max_teams=max_teams)

            elif src_type == "json_api":
                resp = http_get(url)
                data = resp.json()
                rankings = parse_rankings_from_ncaa_json(data, max_teams=max_teams)

            else:
                raise ValueError(f"Unsupported rankings source type: {src_type}")

            log(f"Source '{src_id}' succeeded with {len(rankings)} teams.")
            return {
                "year": year,
                "source_id": src_id,
                "source_title": title,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "rankings": rankings,
            }

        except Exception as e:  # noqa: BLE001
            last_error = e
            log(f"Source '{src_id}' failed: {e!r}")
            # small backoff before trying next source
            time.sleep(1.0)

    raise RuntimeError(f"All rankings sources failed. Last error: {last_error!r}")


# ---------- CLI ----------

def main(argv: List[str]) -> int:
    log(f"Root dir: {ROOT}")
    log(f"Config:   {CONFIG_PATH}")
    log(f"Output:   {OUTPUT_PATH}")

    try:
        cfg = load_config()
    except Exception as e:  # noqa: BLE001
        log(f"ERROR loading config: {e!r}")
        return 1

    try:
        rankings_payload = fetch_rankings(cfg)
    except Exception as e:  # noqa: BLE001
        log(f"ERROR fetching rankings: {e!r}")
        return 1

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(rankings_payload, f, indent=2, ensure_ascii=False)

    log(f"Wrote rankings JSON to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
