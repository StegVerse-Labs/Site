# StegBrowser Runtime Consumption Same-Device InTr Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-RUNTIME-CONSUMPTION-001`
Canonical parent handoff: `StegVerse-Labs/.github/docs/STEGBROWSER_RUNTIME_CONSUMPTION_MIRROR_HANDOFF.md`
COSV: `40000100100000`
Status: `ACTIVE / CHECKED_OUT / SAME_DEVICE_CANONICAL_WORK_INTR_SOURCE_IMPLEMENTED / CURRENT_IPHONE_RUNTIME_PROOF_PENDING`

## Purpose

Expose the active canonical runtime-consumption task through the already-existing root-scoped current-iPhone Universal InTr service worker so the selected `ADMITTED-EPHEMERAL-STEGOS-NODE` substrate can authentically admit the task without a remote device, second scheduler, second service worker, second WorkerCoordinator, or alternate credential path.

## Existing runtime preserved

The prior `/intr-service-worker.js` implementation is retained byte-for-byte as `intr-service-worker-base-v1.js`. The root service-worker URL remains `/intr-service-worker.js` and now imports that exact base plus `intr-canonical-work-extension.js`. This is one service-worker lifecycle and one existing root InTr scope; it is not a parallel runtime.

The existing worker continues to own `/intr/profile`, `/intr/materialization/readiness`, `/intr/materialization`, the device-local write-once request store, current-iPhone runtime identity, TV/TVC credential boundary, and event-ephemeral materialization semantics.

## Exact Canonical Work extension

`intr-canonical-work-extension.js` accepts only:

```text
task_id = STEG-BROWSER-RUNTIME-CONSUMPTION-001
COSV = 40000100100000
registry_commit = f1a55fa4022e19b41f2a9f604978b08ece22f64c
registry_generation = 19
coordination_state = ACTIVE
checkout_state = CHECKED_OUT
selected_execution_substrate = ADMITTED-EPHEMERAL-STEGOS-NODE
destination.boundary = STEGOS_ECOSYSTEM
destination.subsystem = CanonicalWork:Ingress
downstream_owner_ref = STEGVERSE-CANONICAL-WORK-COORDINATION-001
allowed_next_transition = INGRESS_ADMITTED
worker_claim_authority = WORKERCOORDINATOR
worker_claim_ref = null
fence_ref = null
credential_authority = TV/TVC
github_token_runtime_authority = NONE
```

The request remains `stegverse.universal-intr-materialization-request/v1`, event-triggered, non-authorizing, and bound to an existing registered StegVerse Node/Interlock. The extension can emit only `stegverse.canonical-work-intr-materialization-ingress/v1` with `state=INGRESS_ADMITTED`. WorkerCoordinator remains the sole claim/fence authority.

## Current-iPhone launcher

The source now includes:

```text
stegos-bootstrap/canonical-work-runtime-consumption.html
stegos-bootstrap/canonical-work-runtime-consumption.js
```

The launcher:

1. requires the canonical registered Node database and exact `SV-NODE-*` / `SV-IL-*` identities;
2. registers/updates the existing root `/intr-service-worker.js` and waits until `/intr/profile` exposes `CanonicalWork:Ingress` on `CURRENT_USER_IPHONE_SERVICE_WORKER`;
3. builds the exact active task/COSV/registry-generation materialization request;
4. hash-binds the request into the existing registered-node write-once `intr_outbox`;
5. sends `STEGVERSE_INTR_LOCAL_TRIGGER` to that same root worker;
6. refuses success unless the exact active-task `INGRESS_ADMITTED` receipt is observed;
7. then invokes the already-admitted StegVerse local inference path for a non-authorizing self-build analysis and retains its existing device-journal receipt.

The user surface reports `STEGVERSE_SELF_BUILD_STARTED` only if both the exact Canonical Work ingress receipt and the local admitted-analysis receipt are present. If local analysis is unavailable after authentic ingress, it reports the narrower truthful ingress-admitted state. It never claims repository mutation or Goal completion.

## Authority boundary

```text
Task Registry = work identity/coordination truth
Interlock/InTr = transition/admission authority
WorkerCoordinator = claim/fence authority
TV/TVC = credential/route authority
Master Records = reconstruction/custody authority
HeartBeat = timing/reference only
GitHub runtime authority = NONE
current iPhone = selected physical execution surface
```

This Site slice does not mint a WorkerCoordinator claim/fence, does not mark Canonical Work resident consumption complete, does not mutate a repository from the browser, and does not convert local model output into authority.

## Runtime proof boundary

Source, branch, PR, merge, GitHub Pages publication, service-worker installation, and deterministic tests do not prove current-device admission. Authentic proof requires the user's current iPhone to execute the launcher and retain an exact `INGRESS_ADMITTED` receipt from `CURRENT_USER_IPHONE_SERVICE_WORKER`. The subsequent WorkerCoordinator claim/fence and canonical task execution remain evidence predicates and must be observed rather than inferred.

## Validation

`tests/test_canonical_work_runtime_consumption_same_device.py` statically protects the single-worker modularization, exact task/COSV/registry/substrate binding, no-GitHub-token/no-credential widening invariants, registered-node write-once outbox use, and the user surface's evidence-gated success label.

## README disposition

Root `README.md` was reviewed. Its existing “StegOS same-device operational cards” section already documents the current-iPhone physical execution surface, fresh root Universal InTr machine-governed transitions, registered Node/Interlock binding, TV/TVC boundary, no second InTr runtime/WorkerCoordinator/scheduler, and source-vs-runtime evidence separation. This task-specific Canonical Work profile does not change those repository-wide semantics, so no README text mutation is required for this slice.

## Next exact sequence

```text
exact-head validation
-> merge and publish existing Site source
-> current iPhone loads canonical-work-runtime-consumption.html?autostart=1
-> root service worker converges to CanonicalWork:Ingress
-> registered Node outbox trigger retained
-> authentic current-iPhone INGRESS_ADMITTED retained
-> admitted local self-build analysis receipt retained when available
-> continue through canonical WorkerCoordinator claim/fence
-> authentic Canonical Work resident consumption
-> exact stegbrowser_tvc_source_promotion
-> TVC runtime restart/observer
-> OWNER_INGRESS_READY
```

No completion, runtime admission, WorkerCoordinator claim/fence, repository mutation, or OWNER_INGRESS_READY is claimed from source alone.
