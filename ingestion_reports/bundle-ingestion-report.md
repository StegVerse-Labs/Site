# Bundle Ingestion Report

Generated: `2026-05-11T01:59:40Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012k3r-failed-bundle-boundary-processor-v1.zip`
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
- `created` `data/headless-tasks/failed-bundle-boundary-processor-v1.json` → `data/headless-tasks/failed-bundle-boundary-processor-v1.json` — hash differs or target missing
- `created` `data/transition-table/failed-bundle-boundary-policy-v1.json` → `data/transition-table/failed-bundle-boundary-policy-v1.json` — hash differs or target missing
- `created` `docs/MS-012K3R-failed-bundle-boundary-processor.md` → `docs/MS-012K3R-failed-bundle-boundary-processor.md` — hash differs or target missing
- `created` `reviewed_failed_bundles/README.md` → `reviewed_failed_bundles/README.md` — hash differs or target missing
- `created` `tools/failed_bundle_boundary_processor.py` → `tools/failed_bundle_boundary_processor.py` — hash differs or target missing
- `updated` `transition_discovery_reports/README.md` → `transition_discovery_reports/README.md` — hash differs or target missing
