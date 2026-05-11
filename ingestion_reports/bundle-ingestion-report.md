# Bundle Ingestion Report

Generated: `2026-05-11T00:53:30Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012k-transition-discovery-ledger-v1.zip`
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
- `created` `data/headless-tasks/transition-discovery-ledger-v1.json` → `data/headless-tasks/transition-discovery-ledger-v1.json` — hash differs or target missing
- `created` `data/transition-table/transition-discovery-policy-v1.json` → `data/transition-table/transition-discovery-policy-v1.json` — hash differs or target missing
- `created` `docs/MS-012K-transition-discovery-ledger.md` → `docs/MS-012K-transition-discovery-ledger.md` — hash differs or target missing
- `created` `tools/transition_discovery_ledger.py` → `tools/transition_discovery_ledger.py` — hash differs or target missing
- `created` `transition_discovery_reports/README.md` → `transition_discovery_reports/README.md` — hash differs or target missing
