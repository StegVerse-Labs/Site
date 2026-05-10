# Bundle Ingestion Report

Generated: `2026-05-10T22:38:57Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012i-site-ephemeral-sandbox-protocols-v1.zip`
Verdict: `ALLOW`
Route: `ingest`
Bundle class: `ordinary_bundle`

## Summary

- `total_entries_seen`: `10`
- `applied`: `9`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`
- `installed_archived`: `1`
- `source_removed_from_incoming`: `1`

## File Decisions

- `skipped` `README.md` → `None` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/headless-tasks/ephemeral-sandbox-run-v1.json` → `data/headless-tasks/ephemeral-sandbox-run-v1.json` — hash differs or target missing
- `created` `data/sandbox/ephemeral-sandbox-policy-v1.json` → `data/sandbox/ephemeral-sandbox-policy-v1.json` — hash differs or target missing
- `created` `docs/MS-012I-site-ephemeral-sandbox-protocols.md` → `docs/MS-012I-site-ephemeral-sandbox-protocols.md` — hash differs or target missing
- `updated` `incoming/README.md` → `incoming/README.md` — hash differs or target missing
- `updated` `sandbox_queue/README.md` → `sandbox_queue/README.md` — hash differs or target missing
- `updated` `sandbox_reports/README.md` → `sandbox_reports/README.md` — hash differs or target missing
- `created` `sandbox_reviewed/README.md` → `sandbox_reviewed/README.md` — hash differs or target missing
- `created` `tools/ephemeral_sandbox_runner.py` → `tools/ephemeral_sandbox_runner.py` — hash differs or target missing
