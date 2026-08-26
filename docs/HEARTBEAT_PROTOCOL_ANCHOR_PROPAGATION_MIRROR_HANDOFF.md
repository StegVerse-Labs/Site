# Heartbeat Protocol Anchor Propagation Mirror Handoff

Updated: 2026-08-26T15:48:00-05:00

## Authority

```text
goal_id: SITE-HEARTBEAT-PROTOCOL-ANCHOR-PROPAGATION-001
repository: StegVerse-Labs/Site
upstream_semantics: StegVerse-Labs/.github/docs/HEARTBEAT_CARRIER_SIGNAL_MIRROR_HANDOFF.md
upstream_identifier_encoding: StegVerse-Labs/.github/docs/HEARTBEAT_IDENTIFIER_ENCODING_MIRROR_HANDOFF.md
credential_authority: TV/TVC
github_runtime_authority: NONE
state: COMPLETE_VALIDATED
```

## Canonical heartbeat consumed

```text
anchor_epoch: 32
anchor_heartbeat_id: HB-0000000W
identifier_format: HB-XXXXXXXX
identifier_encoding: FIXED_WIDTH_BASE36
identifier_width: 8
integer_epoch_remains_canonical: true
period_ms: 10
reference_rate_hz: 100
progression_dependency: OSCILLATOR_ONLY
continuous_reference_stream: true
new_reference_every_10ms: true
continuous_process_required: false
resident_sampler_required_for_progression: false
observation_is_causal: false
LIVE-009: COMPLETED / INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
authority_effect: NONE
```

Site workload-health transitions and the heartbeat-response `SENT -> RECEIVED -> RESPONDED -> RECOVERED -> REPEAT` lifecycle remain separate state machines and do not cause protocol heartbeat progression. The retained HB29->HB30 iPhone capsule is historical pre-HB32 evidence only.

## Implemented reconciliation

The prior HB32 semantic reconciliation remains installed in `data/ecosystem-heartbeat-state.json`, `scripts/check_ecosystem_heartbeat_orchestration.py`, `docs/ECOSYSTEM_HEARTBEAT_ORCHESTRATION.md`, response-network state/docs/validator, and historical iPhone projection surfaces.

Base36 propagation added:

```text
0612b3be543dfd1cf6a177d2acea202b542f81eb  public heartbeat-transition page displays HB-XXXXXXXX and HB32 alias
1a2dd9e07a7b717947db5efeaeb5908878f6b8da  data/heartbeat-identifier-encoding-awareness.json
53b7805d8dfb0ee2fb0be8375f8620d1e388ead9  scripts/check_heartbeat_identifier_encoding_awareness.py
01bf599c5e092021cb99c426193d79bc94a28e73  markup-safe historical projection validator repair
```

Historical decimal labels and historical receipts remain valid and immutable.

## Validation evidence

An initial Site Bootstrap run exposed only an exact-text/HTML-markup mismatch in the historical projection validator. It was repaired without changing heartbeat semantics.

```text
workflow: Site Bootstrap Validate - No Non-TV/TVC Credential Authority
run_id: 33012027355
job_id: 98320472381
head_sha: 01bf599c5e092021cb99c426193d79bc94a28e73
result: SUCCESS
exclusive claims and Site orchestration: PASS
canonical Site application: PASS
iPhone historical HB29->HB30 projection: PASS
ST-017 isolated validation: PASS
StegFin phone projection: PASS
validation-only authority boundary: PASS
```

GitHub validation is evidence only and is not heartbeat timing/runtime authority.

## Separate active work

Heartbeat propagation completion does not complete the separate HIL/provider/custody chain, issue #234 organization response-network coverage, Site activation, Publisher ST-017 activation, admissibility repository-wide validation, or Guardian HIL interpretation. Those remain governed by their own canonical handoffs.

## User action

None for heartbeat continuity or Base36 identifier propagation. No iPhone action, credential entry, resident sampler, or third-party runtime is required.

## Completion

```text
HB32 semantic propagation: COMPLETE
Base36 identifier propagation into Site current surfaces: COMPLETE
current-main Site validation: PASS
historical compatibility: PRESERVED
authority effect: NONE
```

Continuation of unrelated Site goals does not require reopening this heartbeat propagation goal.
