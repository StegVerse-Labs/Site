# StegBrowser Runtime Consumption Same-Device InTr Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-RUNTIME-CONSUMPTION-001`
Canonical parent handoff: `StegVerse-Labs/.github/docs/STEGBROWSER_RUNTIME_CONSUMPTION_MIRROR_HANDOFF.md`
COSV: `40000100100000`
Status: `ACTIVE / CHECKED_OUT / SAME_DEVICE_CANONICAL_WORK_INTR_BINDING_IN_PROGRESS`

## Purpose

Expose the active canonical runtime-consumption task through the already-existing root-scoped current-iPhone Universal InTr service worker so the selected `ADMITTED-EPHEMERAL-STEGOS-NODE` substrate can authentically admit the task without a remote device, second scheduler, second service worker, second WorkerCoordinator, or alternate credential path.

## Existing runtime to reuse

`/intr-service-worker.js` is the existing registered-node root InTr surface. It already owns `/intr/profile`, `/intr/materialization/readiness`, `/intr/materialization`, the device-local write-once request store, current-iPhone runtime identity, TV/TVC credential boundary, and event-ephemeral materialization semantics.

The current gap is profile-specific: the service worker allowlist covers DEVICE_KV, HIL, Evaluator, and one Master Records transition but not `CanonicalWork:Ingress`. The StegOS Canonical Work same-device adapter is also pinned to an older object-provenance task and therefore cannot admit this active task unchanged.

## Required binding

The existing service worker must accept only the exact destination/owner pair:

```text
destination.boundary = STEGOS_ECOSYSTEM
destination.subsystem = CanonicalWork:Ingress
downstream_owner_ref = STEGVERSE-CANONICAL-WORK-COORDINATION-001
```

The request remains `stegverse.universal-intr-materialization-request/v1`, event-triggered, credential authority `TV/TVC`, GitHub runtime authority `NONE`, request/transport execution authority false, and claim/fence minting false. Admission may produce only the canonical `INGRESS_ADMITTED` transition receipt. WorkerCoordinator remains the sole claim/fence authority.

## Runtime proof boundary

Source, merge, GitHub Pages publication, or service-worker installation do not prove admission. Authentic proof requires the current iPhone's existing `/intr/materialization` handler to return an exact current-task `INGRESS_ADMITTED` receipt from `CURRENT_USER_IPHONE_SERVICE_WORKER`. Canonical Work consumption and WorkerCoordinator claim/fence remain subsequent predicates and must be observed rather than inferred.

## README disposition

Site README must describe this Canonical Work profile addition because it expands the existing root InTr service worker's supported profile set while preserving the same authority model.
