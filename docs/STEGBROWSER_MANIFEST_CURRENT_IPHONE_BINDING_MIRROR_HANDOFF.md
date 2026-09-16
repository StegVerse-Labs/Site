# StegBrowser Manifest Current-iPhone Binding Mirror Handoff

Updated: 2026-09-16
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001`
Canonical handoff: `StegVerse-Labs/.github/docs/STEGBROWSER_MANIFEST_INTR_INGRESS_EXECUTION_MIRROR_HANDOFF.md`
COSV: `40000100100000`
Status: `ACTIVE / SOURCE REPAIR IN VALIDATION / AUTHENTIC CURRENT-IPHONE EXECUTION PENDING`

## Exact repair

The existing current-iPhone root Universal InTr surface was still bound to retired lineage task `STEG-BROWSER-RUNTIME-CONSUMPTION-001` and destination `CanonicalWork:Ingress`. The runtime itself was already correct: the registered StegVerse Node IndexedDB, write-once `intr_outbox`, root `/intr-service-worker.js`, current-iPhone service-worker runtime identity, and fail-closed InTr admission boundary were present.

This repair changes only invocation-specific binding at that existing edge:

```text
Goal = STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001
Parent = STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001
COSV = 40000100100000
nonce = STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z
destination = StegBrowser:ManifestInvocation
downstream owner = StegVerse-Labs/.github#1952
manifest sha256 = fcde63451bf612df8f3b2b62fa6766670dc880f2fcb66605680a2af6f2096f74
```

The old `intr-canonical-work-extension.js` file remains the one existing imported extension file but is repurposed in place. It removes `CanonicalWork:Ingress` from the profile and exposes only the active `StegBrowser:ManifestInvocation` binding for this task. No third service-worker import, second worker, listener, scheduler, dispatcher, materializer, WorkerCoordinator, device, credential path, or authority path is added.

## One-shot preservation

The current-iPhone launcher does not mint a new user request. It binds the already-canonical immutable nonce. Its materialization ID is deterministic from that nonce, so repeated page activation targets the same write-once Node outbox identity rather than creating another invocation.

The binding uses `stegverse.stegbrowser-universal-intr-invocation-binding/v1`; the request remains `stegverse.universal-intr-materialization-request/v1`; and the admission receipt is `stegverse.stegbrowser-intr-materialization-ingress/v1` with `state=INGRESS_ADMITTED`.

## Predicate boundary

Source, CI, merge, publication, service-worker installation, or page load do not promote A1-A4. Authentic current-device proof still requires the existing registered iPhone Node to execute the unchanged invocation and retain the correlated ingress receipt. The launcher reports only `A1_A2_INGRESS_ADMITTED_A3_A4_PENDING` after authentic current-device `INGRESS_ADMITTED`; it does not infer EVENT_EPHEMERAL runtime materialization, WorkerCoordinator claim/fence, A4, or Round Trip 1.

## README disposition

`README.md` reviewed. No byte change is required: the repository already documents the single same-device root Universal InTr/current-iPhone execution topology and authority separation. This repair changes only task-specific binding and evidence correlation.

## Required next evidence

```text
registered Node Receipt #1
-> deterministic unchanged-nonce Node outbox entry
-> root CURRENT_USER_IPHONE_SERVICE_WORKER profile StegBrowser:ManifestInvocation
-> authentic write-once INGRESS_ADMITTED
-> existing bounded EVENT_EPHEMERAL runtime identity
-> existing WorkerCoordinator claim/fence
-> exact A4 governed ingress
```

Only after the entire chain is correlated may Round Trip 1 start.
