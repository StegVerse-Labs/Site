# Ecosystem Heartbeat Response Network

## Authority

Canonical owner: `StegVerse-Labs/Site` issue `#234`.

This protocol extends the existing transition-driven, health-relative heartbeat. It does **not** replace it with periodic polling and does not turn a watchdog, receipt, or response into execution authority.

## Network objective

Every StegVerse organization is a response-network node. A heartbeat exchange may carry pertinent details in both directions so the receiving organization can classify what changed, decide what must be remembered, determine what requires action, update awareness, and return evidence or blockers without requiring a chat session to interpret the exchange.

The initial inventory is the complete organization list shown in the GitHub organization-dashboard screenshots supplied on 2026-08-07:

`StegVerse`, `AaCT-E`, `Admissible-Existence`, `AdmittedCode`, `Data-Continuation`, `ECAT-ICAT-Formal`, `formalism-tests`, `GCAT-BCAT-Engine`, `Infrastructure-Continuity-Ventures`, `master-records`, `StegGhost`, `StegVerse-002`, `StegVerse-Labs`, `StegVerse-org`, and `Triad-Test`.

The durable inventory is `data/ecosystem-heartbeat-response-network.json`.

## Exchange lifecycle

```text
SENT
  -> RECEIVED
  -> RESPONDED
  -> RECOVERED
  -> REPEAT
```

Failure or ambiguity may transition to:

```text
BLOCKED
FAILED
REVIEW_REQUIRED
```

Lifecycle meaning:

- `SENT`: the source has emitted a canonical exchange envelope.
- `RECEIVED`: the destination has independently persisted and hash-acknowledged the envelope.
- `RESPONDED`: the destination has classified the details and returned its own canonical response envelope.
- `RECOVERED`: required durable state, references, or pending actions have been reconstructed after interruption or handoff and the destination proves continuity.
- `REPEAT`: the next exchange is eligible because a new admitted transition occurred or the bounded retry/watchdog policy requires re-observation.

`REPEAT` is never evidence that work progressed. Only admitted transitions may advance progress.

## Detail classes

Every payload has exactly one primary class; related classes may be referenced in the payload.

### MEMORY

Durable information the destination needs later. The receiver must declare a retention class (`EPHEMERAL`, `SESSION`, `PROJECT`, `DURABLE`, or `IMMUTABLE`) before it becomes retained memory. Transport alone never forces permanent memory.

### ACTION

A concrete candidate task for the destination. Receipt means only that the task was received. Execution requires the destination's own authority, collision, dependency, and admissibility checks.

### AWARENESS

State the destination should know but does not need to execute or retain indefinitely. Suitable for broad fanout when relevant.

### AUTHORITY

Evidence describing authority, delegation, policy posture, or limits. The message itself grants no authority.

### EVIDENCE

Receipts, hashes, workflow results, reconstruction results, observations, or other inspectable proof.

### BLOCKER

A condition preventing expected progress, with owner and machine-observable release condition when known.

### CAPABILITY

A newly available or changed capability that may affect routing or future action selection.

### CONTEXT

Supporting information needed to interpret another class but which is not itself memory or an executable action.

## Bidirectional routing

The sender selects destinations by pertinence, not by default ecosystem broadcast. `ACTION` and `AUTHORITY` are targeted. `AWARENESS`, `BLOCKER`, and `CAPABILITY` may fan out when the information materially affects multiple organizations.

Every response is a new envelope with:

- a unique `message_id` for deduplication;
- the same `exchange_id` for correlation;
- `parent_message_id` pointing to the message being answered;
- source and destination reversed for the return path;
- a primary detail class;
- evidence references;
- all transport authority flags fixed to `false`.

## Intervals and recovery

The heartbeat remains transition-driven. Timing exists only to bound observation and recovery:

```text
on admitted transition: emit immediately
receipt watchdog: 5 minutes
response watchdog: 15 minutes
recovery watchdog: 60 minutes
minimum repeat: 60 minutes when retry/watchdog conditions require observation
maximum repeat: 24 hours for unresolved observed state
retry: exponential backoff, capped
```

These are protocol defaults, not universal failure deadlines. A node is stale/failed only when progress was expected under its declared task state and the relevant evidence is absent.

## Coverage semantics

Coverage is reported separately:

1. `registered`: organization exists in the network registry.
2. `protocol_installed`: organization has a known heartbeat-capable repository/adapter.
3. `receive_verified`: at least one direct `RECEIVED` or later receipt is present.
4. `respond_verified`: at least one direct `RESPONDED` or later receipt is present.
5. `recovery_verified`: at least one direct `RECOVERED` receipt is present.

File presence or an installed workflow is never counted as a live response.

## Current rollout boundary

The pre-existing heartbeat is installed in six authoritative repositories spanning five organizations: `StegVerse-Labs`, `StegVerse-org`, `master-records`, `GCAT-BCAT-Engine`, and `StegVerse-002`. The response-network registry expands the target population to all 15 organizations, but the remaining ten organization-owned adapters are not yet claimed as installed.

Cross-organization adapter installation must first read each destination repository's applicable `*_MIRROR_HANDOFF.md`, preserve its authority model, and avoid duplicate claims.

## Machine verification

```text
python -m unittest tests.test_heartbeat_response_network -v
python scripts/check_heartbeat_response_network.py
```

Hosted validation: `.github/workflows/heartbeat-response-network.yml`.

The scheduled run is a watchdog/reconciliation pass only. It does not synthesize SENT/RECEIVED/RESPONDED/RECOVERED events.
