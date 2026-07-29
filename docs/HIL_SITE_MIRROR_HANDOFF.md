# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide activation authority.

## Current goal

Activate the complete v1.1 provenance-bound path from verified Primary and prompt references through exact response bytes, receiver receipt, authenticated private review, append-only publication, Site projection, hash-chained Master Record release, and machine-observed deployed readiness.

```text
Primary surface: humans-as-interoperability-layer.html
Client: assets/hil-experiment-v1.1.js
Receiver discovery: data/hil-receiver-config.json
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Observer formalization: docs/HIL_OBSERVER_MODEL.md
Receiver runtime: StegVerse-org/LLM-adapter
Runtime handoff: StegVerse-org/LLM-adapter/docs/HIL_RUNTIME_MIRROR_HANDOFF.md
Site contract guard: scripts/verify_hil_site_contract.py
Site contract workflow: .github/workflows/hil-site-contract.yml
Result: V1_1_CLIENT_AND_PORTABLE_RECEIVER_IMPLEMENTED_PUBLIC_ACTIVATION_PENDING
Authority: NONE
```

## Canonical v1.1 chain

```text
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Protocol: HIL-PROTOCOL-v1.1
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance schema: HIL-RESPONSE-PROVENANCE-v1.1
Receipt schema: HIL-RECEIVER-RECEIPT-v2
Observer model: HIL-OBSERVER-MODEL-v0.1
```

## Current upload state

The browser client is implemented and fail-closed. It validates the selected PDF, computes the response hash, builds v1.1 provenance, discovers a Site-configured receiver, verifies exact readiness hashes, uploads only to a ready receiver, verifies the returned receipt and its hash continuity, stores verified receipts locally by response hash, and prevents accidental duplicate submission.

`data/hil-receiver-config.json` is intentionally unconfigured. It must remain so until a provider-neutral HTTPS receiver proves the exact v1.1 readiness contract. No provider hostname is an architectural dependency or participant-facing requirement.

The Site contract guard now fails closed when the receiver discovery schema, canonical v1.1 hashes, protocol and provenance versions, client receipt verification, optional-participant-metadata posture, or HTTPS receiver requirement drifts. A configured public receiver URL must use HTTPS, contain a host, contain no embedded credentials, query, or fragment, and declare `CONFORMING_HTTPS_RECEIVER_CONFIGURED`.

## Correct diagnosis of `NOT READY`

The public upload control displays `NOT READY` because no verified public HTTPS receiver is configured in `data/hil-receiver-config.json`.

This state does not mean that the browser client is missing, that the participant must create a receiver, or that a participant-owned machine must remain continuously live. A loopback endpoint such as `http://127.0.0.1:8000` is diagnostic only and cannot satisfy the public Site readiness contract.

The missing capability is:

```text
provider-neutral receiver
→ deployed on managed/serverless or already-enrolled infrastructure
→ exposed through verified HTTPS
→ backed by durable storage
→ configured into Site receiver discovery
```

## Binding unblock and burden rule

A blocked hosting state must remain `BLOCKED_PENDING_INTERNAL_UNBLOCK_SEARCH` until every reasonable ecosystem-owned, managed, ephemeral, serverless, or existing-host option has been evaluated.

A participant may not be assigned missing system roles merely because the participant is capable of performing them. Prohibited involuntary substitutions include:

```text
hardware provider
hardware rehabilitator
installer
node operator
student
experiment operator
schema interpreter
troubleshooter
recovery mechanism
continuity layer
```

No participant-owned continuously live machine may become the canonical HIL receiver unless all lower-dependency alternatives have been formally exhausted, necessity has been demonstrated, role conflicts have been evaluated, burden has been disclosed, and explicit authorization has been granted.

## Authorized local-validation venues

Local validation exists only to verify the unchanged receiver before hosted deployment. It must run in one of the following venues:

```text
repository-owned CI
an ephemeral managed container
an existing enrolled StegVerse node
an already-ready developer environment
```

Local validation must not require constructing participant infrastructure. It must not be treated as the production receiver or as fulfillment of the public Site activation requirement.

## Observer formalization state

`docs/HIL_OBSERVER_MODEL.md` now separates proposer, committer, and observer as functional roles; formalizes the asymmetry between a long-window context that accumulates commitment and a context repeatedly required to propose; distinguishes structure, interpretation, significance, commitment, and observation; defines candidate observer locations; proposes a hash-chainable observer-event record; and requires `UNRESOLVED` when evidence cannot establish whether a proposal entered shared reality.

