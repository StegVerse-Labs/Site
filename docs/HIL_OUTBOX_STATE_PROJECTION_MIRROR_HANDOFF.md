# HIL Outbox State Projection Mirror Handoff

Repository: `StegVerse-Labs/Site`
State: RELEASED
Branch: `fix/hil-outbox-state-projection-20260902`
Updated: 2026-09-02
Authority effect: NONE
Activation effect: false

## Goal

Stop presenting all HIL Node outbox rows as a single ambiguous "pending" state after the registered-iPhone device-local HIL ingress was released.

## State model

The HIL sync surface must distinguish:

- queued with no ingress receipt;
- admitted to the same-device HIL InTr profile;
- delivered to an external sovereign ingress;
- downstream materialization / receiver / TVC state, which remains unclaimed unless separate receipts exist.

The outbox row itself remains immutable local continuity. A delivery receipt changes the **presentation classification**, not the original outbox evidence.

## Required projection

For the currently visible HIL InTr Local Outbox status:

```text
<total> total · <local> admitted locally · <external> delivered externally · <awaiting> awaiting ingress · downstream consumption not claimed
```

When the external fallback target is unavailable, that does not override an already-present local ingress receipt.

## Claimed paths

- `stegos-node/hil-intr-sync.js`
- `scripts/check_hil_intr_node_sync.py`
- `tests/test_hil_intr_node_sync.py`
- `docs/HIL_OUTBOX_STATE_PROJECTION_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-hil-outbox-state-projection-20260902.json`

## Non-goals

No mutation of Node outbox evidence, no downstream completion inference, no receiver/custody/TVC claim, no second device, and no credential or execution authority.


## Release reconciliation — 2026-09-02

PR #942 merged as `91889fb9c0d51c23b9469297a6169fabfe6bbbe2`.

Validated exact head:

- Ecosystem Heartbeat Orchestration `33712838010` — SUCCESS
- Site Handoff Orchestrator `33712838015` — SUCCESS
- Site Bootstrap Validate `33712838022` — SUCCESS
- StegOS Node Public Observation source validation `33712838154` — SUCCESS

The HIL outbox presentation no longer collapses every locally retained row into one generic pending/connected state. It now reports total rows, same-device local admissions, external ingress deliveries, and rows still awaiting ingress separately while explicitly preserving downstream materialization/receiver/TVC state as unclaimed.
