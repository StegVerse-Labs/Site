# Bundle Ingestion Report

Generated: `2026-05-11T02:00:53Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012k5-transition-automation-controller-v1.zip`
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
- `installed_archived`: `1`
- `source_removed_from_incoming`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/headless-tasks/transition-automation-controller-v1.json` → `data/headless-tasks/transition-automation-controller-v1.json` — hash differs or target missing
- `created` `data/transition-automation/transition-automation-controller-policy-v1.json` → `data/transition-automation/transition-automation-controller-policy-v1.json` — hash differs or target missing
- `created` `docs/MS-012K5-transition-automation-controller.md` → `docs/MS-012K5-transition-automation-controller.md` — hash differs or target missing
- `created` `tools/transition_automation_controller.py` → `tools/transition_automation_controller.py` — hash differs or target missing
