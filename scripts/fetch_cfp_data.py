#!/usr/bin/env python3
"""Build the current-season CFP/NCAAF public data projection.

The live file is fail-closed: historical CFP rankings are never carried forward
merely because a fetch failed or a timestamp changed. Before current-season CFP
committee rankings are actually observed, ``rankings`` remains empty and the
tracker exposes ``PRE_CFP_RANKINGS`` while current games and separately labelled
polls may still be shown.

Current scoreboard/AP data comes from the public, credential-free henrygd/ncaa-api
projection of NCAA data. That source is supporting NCAAF data only and is never
promoted to CFP committee authority.

CFP committee rankings come from the ESPN rankings API's structured projection
of the committee's published Top 25 (the official CFP site no longer serves a
parseable rankings table; its ``rankings.aspx`` URL is dead). The poll is
validated before use (exactly 25 ranks, seeds 1-25, current-season poll date);
any fetch or shape failure degrades explicitly through ``source_errors`` and
the rankings remain unobserved rather than stale or inferred.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "cfp-data.json"

NCAA_API_BASE = os.getenv("NCAA_API_BASE", "https://ncaa-api.henrygd.me").rstrip("/")
NCAA_SCOREBOARD_URL = os.getenv("CFP_SCOREBOARD_URL", f"{NCAA_API_BASE}/scoreboard/football/fbs")
NCAA_AP_URL = os.getenv("CFP_POLLS_URL", f"{NCAA_API_BASE}/rankings/football/fbs/associated-press")
CFP_OFFICIAL_URL = "https://collegefootballplayoff.com/rankings.aspx"
CFP_RANKINGS_PAGE_URL = "https://collegefootballplayoff.com/rankings"
ESPN_RANKINGS_URL = os.getenv(
    "CFP_RANKINGS_URL",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings",
)
ESPN_STANDINGS_URL = os.getenv(
    "CFP_STANDINGS_URL",
    "https://site.api.espn.com/apis/v2/sports/football/college-football/standings",
)
ESPN_SCOREBOARD_URL = os.getenv(
    "CFP_SCOREBOARD_ESPN_URL",
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
)
NCAA_ORIGIN_URL = "https://www.ncaa.com/scoreboard/football/fbs"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126 Safari/537.36"
)


def fetch_json(url: str, user_agent: str | None = None) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": user_agent or "StegVerse-CFP-Live-Tracker/2026 (+https://stegverse.org)",
        },
    )
    with urlopen(request, timeout=25) as response:  # nosec B310 - HTTPS public-data endpoints only
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def team_name(team: dict[str, Any]) -> str:
    names = team.get("names") or {}
    if isinstance(names, dict):
        return str(names.get("full") or names.get("short") or names.get("seo") or "TBD")
    return "TBD"


def numeric_score(value: Any) -> int | None:
    text = str(value or "").strip()
    return int(text) if text.isdigit() else None


def kickoff_from_epoch(value: Any) -> str | None:
    try:
        epoch = float(value)
    except (TypeError, ValueError):
        return None
    if epoch > 10_000_000_000:
        epoch /= 1000.0
    try:
        return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return None


def conference_name(team: dict[str, Any]) -> str:
    conferences = team.get("conferences") or []
    if conferences and isinstance(conferences[0], dict):
        return str(conferences[0].get("conferenceName") or conferences[0].get("conferenceSeo") or "")
    return ""


def parse_ncaa_games(payload: dict[str, Any]) -> list[dict[str, Any]]:
    games: list[dict[str, Any]] = []
    for wrapper in payload.get("games") or []:
        if not isinstance(wrapper, dict):
            continue
        game = wrapper.get("game") if isinstance(wrapper.get("game"), dict) else wrapper
        if not isinstance(game, dict):
            continue
        home = game.get("home") or {}
        away = game.get("away") or {}
        if not isinstance(home, dict) or not isinstance(away, dict):
            continue
        state = str(game.get("gameState") or "").lower()
        final_message = str(game.get("finalMessage") or "").strip()
        if state == "final":
            status = final_message or "Final"
        elif state == "live":
            period = str(game.get("currentPeriod") or "").strip()
            clock = str(game.get("contestClock") or "").strip()
            status = " ".join(part for part in (period, clock) if part) or "Live"
        else:
            status = str(game.get("startTime") or "Scheduled")
        kickoff = kickoff_from_epoch(game.get("startTimeEpoch"))
        games.append(
            {
                "id": str(game.get("gameID") or game.get("id") or ""),
                "home": team_name(home),
                "away": team_name(away),
                "home_score": numeric_score(home.get("score")),
                "away_score": numeric_score(away.get("score")),
                "home_record": "",
                "away_record": "",
                "status": status,
                "kickoff": kickoff,
                "conference": conference_name(home) or conference_name(away),
                "note": str(game.get("title") or game.get("network") or ""),
            }
        )
    return games


def parse_rank(value: Any) -> int | None:
    match = re.search(r"\d+", str(value or ""))
    return int(match.group(0)) if match else None


def strip_first_place_votes(value: Any) -> str:
    text = str(value or "").strip()
    return re.sub(r"\s+\(\d+\)\s*$", "", text).strip()


def parse_ncaa_ap_poll(payload: dict[str, Any]) -> list[dict[str, Any]]:
    teams: list[dict[str, Any]] = []
    for row in payload.get("data") or []:
        if not isinstance(row, dict):
            continue
        rank = parse_rank(row.get("RANK"))
        team = strip_first_place_votes(row.get("SCHOOL (1ST VOTES)"))
        if rank is None or not team:
            continue
        teams.append({"rank": rank, "team": team, "record": "", "conference": ""})
    if not teams:
        return []
    return [
        {
            "name": str(payload.get("title") or "Associated Press Top 25"),
            "source_id": "2",
            "updated": payload.get("updated"),
            "teams": teams,
        }
    ]


def espn_poll(payload: dict[str, Any], poll_type: str) -> dict[str, Any] | None:
    for poll in payload.get("rankings") or []:
        if isinstance(poll, dict) and poll.get("type") == poll_type:
            return poll
    return None


def espn_team_name(team: dict[str, Any]) -> str:
    location = str(team.get("location") or "").strip()
    name = str(team.get("name") or "").strip()
    full = " ".join(part for part in (location, name) if part)
    return full or str(team.get("displayName") or team.get("shortDisplayName") or "TBD")


def espn_conference(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("name") or value.get("shortName") or "")
    return str(value or "")


def parse_espn_cfp_rankings(payload: dict[str, Any], season_year: int) -> list[dict[str, Any]]:
    """Normalize the committee poll to the schema 2.0.0 rankings shape.

    Raises ValueError on any shape violation; the caller degrades explicitly
    and the rankings stay unobserved. Nothing is inferred or carried forward.
    """
    poll = espn_poll(payload, "cfp")
    if poll is None:
        raise ValueError("ESPN rankings payload carries no 'cfp' poll")
    poll_date = str(poll.get("date") or "")
    if not poll_date.startswith(f"{season_year}-"):
        raise ValueError(f"CFP poll date {poll_date!r} is not in the {season_year} season")
    ranks = poll.get("ranks") or []
    if len(ranks) != 25:
        raise ValueError(f"CFP poll carries {len(ranks)} ranks, expected 25")
    rankings: list[dict[str, Any]] = []
    seen: set[int] = set()
    for entry in ranks:
        if not isinstance(entry, dict):
            raise ValueError("CFP poll rank entry is not an object")
        seed = entry.get("current")
        if not isinstance(seed, int) or not 1 <= seed <= 25 or seed in seen:
            raise ValueError(f"CFP poll seed invalid or duplicated: {seed!r}")
        seen.add(seed)
        team = entry.get("team") or {}
        if not isinstance(team, dict):
            raise ValueError("CFP poll team entry is not an object")
        rankings.append(
            {
                "seed": seed,
                "team": espn_team_name(team),
                "team_id": str(team.get("id") or ""),
                "record": str(entry.get("recordSummary") or ""),
                "conference": espn_conference(entry.get("conference")),
                "status": "in_play",
                "lock_reason": "",
                "spot_scenarios": [],
                "previous": entry.get("previous"),
                "trend": str(entry.get("trend") or ""),
                "first_round_bye": bool(entry.get("firstRoundBye")),
            }
        )
    if seen != set(range(1, 26)):
        raise ValueError("CFP poll seeds are not exactly 1-25")
    rankings.sort(key=lambda row: row["seed"])
    return rankings


def espn_poll_rank_map(payload: dict[str, Any], poll_type: str) -> dict[str, int]:
    """team_id -> rank for one poll in the ESPN rankings payload."""
    poll = espn_poll(payload, poll_type)
    result: dict[str, int] = {}
    if poll is None:
        return result
    for entry in poll.get("ranks") or []:
        if not isinstance(entry, dict):
            continue
        team = entry.get("team") or {}
        rank = entry.get("current")
        if isinstance(team, dict) and team.get("id") is not None and isinstance(rank, int):
            result[str(team["id"])] = rank
    return result


def parse_espn_conference_records(payload: dict[str, Any]) -> dict[str, str]:
    """team_id -> conference record (e.g. '5-1') from the ESPN standings tree.

    The standings payload groups each team's stats; the conference record is
    the stat named 'vs. Conf.'. Anything unparseable is simply absent, and
    the page renders the overall record alone.
    """
    records: dict[str, str] = {}

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            team = node.get("team")
            stats = node.get("stats")
            if isinstance(team, dict) and team.get("id") is not None and isinstance(stats, list):
                for stat in stats:
                    if isinstance(stat, dict) and stat.get("name") == "vs. Conf.":
                        value = str(stat.get("displayValue") or stat.get("summary") or "").strip()
                        if value and value != "-":
                            records[str(team["id"])] = value
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    visit(payload)
    return records


def espn_next_games(season_year: int, fetch: Any) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """team_id -> next scheduled game, from ESPN scoreboard windows.

    Candidates are today's not-yet-started games plus the next three weeks.
    A game in progress or already final is the current game, not the next
    one. Raises only when the current week cannot be established; a failed
    week fetch narrows the window and is returned as a recorded error.
    """
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    board = fetch(f"{ESPN_SCOREBOARD_URL}?dates={today}&groups=80&limit=200")
    week_number = ((board.get("week") or {}).get("number")) if isinstance(board, dict) else None
    if not isinstance(week_number, int):
        raise ValueError("ESPN scoreboard payload carries no current week number")
    boards: list[dict[str, Any]] = [board]
    errors: list[str] = []
    for week in (week_number + 1, week_number + 2, week_number + 3):
        try:
            boards.append(
                fetch(f"{ESPN_SCOREBOARD_URL}?year={season_year}&week={week}&seasontype=2&groups=80&limit=200")
            )
        except Exception as exc:  # per-week failure: recorded, window narrows
            errors.append(f"week {week}: {type(exc).__name__}: {exc}")
    next_games: dict[str, dict[str, Any]] = {}
    for payload in boards:
        for event in payload.get("events") or []:
            if not isinstance(event, dict):
                continue
            status = ((event.get("status") or {}).get("type") or {}).get("name")
            if status != "STATUS_SCHEDULED":
                continue
            date = str(event.get("date") or "")
            competitions = event.get("competitions") or []
            if not competitions or not isinstance(competitions[0], dict):
                continue
            competitors = competitions[0].get("competitors") or []
            by_id: dict[str, dict[str, Any]] = {}
            for comp in competitors:
                if isinstance(comp, dict) and isinstance(comp.get("team"), dict):
                    by_id[str(comp["team"].get("id"))] = comp
            for team_id, comp in by_id.items():
                opponent = next((c for tid, c in by_id.items() if tid != team_id), None)
                if opponent is None:
                    continue
                opp_team = opponent.get("team") or {}
                candidate = {
                    "next_opponent": str(opp_team.get("location") or opp_team.get("displayName") or ""),
                    "next_date": date,
                    "next_home": comp.get("homeAway") == "home",
                }
                current = next_games.get(team_id)
                if current is None or date < str(current.get("next_date") or "9999"):
                    next_games[team_id] = candidate
    return next_games, errors


def parse_espn_ap_poll(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """AP Top 25 from the same ESPN payload, as a separately labelled poll."""
    poll = espn_poll(payload, "ap")
    if poll is None:
        return []
    teams: list[dict[str, Any]] = []
    for entry in poll.get("ranks") or []:
        if not isinstance(entry, dict):
            continue
        rank = entry.get("current")
        team = entry.get("team") or {}
        if not isinstance(rank, int) or not isinstance(team, dict):
            continue
        teams.append(
            {
                "rank": rank,
                "team": espn_team_name(team),
                "record": str(entry.get("recordSummary") or ""),
                "conference": espn_conference(entry.get("conference")),
            }
        )
    if not teams:
        return []
    teams.sort(key=lambda row: row["rank"])
    return [
        {
            "name": str(poll.get("name") or "AP Top 25"),
            "source_id": "2",
            "updated": poll.get("date"),
            "teams": teams,
        }
    ]


def source_state(source_id: str, label: str, url: str, status: str, error: str | None = None, origin: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"id": source_id, "label": label, "url": url, "status": status, "error": error}
    if origin:
        result["origin"] = origin
    return result


def main() -> int:
    fetched_at = now_iso()
    current_year = datetime.now(timezone.utc).year
    source_errors: dict[str, str] = {}
    scoreboard: dict[str, Any] = {}
    ap_payload: dict[str, Any] = {}

    try:
        scoreboard = fetch_json(NCAA_SCOREBOARD_URL)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        source_errors["scoreboard"] = f"{type(exc).__name__}: {exc}"

    try:
        ap_payload = fetch_json(NCAA_AP_URL)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        source_errors["polls"] = f"{type(exc).__name__}: {exc}"

    games = parse_ncaa_games(scoreboard)
    polls = parse_ncaa_ap_poll(ap_payload)

    # CFP committee rankings: observed only from the structured projection of
    # the committee's published Top 25, validated by parse_espn_cfp_rankings.
    # No supporting poll may become a CFP committee ranking, and a failed or
    # misshapen observation degrades explicitly -- never silently, never by
    # carrying a prior table forward.
    rankings: list[dict[str, Any]] = []
    espn_payload: dict[str, Any] = {}
    try:
        # ESPN's API refuses non-browser user agents (403); that refusal is
        # part of this source's presentation and is absorbed here, at the
        # boundary, rather than propagated as a pipeline failure.
        espn_payload = fetch_json(ESPN_RANKINGS_URL, user_agent=BROWSER_USER_AGENT)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        source_errors["cfp_rankings"] = f"{type(exc).__name__}: {exc}"
    if espn_payload:
        try:
            rankings = parse_espn_cfp_rankings(espn_payload, current_year)
        except ValueError as exc:
            source_errors["cfp_rankings"] = f"ValueError: {exc}"
        if not polls:
            polls = parse_espn_ap_poll(espn_payload)
            if polls:
                source_errors.pop("polls", None)
    if rankings:
        # Four-column join: each committee-ranked team also carries its AP and
        # Coaches ranks (same payload, joined on ESPN team id) and its
        # conference record (standings). sv_rank is reserved for the StegVerse
        # ranking and stays null until that ranking's rules are established;
        # the page renders an honest placeholder, never an invented value.
        ap_ranks = espn_poll_rank_map(espn_payload, "ap")
        coaches_ranks = espn_poll_rank_map(espn_payload, "usa")
        conference_records: dict[str, str] = {}
        try:
            standings = fetch_json(
                f"{ESPN_STANDINGS_URL}?season={current_year}",
                user_agent=BROWSER_USER_AGENT,
            )
            conference_records = parse_espn_conference_records(standings)
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            source_errors["standings"] = f"{type(exc).__name__}: {exc}"
        # SV ranks come only from a sealed SV segment file; absent or
        # unreadable, the column stays empty rather than approximated.
        sv_ranks: dict[str, int] = {}
        try:
            sv_doc = json.loads((ROOT / "data" / "sv-rankings.json").read_text(encoding="utf-8"))
            sv_ranks = {str(k): int(v) for k, v in (sv_doc.get("ranks") or {}).items()}
        except (OSError, ValueError, json.JSONDecodeError):
            sv_ranks = {}
        for row in rankings:
            team_id = str(row.get("team_id") or "")
            row["ap_rank"] = ap_ranks.get(team_id)
            row["coaches_rank"] = coaches_ranks.get(team_id)
            row["sv_rank"] = sv_ranks.get(team_id)
            if "indep" in str(row.get("conference") or "").lower():
                row["conference_record"] = ""
            else:
                row["conference_record"] = conference_records.get(team_id, "")
        try:
            next_games, next_errors = espn_next_games(
                current_year,
                lambda url: fetch_json(url, user_agent=BROWSER_USER_AGENT),
            )
            if next_errors:
                source_errors["next_games"] = "; ".join(next_errors)
            for row in rankings:
                nxt = next_games.get(str(row.get("team_id") or ""))
                row["next_opponent"] = nxt["next_opponent"] if nxt else None
                row["next_date"] = nxt["next_date"] if nxt else None
                row["next_home"] = nxt["next_home"] if nxt else None
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            source_errors["next_games"] = f"{type(exc).__name__}: {exc}"
            for row in rankings:
                row["next_opponent"] = None
                row["next_date"] = None
                row["next_home"] = None

    if rankings:
        phase = "CFP_RANKINGS"
        rankings_state = "PUBLISHED_CURRENT_SEASON"
    else:
        phase = "PRE_CFP_RANKINGS"
        rankings_state = "NOT_YET_PUBLISHED_OR_NOT_OBSERVED"

    data: dict[str, Any] = {
        "schema_version": "2.0.0",
        "season": current_year,
        "phase": phase,
        "last_updated": fetched_at,
        "freshness": {
            "generated_at": fetched_at,
            "current_season_only": True,
            "historical_rankings_carried_forward": False,
            "rankings_state": rankings_state,
            "source_errors": source_errors,
            "supporting_source_observed": bool(games or polls),
        },
        "sources": [
            source_state(
                "1",
                "College Football Playoff Rankings (committee Top 25, ESPN rankings API projection)",
                ESPN_RANKINGS_URL,
                "AVAILABLE" if rankings else ("UNAVAILABLE" if "cfp_rankings" in source_errors else "NOT_YET_OBSERVED_FOR_CURRENT_SEASON"),
                source_errors.get("cfp_rankings"),
                CFP_RANKINGS_PAGE_URL,
            ),
            source_state(
                "2",
                "NCAA-derived AP Top 25 JSON (henrygd/ncaa-api)",
                NCAA_AP_URL,
                "AVAILABLE" if polls else ("UNAVAILABLE" if "polls" in source_errors else "NO_CURRENT_DATA_OBSERVED"),
                source_errors.get("polls"),
                "https://www.ncaa.com/rankings/football/fbs/associated-press",
            ),
            source_state(
                "3",
                "NCAA-derived FBS scoreboard JSON (henrygd/ncaa-api)",
                NCAA_SCOREBOARD_URL,
                "AVAILABLE" if games else ("UNAVAILABLE" if "scoreboard" in source_errors else "NO_CURRENT_EVENTS_OBSERVED"),
                source_errors.get("scoreboard"),
                NCAA_ORIGIN_URL,
            ),
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
    print(f"CFP_INGESTION=PASS season={current_year} phase={phase} games={len(games)} polls={len(polls)} rankings={len(rankings)}")
    if source_errors:
        print("CFP_SOURCE_WARNINGS=" + json.dumps(source_errors, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
