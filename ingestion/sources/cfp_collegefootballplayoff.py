import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

import requests
from bs4 import BeautifulSoup  # you must install beautifulsoup4 in the workflow


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_rankings_from_html(html: str) -> List[Dict[str, Any]]:
    """
    Parse CFP rankings table from the official CFP site HTML.
    This is a best-effort parser and may need tweaks depending on their markup.
    """
    soup = BeautifulSoup(html, "html.parser")

    rankings: List[Dict[str, Any]] = []

    # Try to find main rankings table(s). Adjust selectors as needed.
    # Strategy:
    #   - Look for <table> elements that contain "Rank" and "Team" in the header.
    tables = soup.find_all("table")
    for table in tables:
        headers = [h.get_text(strip=True).lower() for h in table.find_all("th")]
        if not headers:
            continue
        if "rank" in headers and "team" in headers:
            # Found a candidate table
            for row in table.find_all("tr"):
                cells = [c.get_text(strip=True) for c in row.find_all("td")]
                if len(cells) < 2:
                    continue
                try:
                    seed = int(cells[0])
                except ValueError:
                    continue

                team = cells[1]
                record = cells[2] if len(cells) > 2 else ""
                conference = cells[3] if len(cells) > 3 else ""

                rankings.append(
                    {
                        "seed": seed,
                        "team": team,
                        "record": record,
                        "conference": conference,
                        "status": "in_play",      # default; can be refined by logic later
                        "lock_reason": "",
                        "spot_scenarios": []
                    }
                )
            break

    return rankings


def fetch_cfp_data_from_cfp_site(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch CFP rankings (and placeholder standings/polls/games) from the CFP official site.
    cfg should contain:
      - rankings_url: str
    """
    url = cfg.get("rankings_url")
    if not url:
        raise ValueError("rankings_url not configured for cfp_collegefootballplayoff source")

    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    rankings = parse_rankings_from_html(resp.text)

    # Placeholder / minimal versions for other sections so the frontend continues to work.
    # These can later be enriched by additional sources (NCAA API, ESPN, etc.).
    sources = [
        {
            "id": "1",
            "label": "College Football Playoff",
            "url": url
        }
    ]

    data: Dict[str, Any] = {
        "last_updated": iso_now(),
        "sources": sources,
        "cfp_source_id": "1",
        "conf_source_id": None,
        "rankings": rankings,
        "games": [],
        "polls": [],
        "conferences": []
    }

    return data
