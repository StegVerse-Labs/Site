# Bundle Ingestion Report

Generated: `2026-05-10T18:45:02Z`
Mode: `apply`
Bundle: `/home/runner/work/Site/Site/incoming/ms012e-strict-ingestion-thresholds-v1.zip`
Bundle SHA-256: `b2f4073c5df8fd95dee99f33787c542a456c445c0d504ec701dbf905eed5dad2`
Verdict: `ALLOW`

## Summary

- `total_entries_seen`: `16`
- `applied`: `15`
- `would_apply`: `0`
- `unchanged`: `0`
- `skipped`: `1`
- `path_mappings`: `0`
- `unsafe_paths_rejected`: `0`

## Repo Transition

- `before_tree_fingerprint`: `13055eaa987b95f02a7781c4d31f2e881334ddaafb5dbf0639ebd40171f5eac9`
- `after_tree_fingerprint`: `abbe80e53e9a6d6815474e91ef387e91adae25ea4125a60044bc85d291b673e8`
- `changed_files_fingerprint`: `89a6a4de4b79d7af67cd57bcbc033e053aa6fc9556eab40133de5a9eb5b1c2b4`

## Path Mappings

No path mappings applied.

## File Decisions

- `skipped` `README.md` → `(none)` — bundle root README is documentation and is not applied to repo root
- `updated` `bundle-manifest.json` → `bundle-manifest.json` — hash differs or target missing
- `updated` `data/bundle-ingestion-policy-v1.json` → `data/bundle-ingestion-policy-v1.json` — hash differs or target missing
- `created` `data/capability-threshold-gates-v1.json` → `data/capability-threshold-gates-v1.json` — hash differs or target missing
- `created` `data/dependency-map-v1.json` → `data/dependency-map-v1.json` — hash differs or target missing
- `created` `data/stop-gap-policy-v1.json` → `data/stop-gap-policy-v1.json` — hash differs or target missing
- `created` `data/transition-capability-scopes-v1.json` → `data/transition-capability-scopes-v1.json` — hash differs or target missing
- `created` `dependency_reports/README.md` → `dependency_reports/README.md` — hash differs or target missing
- `created` `failed_bundles/README.md` → `failed_bundles/README.md` — hash differs or target missing
- `created` `privileged_queue/README.md` → `privileged_queue/README.md` — hash differs or target missing
- `created` `sandbox_queue/README.md` → `sandbox_queue/README.md` — hash differs or target missing
- `created` `sandbox_reports/README.md` → `sandbox_reports/README.md` — hash differs or target missing
- `updated` `tools/bundle_ingest.py` → `tools/bundle_ingest.py` — hash differs or target missing
- `created` `tools/capability_gate_check.py` → `tools/capability_gate_check.py` — hash differs or target missing
- `created` `tools/dependency_impact_scan.py` → `tools/dependency_impact_scan.py` — hash differs or target missing
- `created` `tools/sandbox_bundle_review.py` → `tools/sandbox_bundle_review.py` — hash differs or target missing
