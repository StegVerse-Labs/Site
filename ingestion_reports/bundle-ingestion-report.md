# Bundle Ingestion Report

Generated: `2026-05-10T19:42:50Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/installed-bundle-archive-smoke-test-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `3`
- `applied`: `2`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`
- `installed_archived`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/installed-bundle-archive-smoke-test-v1.json` → `data/installed-bundle-archive-smoke-test-v1.json` — hash differs or target missing
