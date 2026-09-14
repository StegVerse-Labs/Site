# StegBrowser Runtime Consumption Root Profile Repair Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEG-BROWSER-RUNTIME-CONSUMPTION-001`
COSV: `40000100100000`
Canonical parent handoff: `StegVerse-Labs/.github/docs/STEGBROWSER_RUNTIME_CONSUMPTION_MIRROR_HANDOFF.md`
State: `ACTIVE / CHECKED_OUT / CURRENT_IPHONE_NEGATIVE_RUNTIME_EVIDENCE_OBSERVED / ROOT_PROFILE_ROUTING_REPAIR_IN_VALIDATION`

## Authentic observed failure

The current iPhone executed the published self-build launcher and reached the Canonical Work runtime-start path. The user-visible runtime result was:

```json
{
  "state": "FAIL_CLOSED",
  "reason": "root InTr profile HTTP 404",
  "authority_effect": "NONE"
}
```

This is authentic negative current-device runtime evidence. It does not satisfy `INGRESS_ADMITTED` or `CANONICAL_WORK_RESIDENT_CONSUMPTION_OBSERVED`.

## Root cause

The launcher is hosted under `/stegos-bootstrap/`, which already has a more-specific service-worker scope used by the existing offline/portable runtime. The Canonical Work launcher registers the existing root `/intr-service-worker.js` at scope `/`, but its readiness loop used `fetch("/intr/profile")` from the nested page. The more-specific `/stegos-bootstrap/` controller remained the fetch interception surface for that page, so the readiness request did not reach the root InTr fetch handler and fell through to the network as HTTP 404.

This was a scope-routing defect only. The Canonical Work admission trigger already sends `STEGVERSE_INTR_LOCAL_TRIGGER` directly to the root worker object by `postMessage`; no second worker/runtime is required.

## Repair

The repair preserves the existing root worker and adds one discovery-only message type:

```text
STEGVERSE_INTR_PROFILE_QUERY
```

`intr-service-worker.js` answers that message through the existing `profile()` function after loading the existing base worker and Canonical Work extension. The result is the same non-authorizing profile already exposed at `/intr/profile`.

`stegos-bootstrap/canonical-work-root-profile-bridge.js` intercepts only same-origin `/intr/profile` calls made by the Canonical Work launcher. It obtains the already-registered root service-worker registration with `navigator.serviceWorker.getRegistration("/")`, sends `STEGVERSE_INTR_PROFILE_QUERY` through `MessageChannel`, and converts the returned profile into the same Response shape expected by the existing readiness loop.

The bridge is loaded before `canonical-work-runtime-consumption.js`. All other fetches remain delegated to the native fetch implementation.

## Preserved authority boundaries

- No second service worker.
- No second scheduler or dispatcher.
- No second WorkerCoordinator.
- No new credential route.
- TV/TVC remains credential authority.
- Interlock/InTr remains admission/transition authority.
- WorkerCoordinator remains the sole claim/fence authority.
- GitHub runtime authority remains `NONE`.
- No second user-operated device.
- The direct profile query has `authority_effect=NONE`; it is discovery only.

## Validation requirement

`tests/test_canonical_work_runtime_consumption_same_device.py` now requires:

- the root wrapper still imports exactly the same base + Canonical Work extension;
- the root wrapper supports `STEGVERSE_INTR_PROFILE_QUERY` and returns `profile()`;
- the bridge resolves the existing root registration at `/`;
- the bridge uses `MessageChannel` to the existing root worker;
- only `/intr/profile` is intercepted;
- the bridge loads before the unchanged Canonical Work launcher;
- the launcher still uses the existing `STEGVERSE_INTR_LOCAL_TRIGGER` admission route and write-once Node outbox.

Source, CI, merge, GitHub Pages publication, or service-worker installation do not prove admission. After merge/public propagation, the same current iPhone must rerun the launcher and retain the next authentic runtime result.

## README disposition

No repository-wide architecture or user contract changed. The existing README already states the same-device current-iPhone runtime, single root InTr authority separation, and source-vs-runtime proof boundary. No README mutation is required for this bounded routing repair.

## Next unresolved predicate

`CANONICAL_WORK_RESIDENT_CONSUMPTION_OBSERVED`

Before that predicate can be satisfied, the repaired current-device path must first produce an authentic `INGRESS_ADMITTED` result. If that occurs, continue to the current WorkerCoordinator claim/fence and existing resident-consumption chain. If another fail-closed result appears, retain it as runtime evidence and repair only that exact next blocker.
