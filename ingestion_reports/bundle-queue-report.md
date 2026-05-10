# Bundle Queue Report

Generated: `2026-05-10T20:54:57Z`
Milestone: `MS-012E.5 — Default Queue Mode Ingestor`
Mode: `apply`
Bundles seen: `19`
Stale files seen: `1`

## Results

- `ingestion-smoke-test-bundle-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `installed-bundle-archive-smoke-test-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_installed; quarantined as stale queue debris instead of being silently skipped.
- `ms012-promotion-bundle-v1.zip` → `ALLOW` / `ingest` — ordinary bundle allowed
- `ms012d-workflow-report-evidence-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_privileged_routed; quarantined as stale queue debris instead of being silently skipped.
- `ms012d1-evidence-artifact-routing-v1.zip` → `SANDBOX_REQUIRED` / `sandbox_queue` — automatic queue mode must not apply bundles that mutate the ingestion engine
- `ms012e-strict-ingestion-thresholds-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `ms012e1-stale-incoming-quarantine-v1.zip` → `SANDBOX_REQUIRED` / `sandbox_queue` — automatic queue mode must not apply bundles that mutate the ingestion engine
- `ms012e2-already-seen-incoming-quarantine-fix-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `ms012e3-installed-bundle-archive-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `ms012e4-declared-task-runner-v1.zip` → `ALLOW` / `ingest` — ordinary bundle allowed
- `ms012e5-default-queue-mode-ingestor-v1.zip` → `SANDBOX_REQUIRED` / `sandbox_queue` — automatic queue mode must not apply bundles that mutate the ingestion engine
- `ms012f-deprecated-purpose-sandbox-review-v1.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `ms012f-lifecycle-reconciler-v1.zip` → `ALLOW` / `ingest` — ordinary bundle allowed
- `ms012g-human-design-authority-gcat-bcat-gate-v1.zip` → `ALLOW` / `ingest` — ordinary bundle allowed
- `ms012h-path-function-sentinel-sandbox-loop-v2.zip` → `ALLOW` / `ingest` — ordinary bundle allowed
- `page-contract-report 2.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `page-contract-report.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `transition-replay-report 2.zip` → `ALLOW` / `ingest` — known report artifact bundle
- `transition-replay-report.zip` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Incoming bundle is already seen as already_applied; quarantined as stale queue debris instead of being silently skipped.
- `README.md` → `STALE_INCOMING_QUARANTINED` / `failed_bundles` — Non-ZIP file in incoming/ cannot be ingested as a bundle.
