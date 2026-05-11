# Bundle Ingestion Report

Generated: `2026-05-11T08:35:27Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012l0-canonical-shell-dependency-map-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `8`
- `applied`: `7`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`
- `installed_archived`: `1`
- `source_removed_from_incoming`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/canonical/blocked-transitions-v1.json` → `data/canonical/blocked-transitions-v1.json` — hash differs or target missing
- `created` `data/canonical/execution-surfaces-v1.json` → `data/canonical/execution-surfaces-v1.json` — hash differs or target missing
- `created` `data/canonical/shells-v1.json` → `data/canonical/shells-v1.json` — hash differs or target missing
- `created` `data/canonical/transition-dependency-graph-v1.json` → `data/canonical/transition-dependency-graph-v1.json` — hash differs or target missing
- `created` `data/transition-table/execution-surface-transition-blocks-v1.json` → `data/transition-table/execution-surface-transition-blocks-v1.json` — hash differs or target missing
- `created` `docs/MS-012L0-canonical-shell-dependency-map.md` → `docs/MS-012L0-canonical-shell-dependency-map.md` — hash differs or target missing
