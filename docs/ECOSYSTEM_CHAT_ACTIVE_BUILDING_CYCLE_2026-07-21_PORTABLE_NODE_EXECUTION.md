# Ecosystem Chat Portable-Node Execution Cycle

Date: 2026-07-21

## Active goal

Complete the governed Ecosystem Chat path:

request → governed provider response → usage persistence → custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

## Current proven state

The canonical adapter source builds and runs on a connected machine. The core-node compatibility receipt is retained on `main`, and the machine-intake issue is closed. The adapter exposes the health-bound `stegverse.node.endpoint-advertisement.v1` contract. Site now consumes verified loopback or HTTPS advertisements through its existing gateway configuration and request client.

## Work performed

- Promoted the verified core-node compatibility receipt to the existing repository receipt path and closed core-node Issue #5.
- Reused the adapter's existing `/api/stegverse-node` advertisement.
- Added a bounded Site discovery adapter before the existing transition client.
- Integrated retained loopback candidates from Site PR #29 without removing or closing that PR.
- Reused the existing Site validation workflow to launch the canonical adapter source fail-closed on loopback.
- Executed one real non-restricted request through the canonical gateway.
- Retained a hash-bound Site portable-node runtime report in the existing Site validation artifact.

## Existing capabilities reused

- `StegVerse-org/LLM-adapter/llm_adapter/combined_gateway.py`
- `StegVerse-org/LLM-adapter/llm_adapter/node_bootstrap.py`
- `StegVerse-org/LLM-adapter/llm_adapter/node_service.py`
- `StegVerse-Labs/Site/data/ecosystem-chat-gateway.json`
- `StegVerse-Labs/Site/assets/ecosystem-chat-transition-identity.js`
- `StegVerse-Labs/Site/.github/workflows/validate.yml`
- Existing Site current-main receipt and artifact-manifest path
- Existing local classification fallback

## Components modified or added

- Added `assets/ecosystem-chat-node-discovery.js` as a bounded interface adapter.
- Extended `data/ecosystem-chat-gateway.json` with verified advertisement candidates.
- Updated the existing loader so discovery runs before the existing transition client.
- Updated the existing gateway activation validator.
- Added `scripts/verify_portable_node_site_runtime.py` to execute and retain the smallest working Site-to-node slice.
- Extended the existing Site validation workflow; no new workflow was created.

## Runtime tests executed

Site run `29860538192` executed:

1. Site sandbox validation.
2. Complete application validation.
3. Canonical adapter source checkout.
4. Canonical service dependency installation.
5. Fail-closed gateway startup on `127.0.0.1:8000`.
6. Health verification.
7. Node advertisement retrieval and canonical SHA-256 verification.
8. Node identity, capability, health-binding, same-origin, and false-authority validation.
9. One real governed request.
10. Transition/run/event/origin identity continuity verification.
11. Bounded response and local SQLite persistence verification.
12. Runtime shutdown.
13. Current-main receipt and artifact manifest generation and verification.
14. Evidence artifact upload.

## Observed result

- Portable-node identity: VERIFIED in the executed slice.
- Local health-bound advertisement: VERIFIED.
- Site-to-node governed request: EXECUTED and VERIFIED fail-closed.
- Bounded response: VERIFIED.
- Local transition persistence: VERIFIED.
- Provider execution: DISABLED FAIL-CLOSED.
- Custody and reconstruction: UNPROVEN.
- Immutable activation receipt: UNPROVEN.
- Site activation and downstream propagation: UNPROVEN.

## Durable evidence

- Core-node receipt merge: `c12e68900973a15ee0d72352e48911634ac25229`
- Core-node Issue #5: closed completed
- Site discovery merge: `84750eb3a8ec48bd89bda44862b75e4e67a8df2f`
- Loopback discovery integration merge: `db9bf7d31294d0e7392209816fa00f2e5e115e3d`
- Site runtime execution merge: `d3358604b046a024dbbb682d168449de7d7e28ae`
- Site validation run: `29860538192`
- Site validation artifact ID: `8507100975`
- Site validation artifact digest: `sha256:347f9d1917a51113e5c7d181a68531873cbfc8716cda3295dac69d920f308903`

## State classification

- Canonical portable-node implementation: IMPLEMENTED.
- Adapter node advertisement: INTEGRATED.
- Site discovery binding: INTEGRATED.
- Site-to-portable-node request: EXECUTED.
- Fail-closed request slice: VERIFIED.
- Real governed provider response: UNPROVEN.
- Authenticated custody: UNPROVEN.
- Reconstruction PASS: UNPROVEN.
- Immutable VERIFIED activation receipt: UNPROVEN.
- Site activation: UNPROVEN.
- Downstream ingestion: UNPROVEN.

## Removals proposed but not performed

None.

Render PR #23 and retained Site PR #29 were not closed, removed, or replaced. No heartbeat component was modified.

## Goal delta

Before this cycle, portable-node discovery and Site binding existed only as source-level implementations. The canonical adapter now starts inside the established Site validation path, advertises itself, accepts a real governed Site request, preserves identity, returns a bounded response, and persists the transition locally.

## Reuse delta

The existing adapter gateway, advertisement, node lifecycle, Site request client, gateway configuration, validation workflow, receipt generation, and artifact retention eliminated the need for another host adapter, discovery service, gateway, workflow, or receipt family.

## Non-progress

- The executed provider-disabled fallback is not a real provider response.
- Local SQLite persistence is not Master-Records custody.
- Advertisement verification is not publication authority.
- CI execution is not persistent deployment or runtime heartbeat.
- The cycle does not complete custody, reconstruction, activation, or propagation.

## Current blocker

The next failing boundary is authorized real provider and Master-Records configuration for the existing portable-node runtime. No repository implementation gap has yet been observed at that boundary because those credentials and authority were intentionally absent from the fail-closed execution.

## Next executable step

Execute the same existing portable-node slice with an already-authorized provider configuration and established Master-Records endpoint, then retain the first exact provider, usage-persistence, custody, reconstruction, or receipt failure. Do not add another runtime, host adapter, gateway, receipt schema, scheduler, or heartbeat mechanism.

Manual user action required for routine repository work: false.
