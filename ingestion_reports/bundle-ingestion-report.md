# Bundle Ingestion Report

Generated: `2026-05-10T19:14:29Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012f-deprecated-purpose-sandbox-review-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `6`
- `applied`: `5`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/deprecation-policy-v1.json` → `data/deprecation-policy-v1.json` — hash differs or target missing
- `created` `data/sandbox-review-policy-v1.json` → `data/sandbox-review-policy-v1.json` — hash differs or target missing
- `updated` `sandbox_reports/README.md` → `sandbox_reports/README.md` — hash differs or target missing
- `updated` `tools/sandbox_bundle_review.py` → `tools/sandbox_bundle_review.py` — hash differs or target missing
