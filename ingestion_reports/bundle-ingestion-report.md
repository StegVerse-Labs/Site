# Bundle Ingestion Report

Generated: `2026-05-11T02:51:32Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012k6-approval-ingestion-engine-update-review-packet-v1.zip`
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
- `created` `docs/MS-012K6-approval-ingestion-engine-update-review-packet.md` → `docs/MS-012K6-approval-ingestion-engine-update-review-packet.md` — hash differs or target missing
- `created` `privileged_queue/ms012k6-ingestion-engine-update-review-packet.json` → `privileged_queue/ms012k6-ingestion-engine-update-review-packet.json` — hash differs or target missing
- `created` `privileged_queue/ms012k6-ingestion-engine-update-review-packet.md` → `privileged_queue/ms012k6-ingestion-engine-update-review-packet.md` — hash differs or target missing
- `created` `transition_authority_reports/ms012k6-ingestion-engine-update-authority-review.json` → `transition_authority_reports/ms012k6-ingestion-engine-update-authority-review.json` — hash differs or target missing
- `created` `transition_authority_reports/ms012k6-ingestion-engine-update-authority-review.md` → `transition_authority_reports/ms012k6-ingestion-engine-update-authority-review.md` — hash differs or target missing
