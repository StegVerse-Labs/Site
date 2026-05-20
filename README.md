# Site Single-Source Status Bundle

## Assumptions

1. The current stage/status should be changed in one Site data file only.
2. All transition status pages should render that status from the same source.
3. The single Site status source is `data/formalism-tests/transition-proof-surface.json`.
4. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. Stage/current status values live in `data/formalism-tests/transition-proof-surface.json`.
2. Shared rendering logic lives in `assets/transition-site-status.js`.
3. Main transition pages call the shared renderer instead of carrying separate status logic.
4. Updating `current_stage`, `status`, stage statuses, `stage6_result`, or `next_integration_target` in the JSON updates every included page.
5. No workflow files are included.

## Files Included

| Path | Purpose |
|---|---|
| `data/formalism-tests/transition-proof-surface.json` | Single Site status source. |
| `assets/transition-site-status.js` | Shared client-side renderer for Site transition status pages. |
| `transition-proof-surface.html` | Uses shared renderer. |
| `transition-release-index.html` | Uses shared renderer. |
| `transition-development-status.html` | Uses shared renderer. |
| `transition-milestones.html` | Uses shared renderer. |
| `transition-verification-guide.html` | Uses shared renderer. |
| `transition-replay-packet.html` | Uses shared renderer. |
| `stage6-unified-gate-results.html` | Uses shared renderer. |
| `README.md` | Bundle explanation. |
| `bundle_manifest.json` | Bundle manifest. |

## What Changes Going Forward

To update the public status across these pages, edit only:

```text
data/formalism-tests/transition-proof-surface.json
```

Examples of fields that update all included pages:

```text
current_stage
status
stages[*].status
stage6_result
verified_tasks
source_artifacts
site_pages
next_integration_target
authority_boundary
```

## Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
