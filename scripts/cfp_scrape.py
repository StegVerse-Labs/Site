# scripts/cfp_scrape.py

"""
CFP / NCAAF data scraper that uses data/cfp_sources.json
as the single source of truth for where to fetch from.

Outputs:
- data/cfp-data.json   (high-level combined snapshot)
- data/cfp-2025.json   (raw CFP rankings & bracket-ish info)
- data/cfp-teams.json  (teams + records)
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup  # make sure 'beautifulsoup4' is in requirements.txt

from scripts.cfp_sources import pick_best_source, SourceConfigError


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def fetch_html(url: str) -> str:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text


# --- Parsers ---------------------------------------------------------------

def parse_cfp_official_rankings(html: str) -> Dict[str, Any]:
    """
    Parse the official CFP rankings from the HTML page.

    NOTE: This is intentionally simple / placeholder-ish. You can tighten
    this as you learn the exact HTML structure.
    """
    soup = BeautifulSoup(html, "html.parser")

    # You will want to inspect the real page structure in a desktop browser
    # and adjust these selectors accordingly.
    table = soup.find("table")
    if not table:
        raise RuntimeError("Could not find rankings table in CFP HTML")

    rows = table.find_all("tr")
    rankings: List[Dict[str, Any]] = []

    for row in rows[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 3:
            continue
        rank_txt, team, record = cols[:3]

        try:
            rank = int(rank_txt.replace("#", "").strip())
        except ValueError:
            continue

        rankings.append(
            {
                "rank": rank,
                "team": team,
                "record": record,
            }
        )

    return {
        "source": "cfp_official_rankings",
        "rankings": rankings,
    }


def parse_ap_poll(html: str) -> Dict[str, Any]:
    # TODO: implement real scraping once we lock the AP page structure.
    # For now we just stub it.
    soup = BeautifulSoup(html, "html.parser")
    # ... parse ...
    return {
        "source": "ap_top25",
        "rankings": [],
    }


def parse_coaches_poll(html: str) -> Dict[str, Any]:
    # TODO: implement real scraping once we lock the Coaches page structure.
    soup = BeautifulSoup(html, "html.parser")
    # ... parse ...
    return {
        "source": "coaches_poll",
        "rankings": [],
    }


def parse_cfbd_api(url: str, api_key: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return {
        "source": "cfbd_api",
        "raw": data,
    }


# --- Orchestration ---------------------------------------------------------


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    try:
        cfp_src = pick_best_source(kind="cfp_rankings", season=2025)
    except SourceConfigError as e:
        print(f"[cfp_scrape] ERROR loading source config: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[cfp_scrape] Using CFP rankings source: {cfp_src['id']} ({cfp_src['url']})")

    parser_id = cfp_src.get("parser")
    url = cfp_src["url"]

    if parser_id == "cfp_official_html_v1":
        html = fetch_html(url)
        cfp_data = parse_cfp_official_rankings(html)
    elif parser_id == "cfbd_api_v1":
        from os import getenv

        api_key_name = cfp_src.get("env_api_key", "CFBD_API_KEY")
        api_key = getenv(api_key_name)
        if not api_key:
            raise RuntimeError(f"CFBD backup source selected but env var {api_key_name} is not set")
        cfp_data = parse_cfbd_api(url, api_key)
    else:
        raise RuntimeError(f"Unknown parser id: {parser_id}")

    # For now we just dump this straight into cfp-2025.json and cfp-data.json
    write_json(DATA_DIR / "cfp-2025.json", cfp_data)
    write_json(DATA_DIR / "cfp-data.json", {"cfp": cfp_data})

    print("[cfp_scrape] Wrote data/cfp-2025.json and data/cfp-data.json")


if __name__ == "__main__":
    main()
