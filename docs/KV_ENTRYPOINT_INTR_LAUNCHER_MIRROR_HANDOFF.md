# KV Entrypoint Interlock/InTr Launcher Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-RUNTIME-CONSUMPTION-001`
COSV: `40000100100000`
Claim: `SITE-KV-ENTRYPOINT-INTR-LAUNCHER-20260914`
Branch: `feat/kv-entrypoint-intr-launcher`
Status: `RELEASED_COMPLETE` for Site source; original runtime admission/readback `UNKNOWN_NOT_AUTHENTICALLY_OBSERVED`

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

`STEG-BROWSER-RUNTIME-CONSUMPTION-001` is RETIRED in the current canonical Registry; this is its historical Site source claim, not a live checkout. This source slice corrects the progression surface: the KV launcher belongs behind Interlock/InTr at the StegVerse entry point. A device-specific debug launcher is not the required progression mechanism.

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

Root `README.md` was reviewed. It already establishes the Site authority boundary, MyKV/KnowledgeVault projection role, and Interlock/InTr/authority separation. This change does not alter those repository-wide semantics; it changes the task-specific entry behavior from a plain My KV hyperlink to the existing governed DEVICE_KV query/return path. The exact entrypoint contract is therefore retained in this mirror handoff and regression test; no broad README rewrite is required for this bounded slice.

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

## 2026-09-27 stale-claim reconciliation

Site PR #1311 merged the governed launcher at `5f6c663b1294bb9f7cc8083c78c574b293e5ddf7`; its exact source head was `833d4bbc20f983e8c630f8b3619ef3882b73abc8`. Historical Pages propagation run #34861289935 is recorded as successful in the original release proposal, Site PR #1312, which was closed **without merge**. This correction explicitly releases the lingering source claim without claiming that PR #1312 merged. The retired historical goal and COSV must not be used for new claims; select a currently ACTIVE canonical successor from the Registry for any new runtime transition. No authentic original KV InTr disposition or sovereign organization ledger readback was obtained in this documentation repair. All execution is manifest-bound and state-transition-dependent, with no connected-device inventory prerequisite.

## 2026-09-27 post-merge projection repair

Site PR #1469 merged at `e3bbb10c1acac1857a412319ce67c5339846ad6f` despite failing exact-head checks and without a submitted independent review. Its historical binding mode was not supported by the existing COSV validator. This source repair implements explicit read-only historical released-claim validation, retains original claimed vector `20010000100000` as provenance, and derives source-only `91000000100000` with `evidence_complete=false`, `activated=false`, `propagated=false`. Source merge and deployment are not original manifest-bound runtime disposition or organization/Master Records readback. Do not use the retired goal as active execution authority.

## 2026-09-27 source-owner reconciliation for PR #1471

The bounded Site-local validation claim `SITE-STEGBROWSER-HISTORICAL-COSV-PROJECTION-VALIDATION-20260927` has unique local task identity `SITE-STEGBROWSER-HISTORICAL-COSV-PROJECTION-VALIDATION-001` and names existing `SITE-COSV-REPOSITORY-WIDE-ADOPTION-001` as its Site COSV source owner (the original source adoption task is `RELEASED_COMPLETE`). This is a corrective source-validation continuation, not a second canonical runtime task, not a reopened retired custody observation and not an extension of the adoption owner's original completed execution. Its claim is bounded to Site projection validator/index/tests and releases after reviewed merge. StegBrowser's active runtime successors retain their separate original authority and evidence requirements. Original manifest-bound InTr and sovereign readback remain unobserved here.
