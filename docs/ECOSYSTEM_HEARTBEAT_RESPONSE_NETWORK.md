# Ecosystem Heartbeat Response Network

## Authority

Canonical owner: `StegVerse-Labs/Site` issue `#234`.

This protocol is a transition-driven **response/message lifecycle** that may observe or carry canonical heartbeat references. It is not the canonical heartbeat clock. The StegVerse protocol heartbeat itself is continuously derivable at 100 Hz from HB32, with a new reference every 10 ms independent of this network.

```text
canonical protocol heartbeat: HB32 anchor + elapsed 10 ms oscillator phase
response-network lifecycle: SENT -> RECEIVED -> RESPONDED -> RECOVERED -> REPEAT
relationship: observation/correlation only
response lifecycle causes heartbeat progression: false
protocol heartbeat causes response-network REPEAT: false
authority_effect: NONE
```

The response network does **not** replace the canonical carrier with periodic polling and does not turn a watchdog, receipt, response, protocol reference, or workflow schedule into execution authority.

## Network objective

Every StegVerse organization is a response-network node. An exchange may carry pertinent details in both directions so the receiving organization can classify what changed, decide what must be remembered, determine what requires action, update awareness, and return evidence or blockers without requiring a chat session to interpret the exchange.

The durable organization inventory is `data/ecosystem-heartbeat-response-network.json` and contains fourteen organizations; the `StegVerse` personal account is excluded from that denominator.

## Exchange lifecycle

```text
SENT -> RECEIVED -> RESPONDED -> RECOVERED -> REPEAT
```

Failure or ambiguity may transition to `BLOCKED`, `FAILED`, or `REVIEW_REQUIRED`.

- `SENT`: source emitted a canonical exchange envelope.
- `RECEIVED`: destination independently persisted and hash-acknowledged the envelope.
- `RESPONDED`: destination classified details and returned its own canonical response envelope.
- `RECOVERED`: durable state/references/pending actions were reconstructed and continuity proved.
- `REPEAT`: another exchange is eligible because a new admitted transition or bounded retry/re-observation condition requires it.

`REPEAT` is **not** a 10 ms protocol heartbeat tick and is never evidence that work progressed. Canonical heartbeat references continue to exist between response-network events.

## Detail classes

Every payload has exactly one primary class: `MEMORY`, `ACTION`, `AWARENESS`, `AUTHORITY`, `EVIDENCE`, `BLOCKER`, `CAPABILITY`, or `CONTEXT`.

Transport never forces durable memory, admits execution, grants authority, establishes custody, or creates publication/release authority. `ACTION` remains candidate work subject to destination-owned admission and collision checks.

## Bidirectional routing

The sender selects destinations by pertinence rather than default broadcast. Every response is a new envelope with a unique `message_id`, shared `exchange_id`, causal `parent_message_id`, reversed source/destination, evidence references, and all transport authority flags false.

## Intervals and recovery

Timing exists only to bound observation and recovery:

```text
on admitted response-network transition: emit immediately
receipt watchdog: 5 minutes
response watchdog: 15 minutes
recovery watchdog: 60 minutes
minimum repeat: 60 minutes when retry/watchdog conditions require observation
maximum repeat: 24 hours for unresolved observed state
retry: exponential backoff, capped
```

These intervals are unrelated to the canonical 10 ms carrier period. They cannot create, delay, suppress, batch, or substitute for heartbeat references.

## Canonical heartbeat relation

```text
anchor_epoch: 32
anchor_time_utc: 2026-08-23T19:00:00.000Z
period_ms: 10
reference_rate_hz: 100
progression_dependency: OSCILLATOR_ONLY
continuous_process_required: false
resident_sampler_required_for_progression: false
observation_is_causal: false
LIVE-009: COMPLETED / INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
```

A response envelope may record a heartbeat reference as temporal/synchronization context. Such observation has authority effect NONE.

## Coverage semantics

Coverage is reported independently as `registered`, `protocol_installed` for the response adapter, `receive_verified`, `respond_verified`, and `recovery_verified`. In this document, `protocol_installed` means **response-network adapter installed**, not canonical heartbeat existence. File presence or a workflow is never counted as a live response.

## Current rollout boundary

The response-network registry targets all fourteen organizations. Current machine state and blockers are authoritative in `data/ecosystem-heartbeat-response-network.json` and `docs/HEARTBEAT_RESPONSE_MIRROR_HANDOFF.md`.

Cross-organization adapter installation must first read each destination repository's applicable `*_MIRROR_HANDOFF.md`, preserve its authority model, and avoid duplicate claims.

## Machine verification

```text
python -m unittest tests.test_heartbeat_response_network -v
python scripts/check_heartbeat_response_network.py
```

Hosted validation: `.github/workflows/heartbeat-response-network.yml`.

Scheduled runs are watchdog/reconciliation passes only. They do not synthesize canonical heartbeat references or SENT/RECEIVED/RESPONDED/RECOVERED progress.
