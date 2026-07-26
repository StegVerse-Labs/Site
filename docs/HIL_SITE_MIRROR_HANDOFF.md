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
Receiver runtime: StegVerse-org/LLM-adapter
Runtime handoff: StegVerse-org/LLM-adapter/docs/HIL_RUNTIME_MIRROR_HANDOFF.md
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
```

## Current upload state

The browser client is implemented and fail-closed. It validates the selected PDF, computes the response hash, builds v1.1 provenance, discovers a Site-configured receiver, verifies exact readiness hashes, uploads only to a ready receiver, verifies the returned receipt and its hash continuity, stores verified receipts locally by response hash, and prevents accidental duplicate submission.

The experiment manifest now matches the receiver contract: the exact Primary, protocol, prompt, and response chain is mandatory; model, provider, conversation reference, producer signature detail, participant identity, consent, and participant declarations remain optional. Missing optional values grant no consent, attribution, publication, custody, execution, acceptance, or Master Record authority. Contract reconciliation commit: `7ab0413d30becec01840cc4e990d7a1af9de72a7`.

`data/hil-receiver-config.json` is intentionally unconfigured. It must remain so until a provider-neutral HTTPS receiver proves the exact v1.1 readiness contract. No provider hostname is an architectural dependency or participant-facing requirement.

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

1. Start the receiver locally with `sh scripts/start-hil-runtime.sh`.
2. Confirm `READY` with the exact v1.1 Primary and prompt hashes.
3. Deploy the unchanged OCI runtime behind any conforming HTTPS endpoint with durable mounted storage.
4. Verify public `/api/hil/readiness` and `/api/hil/publication-readiness`.
5. Set `data/hil-receiver-config.json` to the proven receiver base URL.
6. Upload one controlled PDF and preserve the verified receiver receipt.
7. Restart or replace the receiver while retaining storage and prove exact-byte and manifest persistence.
8. Record one authenticated, write-once `ACCEPT_PRIVATE` decision.
9. Record one separately authenticated append-only publication.
10. Import the first public record into `data/hil-responses.json`.
11. Build and validate the first `HIL-MASTER-RECORD-RELEASE-v1` chain.
12. Submit to `master-records/orchestration` only under separate authorization.
13. Open public acquisition only after all evidence is preserved.

## Participant continuation

Sara Katpar's initiating trace, granted attribution/reproduction permission, participant-controlled continuation, and later outreach remain preserved. These records do not grant technical activation, intake, review, publication, custody, execution, or Master Record authority. Her response packet may be submitted only after the governed receiver is ready; her potential ecosystem-node beta participation remains a separate role and consent track.

## Known remaining files and destinations

```text
StegVerse-Labs/Site
- data/hil-receiver-config.json: add proven HTTPS receiver after readiness
- data/hil-responses.json: first publication pending
- data/hil-master-records.json: first release pending
- issue #81: active controlled-cycle tracker

StegVerse-org/LLM-adapter
- public runtime deployment evidence: pending
- controlled upload and receipt evidence: pending
- actual restart persistence evidence: pending
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
readiness declaration != durable-state proof
receiver receipt != private acceptance
private acceptance != publication
publication record != original-byte custody
Site projection != endorsement
Master Record release != custody
participant interest != role assignment
```

## Release posture

No release tag or public data-acquisition activation is authorized until one deployed controlled cycle produces a verified receipt, survives an actual restart or replacement, completes authenticated private review and append-only publication, updates the Site projection, and produces a validated Master Record release.
