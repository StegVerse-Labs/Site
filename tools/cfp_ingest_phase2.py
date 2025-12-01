#!/usr/bin/env python
"""
CFP Phase 2 Ingestion: Standings + Polls

- Reads config from cfp/cfp-sources.json
- Loads existing data/cfp-data.json (if present)
- Scrapes polls + standings from primary sources
- Writes updated polls + conferences + sources back to cfp-data.json

NOTE: HTML structures can change; treat this as a best-effort starting point.
You can refine individual parser functions as needed.
"""

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cfp-data.json"
SOURCES_PATH = ROOT / "cfp" / "cfp-sources.json"


# ---------------------------
# Helpers
# ---------------------------

def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class PollEntry:
    rank: int
    team: str
    record: str
    conference: str = ""


@dataclass
class ConferenceTeam:
    team: str
    overall: str
    conference_record: str
    pf: int
    pa: int


@dataclass
class ConferenceBlock:
    id: str
    name: str
    teams: List[ConferenceTeam]


# ---------------------------
# Generic HTML helpers
# ---------------------------

def fetch_html(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def clean(text: str) -> str:
    return " ".join((text or "").replace("\xa0", " ").split())


# ---------------------------
# Poll parsers (best-effort)
# ---------------------------

def parse_generic_poll_table(soup: BeautifulSoup) -> List[PollEntry]:
    """
    Generic helper:
    - Find the first table whose header row contains 'Rank' or 'RK'
    - Extract rank, team, record from each row
    """
    tables = soup.find_all("table")
    best_table = None
    for tbl in tables:
        header = tbl.find("thead") or tbl
        header_row = header.find("tr")
        if not header_row:
            continue
        headers = [clean(th.get_text()) for th in header_row.find_all("th")]
        headers_lower = [h.lower() for h in headers]
        if any("rk" in h or "rank" in h for h in headers_lower):
            best_table = tbl
            break

    if not best_table:
        return []

    body = best_table.find("tbody") or best_table
    rows = body.find_all("tr")
    entries: List[PollEntry] = []
    for row in rows:
        cells = [clean(td.get_text()) for td in row.find_all(["td", "th"])]
        if len(cells) < 2:
            continue
        try:
            rank = int(cells[0].split()[0])
        except Exception:
            continue
        team = cells[1]
        record = ""
        # crude guess: record often appears in later cells like "10-1"
        for c in cells[2:]:
            if "-" in c and any(ch.isdigit() for ch in c):
                record = c
                break
        entries.append(PollEntry(rank=rank, team=team, record=record))
    return entries


def fetch_cfp_poll(url: str) -> List[PollEntry]:
    soup = fetch_html(url)
    # CFP site often has a ranking table with Rank/School/Record
    entries = parse_generic_poll_table(soup)
    return entries


def fetch_ap_poll(url: str) -> List[PollEntry]:
    soup = fetch_html(url)
    entries = parse_generic_poll_table(soup)
    return entries


def fetch_coaches_poll(url: str) -> List[PollEntry]:
    soup = fetch_html(url)
    entries = parse_generic_poll_table(soup)
    return entries


# ---------------------------
# Standings parser (best-effort, ESPN-style)
# ---------------------------

def fetch_espn_standings(url: str) -> List[ConferenceBlock]:
    soup = fetch_html(url)
    # ESPN typically has multiple tables grouped by conference/division.
    # We'll look for tables with a header containing "TEAM" or similar,
    # then group them by the preceding <h2>/<h3> label.
    blocks: List[ConferenceBlock] = []

    # Strategy:
    #   - Walk through headings and tables in order
    #   - When we see a heading, remember conference name
    #   - When we see a table under that heading, parse it
    headings = soup.find_all(["h2", "h3"])
    for heading in headings:
        conf_name = clean(heading.get_text())
        # look for next table sibling
        tbl = heading.find_next("table")
        if not tbl:
            continue

        thead = tbl.find("thead") or tbl
        header_row = thead.find("tr")
        if not header_row:
            continue
        headers = [clean(th.get_text()).lower() for th in header_row.find_all("th")]
        if not any("team" in h for h in headers):
            # not a standings table
            continue

        body = tbl.find("tbody") or tbl
        teams: List[ConferenceTeam] = []
        for row in body.find_all("tr"):
            cells = [clean(td.get_text()) for td in row.find_all(["td", "th"])]
            if len(cells) < 3:
                continue
            team_name = cells[0]
            overall = ""
            conf_rec = ""
            pf = 0
            pa = 0

            # naive mapping: search for “-” as record pattern
            for c in cells[1:]:
                if "-" in c and any(ch.isdigit() for ch in c):
                    if not overall:
                        overall = c
                    elif not conf_rec:
                        conf_rec = c

            # PF / PA guesses: look for ints near end
            ints = []
            for c in cells:
                try:
                    ints.append(int(c))
                except Exception:
                    continue
            if len(ints) >= 2:
                pf, pa = ints[-2], ints[-1]

            teams.append(
                ConferenceTeam(
                    team=team_name,
                    overall=overall,
                    conference_record=conf_rec,
                    pf=pf,
                    pa=pa,
                )
            )

        if teams:
            block_id = conf_name.lower().replace(" ", "_").replace("&", "and")
            blocks.append(
                ConferenceBlock(
                    id=block_id,
                    name=conf_name,
                    teams=teams,
                )
            )

    return blocks


# ---------------------------
# Main orchestration
# ---------------------------

def main() -> int:
    # 1) Load config
    sources_cfg = load_json(SOURCES_PATH, default={})
    polls_cfg = sources_cfg.get("polls", {})
    standings_cfg = sources_cfg.get("standings", {})
    source_index_cfg: List[Dict[str, str]] = sources_cfg.get("source_index", [])

    # 2) Load existing cfp-data.json or stub
    data = load_json(
        DATA_PATH,
        default={
            "last_updated": None,
            "sources": [],
            "cfp_source_id": "cfp_official",
            "conf_source_id": "espn_standings",
            "rankings": [],
            "games": [],
            "polls": [],
            "conferences": []
        },
    )

    # Preserve existing rankings/games; we only touch polls + conferences + sources
    existing_sources: List[Dict[str, Any]] = data.get("sources", [])

    # Build a map for sources by id, starting from existing then overlay config
    sources_by_id: Dict[str, Dict[str, Any]] = {s["id"]: s for s in existing_sources if "id" in s}
    for s in source_index_cfg:
        sid = s.get("id")
        if not sid:
            continue
        sources_by_id[sid] = {
            "id": sid,
            "label": s.get("label", sid),
            "url": s.get("url", "")
        }

    # 3) Fetch polls
    new_polls: List[Dict[str, Any]] = []

    # CFP
    cfp_cfg = polls_cfg.get("cfp")
    if cfp_cfg:
        url = cfp_cfg["primary"]["url"]
        print(f"[cfp] Fetching CFP poll from {url}")
        cfp_entries = fetch_cfp_poll(url)
        new_polls.append({
            "name": "CFP Rankings",
            "source_id": cfp_cfg["id"],
            "teams": [
                {
                    "rank": e.rank,
                    "team": e.team,
                    "record": e.record,
                    "conference": e.conference,
                }
                for e in cfp_entries
            ],
        })

    # AP
    ap_cfg = polls_cfg.get("ap")
    if ap_cfg:
        url = ap_cfg["primary"]["url"]
        print(f"[cfp] Fetching AP poll from {url}")
        ap_entries = fetch_ap_poll(url)
        new_polls.append({
            "name": "AP Top 25",
            "source_id": ap_cfg["id"],
            "teams": [
                {
                    "rank": e.rank,
                    "team": e.team,
                    "record": e.record,
                    "conference": e.conference,
                }
                for e in ap_entries
            ],
        })

    # Coaches
    coaches_cfg = polls_cfg.get("coaches")
    if coaches_cfg:
        url = coaches_cfg["primary"]["url"]
        print(f"[cfp] Fetching Coaches poll from {url}")
        coaches_entries = fetch_coaches_poll(url)
        new_polls.append({
            "name": "Coaches Poll",
            "source_id": coaches_cfg["id"],
            "teams": [
                {
                    "rank": e.rank,
                    "team": e.team,
                    "record": e.record,
                    "conference": e.conference,
                }
                for e in coaches_entries
            ],
        })

    # 4) Fetch standings (FBS)
    new_confs: List[Dict[str, Any]] = []
    fbs_cfg = standings_cfg.get("fbs")
    if fbs_cfg:
        url = fbs_cfg["primary"]["url"]
        print(f"[cfp] Fetching standings from {url}")
        blocks = fetch_espn_standings(url)
        for b in blocks:
            new_confs.append({
                "id": b.id,
                "name": b.name,
                "teams": [
                    {
                        "team": t.team,
                        "overall": t.overall,
                        "conference_record": t.conference_record,
                        "pf": t.pf,
                        "pa": t.pa,
                    }
                    for t in b.teams
                ],
            })

    # 5) Write back into data structure
    data["last_updated"] = now_iso()
    data["sources"] = list(sources_by_id.values())
    if cfp_cfg:
        data["cfp_source_id"] = cfp_cfg["id"]
    data["conf_source_id"] = "espn_standings"
    data["polls"] = new_polls
    data["conferences"] = new_confs

    save_json(DATA_PATH, data)
    print(f"[cfp] Updated {DATA_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
