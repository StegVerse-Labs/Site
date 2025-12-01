#!/usr/bin/env python3
"""
universal_ingest.py

Universal ingestion runner for StegVerse/site.

- Reads ingest/ingest_config.yml
- For each enabled dataset:
    - Chooses primary/backup source(s)
    - Calls a handler by "kind"
    - Updates a target JSON file + field
- Designed to be run from GitHub Actions or locally.

NOTE: Scraper implementations are intentionally minimal / stubbed
and may need selector tuning once you see real HTML.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml  # PyYAML
import requests
from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[1]  # repo root (…/site)


def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{ts}] {msg}")


def load_config() -> Dict[str, Any]:
    cfg_path = ROOT / "ingest" / "ingest_config.yml"
    if not cfg_path.exists():
        raise SystemExit(f"Config file not found: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"WARN: Failed to parse JSON at {path}: {e}")
        return {}


def save_json_file(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
    tmp.replace(path)


def fetch_html(url: str) -> str:
    log(f"Fetching HTML: {url}")
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text


def fetch_json_api(url: str) -> Any:
    log(f"Fetching JSON API: {url}")
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------------------------
# HANDLERS (by dataset.kind)
# --------------------------------------------------------------------

def handle_cfp_rankings_html(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse CFP rankings from the official site (or backup).
    OUTPUT: list of ranking dicts to put into cfp-data.json["rankings"].

    NOTE: This is a minimal skeleton. Selector logic will likely need tuning
    after we inspect the actual HTML structure.
    """
    html = fetch_html(source["url"])
    soup = BeautifulSoup(html, "html.parser")

    # TODO: Adjust selectors based on real markup.
    # For now, we look for a table where header contains "Rank" and "School" or similar.
    table = None
    for t in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
        if any("rank" in h for h in headers) and any("school" in h or "team" in h for h in headers):
            table = t
            break
    if not table:
        log("WARN: CFP rankings table not found; returning empty list.")
        return []

    rankings: List[Dict[str, Any]] = []
    for row in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cells or not cells[0].isdigit():
            continue
        try:
            seed = int(cells[0])
        except ValueError:
            continue
        team = cells[1] if len(cells) > 1 else ""
        record = cells[2] if len(cells) > 2 else ""
        conference = ""
        if len(cells) > 3:
            conference = cells[3]

        rankings.append(
            {
                "seed": seed,
                "team": team,
                "record": record,
                "conference": conference,
                "status": "in_play",      # default; UI can refine logic
                "lock_reason": "",
                "spot_scenarios": [],
            }
        )

    log(f"Parsed {len(rankings)} CFP ranking rows.")
    return rankings


def handle_ncaaf_standings_html(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse conference standings from ESPN standings.
    OUTPUT: list of conference dicts, each with teams list.
    """
    html = fetch_html(source["url"])
    soup = BeautifulSoup(html, "html.parser")

    conferences: List[Dict[str, Any]] = []

    # ESPN typically has sections per conference.
    # We'll look for table sections with headings.
    for section in soup.find_all(["section", "div"]):
        heading = section.find(["h2", "h3"])
        if not heading:
            continue
        conf_name = heading.get_text(strip=True)
        # crude filter to skip junk
        if "conference" not in conf_name.lower() and "big" not in conf_name.lower() and "sec" not in conf_name.lower():
            continue

        table = section.find("table")
        if not table:
            continue

        teams: List[Dict[str, Any]] = []
        for row in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if not cells or cells[0].lower() in ("team", "school"):
                continue
            team_name = cells[0]
            overall = cells[1] if len(cells) > 1 else ""
            conf_record = cells[2] if len(cells) > 2 else ""
            pf = cells[3] if len(cells) > 3 else ""
            pa = cells[4] if len(cells) > 4 else ""
            teams.append(
                {
                    "team": team_name,
                    "overall": overall,
                    "conference_record": conf_record,
                    "pf": pf,
                    "pa": pa,
                }
            )

        if teams:
            conferences.append(
                {
                    "id": conf_name.lower().replace(" ", "_"),
                    "name": conf_name,
                    "teams": teams,
                }
            )

    log(f"Parsed {len(conferences)} conferences for NCAAF standings.")
    return conferences


def handle_ncaaf_polls_html(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parse AP / Coaches / possibly CFP polls from configured HTML pages.
    We return a list of poll objects matching your cfp-data.json schema.

    We'll parse each source independently and label them by `id` or descriptive name.
    """
    polls: List[Dict[str, Any]] = []

    for src in sources:
        url = src["url"]
        html = fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")

        # Very generic table parsing; you may want to specialize later.
        # Try to find a table with Rank / Team headers.
        table = None
        for t in soup.find_all("table"):
            headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
            if any("rank" in h for h in headers) and any("team" in h or "school" in h for h in headers):
                table = t
                break

        teams: List[Dict[str, Any]] = []
        if table:
            for row in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in row.find_all("td")]
                if not cells or not cells[0].isdigit():
                    continue
                try:
                    rank = int(cells[0])
                except ValueError:
                    continue
                team_name = cells[1] if len(cells) > 1 else ""
                record = cells[2] if len(cells) > 2 else ""
                teams.append(
                    {
                        "rank": rank,
                        "team": team_name,
                        "record": record,
                        "conference": "",
                    }
                )
        else:
            log(f"WARN: No poll table found at {url}; skipping.")

        name = "Poll"
        sid = src["id"]
        if "ap" in sid.lower():
            name = "AP Top 25"
        elif "coaches" in sid.lower():
            name = "Coaches Poll"
        elif "cfp" in sid.lower():
            name = "CFP Rankings"

        polls.append(
            {
                "name": name,
                "source_id": sid,
                "teams": sorted(teams, key=lambda t: t["rank"]) if teams else [],
            }
        )

    log(f"Parsed {len(polls)} poll objects.")
    return polls


