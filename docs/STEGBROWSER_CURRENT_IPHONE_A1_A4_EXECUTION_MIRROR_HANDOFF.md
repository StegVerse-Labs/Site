# StegBrowser Current-iPhone A1-A4 Execution Mirror Handoff

Updated: 2026-09-16
Repository: `StegVerse-Labs/Site`

## Task pointer

- Goal Task ID: `STEG-BROWSER-CURRENT-IPHONE-A1-A4-EXECUTION-001`
- Parent Goal: `STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001`
- COSV: `40000100100000`
- Status: `ACTIVE / CHECKED_OUT / A1-A2 CURRENT-IPHONE INGRESS SOURCE PRESENT / A2-TO-EVENT-EPHEMERAL CONTINUATION STAGED / EXACT-HEAD VALIDATION PENDING / AUTHENTIC A3-A4 PENDING`

## Immutable invocation

Reuse only:

```text
source goal = STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001
canonical request commit = 19935454cd8c68000b3a0fd70478b0d89d5cd622
nonce = STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z
requested invocation count = 1
destination = StegBrowser:ManifestInvocation
COSV = 40000100100000
```

No second request or payload mutation is allowed.

## Existing source chain

Current main already provides:

```text
registered Node Receipt #1
-> immutable Node-bound outbox entry
-> root Universal InTr service worker
-> StegBrowser:ManifestInvocation
-> write-once INGRESS_ADMITTED receipt
```

The previously merged Site adaptation also provides `assets/stegbrowser-manifest-runtime-materializer.js`, which creates the bounded self-contained EVENT_EPHEMERAL browser runtime and emits `stegverse.stegbrowser-event-ephemeral-execution-readiness/v1` without minting a claim/fence or widening authority.

## First source gap identified and staged repair

The existing current-iPhone page stopped after `INGRESS_ADMITTED` and reported `A1_A2_INGRESS_ADMITTED_A3_A4_PENDING`; it did not call the already-merged EVENT_EPHEMERAL materializer. The staged repair adds `stegos-bootstrap/stegbrowser-current-iphone-event-continuation.js` and loads the existing materializer before that continuation.

The continuation:

```text
authentic current-device INGRESS_ADMITTED
-> same immutable materialization_id
-> same Node outbox entry
-> exact static StegBrowser runtime binding
-> existing StegVerseStegBrowserManifestRuntime.materialize(...)
-> EVENT_EPHEMERAL runtime-readiness receipt
-> WorkerCoordinator claim/fence remains pending
-> A4 remains pending
```

It does not add another request, listener, scheduler, dispatcher, runtime architecture, WorkerCoordinator, credential path, or second device. It explicitly reports `second_request_emitted=false`, `a1_a4_complete=false`, and `round_trip_1_started=false`.

## Validation

A dedicated validation-only workflow is staged at `.github/workflows/stegbrowser-current-iphone-a1-a4-continuation.yml`. It runs the exact same-device test and has no runtime authority. Standard Site Bootstrap, Handoff Orchestrator, and Heartbeat remain incidental validation lanes.

Source or CI success may establish only that this continuation is wired correctly. It must not mark authentic runtime predicates true.

## Authority boundaries

- Node: continuity/admission anchor only.
- Interlock/InTr: governed transition authority.
- EVENT_EPHEMERAL browser materializer: bounded runtime materialization only; claim/fence minting prohibited.
- WorkerCoordinator: sole claim/fence authority.
- TV/TVC: credential authority.
- GitHub/CI: source validation/evidence transport only; runtime authority `NONE`.

## Current authentic predicates

No authentic predicate is promoted by this staged source repair. Until current-device authority-owned evidence is observed, the canonical task predicates remain unchanged.

## README review

`README.md` reviewed. No byte change is required: it already documents the single root Universal InTr topology, bounded `EVENT_EPHEMERAL` execution, authority separation, and no second user-operated device requirement. This repair connects two existing documented stages rather than changing topology.

## Next transition

Exact-head validate the staged repair. If green, merge with expected-head protection, reconcile this handoff on main, then re-observe the existing same-iPhone runtime automatically. If authentic EVENT_EPHEMERAL readiness appears, continue only through the already-canonical WorkerCoordinator claim/fence and A4 path.

## Manual work

None.
