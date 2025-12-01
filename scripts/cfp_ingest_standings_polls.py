#!/usr/bin/env python3
"""
cfp_ingest_standings_polls.py

Phase 2: universal ingestion skeleton for standings + polls.

- Reads cfp/cfp_sources.yaml
- Loads existing data/cfp-data.json
- (Stub) fetches + parses standings & polls
- Writes updated data/cfp-data.json

NOTE:
The actual HTML parsing functions are placeholders with clear TODO notes.
You can fill them in incrementally without changing the overall framework.
"""

import json
import pathlib
import sys
from typing import Any, Dict, List

import yaml  # pip install pyyaml
import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cfp-data.json"
SOURCES_PATH = ROOT / "cfp" / "cfp_sources.yaml"


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: pathlib.Path, data: Dict[str, Any]):
    tmp = path.with_suffix(".tmp.json")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
    tmp.replace(path)


def load_sources() -> Dict[str, Any]:
    if not SOURCES_PATH.exists():
        print(f"[WARN] {SOURCES_PATH} not found; no ingestion performed.", file=sys.stderr)
        return {}
    with SOURCES_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_html(url: str) -> BeautifulSoup:
    print(f"[INFO] Fetching {url}")
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# ------------------- Parsers (STUBS with TODOs) -------------------


def parse_cfp_official_rankings(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    TODO: Implement real parsing of the official CFP rankings table.

    For now, returns an empty list (so we DO NOT overwrite your current
    rankings in cfp-data.json until the parser is ready).
    """
    print("[WARN] parse_cfp_official_rankings() is not implemented; leaving rankings unchanged.")
    return []


def parse_ap_poll(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    TODO: Parse AP Top 25 HTML into our internal poll format:
    [
      { "rank": 1, "team": "...", "record": "12-0", "conference": "SEC" },
      ...
    ]
    """
    print("[WARN] parse_ap_poll() is not implemented; AP poll will not be updated.")
    return []


def parse_coaches_poll(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    TODO: Parse Coaches Poll HTML into our internal poll format.
    """
    print("[WARN] parse_coaches_poll() is not implemented; Coaches poll will not be updated.")
    return []


def parse_espn_standings(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    TODO: Parse ESPN standings HTML into a list of conferences with teams:
    [
      {
        "id": "big12",
        "name": "Big 12",
        "teams": [
          { "team": "Texas Tech", "overall": "11-1", "conference_record": "8-1", "pf": 420, "pa": 260 },
          ...
        ]
      },
      ...
    ]
    """
    print("[WARN] parse_espn_standings() is not implemented; standings will not be updated.")
    return []


# ------------------- Ingestion Orchestration -------------------


def update_polls(existing: Dict[str, Any], cfg: Dict[str, Any]) -> None:
    poll_sources = cfg.get("poll_sources", []) or []

    # Keep existing polls if parsers are not implemented
    polls: List[Dict[str, Any]] = existing.get("polls", [])

    for src in poll_sources:
        if not src.get("enabled"):
            continue
        sid = src["id"]
        url = src["url"]
        kind = src["kind"]

        soup = fetch_html(url)

        if kind == "cfp_rankings":
            new_rankings = parse_cfp_official_rankings(soup)
            if new_rankings:
                # Replace rankings poll entry with new CFP poll
                polls = [p for p in polls if p.get("name") != "CFP Rankings"]
                polls.insert(
                    0,
                    {
                        "name": "CFP Rankings",
                        "source_id": sid,
                        "teams": new_rankings,
                    },
                )
        elif kind == "ap_poll":
            teams = parse_ap_poll(soup)
            if teams:
                polls = [p for p in polls if p.get("name") != "AP Top 25"]
                polls.append(
                    {
                        "name": "AP Top 25",
                        "source_id": sid,
                        "teams": teams,
                    }
                )
        elif kind == "coaches_poll":
            teams = parse_coaches_poll(soup)
            if teams:
                polls = [p for p in polls if p.get("name") != "Coaches Poll"]
                polls.append(
                    {
                        "name": "Coaches Poll",
                        "source_id": sid,
                        "teams": teams,
                    }
                )

    existing["polls"] = polls


def update_standings(existing: Dict[str, Any], cfg: Dict[str, Any]) -> None:
    standing_sources = cfg.get("standing_sources", []) or []

    # By default, we replace the conference list only if we get something non-empty
    conferences = existing.get("conferences", [])

    for src in standing_sources:
        if not src.get("enabled"):
            continue
        sid = src["id"]
        url = src["url"]
        kind = src["kind"]

        soup = fetch_html(url)

        if kind == "conference_standings":
            parsed = parse_espn_standings(soup)
            if parsed:
                conferences = parsed
                # We can optionally store which source we used:
                existing["conf_source_id"] = sid
                break  # First successful source wins

    existing["conferences"] = conferences


def main():
    cfg = load_sources()
    if not cfg:
        print("[WARN] No cfp_sources.yaml; exiting with no changes.")
        return

    data = load_json(DATA_PATH)
    if not data:
        print(f"[WARN] {DATA_PATH} missing or empty; starting fresh structure.")
        data = {
            "last_updated": "",
            "rankings": [],
            "polls": [],
            "conferences": [],
            "games": [],
            "sources": [],
        }

    update_polls(data, cfg)
    update_standings(data, cfg)

    # Update last_updated timestamp (UTC-like string)
    import datetime as dt

    data["last_updated"] = dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    save_json(DATA_PATH, data)
    print(f"[OK] Updated {DATA_PATH}")


if __name__ == "__main__":
    main()