This formalization is research-layer work only. It grants no activation, intake, review, publication, custody, execution, or Master Record authority. The v1.1 receipt path can prove exact-byte continuity and transfer-related events, but it does not by itself prove that participant meaning changed or that a proposal became a committed shared state.

## Provider-neutral runtime

The canonical receiver package is owned by `StegVerse-org/LLM-adapter`:

```text
Dockerfile
compose.yaml
scripts/container-entrypoint.sh
scripts/start-hil-runtime.sh
docs/PLATFORM_AGNOSTIC_RUNTIME.md
docs/HIL_RUNTIME_QUICKSTART.md
docs/HIL_RUNTIME_MIRROR_HANDOFF.md
```

The runtime consumes only a configurable port, durable data directory, runtime-injected secrets, HTTPS termination, and standard health/readiness paths. Render and all other provider manifests are optional examples and grant no activation status.

## Required next vertical slice

1. Validate the unchanged OCI receiver in repository-owned CI or another authorized ephemeral venue.
2. Select a conforming managed/serverless deployment target that supplies HTTPS, secret injection, durable storage, restart/replacement support, and exportable evidence.
3. Deploy the unchanged provider-neutral runtime without requiring participant-owned continuously live hardware.
4. Verify public `/api/hil/readiness` and `/api/hil/publication-readiness` against the exact v1.1 Primary and prompt hashes.
5. Perform a controlled hosted restart or replacement while retaining storage and prove exact-byte and manifest persistence.
6. Set `data/hil-receiver-config.json` to the proven receiver base URL and `CONFORMING_HTTPS_RECEIVER_CONFIGURED`.
7. Confirm the existing public upload control transitions from `NOT READY` to `READY`.
8. Upload one controlled PDF through the existing Site browser client and preserve the verified receiver receipt.
9. Record one authenticated, write-once `ACCEPT_PRIVATE` decision.
10. Record one separately authenticated append-only publication.
11. Import the first public record into `data/hil-responses.json`.
12. Build and validate the first `HIL-MASTER-RECORD-RELEASE-v1` chain.
13. Submit to `master-records/orchestration` only under separate authorization.
14. Open public acquisition only after all evidence is preserved.
15. Extend `data/hil-experiment.json` with an observer-mode declaration only after schema review.
16. Add fixtures that preserve message structure while withholding interpretation or commitment evidence and require `UNRESOLVED`.

## Participant continuation

Sara Katpar's initiating trace, granted attribution/reproduction permission, participant-controlled continuation, and later outreach remain preserved. These records do not grant technical activation, intake, review, publication, custody, execution, or Master Record authority. Her response packet may be submitted only after the governed receiver is ready; her potential ecosystem-node beta participation remains a separate role and consent track.

## Known remaining files and destinations

```text
StegVerse-Labs/Site
- data/hil-receiver-config.json: add proven HTTPS receiver after readiness
- data/hil-responses.json: first publication pending
- data/hil-master-records.json: first release pending
- data/hil-experiment.json: observer-mode schema extension pending review
- tests/fixtures or equivalent: observer ambiguity and UNRESOLVED cases pending
- issue #81: active hosted-receiver and controlled-cycle tracker

StegVerse-org/LLM-adapter
- automated authorized-venue runtime validation: pending
- public managed/serverless runtime deployment evidence: pending
- controlled Site upload and receipt evidence: pending
- hosted restart/replacement persistence evidence: pending
- authenticated private-review evidence: pending
- append-only publication evidence: pending

GCAT-BCAT-Engine/Publisher
- release verification task: create at authorized release/tag stage

admissibility-wiki
- release verification task: create at authorized release/tag stage

stegguardian-wiki
- release verification task: create at authorized release/tag stage
```

## Authority boundaries

```text
client implementation != live receiver
OCI image build != deployment
local validation != public activation
participant hardware != canonical hosting
readiness declaration != durable-state proof
receiver receipt != private acceptance
private acceptance != publication
publication record != original-byte custody
Site projection != endorsement
Master Record release != custody
participant interest != role assignment
CI success != live activation
proposal generated != committed transition
observer visibility != commit authority
structure preserved != meaning reconstructed
interpretation recorded != significance established
```

## Release posture

No release tag or public data-acquisition activation is authorized until one deployed controlled cycle produces a verified receipt, survives an actual hosted restart or replacement, completes authenticated private review and append-only publication, updates the Site projection, and produces a validated Master Record release.