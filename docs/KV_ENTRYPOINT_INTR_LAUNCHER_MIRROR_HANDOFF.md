# KV Entrypoint Interlock/InTr Launcher Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-RUNTIME-CONSUMPTION-001`
COSV: `40000100100000`
Claim: `SITE-KV-ENTRYPOINT-INTR-LAUNCHER-20260914`
Branch: `feat/kv-entrypoint-intr-launcher`
Status: `ACTIVE / CHECKED_OUT / SOURCE_IMPLEMENTED / VALIDATION_PENDING`

## Architectural correction

The StegVerse entry point must not make a particular physical device the progression architecture for KnowledgeVault access.

The intended entry path is:

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

No new KV protocol or runtime owner is created. The launcher reuses:

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

## Entrypoint implementation

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

`STEG-BROWSER-RUNTIME-CONSUMPTION-001` remains the active canonical Goal. This source slice corrects the progression surface: the KV launcher belongs behind Interlock/InTr at the StegVerse entry point. A device-specific debug launcher is not the required progression mechanism.

This source change does not itself establish:

- authentic KV runtime admission;
- Canonical Work resident consumption;
- WorkerCoordinator claim/fence;
- TVC source promotion/restart;
- immutable observer execution;
- `OWNER_INGRESS_READY_OBSERVED`.

Those remain authentic runtime evidence predicates.

## Validation

`tests/test_kv_entrypoint_intr_launcher.py` protects:

- no plain `My KV` direct link at the entry point;
- canonical dependency ordering;
- reuse of `StegVerseKVInstallationStatusBridge`;
- exact `kv.interlock.request.v1` / InTr / `KnowledgeVault:Interlock` semantics;
- TV/TVC authority boundary;
- no device-class/iPhone requirement in the launcher;
- no launcher-owned service-worker registration or direct fetch transport;
- exact projection validation before navigation;
- Goal/COSV/claim handoff binding.

## README disposition

The repository README must state that the StegVerse entry point launches Personal KnowledgeVault through the existing Interlock/InTr DEVICE_KV path and that device class is incidental transport, not the progression or authority boundary.

## Next sequence

```text
exact-head validation
-> merge
-> verify public propagation
-> entry point invokes existing KV Interlock/InTr launcher path
-> retain authentic admission/readback evidence when observed
-> continue canonical runtime-consumption Goal from the next authentic predicate
```

No source/CI/merge/publication event may be promoted into runtime evidence.
