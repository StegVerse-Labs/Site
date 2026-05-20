# Transition Discovery Color Sync Bundle

## Assumptions

1. The missing visual page should be restored as `transition-discovery.html`.
2. The discovery page should be data-driven from `data/formalism-tests/transition-discovery-map.json`.
3. Transition classifications should reuse the same 0–5 color scale used by the discovery map.
4. `formalism-tests` remains the proof/receipt authority; `Site` mirrors public proof data.
5. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `transition-discovery.html` renders transition elements in ascending completion order from level 0 through level 5.
2. `transition-table-classes.html` applies the same level colors to transition classification rows.
3. `transition-release-index.html` links to the restored discovery map.
4. `data/formalism-tests/transition-discovery-map.json` carries the shared completion scale.
5. No workflow files are included.

## Files Included

| Path | Purpose |
|---|---|
| `transition-discovery.html` | Restored data-driven visual transition discovery page. |
| `data/formalism-tests/transition-discovery-map.json` | Shared completion-level map and color scale. |
| `transition-table-classes.html` | Full replacement that applies discovery colors to transition classifications. |
| `transition-release-index.html` | Full replacement that links to discovery and class pages. |
| `README.md` | Bundle explanation and verification checklist. |
| `bundle_manifest.json` | Bundle manifest. |

## Completion Scale

| Level | Meaning |
|---:|---|
| 0 | Unobserved |
| 1 | Observed |
| 2 | Partitioned |
| 3 | Tested |
| 4 | Integrated |
| 5 | Unified |

## Expected Public URLs

```text
https://stegverse-labs.github.io/Site/transition-discovery.html
https://stegverse-labs.github.io/Site/data/formalism-tests/transition-discovery-map.json
https://stegverse-labs.github.io/Site/transition-table-classes.html
https://stegverse-labs.github.io/Site/transition-release-index.html
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
