# Transition Discovery Public Surface

## Purpose

This document records the Site public-surface correction that makes the transition pages render from one shared discovery model.

## Canonical files

```text
assets/transition-discovery-state.js
assets/transition-page-renderer.js
data/transition-discovery-state-v1.json
data/transition-page-contract-v1.json
```

`assets/transition-discovery-state.js` owns the browser-facing public discovery state.

`assets/transition-page-renderer.js` renders each public page from that state and injects the shared transition discovery styling so lightweight shells remain presentable.

`data/transition-discovery-state-v1.json` mirrors the public discovery state for validators, ingestion engines, and non-browser consumers.

`data/transition-page-contract-v1.json` defines the machine-readable contract for the seven public page roles, expected views, required shared loads, required JSON exposure, workflow command, non-claims, and pending Publisher closure boundary.

## Root-level pages

```text
transition-table.html
transition-milestones.html
transition-development-status.html
transition-release-snapshot.html
transition-release-index.html
transition-verification-guide.html
transition-replay-packet.html
```

## Public roles

```text
transition-table.html              Map of discovered transition space
transition-milestones.html         Epistemic ledger of threshold crossings
transition-development-status.html Current frontier of the exploration
transition-release-snapshot.html   Frozen knowledge boundary
transition-release-index.html      Index of public discovery states
transition-verification-guide.html Reader procedure for checking table claims
transition-replay-packet.html      Reconstructable evidence surface
```

## Current state

```text
Current release: MS-012
Current frontier: MS-012F
Receipt-backed partitions: T13, T14
Expected replay verdict: ALLOW
Machine-readable mirror: data/transition-discovery-state-v1.json
Machine-readable page contract: data/transition-page-contract-v1.json
```

## Validator

```text
python scripts/check_transition_discovery_public_surface.py
```

The checker verifies that:

```text
canonical JavaScript state exists
machine-readable JSON mirror exists
machine-readable page contract exists
JSON mirror schema is stegverse.transition_discovery_state.v1
page contract schema is stegverse.transition_page_contract.v1
shared renderer exists
shared renderer injects transition discovery styling
all seven root-level public pages load both shared files
all seven pages declare the expected transition view
T13 and T14 remain receipt-backed in both canonical and JSON state
JSON state lists all 16 current transition partitions
JSON state preserves pending Publisher closure boundary
page contract lists exactly the seven transition pages
page contract preserves MS-012, MS-012F, T13/T14, and pending Publisher closure boundary
page contract requires each page to expose data/transition-discovery-state-v1.json
this documentation lists the expected public surfaces and boundary references
the dedicated workflow exists and calls the checker
the iosnoperiod workflow mirror matches the canonical workflow exactly
the iosnoperiod manifest maps canonical and mirror workflow paths
```

## Workflow enforcement

Canonical workflow path:

```text
.github/workflows/transition-discovery-public-surface.yml
```

Displayed without the leading dot for iOS-safe review:

```text
github/workflows/transition-discovery-public-surface.yml
```

The workflow runs on manual dispatch and on pushes that affect the canonical discovery state, machine-readable state, machine-readable page contract, renderer, seven root-level public pages, this document, or the checker.

## iOS-safe mirror

```text
iosnoperiod/github/workflows/transition-discovery-public-surface.yml
iosnoperiod/manifest.json
```

The mirror is not authoritative. It is an iOS-safe copy of the canonical workflow path for review or restoration.

## Boundary note

This document describes the transition-page public research surface only. It does not change the Site mirror activation boundary defined in `docs/SITE_MIRROR_HANDOFF.md`.

Site mirror activation remains pending Publisher closure evidence. Public transition discovery pages may continue to improve without claiming Publisher-to-Site mirror activation.
