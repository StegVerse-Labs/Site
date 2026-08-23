# Heartbeat Protocol Anchor Propagation Mirror Handoff

Updated: 2026-08-23T17:02:00-05:00

## Authority and goal

```text
goal_id: SITE-HEARTBEAT-PROTOCOL-ANCHOR-PROPAGATION-001
repository: StegVerse-Labs/Site
branch: main
upstream_semantics_authority: StegVerse-Labs/.github/docs/HEARTBEAT_CARRIER_SIGNAL_MIRROR_HANDOFF.md
upstream_deployment_authority: StegVerse-Labs/.github/docs/SOVEREIGN_HEARTBEAT_DEPLOYMENT_MIRROR_HANDOFF.md
upstream_live_proof: StegVerse-Labs/.github/handoffs/HEARTBEAT-INDEPENDENT-OSCILLATOR-LIVE-009.json
upstream_validation_receipt: StegVerse-Labs/.github/receipts/heartbeat/HEARTBEAT-PROTOCOL-ANCHOR-013-validation.json
credential_authority: TV/TVC
github_runtime_authority: NONE
third_party_runtime_required: false
```

This handoff owns propagation of the corrected canonical heartbeat semantics into Site. It does not own the Site heartbeat-response network lifecycle, workload orchestration transitions, or any downstream execution authority.

## Canonical protocol heartbeat

```text
anchor epoch: HB32
anchor time: 2026-08-23T19:00:00.000Z
period: 10 ms
rate: 100 Hz
progression dependency: OSCILLATOR_ONLY
continuous process required: false
resident sampler required for progression: false
observation is causal: false
authority effect: NONE
```

The protocol heartbeat is derived from the durable anchor plus elapsed oscillator phase. A daemon, repository action, worker, workflow, transition, task, claim, fence, lease, route, credential, observation, response-network receipt, or Site orchestration event does not make the next heartbeat reference exist.

## Required terminology separation

Site currently contains two transition-driven mechanisms that historically use the word heartbeat:

1. `data/ecosystem-heartbeat-state.json` / Site orchestration health and workload-transition counters.
2. `docs/HEARTBEAT_RESPONSE_MIRROR_HANDOFF.md` / the organization response lifecycle `SENT -> RECEIVED -> RESPONDED -> RECOVERED -> REPEAT`.

These mechanisms remain valid as orchestration/response state machines, but neither is the canonical 100 Hz protocol heartbeat.

Required interpretation:

```text
protocol heartbeat = HB32-anchored oscillator-derived reference
Site orchestration heartbeat = repository/workload health projection only
heartbeat response network = transition-driven message/receipt lifecycle only
```

Time-based watchdogs on Site remain retry/silence observers only. They do not advance protocol heartbeat references and do not grant execution authority.

## Upstream proof consumed

The upstream LIVE-009 handoff is terminal:

```text
state: COMPLETED
transition_id: INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
verification_mode: DIRECT_DETERMINISTIC_PROTOCOL_DERIVATION
focused tests: 6/6 PASS
continuous process required: false
resident sampler required for progression: false
observation_is_causal: false
authority_effect: NONE
```

The validation receipt concludes `CANONICAL_HEARTBEAT_REFERENCE_IS_ACTIVE_BY_PROTOCOL_DERIVATION` and explicitly does not claim optional resident sampler installation.

## Site propagation requirements

1. Site status/documentation must not report a resident heartbeat daemon as an activation prerequisite.
2. Site orchestration validators must not interpret Site workload-transition counters as the protocol heartbeat epoch.
3. Heartbeat-response network `REPEAT` remains event-driven and must not be synthesized from the 10 ms protocol heartbeat.
4. Protocol references may be observed/correlated by Site, but observation carries `authority_effect=NONE`.
5. Site workflows remain validation/coordination surfaces and are not production heartbeat timing authority.
6. Existing transition-driven Site terminology must be qualified as orchestration or response-network state when ambiguity exists.
7. Downstream status projection should identify LIVE-009 as completed and the canonical protocol heartbeat as active by derivation.

## Current state

```text
upstream protocol anchor: INSTALLED
upstream deterministic derivation: VERIFIED
upstream LIVE-009: COMPLETED
Site propagation handoff: INSTALLED
Site consumer audit: OPEN
Site terminology reconciliation: OPEN
Site status projection reconciliation: OPEN
```

## Next executable work

Search Site runtime/config/docs/tests for any statement or predicate that treats:

- `TRANSITION_DRIVEN` Site orchestration as canonical heartbeat progression;
- a resident sampler or daemon as required for heartbeat existence;
- response-network `REPEAT` as equivalent to a protocol heartbeat tick;
- CI/workflow cadence as heartbeat timing authority.

Correct each active semantic surface while preserving historical evidence and transition-driven Site behavior under its narrower orchestration/response meaning.

## Completion predicate

This propagation goal is complete only when:

```text
no active Site predicate requires resident process liveness for protocol heartbeat progression
no active Site predicate equates workload transition counters with HB protocol epochs
no active Site predicate equates response-network REPEAT with protocol heartbeat progression
Site status documents upstream LIVE-009 as COMPLETED
Site preserves oscillator-only 10 ms / 100 Hz protocol semantics
authority_effect remains NONE
GitHub runtime authority remains NONE
TV/TVC remains sole credential authority
```

Do not rewrite historical Site receipts merely because terminology is narrowed. Correct active authority and current-state surfaces only.
