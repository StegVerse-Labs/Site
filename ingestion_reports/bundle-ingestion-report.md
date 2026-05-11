# Bundle Ingestion Report

Generated: `2026-05-11T03:50:42Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms013a-vaulted-capability-automation-runset-extension-v1.zip`
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
- `updated` `data/headless-task-runsets/transition-discovery-automation-runset-v1.json` → `data/headless-task-runsets/transition-discovery-automation-runset-v1.json` — hash differs or target missing
- `created` `docs/MS-013A-vaulted-capability-automation-runset-extension.md` → `docs/MS-013A-vaulted-capability-automation-runset-extension.md` — hash differs or target missing
- `updated` `transition_discovery_reports/README.md` → `transition_discovery_reports/README.md` — hash differs or target missing
