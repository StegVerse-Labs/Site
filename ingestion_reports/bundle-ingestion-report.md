# Bundle Ingestion Report

Generated: `2026-05-10T19:36:07Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012e3-installed-bundle-archive-v1.zip`
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

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `updated` `data/bundle-ingestion-policy-v1.json` → `data/bundle-ingestion-policy-v1.json` — hash differs or target missing
- `created` `installed_bundles/README.md` → `installed_bundles/README.md` — hash differs or target missing
- `updated` `tools/bundle_ingest.py` → `tools/bundle_ingest.py` — hash differs or target missing
