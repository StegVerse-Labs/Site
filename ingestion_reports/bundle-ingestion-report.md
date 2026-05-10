# Bundle Ingestion Report

Generated: `2026-05-10T11:59:34Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ingestion-smoke-test-bundle-v1.zip`
Bundle SHA-256: `645dcc3dbef900e9920d9a782e79ac5cbb90c46f25a58249afa6f75210d332d1`
Verdict: `ALLOW`

## Summary

- `total_entries_seen`: `3`
- `applied`: `2`
- `would_apply`: `0`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`

## Repo Transition

- `before_tree_fingerprint`: `54e3a9ae922bc5f91ca3dcf34f4c51e711b31595a35c828857fc736fd424851a`
- `after_tree_fingerprint`: `7c9a7aa6c55854e35d36fac159aa4a32e068d60321e675ed39dd20fef70b1b20`
- `changed_files_fingerprint`: `866f4a6412afdb595a3751abc221a611e0461205e4cb78dff28b4daebcbffd0b`

## Path Mappings

No path mappings applied.

## File Decisions

- `skipped` `README.md` → `(none)` — bundle root README is documentation and is not applied to repo root
- `created` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `created` `data/ingestion-smoke-test-v1.json` → `data/ingestion-smoke-test-v1.json` — hash differs or target missing
