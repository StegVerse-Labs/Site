# StegVerse-002 Public Observation Mirror Handoff

Updated: 2026-08-29

## Canonical scope

```text
repository: StegVerse-Labs/Site
issue: #665
implementation PR: #666
implementation merge: c3fe242fc51af9176da35e70ce88534d4e9f50aa
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

## Merged Site surface

- `sv002-observe/index.html`: public shell and human-readable evidence panels.
- `assets/sv002-observe.js`: node gate, dedicated `SV002_PUBLIC_OBSERVE` request, full Node Receipt #1 binding, dual InTr receipt validation, read-only projection rendering.
- `assets/stegverse-node-continuity.js`: canonical browser Node continuity source.
- `assets/evaluator-intr-connector.js`: canonical browser Interlock carrier adapter with class-specific `/intr/sv002-observe` routing.

There is deliberately no static JSON experiment-data fallback.

The Site implementation claim is RELEASED on main. The Site source lane is not an activation blocker.

## Sovereign receiving runtime

Canonical owner:

```text
repository: StegVerse-Labs/.github
issue: #462
implementation PR: #474
implementation merge: da1e5d1cd9761122e65c7be3b05fb24415d2abc6
task: SHWP-SV002-PUBLIC-OBSERVATION-RUNTIME-001
resident request: RESIDENT-EXEC-SV002-PUBLIC-OBSERVATION-RUNTIME-001
```

The merged sovereign runtime admits:

```text
schema_version: stegverse.sv002.public_observation.interlock_request.v1
request_class: SV002_PUBLIC_OBSERVE
operation: READ_OBSERVATION
transport: InTr
```

It independently validates the full viewer Node Receipt #1 and exact node/interlock/registration-hash binding before releasing data. It derives projection data only from authentic evidence surfaces and returns distinct canonical ingress and egress InTr receipts.

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

## Current state

```text
Site shell source: MERGED / VALIDATED (#666)
Node gating: MERGED / VALIDATED
class-specific /intr/sv002-observe connector routing: MERGED / VALIDATED
static payload fallback: ABSENT
observer -> StegVerse-002 direct interaction: FORBIDDEN
sovereign receiving runtime source/control: MERGED / VALIDATED (.github #474)
resident request consumption: NOT OBSERVED
receiver READY: NOT OBSERVED
public deployed route behavior: NOT OBSERVED
authentic ingress receipt: NOT OBSERVED
authentic egress receipt: NOT OBSERVED
authentic experiment events: NOT OBSERVED
Master Records reconstruction: NOT OBSERVED
```

Site source, runtime source, CI, merge, deployment, or request registration must never be treated as authentic observation.

## Next authorized evidence boundary

The next state-changing proof must originate from an eligible non-hosted sovereign runtime:

```text
resident source refresh
-> consume RESIDENT-EXEC-SV002-PUBLIC-OBSERVATION-RUNTIME-001
-> materialize admitted route
-> observe SV002_PUBLIC_OBSERVATION_RECEIVER_READY
-> valid observer Node opens Interlock
-> authentic ingress RECEIVED receipt
-> read-only projection
-> authentic egress FORWARDED receipt
```

No second user machine or manual credential entry is part of this contract.
