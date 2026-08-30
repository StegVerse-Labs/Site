# StegVerse-002 Public Observation Mirror Handoff

Updated: 2026-08-30

## Canonical scope

```text
repository: StegVerse-Labs/Site
original public surface issue: #665
original implementation PR: #666
current event-materialization issue: #696
surface: /sv002-observe/
experiment: STEGVERSE-002-SELF-CHARACTERIZATION-001
authority_effect: NONE
activation_effect: false
credential_authority: TV/TVC
```

## Governing invariant

The URL shell may be publicly reachable. Experiment data may not be delivered anonymously.

```text
URL reachable != experiment data accessible

valid StegVerse Node
-> exact READ_OBSERVATION request prepared locally
-> non-authorizing Universal Interlock/InTr materialization intent
-> shared /intr/materialization ingress
-> event-ephemeral sovereign read-only receiver request
-> existing WorkerCoordinator task authority
-> receiver READY observed downstream
-> exact original READ_OBSERVATION request
-> canonical /intr/sv002-observe Interlock/InTr ingress
-> read-only observation projection
-> canonical InTr egress
-> observer browser

no valid Node => no materialization request and no experiment data
```

Observer traffic terminates at the read-only observation projection. An observer does not gain an interaction edge to StegVerse-002 merely by watching.

## Site surface

Original merged surfaces remain:

- `sv002-observe/index.html`: public shell and human-readable evidence panels.
- `assets/sv002-observe.js`: Node gate, dedicated `SV002_PUBLIC_OBSERVE` request, full Node Receipt #1 binding, dual InTr receipt validation, read-only projection rendering.
- `assets/stegverse-node-continuity.js`: canonical browser Node continuity source.
- `assets/evaluator-intr-connector.js`: canonical browser Interlock carrier adapter with class-specific `/intr/sv002-observe` routing.

Issue #696 adds:

- `assets/sv002-materialization.js`: deterministic Universal InTr intent/materialization request construction, Node-bound write-once trigger, `/intr/materialization` submission, and exact ingress-receipt validation;
- `materialization_endpoint: /intr/materialization` on the observation page;
- materialization-before-observation sequencing;
- bounded retry of the exact same read-only request while the event-ephemeral receiver becomes available;
- materialization ingress receipt shown separately from observation ingress/egress receipts.

There is deliberately no static JSON experiment-data fallback.

## Event-materialization contract

The browser constructs:

```text
stegverse.universal-intr-transport/v1
source: DEVICE_SYSTEM / SV002:ObserverNode
destination: STEGOS_ECOSYSTEM / SV002:PublicObservation
always_on_receiver_required: false
second_user_device_required: false
exact_packet_transport_retry_allowed: true
blind_consequence_retry_allowed: false
transport_grants_execution_authority: false
credential_authority: TV/TVC

-> stegverse.universal-intr-materialization-request/v1
request_grants_execution_authority: false
claim_or_fence_minted: false
github_token_runtime_authority: NONE

-> stegos.node_intr_outbox_entry.v1
-> stegos.node_intr_materialization_trigger.v1
-> /intr/materialization
```

The observation request itself is created once. After materialization admission, retries reuse that exact request object and remain `READ_OBSERVATION`; no new consequential request is generated.

## Sovereign receiving runtime

Canonical owners:

```text
repository: StegVerse-Labs/.github
public observation issue: #462
event-ephemeral materialization issue: #493
task: SHWP-SV002-PUBLIC-OBSERVATION-RUNTIME-001
```

The event-materialization lane deliberately removes G18 terminalization and persistent receiver readiness as prerequisites. The materialization ingress/consumer do not mint execution authority; the existing WorkerCoordinator remains the only claim/fence authority for the target task.

The receiving runtime independently validates the viewer Node Receipt #1 and exact node/interlock/registration-hash binding before releasing data. It derives projection data only from authentic evidence surfaces and returns distinct canonical ingress and egress InTr receipts.

The receiving runtime must not route observer requests into StegVerse-002 as experimental interactions.

## Observation projection

The response may expose only evidence-derived projection classes:

- current observed state;
- relationship topology;
- knowledge/provenance evidence states;
- externally observable event stream;
- manifest/receipt references;
- Master Records custody/reconstruction status when independently evidenced.

It must not claim private chain-of-thought or synthesize missing events.

## Evidence separation

The following are distinct and may not be collapsed:

```text
materialization request constructed
materialization ingress admitted
materialization consumer dispatched
ESRL runtime materialized
receiver READY observed
observation ingress RECEIVED
read-only projection produced
observation egress FORWARDED
Master Records custody/reconstruction observed
principal self-characterization executed
```

Source, tests, CI, merge, route configuration, materialization admission, or dispatch never satisfy later states automatically.

## Current state at #696 implementation

```text
Site shell source: MERGED / VALIDATED (#666)
Node gating: MERGED / VALIDATED
class-specific /intr/sv002-observe connector routing: MERGED / VALIDATED
static payload fallback: ABSENT
observer -> StegVerse-002 direct interaction: FORBIDDEN
bounded receiver HTTP socket: OBSERVED_BOUNDED_LIVE_VALIDATION
shared Gateway -> loopback observation forwarding: OBSERVED_BOUNDED_LIVE_VALIDATION
event-materialization browser source: IMPLEMENTING (#696)
event-materialization sovereign source: IMPLEMENTING (.github #493)
authentic external Node materialization ingress: NOT OBSERVED
event-ephemeral receiver READY: NOT OBSERVED
public deployed observation round trip: NOT OBSERVED
authentic observation ingress receipt: NOT OBSERVED
authentic observation egress receipt: NOT OBSERVED
authentic experiment events: NOT OBSERVED
Master Records reconstruction: NOT OBSERVED
```

## Next authorized evidence boundary

After #493 and #696 are merged and propagated, the next authentic state-changing proof is:

```text
valid external observer Node
-> Open observation Interlock
-> exact event-materialization trigger admitted
-> SV002 materialization ingress receipt observed
-> event-ephemeral receiver execution/READY observed
-> exact READ_OBSERVATION request succeeds
-> authentic ingress RECEIVED receipt
-> read-only projection
-> authentic egress FORWARDED receipt
```

No second user machine, G18 completion, continuously READY application receiver, or manual credential entry is part of this contract.
