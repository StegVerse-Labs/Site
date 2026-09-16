# StegBrowser Manifest Current-iPhone Binding Mirror Handoff

Updated: 2026-09-16
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001`
Canonical handoff: `StegVerse-Labs/.github/docs/STEGBROWSER_MANIFEST_INTR_INGRESS_EXECUTION_MIRROR_HANDOFF.md`
COSV: `40000100100000`
Status: `ACTIVE / SOURCE MERGED+VALIDATED / EVENT_RUNTIME BRIDGE UNDER VALIDATION / AUTHENTIC CURRENT-IPHONE A1-A4 EXECUTION PENDING`

## Exact repair

The existing current-iPhone root Universal InTr surface was still bound to retired lineage task `STEG-BROWSER-RUNTIME-CONSUMPTION-001` and destination `CanonicalWork:Ingress`. The runtime itself was already correct: the registered StegVerse Node IndexedDB, write-once `intr_outbox`, root `/intr-service-worker.js`, current-iPhone service-worker runtime identity, and fail-closed InTr admission boundary were present.

Site PR `#1360` repaired only that first observed transition defect by rebinding the existing surface to:

```text
Goal = STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001
Parent = STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001
COSV = 40000100100000
nonce = STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z
destination = StegBrowser:ManifestInvocation
downstream owner = StegVerse-Labs/.github#1952
manifest sha256 = fcde63451bf612df8f3b2b62fa6766670dc880f2fcb66605680a2af6f2096f74
```

The old `intr-canonical-work-extension.js` file remains the one existing imported extension file but is repurposed in place. It removes `CanonicalWork:Ingress` from the active profile and exposes the active `StegBrowser:ManifestInvocation` binding. No third service-worker import, second worker, listener, scheduler, dispatcher, materializer, WorkerCoordinator, device, credential path, or authority path was added.

## Source validation and merge evidence

- Site PR: `#1360`
- Exact validated source head: `d031a1c560814a1c1cd275656925258cee11f323`
- Site Handoff Orchestration: PASS
- Session Work Claims: PASS
- Ecosystem Heartbeat contract: PASS
- Site validation / Node continuity and IndexedDB alignment: PASS
- Cloudflare Workers build: SUCCESS, version `4d24d113-f37e-4b59-8c94-c49b60cd559b`
- Merge commit: `76af62f2befdfa7034d3dd00891bfe60a0990abb`
- GitHub/CI runtime authority: `NONE`
- Authentic A1-A4 execution inferred from source/CI: `false`

## One-shot preservation

The current-iPhone launcher does not mint a new user request. It binds the already-canonical immutable nonce. Its materialization ID is deterministic from that nonce, so repeated page activation targets the same write-once Node outbox identity rather than creating another invocation.

The binding uses `stegverse.stegbrowser-universal-intr-invocation-binding/v1`; the request remains `stegverse.universal-intr-materialization-request/v1`; and the admission receipt is `stegverse.stegbrowser-intr-materialization-ingress/v1` with `state=INGRESS_ADMITTED`.

## Existing EVENT_EPHEMERAL continuation repair — 2026-09-16

Source review after #1360 found that the current-iPhone launcher stopped intentionally at authentic `INGRESS_ADMITTED`, even though the already-validated Site SV002-derived StegBrowser runtime materializer was present at `assets/stegbrowser-manifest-runtime-materializer.js`. That meant the public execution page could never advance the same invocation into the existing EVENT_EPHEMERAL Web Worker and execution-time runtime identity.

The bounded repair on branch `stegbrowser-current-iphone-event-runtime-bridge-001` does not add a materializer or mutate the immutable request. It:

1. retains the exact same deterministic Node outbox entry and ingress receipt;
2. loads the already-existing canonical route binding from `/data/stegbrowser-manifest-runtime-binding.v1.json`;
3. invokes the already-existing `StegVerseStegBrowserManifestRuntime.materialize(...)` only after authentic same-invocation `INGRESS_ADMITTED`;
4. binds the runtime to the admitted Node ID, Interlock ID, and Receipt #1 hash;
5. returns `RUNTIME_READY_FOR_WORKERCOORDINATOR` only when the existing materializer produces an `EVENT_EPHEMERAL` runtime-readiness receipt;
6. leaves WorkerCoordinator claim/fence and A4 pending and leaves Round Trip 1 false.

The repair introduces no second request, listener, service worker, scheduler, dispatcher, materializer, WorkerCoordinator, device, credential path, or GitHub runtime authority. The original ingress-only function remains available as `startIngressOnly` for bounded diagnostics.

Focused regression coverage is `tests/test_stegbrowser_current_iphone_event_runtime_bridge.py`. Exact-head CI evidence must be recorded before merge; source green alone will not promote runtime predicates.

## Predicate boundary

Source, CI, merge, publication, service-worker installation, or page load do not promote A1-A4. Authentic current-device proof still requires the existing registered iPhone Node to execute the unchanged invocation and retain correlated authority-owned evidence.

After the bounded event-runtime bridge is merged, a successful current-device page result may directly evidence through:

```text
REGISTERED_STEGVERSE_NODE_BOUND_TO_INVOCATION
INTERLOCK_BOUND_TO_NODE_AND_MANIFEST
INTR_MATERIALIZATION_ADMITTED
INVOCATION_SCOPED_LEASE_ESTABLISHED
EVENT_EPHEMERAL_STEGOS_RUNTIME_MATERIALIZED
EXECUTION_TIME_RUNTIME_IDENTITY_BOUND
```

It must still report WorkerCoordinator claim/fence and A4 as pending until those authority-owned transitions are actually observed. It must not infer Round Trip 1.

## Current execution surface

The existing same-device execution page is:

`/stegos-bootstrap/canonical-work-runtime-consumption.html`

It loads the existing Node bootstrap, root-profile bridge, existing StegBrowser event-runtime materializer, and current-iPhone launcher. The execution control reads the registered Node from the existing `stegos-node-v1` IndexedDB and submits the deterministic unchanged-nonce trigger through the existing root `/intr-service-worker.js`.

## README disposition

`README.md` reviewed. No byte change is required: the repository already documents the single same-device root Universal InTr/current-iPhone execution topology and authority separation. This repair only joins two already-documented validated pieces of the same execution path.

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
