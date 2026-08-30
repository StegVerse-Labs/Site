# StegVerse-002 Public Observation Mirror Handoff

Updated: 2026-08-29

## Canonical scope

```text
repository: StegVerse-Labs/Site
issue: #665
branch: feat/sv002-public-observe-665
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
-> canonical Interlock Connector
-> InTr ingress
-> read-only observation projection
-> InTr egress
-> observer browser

no valid Node => no experiment data
```

Observer traffic terminates at the read-only observation projection. An observer does not gain an interaction edge to StegVerse-002 merely by watching.

## Implemented Site surface

- `sv002-observe/index.html`: public shell and human-readable evidence panels.
- `assets/sv002-observe.js`: node gate, dedicated `SV002_PUBLIC_OBSERVE` request, dual InTr receipt validation, read-only projection rendering.
- `assets/stegverse-node-continuity.js`: existing canonical browser Node continuity source.
- `assets/evaluator-intr-connector.js`: existing canonical browser Interlock carrier adapter.

There is deliberately no static JSON experiment-data fallback.

## Required receiving runtime

The sovereign receiving runtime must admit:

```text
schema_version: stegverse.sv002.public_observation.interlock_request.v1
request_class: SV002_PUBLIC_OBSERVE
operation: READ_OBSERVATION
```

It must validate the observer Node binding, obtain the current observation projection from canonical evidence/Master Records surfaces, return a read-only projection, and return distinct verified ingress and egress InTr receipts.

The receiving runtime must not route observer requests into StegVerse-002 as experimental interactions.

## Observation projection

The response may expose only evidence-derived projection classes:

- current observed state;
- relationship topology;
- knowledge/provenance evidence states;
- externally observable event stream;
- manifest/receipt references;
- Master Records custody/reconstruction status.

It must not claim private chain-of-thought or synthesize missing events.

## Current state

```text
Site shell: IMPLEMENTED_ON_BRANCH
Node gating: IMPLEMENTED_ON_BRANCH
static payload fallback: ABSENT
observer -> StegVerse-002 direct interaction: FORBIDDEN
receiving runtime support: PENDING
public deployed route: NOT OBSERVED
authentic experiment events: NOT OBSERVED
```
