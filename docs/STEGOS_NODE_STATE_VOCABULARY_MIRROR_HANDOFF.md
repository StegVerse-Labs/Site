# StegOS Node State Vocabulary Mirror Handoff

Repository: `StegVerse-Labs/Site`
State: RELEASED
Branch: `fix/stegos-node-state-vocabulary-20260902`
Updated: 2026-09-02
Authority effect: NONE
Activation effect: false

## Observed problem

Current iPhone screenshots exposed several true but differently-scoped status values that appear contradictory when rendered with overloaded words such as "connected" or "Interlock runtime not observed."

The StegOS Node already exposes distinct state dimensions:

- Node registration / Receipt #1 continuity;
- local receipt head;
- StegOS network sync history;
- HIL InTr local outbox depth;
- Personal KV sync history;
- KnowledgeVault local availability;
- governed capability activation readiness.

The capability-shell line currently says:

```text
INSTALLED_INACTIVE · ... · Interlock runtime not observed · authority NONE
```

That wording is too broad because the same iPhone can have an active device-local InTr service-worker transport while the historical capability-shell snapshot still has `production_interlock_runtime_activated=false`.

## Goal

Repair presentation vocabulary without changing readiness facts.

Required behavior:

- retain the exact source readiness predicate `production_interlock_runtime_activated`;
- stop presenting that predicate as a claim about all Interlock/InTr runtime on the device;
- label it specifically as the governed capability activation predicate from the source snapshot;
- explicitly distinguish local availability from governed activation readiness;
- preserve counts, blockers, snapshot hashes, and all authority semantics.

## Claimed surfaces

- `stegos-node/stegos-node.js`
- `stegos-node/index.html`
- `tests/test_stegos_node_projection.py`
- `scripts/check_stegos_node_projection.py`
- `docs/STEGOS_NODE_STATE_VOCABULARY_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-stegos-node-state-vocabulary-20260902.json`

## Non-goals

This lane does not activate any capability, rewrite the KV readiness snapshot, infer runtime evidence, change HIL delivery, modify Node registration, or create a second runtime.


## Release reconciliation — 2026-09-02

PR #936 merged as `7e047c87682cc837e2e67d3dc0c39067a26b08a5`.

Validated exact head:

- Site Bootstrap Validate `33704680462` — SUCCESS
- Site Handoff Orchestrator `33704680488` — SUCCESS
- Ecosystem Heartbeat Orchestration `33704680465` — SUCCESS
- StegOS Node Public Observation source validation `33704680471` — SUCCESS

The capability-shell source predicate remains unchanged. The public vocabulary now scopes it as the **governed capability activation predicate** and explicitly states that device-local InTr state is separate. The generic phrase `Interlock runtime not observed` is prohibited by regression validation on this surface.
