# StegBrowser Current-iPhone A1-A4 Execution Mirror Handoff

Updated: 2026-09-16
Repository: `StegVerse-Labs/Site`

## Task pointer

- Goal Task ID: `STEG-BROWSER-CURRENT-IPHONE-A1-A4-EXECUTION-001`
- Parent Goal: `STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001`
- COSV: `40000100100000`
- Status: `ACTIVE / CHECKED_OUT / A1-A2 CURRENT-IPHONE INGRESS SOURCE PRESENT / A2-TO-EVENT-EPHEMERAL CONTINUATION REPAIR IN PROGRESS / AUTHENTIC A3-A4 PENDING`

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

## First source gap identified

`stegos-bootstrap/canonical-work-runtime-consumption.html` and `.js` currently stop deliberately after `INGRESS_ADMITTED` and report `A1_A2_INGRESS_ADMITTED_A3_A4_PENDING`. They do not call the already-merged EVENT_EPHEMERAL materializer. Therefore an otherwise valid same-iPhone invocation cannot continue into A2.1/A2.2 through this surface.

This repair wires that existing materializer into the existing page only. It does not add another request, listener, scheduler, dispatcher, runtime architecture, WorkerCoordinator, credential path, or second device.

## Authority boundaries

- Node: continuity/admission anchor only.
- Interlock/InTr: governed transition authority.
- EVENT_EPHEMERAL browser materializer: bounded runtime materialization only; claim/fence minting prohibited.
- WorkerCoordinator: sole claim/fence authority.
- TV/TVC: credential authority.
- GitHub/CI: source validation/evidence transport only; runtime authority `NONE`.

## Predicate discipline

Source or CI validation of this repair may establish only that the continuation is wired correctly. It must not mark any authentic runtime predicate true. Authentic predicate promotion requires current-device authority-owned evidence with exact Goal/COSV/nonce/manifest/node/interlock/materialization/lease/runtime correlation.

## Next source transition

After this repair, a valid current-iPhone `INGRESS_ADMITTED` result should immediately continue through the existing EVENT_EPHEMERAL materializer and return runtime-readiness evidence while keeping WorkerCoordinator claim/fence and exact A4 ingress explicitly pending.

## README

README will be reviewed and updated only if this repair changes the documented runtime topology. The intended topology remains unchanged; this work connects two already-documented existing stages.

## Manual work

None.
