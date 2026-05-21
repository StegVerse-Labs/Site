# Site Dynamic Transition Schema Fix

## Purpose

This bundle fixes the mismatch between the current Site JSON and the dynamic page renderer.

The uploaded `transition-proof-surface.json` was schema v2 and did not include:

```text
pages
stages
artifact_paths
release
```

The dynamic renderer now supports both:

```text
stegverse_site_transition_proof_surface.v2
stegverse_site_transition_proof_surface.v4
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Updated Files

```text
assets/js/transition-page-renderer.js
data/formalism-tests/transition-proof-surface.json
data/formalism-tests/transition-table-classes.json
```

The HTML pages remain dynamic shells.
