# CFP Live Tracker Mirror Handoff

## Source of truth

This file is the bounded continuation record for the College Football Playoff / NCAAF live-tracker lane in `StegVerse-Labs/Site`.

Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. This handoff grants no execution, publication, activation, licensing, affiliation, wagering, ticketing, or external-data authority.

## Goal

Restore the existing `/cfp/` surface into a current-season, self-describing college-football tracker that can reliably render current games, rankings/polls when available, conference context, source provenance, and ticket links without presenting stale data as live.

## Current repository state observed 2026-09-05

Implemented surfaces:

- `cfp/index.html` redirects to `cfp/cfp.html`.
- `cfp/cfp.html`, `cfp/cfp.css`, and `cfp/cfp.js` implement the primary tracker UI.
- `cfp/bracket.html` / `cfp/bracket.js` implement a bracket surface.
- `cfp/team.html` / `cfp/cfp-team.js` implement a team-detail surface.
- `data/cfp-tickets.json` provides config-driven ticket-provider links.
- Multiple ingestion experiments exist under `scripts/`, `tools/cfp/`, `ingest/`, and `cfp/`.

Current defects / stale assumptions:

1. `data/cfp-data.json` is stamped in September 2026 but contains a 2025 final CFP ranking snapshot and empty `games`, `polls`, and `conferences` arrays.
2. `scripts/fetch_cfp_data.py` explicitly leaves rankings, standings, games, and polls ingestion as stubs/TODOs.
3. `data/README-cfp-source.md` states that `.github/workflows/cfp_ingest.yml` updates the live file, but that workflow is absent from `main`.
4. Multiple overlapping ingestion implementations exist and do not share one canonical contract.
5. The UI labels the product as a live tracker even when the dataset is stale or structurally incomplete.
6. The current 2026 regular season is underway, while official CFP committee rankings are not yet available; the product must distinguish AP/other poll data from official CFP rankings instead of substituting one for another.

## Collision check

No open pull request matching CFP / college-football work was observed before this branch was created.

Branch owner for this continuation:

`goal/cfp-live-2026-revival`

## Machine preflight status

Required repository preflight commands are:

```text
python scripts/site_handoff_orchestrator.py
python scripts/check_ecosystem_heartbeat_orchestration.py
```

The current ChatGPT execution container could not resolve `github.com`, so it could not clone the repository and run those commands locally. Functional mutation is therefore fail-closed until equivalent repository validation runs on the branch/PR execution surface.

Governance/documentation-only creation of this handoff is admitted as the required first action for a repo lane that previously lacked a `*_MIRROR_HANDOFF.md`.

## README impact determination

Functional restoration of CFP data ingestion materially changes Site behavior and freshness semantics. Therefore `cfp/README_CFP.md` and the relevant repository-level documentation must be updated in the same functional change set. No determination of "README change not required" is admissible for the planned restoration.

## Canonical restoration sequence

1. Preserve this handoff and branch ownership.
2. Run repository preflight/validation through the available GitHub execution surface before functional merge.
3. Select one canonical CFP/college-football data contract and retire or mark superseded duplicate ingestion paths.
4. Make freshness explicit in the schema: season, data class, generated-at, source timestamps, and stale/error state.
5. Do not claim official CFP rankings before the committee publishes them; render "not yet released" while still showing current-season games and other clearly labeled poll data.
6. Restore a scheduled/manual ingestion workflow that writes the canonical JSON and fails closed rather than refreshing stale historical data timestamps.
7. Add validation that rejects season/date mismatches such as a 2026 timestamp attached to 2025 CFP final rankings without an explicit historical-snapshot label.
8. Update the UI to show source/freshness state and degrade gracefully when rankings/polls/standings are unavailable.
9. Validate `/cfp/`, `/cfp/cfp.html`, bracket, team pages, data loading, mobile rendering, and external ticket-link generation.
10. After merge/deployment, verify public behavior before describing the tracker as live.

## Remaining files/modules to install or repair

Destination `StegVerse-Labs/Site`:

- canonical CFP data schema / validator
- one canonical ingestion script
- `.github/workflows/cfp_ingest.yml` or successor scheduled/manual workflow
- current-season game ingestion
- clearly labeled AP poll ingestion when available
- official CFP ranking ingestion only when published
- optional conference-standings ingestion after source/licensing review
- stale-data/freshness UI state
- CFP browser/static validation coverage
- updates to `cfp/README_CFP.md`, `data/README-cfp-source.md`, and `docs/SITE_MIRROR_HANDOFF.md`

Potential later integrations after verified Site behavior:

- `GCAT-BCAT-Engine/Publisher` for governed publication projection if this sports lane becomes a publication source
- `StegVerse-Labs/admissibility-wiki` only if sports data provenance/admissibility semantics become relevant
- `StegVerse-002/stegguardian-wiki` only if guardian-policy semantics are introduced

No downstream integration is activated by this handoff.

## Completion predicate

This goal is not complete until:

- current-season game data is generated from an identified source;
- stale 2025 data cannot masquerade as current 2026 data;
- official CFP ranking availability is represented accurately;
- the canonical update workflow is present and passing;
- the UI renders valid data and explicit degraded states;
- repository validation passes;
- deployed/public behavior is observed;
- this handoff and repository documentation are updated with completion evidence.
