# Bundle Ingestion Report

Generated: `2026-05-11T08:40:09Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012l1-transition-table-self-correction-ledger-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `7`
- `applied`: `6`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`
- `installed_archived`: `1`
- `source_removed_from_incoming`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/canonical/transition-correction-ledger-v1.json` → `data/canonical/transition-correction-ledger-v1.json` — hash differs or target missing
- `created` `data/canonical/transition-evidence-schema-v1.json` → `data/canonical/transition-evidence-schema-v1.json` — hash differs or target missing
- `created` `data/canonical/transition-status-index-v1.json` → `data/canonical/transition-status-index-v1.json` — hash differs or target missing
- `created` `data/transition-table/transition-table-self-correction-model-v1.json` → `data/transition-table/transition-table-self-correction-model-v1.json` — hash differs or target missing
- `created` `docs/MS-012L1-transition-table-self-correction-ledger.md` → `docs/MS-012L1-transition-table-self-correction-ledger.md` — hash differs or target missing
