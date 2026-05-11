# Bundle Ingestion Report

Generated: `2026-05-11T08:47:19Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012l3-public-canonical-page-contract-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `5`
- `applied`: `4`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`
- `installed_archived`: `1`
- `source_removed_from_incoming`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/canonical/public-canonical-page-status-v1.json` → `data/canonical/public-canonical-page-status-v1.json` — hash differs or target missing
- `created` `data/page-contracts/public-canonical-page-contract-v1.json` → `data/page-contracts/public-canonical-page-contract-v1.json` — hash differs or target missing
- `created` `docs/MS-012L3-public-canonical-page-contract.md` → `docs/MS-012L3-public-canonical-page-contract.md` — hash differs or target missing
