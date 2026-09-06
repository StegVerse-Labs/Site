#!/usr/bin/env python3
"""Build the current-season CFP/NCAAF public data projection.

The live file is intentionally fail-closed: historical CFP rankings are never
carried forward merely because a fetch failed or a timestamp changed.  Before the
committee publishes rankings for the current season, ``rankings`` remains empty
and the tracker exposes ``PRE_CFP_RANKINGS`` while still carrying current games
and non-CFP polls when those sources are available.

This is a public-data projection only.  It grants no sports, wagering, ticketing,
publication, governance, or execution authority.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "cfp-data.json"

ESPN_SCOREBOARD_URL = os.getenv(
    "CFP_SCOREBOARD_URL",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=100",
)
ESPN_RANKINGS_URL = os.getenv(
    "CFP_POLLS_URL",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings",
)
CFP_OFFICIAL_URL = "https://collegefootballplayoff.com/rankings.aspx"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "StegVerse-CFP-Live-Tracker/2026 (+https://stegverse.org)",
        },
    )
    with urlopen(request, timeout=25) as response:  # nosec B310 - fixed HTTPS public-data endpoints
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def record_from_competitor(row: dict[str, Any]) -> str:
    records = row.get("records") or []
    for record in records:
        if isinstance(record, dict) and record.get("type") == "total":
            return str(record.get("summary") or "")
    return ""


def parse_games(payload: dict[str, Any]) -> list[dict[str, Any]]:
    games: list[dict[str, Any]] = []
    for event in payload.get("events") or []:
        if not isinstance(event, dict):
            continue
        competitions = event.get("competitions") or []
        if not competitions or not isinstance(competitions[0], dict):
            continue
        competition = competitions[0]
        competitors = competition.get("competitors") or []
        home = next((c for c in competitors if isinstance(c, dict) and c.get("homeAway") == "home"), {})
        away = next((c for c in competitors if isinstance(c, dict) and c.get("homeAway") == "away"), {})
        home_team = (home.get("team") or {}) if isinstance(home, dict) else {}
        away_team = (away.get("team") or {}) if isinstance(away, dict) else {}
        status = (competition.get("status") or {}).get("type") or {}
        conference = ""
        notes = competition.get("notes") or []
        note = ""
        if notes and isinstance(notes[0], dict):
            note = str(notes[0].get("headline") or "")
        games.append(
            {
                "id": str(event.get("id") or ""),
                "home": str(home_team.get("displayName") or home_team.get("shortDisplayName") or "TBD"),
                "away": str(away_team.get("displayName") or away_team.get("shortDisplayName") or "TBD"),
                "home_score": int(home.get("score")) if str(home.get("score", "")).isdigit() else None,
                "away_score": int(away.get("score")) if str(away.get("score", "")).isdigit() else None,
                "home_record": record_from_competitor(home) if isinstance(home, dict) else "",
                "away_record": record_from_competitor(away) if isinstance(away, dict) else "",
                "status": str(status.get("shortDetail") or status.get("detail") or status.get("description") or ""),
                "kickoff": event.get("date"),
                "conference": conference,
                "note": note,
            }
        )
    return games


def normalize_poll_name(value: str) -> str:
    return " ".join(value.lower().replace("-", " ").split())


def is_cfp_poll(name: str) -> bool:
    normalized = normalize_poll_name(name)
    return "college football playoff" in normalized or normalized in {"cfp", "cfp rankings"}


def parse_polls(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    polls: list[dict[str, Any]] = []
    cfp_rankings: list[dict[str, Any]] = []
    cfp_poll_name: str | None = None

    for poll in payload.get("rankings") or []:
        if not isinstance(poll, dict):
            continue
        name = str(poll.get("name") or poll.get("shortName") or "Poll")
        teams: list[dict[str, Any]] = []
        for item in poll.get("ranks") or []:
            if not isinstance(item, dict):
                continue
            team = item.get("team") or {}
            record = str(item.get("recordSummary") or item.get("record") or "")
            rank = item.get("current") or item.get("rank")
            if not isinstance(rank, int):
                try:
                    rank = int(rank)
                except (TypeError, ValueError):
                    continue
            conference = ""
            groups = team.get("groups") or {}
            if isinstance(groups, dict):
                conference = str(groups.get("shortName") or groups.get("name") or "")
            teams.append(
                {
                    "rank": rank,
                    "team": str(team.get("displayName") or team.get("location") or "Unknown"),
                    "record": record,
                    "conference": conference,
                }
            )
        if not teams:
            continue
        source_id = "1" if is_cfp_poll(name) else "2"
        polls.append({"name": name, "source_id": source_id, "teams": teams})
        if is_cfp_poll(name):
            cfp_poll_name = name
            cfp_rankings = [
                {
                    "seed": team["rank"],
                    "team": team["team"],
                    "record": team["record"],
                    "conference": team["conference"],
                    "status": "in_play",
                    "lock_reason": "Current CFP committee ranking; playoff seed is not inferred unless explicitly published.",
                    "spot_scenarios": [],
                }
                for team in teams
            ]

    return polls, cfp_rankings, cfp_poll_name


def season_from_payload(scoreboard: dict[str, Any]) -> int:
    season = scoreboard.get("season") or {}
    try:
        return int(season.get("year"))
    except (TypeError, ValueError):
        return datetime.now(timezone.utc).year


def source_state(source_id: str, label: str, url: str, ok: bool, error: str | None = None) -> dict[str, Any]:
    return {
        "id": source_id,
        "label": label,
        "url": url,
        "status": "AVAILABLE" if ok else "UNAVAILABLE",
        "error": error,
    }


def main() -> int:
    fetched_at = now_iso()
    scoreboard: dict[str, Any] = {}
    poll_payload: dict[str, Any] = {}
    source_errors: dict[str, str] = {}

    try:
        scoreboard = fetch_json(ESPN_SCOREBOARD_URL)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        source_errors["scoreboard"] = f"{type(exc).__name__}: {exc}"

    try:
        poll_payload = fetch_json(ESPN_RANKINGS_URL)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        source_errors["polls"] = f"{type(exc).__name__}: {exc}"

    season = season_from_payload(scoreboard)
    games = parse_games(scoreboard)
    polls, rankings, cfp_poll_name = parse_polls(poll_payload)

    if cfp_poll_name and rankings:
        phase = "CFP_RANKINGS"
        rankings_state = "PUBLISHED_CURRENT_SEASON"
    else:
        phase = "PRE_CFP_RANKINGS"
        rankings_state = "NOT_YET_PUBLISHED_OR_NOT_OBSERVED"
        rankings = []

    data: dict[str, Any] = {
        "schema_version": "2.0.0",
        "season": season,
        "phase": phase,
        "last_updated": fetched_at,
        "freshness": {
            "generated_at": fetched_at,
            "current_season_only": True,
            "historical_rankings_carried_forward": False,
            "rankings_state": rankings_state,
            "source_errors": source_errors,
        },
        "sources": [
            source_state("1", "College Football Playoff", CFP_OFFICIAL_URL, bool(cfp_poll_name)),
            source_state("2", "ESPN College Football polls", ESPN_RANKINGS_URL, "polls" not in source_errors, source_errors.get("polls")),
            source_state("3", "ESPN College Football scoreboard", ESPN_SCOREBOARD_URL, "scoreboard" not in source_errors, source_errors.get("scoreboard")),
        ],
        "cfp_source_id": "1",
        "conf_source_id": None,
        "rankings": rankings,
        "polls": polls,
        "conferences": [],
        "games": games,
        "availability": {
            "cfp_rankings": rankings_state,
            "games": "AVAILABLE" if games else ("SOURCE_UNAVAILABLE" if "scoreboard" in source_errors else "NO_CURRENT_EVENTS_OBSERVED"),
            "polls": "AVAILABLE" if polls else ("SOURCE_UNAVAILABLE" if "polls" in source_errors else "NO_CURRENT_POLLS_OBSERVED"),
            "conference_standings": "NOT_YET_CANONICALLY_INGESTED",
        },
        "historical_reference": {
            "season": 2025,
            "path": "/sports/ncaaf/2025/",
            "included_in_current_rankings": False,
        },
        "authority": {
            "sports_officiating": False,
            "wagering": False,
            "ticketing": False,
            "governance": False,
            "publication": False,
        },
    }

    OUTPUT_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"CFP_INGESTION=PASS season={season} phase={phase} games={len(games)} polls={len(polls)} rankings={len(rankings)}")
    if source_errors:
        print("CFP_SOURCE_WARNINGS=" + json.dumps(source_errors, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
