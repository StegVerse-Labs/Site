# Interlock / InTr concurrent manifested fan-in

Goal Task ID: `SITE-INTERLOCK-INTR-CONCURRENT-MANIFEST-FANIN-002`
Parent: `SITE-INTERLOCK-INTR-CONNECTION-DOCS-001`
Related SDK conformance: `SDK-MANIFEST-RELATIONAL-INVARIANT-CONCURRENCY-004`

## Core rule

Universal InTr is one protocol substrate, not one global connection instance.

```text
one Universal InTr protocol != one active connection
N submitted manifests -> N independently bound connection state machines
```

HIL remains a concrete reference implementation of the connection lifecycle. It is not a singleton lane through which all systems must serialize.

## Manifest semantics precede transport

A StegVerse manifest already declares/binds its source data and any governance-relevant source-native relationships before governance evaluation.

Transport must preserve that manifested state. It must not infer or rewrite semantic relationships from:

- simultaneous arrival;
- arrival order;
- use of the same adapter family;
- a shared `source_framework` such as MIR;
- a shared subject;
- use of the same InTr profile;
- use of the same Universal InTr transport schema.

```text
manifest semantics first
-> exact source/payload/candidate/relationship commitments
-> Universal InTr transport
-> Interlock/InTr admission
-> governance evaluation
```

Concurrency changes scheduling and throughput. It does not change meaning.

## Two simultaneous MIR submissions

Two MIR manifests may legitimately use the same MIR adapter and the same Universal InTr profile at the same time.

They remain separate governance objects:

```text
MIR manifest A
  source_output_id A
  payload/hash A
  declared relationships A
  candidate A
  canonical manifest hash A
  connection/materialization identity A
  outbox entry A
  ingress receipt A
  governance result A

MIR manifest B
  source_output_id B
  payload/hash B
  declared relationships B
  candidate B
  canonical manifest hash B
  connection/materialization identity B
  outbox entry B
  ingress receipt B
  governance result B
```

The fact that A and B arrived simultaneously does not create a relation between them. If A or B declares a governance-relevant relationship, that declared relationship is part of manifested source state and remains independently bound.

## N-way fan-in

When ten platforms connect at once, the registered Node may have ten independently retained outbox entries and ten independently advancing connection state machines.

The implementation may execute work concurrently or schedule it under bounded local resource limits. Scheduling must not collapse identities.

Each connection requires its own:

- source/manifest identity;
- exact packet or payload commitment;
- connection/request identity;
- profile/adapter identity;
- write-once outbox identity;
- materialization trigger;
- ingress receipt;
- retry/deduplication state;
- downstream receipt where applicable;
- final connection state.

One connection's receipt or predicate may never satisfy another connection merely because both use the same profile or adapter.

## Backpressure and fairness

Resource pressure is a scheduling condition, not a semantic failure.

A valid independently bound request may remain staged while capacity is unavailable. Implementations should preserve an explicit waiting state rather than falsely reporting either failure or connection completion.

Backpressure must preserve:

- exact request identity;
- ordering requirements declared by that manifest/profile, if any;
- no cross-manifest predicate satisfaction;
- no silent substitution;
- bounded retry;
- fairness sufficient to prevent one high-volume profile from permanently starving unrelated admitted work.

Backpressure never grants Heartbeat routing/transition authority. Heartbeat remains `NONE_CARRIER_ONLY`.

## Retry and deduplication

Retry operates on the exact connection/materialization identity. Duplicate delivery of the same exact manifested request must not create a second semantic object merely because transport retried it.

A materially changed manifest, source payload, relationship declaration, candidate, or exact commitment is not the same request. It requires a new manifested identity according to the applicable profile.

```text
same exact manifested identity + permitted retry -> same logical connection attempt
changed manifested semantics -> new identity / new evaluation
```

## SDK deterministic conformance

`StegVerse-org/StegVerse-SDK` task `SDK-MANIFEST-RELATIONAL-INVARIANT-CONCURRENCY-004` verifies the SDK conversion boundary with two MIR-like manifests sharing one source framework and installed governance route.

The deterministic suite verifies that source-native relationship declarations survive conversion unchanged, no relationship is injected from concurrent processing, relationship mutation changes the manifested commitment/identity, and reversing arrival order does not change request semantics.

That is source/conformance evidence only. It is not proof that a resident InTr dispatcher has already processed ten authentic live connections simultaneously.

## Authority boundary

```text
manifest validity grants governance authority = false
transport concurrency grants relationship semantics = false
shared adapter grants relationship semantics = false
arrival order grants relationship semantics = false
Universal InTr authority = bounded transport/admission only
Interlock/InTr governs transition admission
credential authority = TV/TVC
Heartbeat authority = NONE_CARRIER_ONLY
GitHub Actions runtime authority = NONE
```

Authentic resident concurrency must be demonstrated separately by runtime receipts bound to each independent manifested connection.