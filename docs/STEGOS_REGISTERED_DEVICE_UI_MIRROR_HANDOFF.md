# StegOS Registered Device UI Mirror Handoff

## Current source of truth

Repository: `StegVerse-Labs/Site`
Issue: `#770`
Branch: `fix/stegos-registered-device-ui-770-r2-20260902`
State: ACTIVE_IMPLEMENTATION
Authority effect: NONE
Activation effect: false
Updated: 2026-09-02

## Goal

A browser/device with canonical Receipt #1 must not be offered device registration again.

## Current defect

Current `stegos-node/index.html` always renders:

- `Register Device`
- `Register & Export Evidence`

even when the canonical local Node projection resolves to `REGISTERED`.

The Node Status panel can therefore truthfully report `REGISTERED` while the registration mutation controls remain visible. That is a presentation/state-machine defect.

## Required behavior

```text
UNRESOLVED
 -> hide registration mutation controls while canonical status resolves

UNREGISTERED
 -> show Register Device
 -> show Register & Export Evidence

REGISTERED
 -> hide both registration mutation controls
 -> show Check Current Registration
 -> preserve Export Node Evidence
```

`Check Current Registration` is non-mutating. It validates the existing Receipt #1 and reports the established Node identity.

## Invariants

- Receipt #1 semantics are unchanged.
- No cross-browser/cross-device registration discovery is invented.
- KV sync, StegOS network sync, HIL outbox, governed capability activation, and offline reload remain separate state dimensions.
- No hardware-attestation, physical-activation, network-activation, execution-authority, or credential-authority claim is introduced.
- TV/TVC remains credential authority.
- No second user-operated device is required.

## Claimed surfaces

- `stegos-node/index.html`
- `tests/test_stegos_node_projection.py`
- `docs/STEGOS_REGISTERED_DEVICE_UI_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-stegos-registered-device-ui-770.json`

## Release boundary

Release after focused StegOS Node regression coverage and current Site orchestration/bootstrap validation pass, merge, and truthful claim/handoff reconciliation. Public iPhone re-observation may confirm deployment behavior but is not a reason to keep the source implementation claim open.
