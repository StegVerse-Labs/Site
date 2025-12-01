import json, os, sys, datetime
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# Paths & source config
# ---------------------------------------------------------

# Root of the repo (assumes this file lives in site/cfp/)
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# Our main JSON that the site frontend reads
CFP_JSON_PATH = os.path.join(ROOT_DIR, "cfp", "cfp-data.json")

# Primary CFP ranking page (scraped)
CFP_SOURCE_URL = "https://collegefootballplayoff.com/rankings"

# Optional backup (currently unused, but reserved)
BACKUP_RANKINGS_URL = "https://www.espn.com/college-football/rankings"


# ---------------------------------------------------------
# Helpers: load/save JSON
# ---------------------------------------------------------

def load_existing() -> Dict[str, Any]:
    """Load existing cfp-data.json if present, else return empty structure."""
    if not os.path.exists(CFP_JSON_PATH):
        return {}
    try:
        with open(CFP_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[cfp_ingest] failed to load existing JSON: {e}", file=sys.stderr)
        return {}


def save_data(data: Dict[str, Any]) -> None:
    """Write updated JSON with a fresh last_updated timestamp."""
    data["last_updated"] = (
        datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    )
    os.makedirs(os.path.dirname(CFP_JSON_PATH), exist_ok=True)
    with open(CFP_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
    print(f"[cfp_ingest] wrote {CFP_JSON_PATH}")


# ---------------------------------------------------------
# Scraping: CFP rankings (primary source)
# ---------------------------------------------------------

def scrape_cfp_rankings() -> List[Dict[str, Any]]:
    """
    Scrape CFP Top 25 from the official CFP rankings page.

    NOTE: The CSS/HTML structure here is a best-effort guess. If the page changes,
    you'll only need to update the table/selector logic below (the rest of the
    ingestion + site stays the same).
    """
    rankings: List[Dict[str, Any]] = []

    print(f"[cfp_ingest] fetching CFP rankings from {CFP_SOURCE_URL}")
    try:
        resp = requests.get(CFP_SOURCE_URL, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"[cfp_ingest] primary CFP source failed: {e}", file=sys.stderr)
        return rankings

    soup = BeautifulSoup(resp.text, "html.parser")

    # -----
    # WARNING:
    # This is intentionally generic so it has a decent chance of working
    # without knowing the exact HTML:
    #   - finds the first <table> that has numeric seeds in first column
    #   - expects rows like: Rank | Team | Record | ...
    # If CFP changes structure, we tweak only this block.
    # -----
    table = soup.find("table")
    if not table:
        print("[cfp_ingest] no <table> found on CFP page", file=sys.stderr)
        return rankings

    for row in table.find_all("tr"):
        cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
        if not cells:
            continue
        # Skip header rows and non-numeric seeds
        if not cells[0].isdigit():
            continue

        try:
            seed = int(cells[0])
        except ValueError:
            continue

        team = cells[1] if len(cells) > 1 else ""
        record = cells[2] if len(cells) > 2 else ""
        conference = ""  # can be enriched later from schedule/standings sources

        rankings.append({
            "seed": seed,
            "team": team,
            "record": record,
            "conference": conference,
            "status": "in_play",    # can be locked/in_play/eliminated by logic later
            "lock_reason": "",
            "spot_scenarios": [],   # filled by your scenario logic later
        })

    print(f"[cfp_ingest] parsed {len(rankings)} ranking rows")
    return rankings


# ---------------------------------------------------------
# Main entry
# ---------------------------------------------------------

def main() -> None:
    data = load_existing()

    # If file was empty/non-existent, initialize minimal structure
    if not data:
        data = {
            "last_updated": "",
            "sources": [],
            "cfp_source_id": "cfp",
            "conf_source_id": "standings",
            "rankings": [],
            "games": [],
            "polls": [],
            "conferences": [],
        }

    # -----
    # 1) Update rankings from CFP
    # -----
    rankings = scrape_cfp_rankings()
    if rankings:
        data["rankings"] = rankings

        # Ensure sources array exists
        if "sources" not in data or not isinstance(data["sources"], list):
            data["sources"] = []

        # Add/refresh CFP source record
        existing = [s for s in data["sources"] if s.get("id") == "cfp"]
        if not existing:
            data["sources"].append({
                "id": "cfp",
                "label": "College Football Playoff (scraped)",
                "url": CFP_SOURCE_URL,
            })
        else:
            for s in data["sources"]:
                if s.get("id") == "cfp":
                    s["label"] = "College Football Playoff (scraped)"
                    s["url"] = CFP_SOURCE_URL

        data["cfp_source_id"] = "cfp"
    else:
        print("[cfp_ingest] keeping existing rankings (scrape produced 0 rows)", file=sys.stderr)

    # -----
    # 2) (Future) Update games / standings / polls from other scraped sources
    #    For now we just leave them as-is so nothing breaks.
    # -----

    save_data(data)


if __name__ == "__main__":
    main()
