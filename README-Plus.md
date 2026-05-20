# Transition Table Mobile Expand Bundle

## Assumptions

1. Desktop users should retain a full transition-class table.
2. Mobile users should see a periodic-table-like list of color-coded expandable transition tiles.
3. The data source remains `data/formalism-tests/transition-table-classes.json`.
4. Completion level and color information comes from `data/formalism-tests/transition-discovery-map.json`.
5. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `transition-table-classes.html` renders a full table on desktop.
2. `transition-table-classes.html` renders expandable mobile transition tiles on mobile.
3. Each mobile tile shows level, transition name, transition ID, and decision before expansion.
4. Each expanded tile shows family, theorem, role, coupling, boundary, replay, capacity, recoverability, inference-window, linked element, and basis.
5. Tile colors mirror the discovery 0–5 completion scale.
6. Filters work for both desktop table rows and mobile tiles.

## File Included

| Path | Purpose |
|---|---|
| `transition-table-classes.html` | Full replacement with desktop table plus mobile expandable periodic-style transition tiles. |
| `README.md` | Bundle explanation and verification checklist. |
| `bundle_manifest.json` | Bundle manifest. |

## Mobile Behavior

On screens below `820px`, the wide table is hidden and the page shows expandable cards:

```text
[Level]  transition_name                  [Decision]
         transition_id

Tap to expand:
  Family
  Theorem
  Role
  Coupling
  Boundary
  Replay
  Capacity
  Recoverability
  Inference Window
  Element
  Basis
```

## Desktop Behavior

On screens above `820px`, the page keeps the full table view.

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
