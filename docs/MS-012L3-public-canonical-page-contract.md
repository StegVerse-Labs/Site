# MS-012L.3 Public Canonical Page Contract

## Purpose

This artifact defines how the new canonical shell, dependency, correction, and closure data should appear on public GitHub Pages HTML.

It does not modify workflows.
It does not modify tools.
It does not claim automatic HTML regeneration is active.

## Current state

```text
Canonical data:
  updating

Public HTML:
  not automatically reflecting new canonical files yet
```

## Reason

The existing transition page builder consumes older transition element files, not the new canonical files:

```text
data/canonical/shells-v1.json
data/canonical/execution-surfaces-v1.json
data/canonical/transition-correction-ledger-v1.json
data/canonical/transition-dependency-closure-status-v1.json
```

## Required public pages

```text
canonical-shell-map.html
transition-dependency-closure.html
transition-self-correction-ledger.html
```

## Existing public pages that should link them

```text
transition-periodic-table.html
transition-development-status.html
```

## Public page invariants

```text
Public pages must not claim blocked transitions are executable.
Public pages must distinguish discovery_state from execution_state.
Public pages must display unresolved dependencies when execution_state is blocked.
Public pages must cite canonical data files as source surfaces.
```

## Current allowed next steps

```text
Install this page contract.
Generate static public HTML pages from canonical data as ordinary site files.
Do not edit tools/build_transition_pages.py yet.
Do not edit workflows.
```

## Files

```text
data/page-contracts/public-canonical-page-contract-v1.json
data/canonical/public-canonical-page-status-v1.json
```
