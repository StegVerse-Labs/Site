# StegOS Registered Device UI Mirror Handoff

## Current source of truth

This file is the authoritative continuation record for StegVerse-Labs/Site issue #770.

## Goal

A browser/device with canonical Receipt #1 must not be offered device registration again.

## Observed device evidence

Observed 2026-08-30 from a user-exported `stegos.node_physical_evidence_export.v1`:
- node_id: `SV-NODE-9fdb116d9520079e71a7f82b`
- receipt_number: 1
- transition: `NODE_REGISTERED`
- resulting_state: `REGISTERED`
- local receipt SHA-256: `540a73888130ed10080243046069c616ed16c1c868dbdb4f755500584bc21258`
- personal KV sync: not observed
- StegOS network sync: not observed
- offline reload proof: not observed
- authority effect: NONE
- physical activation claimed: false
- network activation claimed: false

The export is evidence of browser-local canonical registration only. It does not establish hardware attestation, physical activation, network activation, KV synchronization, network synchronization, or offline reload continuity.

## Required UI behavior

- UNREGISTERED: show `Register Device` and `Register & Export Evidence`.
- REGISTERED: suppress both registration actions.
- REGISTERED: show a non-mutating `Check Current Registration` action.
- REGISTERED: preserve `Export Node Evidence`.
- Registration check must validate the existing Receipt #1 and report the existing Node identity without minting a new receipt.
- TV/TVC remains credential authority.
- No hardware-attestation, physical-activation, network-activation, or execution-authority claim is introduced.

## Implementation surface

- `stegos-node/index.html`
- `tests/test_stegos_node_projection.py`
- `docs/STEGOS_REGISTERED_DEVICE_UI_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-stegos-registered-device-ui-770.json`

## State

`IMPLEMENTATION_IN_PROGRESS`

## Remaining gates

1. Install source and regression tests.
2. Validate branch.
3. Merge through normal Site claim/orchestration gates.
4. Re-observe the public StegOS Node route on an already-registered device.
5. Keep KV sync, StegOS network sync, and offline reload proof as separate evidence gates.