def handle_ncaaf_games_html(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse games (scoreboard) from a primary HTML page.
    This is intentionally minimal and may need tuning later.
    """
    html = fetch_html(source["url"])
    soup = BeautifulSoup(html, "html.parser")

    games: List[Dict[str, Any]] = []

    # Very generic: look for game containers.
    for g in soup.find_all(["article", "section", "div"]):
        # This is intentionally conservative, you may refine with class names on ESPN
        text = g.get_text(" ", strip=True)
        if "vs" not in text and "@" not in text:
            continue

        # Extremely rough parsing – placeholder.
        # You will likely want to replace this with real scoreboard selectors.
        # For now, just skip to avoid garbage.
        continue

    log("Games handler currently stubbed; returning empty list.")
    return games


# Map dataset.kind -> handler function
HANDLERS = {
    "cfp_rankings_html": handle_cfp_rankings_html,
    "ncaaf_standings_html": handle_ncaaf_standings_html,
    "ncaaf_polls_html": handle_ncaaf_polls_html,
    "ncaaf_games_html": handle_ncaaf_games_html,
}


def choose_sources(dataset: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    prim = dataset.get("primary_sources", []) or []
    backup = dataset.get("backup_sources", []) or []
    return prim, backup


def run_dataset(dataset: Dict[str, Any], dry_run: bool) -> bool:
    did_something = False
    did_error = False

    if not dataset.get("enabled", False):
        log(f"[SKIP] {dataset['id']} (disabled)")
        return True

    dataset_id = dataset["id"]
    kind = dataset["kind"]
    output = dataset["output"]
    handler = HANDLERS.get(kind)

    if not handler:
        log(f"[ERROR] No handler for kind={kind} (dataset={dataset_id})")
        return False

    prim, backup = choose_sources(dataset)
    sources_to_try: List[Dict[str, Any]] = prim + backup

    if not sources_to_try:
        log(f"[ERROR] No sources configured for dataset={dataset_id}")
        return False

    # Decide if handler expects multiple sources or single
    multi_source = kind in ("ncaaf_polls_html",)

    data: Any = None
    last_error: str = ""

    if multi_source:
        try:
            data = handler(prim)  # type: ignore[arg-type]
        except Exception as e:
            last_error = str(e)
            did_error = True
            log(f"[ERROR] Handler failed for dataset={dataset_id}: {e}")
    else:
        for src in sources_to_try:
            try:
                data = handler(src)
                if data is not None:
                    break
            except Exception as e:
                last_error = str(e)
                log(f"[WARN] Handler failed for source={src.get('id')} dataset={dataset_id}: {e}")
                continue

    if data is None:
        log(f"[ERROR] No data produced for dataset={dataset_id}. Last error: {last_error}")
        return False

    out_path = ROOT / output["path"]
    out_field = output["field"]

    if dry_run:
        log(f"[DRY-RUN] Would update {out_path} field '{out_field}' with {len(data)} items.")
        return not did_error

    doc = load_json_file(out_path)
    doc[out_field] = data

    # Maintain/update global timestamps if cfp-data.json
    if "last_updated" in doc or out_path.name == "cfp-data.json":
        doc["last_updated"] = int(time.time())

    save_json_file(out_path, doc)
    log(f"[OK] Updated {out_path} field '{out_field}' with {len(data)} items.")
    did_something = True

    return not did_error and did_something


def main() -> int:
    cfg = load_config()
    defaults = cfg.get("defaults", {})
    dry_run = bool(defaults.get("dry_run", False))

    datasets: List[Dict[str, Any]] = cfg.get("datasets", [])
    # Sort by priority (desc) so important ones go first
    datasets = sorted(datasets, key=lambda d: d.get("priority", 0), reverse=True)

    if not datasets:
        log("No datasets configured.")
        return 0

    log(f"Starting universal ingestion (dry_run={dry_run}) for {len(datasets)} datasets")

    ok_all = True
    for ds in datasets:
        log(f"--- Dataset: {ds['id']} (kind={ds['kind']}) ---")
        ok = run_dataset(ds, dry_run=dry_run)
        ok_all = ok_all and ok

    if ok_all:
        log("Universal ingestion completed successfully.")
        return 0
    else:
        log("Universal ingestion completed with errors.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
