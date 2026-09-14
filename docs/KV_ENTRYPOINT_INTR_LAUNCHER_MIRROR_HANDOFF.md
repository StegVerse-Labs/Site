# KV Entrypoint Interlock/InTr Launcher Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-RUNTIME-CONSUMPTION-001`
COSV: `40000100100000`
Claim: `SITE-KV-ENTRYPOINT-INTR-LAUNCHER-20260914`
Released PR: `StegVerse-Labs/Site#1311`
Release commit: `5f6c663b1294bb9f7cc8083c78c574b293e5ddf7`
Pages propagation: run `34861289935` = `SUCCESS`
Status: `ACTIVE / CHECKED_OUT / SOURCE_RELEASED_AND_PROPAGATED / AUTHENTIC_KV_RUNTIME_EVIDENCE_PENDING`

## Architectural correction

The StegVerse entry point must not make a particular physical device the progression architecture for KnowledgeVault access.

The released entry path is:

```text
StegVerse entry point
-> KV launcher
-> canonical KnowledgeVault Interlock request
   schema = kv.interlock.request.v1
-> generated DEVICE_KV InTr transport/materialization
-> destination = KV / KnowledgeVault:Interlock
-> existing DEVICE_KV ingress + query/return path
-> governed installation projection/readback
-> My KV user surface
```

The browser/Node/device that happens to carry the request is an interchangeable execution/transport surface. The launcher itself has `device_class_requirement=NONE` and contains no iPhone-specific condition.

## Existing canonical components reused

No new KV protocol or runtime owner was created. The launcher reuses:

- `assets/generated/site-browser-intr-connectors.js`
  - generated `device-kv` profile;
  - destination `KV / KnowledgeVault:Interlock`;
  - `protocol=InTr`;
  - TV/TVC credential authority;
  - no transport authority transfer.
- `assets/hb-intr-carrier.js`
  - existing non-authorizing carrier binding.
- `assets/stegverse-node-continuity.js`
  - existing Node continuity/outbox binding.
- `stegos-node/device-kv-intr-sync.js`
  - existing exact DEVICE_KV materialization ingress/result transport.
- `assets/my-kv-device-kv-query-bridge.js`
  - existing `kv.interlock.request.v1` construction;
  - existing `MY_KV_INSTALLATION_STATUS` bounded request;
  - exact admitted result/readback validation.
- `StegVerse-Labs/continuity-vault-kit#79`
  - canonical downstream KnowledgeVault/Interlock owner.

## Released entrypoint implementation

`index.html` no longer exposes `My KV` as a plain direct navigation link. It exposes `#kv-entry-launcher` and loads the canonical DEVICE_KV dependencies before `assets/kv-entrypoint-intr-launcher.js`.

The launcher performs only:

```text
StegVerseKVInstallationStatusBridge.getInstallationStatus()
-> validate exact stegverse.kv.installation-status-projection/v1
-> require KV_INSTALLATION_VERIFIED or KV_INSTALLATION_NOT_VERIFIED
-> require credential_material_present=false
-> require provider_operation_authorized=false
-> require authority_effect=NONE
-> navigate to my-kv.html only after that governed return
```

The launcher does not register another service worker, call a new network endpoint, create another scheduler/WorkerCoordinator, or invent a new KV request schema. It delegates all governed transport/admission/readback behavior to the existing DEVICE_KV Interlock/InTr chain.

## Validation and release evidence

The first PR head exposed one compatibility regression: the historical homepage validator required a plain `href="my-kv.html"` link. That validator and its regression test were corrected on the same branch to require the governed launcher instead, without weakening chat or organizational-KV semantics.

Exact head `833d4bbc20f983e8c630f8b3619ef3882b73abc8` then passed all six triggered validations:

- Site Handoff Orchestrator
- Site Node Continuity
- Site Homepage Chat
- Node IndexedDB Schema Migration
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority
- Ecosystem Heartbeat Orchestration

PR `#1311` merged as `5f6c663b1294bb9f7cc8083c78c574b293e5ddf7`.

GitHub Pages deployment run `34861289935` for that exact merge completed successfully.

These prove source release and public propagation only. They do not prove an authentic KV request was admitted or read back through Interlock/InTr.

## Authority invariants

```text
KnowledgeVault = durable user-controlled state
Interlock = state-transition admission/governance
InTr = bounded adjacent transport; no authority transfer
TV/TVC = credential authority
WorkerCoordinator = execution claim/fence authority where applicable
Master Records = observed-reality/provenance authority
GitHub = source/validation/evidence transport only; runtime authority NONE
physical device class = not an authority and not a launcher prerequisite
```

The entrypoint launcher must never infer that a particular phone, browser, service worker instance, or device model owns KV authority.

## Relationship to current Goal

`STEG-BROWSER-RUNTIME-CONSUMPTION-001` remains the active canonical Goal. This released Site slice corrects the progression surface: the KV launcher belongs behind Interlock/InTr at the StegVerse entry point. A device-specific debug launcher is not the required progression mechanism.

This source release does not itself establish:

- authentic KV runtime admission/readback;
- Canonical Work resident consumption;
- WorkerCoordinator claim/fence;
- TVC source promotion/restart;
- immutable observer execution;
- `OWNER_INGRESS_READY_OBSERVED`.

Those remain authentic runtime evidence predicates.

## README disposition

Root `README.md` was reviewed. It already establishes the Site authority boundary, MyKV/KnowledgeVault projection role, and Interlock/InTr/authority separation. This bounded release changes entry behavior rather than repository-wide semantics, so the exact launcher contract remains in this mirror handoff and regression suite without a broad README rewrite.

## Next sequence

```text
source release + public propagation [DONE]
-> entry point invokes existing KV Interlock/InTr launcher path
-> retain authentic admission/readback evidence when observed
-> feed that evidence into canonical work progression where applicable
-> continue canonical runtime-consumption Goal from the next authentic predicate
```

No source/CI/merge/publication event may be promoted into runtime evidence.
