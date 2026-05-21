# Dynamic Transition Pages

## Purpose

These pages are dynamic GitHub Pages shells. They render from shared JSON instead of duplicating status content across multiple HTML files.

## Shared Source

```text
data/formalism-tests/transition-proof-surface.json
```

## Release Source

```text
data/formalism-tests/transition-table-v1-rc1/index.json
data/formalism-tests/transition-table-v1-rc1/canonical_transition_table_release.json
```

## Pages

```text
transition-release-index.html
transition-development-status.html
transition-proof-surface.html
stage6-unified-gate-results.html
transition-verification-guide.html
stage10-canonical-release.html
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Rule

The HTML pages should not carry independent proof status.

They should load and render mirrored JSON.
