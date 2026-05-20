# Stage 6 Site Data Mirror Bundle

## Assumptions

1. `formalism-tests` remains the authority for tests, candidates, receipts, declared tasks, and workflow output.
2. `StegVerse-Labs/Site` mirrors public proof data under `data/formalism-tests/`.
3. Site pages should fetch mirrored JSON data instead of hardcoding proof values.
4. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `stage6-unified-gate-results.html` fetches and renders `data/formalism-tests/stage6-unified-gate-results.json`.
2. The JSON data file contains the Stage 6 successful declared-task result.
3. `transition-release-index.html` links to `stage6-unified-gate-results.html`.
4. `transition-table-classes.html` links to `stage6-unified-gate-results.html`.
5. No workflow files are included.

## Files Included

| Path | Purpose |
|---|---|
| `stage6-unified-gate-results.html` | Data-driven Stage 6 public page. |
| `data/formalism-tests/stage6-unified-gate-results.json` | Mirrored public Stage 6 proof data. |
| `transition-release-index.html` | Full replacement adding Stage 6 link. |
| `transition-table-classes.html` | Full replacement adding Stage 6 link and reset/evolve filter support. |
| `README.md` | Bundle explanation and verification checklist. |
| `bundle_manifest.json` | Bundle manifest. |

## Expected Public URLs

```text
https://stegverse-labs.github.io/Site/stage6-unified-gate-results.html
https://stegverse-labs.github.io/Site/data/formalism-tests/stage6-unified-gate-results.json
```

## Public Result Mirrored

```text
candidate_count: 10
assertion_count: 320
success: true
ALLOW: 3
FAIL_CLOSED: 5
RESET_BOUNDARY: 1
EVOLVE_BOUNDARY: 1
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
