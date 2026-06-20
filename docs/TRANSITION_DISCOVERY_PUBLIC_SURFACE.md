# Transition Discovery Public Surface

## Purpose

This document records the Site public-surface correction that makes the transition pages render from one shared discovery model.

## Canonical files

```text
assets/transition-discovery-state.js
assets/transition-page-renderer.js
```

`assets/transition-discovery-state.js` owns the public discovery state.

`assets/transition-page-renderer.js` renders each public page from that state and injects the shared transition discovery styling so lightweight shells remain presentable.

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
```

## Validator

```text
python scripts/check_transition_discovery_public_surface.py
```

The checker verifies that:

```text
canonical state exists
shared renderer exists
shared renderer injects transition discovery styling
all seven root-level public pages load both shared files
all seven pages declare the expected transition view
T13 and T14 remain receipt-backed in the canonical state
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

The workflow runs on manual dispatch and on pushes that affect the canonical discovery state, renderer, seven root-level public pages, this document, or the checker.

## iOS-safe mirror

```text
iosnoperiod/github/workflows/transition-discovery-public-surface.yml
iosnoperiod/manifest.json
```

The mirror is not authoritative. It is an iOS-safe copy of the canonical workflow path for review or restoration.

## Boundary note

This document describes the transition-page public research surface only. It does not change the Site mirror activation boundary defined in `docs/SITE_MIRROR_HANDOFF.md`.

Site mirror activation remains pending Publisher closure evidence. Public transition discovery pages may continue to improve without claiming Publisher-to-Site mirror activation.
