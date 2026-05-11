# Bundle Ingestion Report

Generated: `2026-05-11T03:25:10Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms013-vaulted-capability-transition-layer-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `9`
- `applied`: `8`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`
- `installed_archived`: `1`
- `source_removed_from_incoming`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/headless-tasks/vaulted-capability-gate-v1.json` → `data/headless-tasks/vaulted-capability-gate-v1.json` — hash differs or target missing
- `created` `data/transition-table/vaulted-capability-transition-layer-v1.json` → `data/transition-table/vaulted-capability-transition-layer-v1.json` — hash differs or target missing
- `created` `data/vault/example-vaulted-capability-request-v1.json` → `data/vault/example-vaulted-capability-request-v1.json` — hash differs or target missing
- `created` `data/vault/vaulted-capability-policy-v1.json` → `data/vault/vaulted-capability-policy-v1.json` — hash differs or target missing
- `created` `docs/MS-013-vaulted-capability-transition-layer.md` → `docs/MS-013-vaulted-capability-transition-layer.md` — hash differs or target missing
- `created` `tools/vaulted_capability_gate.py` → `tools/vaulted_capability_gate.py` — hash differs or target missing
- `created` `vault_reports/README.md` → `vault_reports/README.md` — hash differs or target missing
