# StegVerse CFP / NCAAF current-season tracker

The CFP surface is a **current-season public data projection**. It must never make a historical College Football Playoff ranking look current merely because a file or deployment timestamp changed.

## Current contract

`data/cfp-data.json` uses schema `2.0.0` and carries explicit season and phase metadata.

Supported phases:

- `PRE_CFP_RANKINGS` — current-season games and non-CFP polls may be displayed, but `rankings` MUST be empty. The page says that CFP committee rankings have not yet been published or observed.
- `CFP_RANKINGS` — current-season CFP committee rankings have been observed and may populate `rankings`.
- `SELECTION` — the selection-state projection may be shown only from current-season authoritative source data.
- `PLAYOFF` — playoff-state data may be shown only after current-season playoff data is observed.

AP, Coaches, ESPN, or other polls are never silently promoted into CFP committee rankings. Historical rankings are never carried forward into the current file.

## Canonical ingestion

The canonical ingestion entry point is:

```bash
python scripts/fetch_cfp_data.py
python scripts/check_cfp_data_freshness.py
```

`scripts/fetch_cfp_data.py` retrieves public college-football scoreboard and ranking/poll JSON, writes the current-season projection, and fails safe when a source is unavailable. It does **not** preserve an older CFP ranking simply to keep the table populated.

The scheduled/manual workflow is `.github/workflows/cfp_ingest.yml`. It invokes the same canonical script and validator rather than maintaining a second scraper.

Legacy files such as `cfp/cfp_ingest.py`, `scripts/ingest_sports.py`, and `ingest/ingest_config.yml` are not additional authorities for the live CFP contract. They remain legacy implementation debt until explicitly retired or redirected to the canonical path.

## Data semantics

Important fields in `data/cfp-data.json`:

- `season` — current UTC season year for this projection.
- `phase` — one of the supported phase values above.
- `last_updated` — time the projection was generated; it does **not** prove that every upstream source changed at that time.
- `freshness.current_season_only` — must be `true`.
- `freshness.historical_rankings_carried_forward` — must be `false`.
- `freshness.rankings_state` — explains whether current CFP rankings were actually observed.
- `availability` — per-surface availability/degraded-state information.
- `historical_reference` — pointer to retained historical material; `included_in_current_rankings` must remain `false`.

A source fetch failure is represented as unavailable/degraded data. It is not repaired by copying an old ranking forward.

## Public rendering

`cfp/cfp.js` consumes `/data/cfp-data.json`. The UI must distinguish “no current CFP rankings yet” from an ingestion failure and from a legitimately empty current event set. The 2025 historical lane remains available separately under `/sports/ncaaf/2025/` and is not the live 2026 ranking source.

## Sources

Current canonical ingestion uses public college-football data endpoints for scoreboard and poll projection and retains the College Football Playoff site as the CFP authority reference. Source availability is recorded in the data file.

No provider credential, API key, TV/TVC credential material, GitHub token runtime authority, wagering authority, ticketing authority, or sports-officiating authority is created by this tracker.

## Validation

Run:

```bash
python scripts/check_cfp_data_freshness.py
```

The validator fails if, among other things:

- the live season is not the current UTC year;
- `PRE_CFP_RANKINGS` contains CFP rankings;
- a ranking phase lacks current rankings;
- historical rankings are marked as carried forward;
- a current source points at a 2025 snapshot;
- the required README completeness markers are missing.

Source, CI, merge, workflow success, or deployment alone does not prove a current public data observation. Public verification remains a separate completion predicate.
