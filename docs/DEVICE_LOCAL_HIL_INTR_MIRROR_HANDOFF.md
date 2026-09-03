# Device-Local HIL InTr Mirror Handoff

Repository: `StegVerse-Labs/Site`
State: ACTIVE_IMPLEMENTATION
Branch: `feat/device-local-hil-intr-20260902`
Updated: 2026-09-02
Authority effect: NONE
Activation effect: false

## Goal

Use the already-established root-scoped current-iPhone Universal InTr service worker as a canonical HIL ingress profile instead of requiring the HIL Node sync client to remain dependent on a separate external ingress locator.

## Existing substrate

The root `/intr-service-worker.js` already provides:

- `GET /intr/profile`;
- `POST /intr/materialization`;
- `runtime_surface=CURRENT_USER_IPHONE_SERVICE_WORKER`;
- `runtime_owner=REGISTERED_STEGVERSE_NODE`;
- event-ephemeral, no-second-device semantics;
- TV/TVC-only credential authority;
- write-once request admission;
- no execution authority.

It currently advertises only `KV:KnowledgeVaultInterlock`.

## Required extension

Add bounded profile `HIL:Ingress`.

The same-device HIL path must:

1. validate the exact registered Node trigger and outbox hash;
2. admit only destination `{boundary:STEGOS_ECOSYSTEM, subsystem:HIL:Ingress}`;
3. admit only owner `StegVerse-Labs/.github#246`;
4. write the exact materialization request once in the existing service-worker request store;
5. return `stegverse.hil-intr-materialization-ingress/v1` with `INGRESS_ADMITTED`;
6. claim no HIL custody, receiver readiness, runtime execution, TVC lifecycle, claim/fence, G18 requirement, or network delivery;
7. classify same-origin service-worker admission as **local ingress**, not StegOS network sync;
8. leave the static HIL target JSON fail-closed as fallback for genuinely external sovereign ingress.

No PDF bytes are copied into the service worker by this lane.

## Claimed paths

- `intr-service-worker.js`
- `stegos-node/hil-intr-sync.js`
- `scripts/check_hil_intr_node_sync.py`
- `tests/test_hil_intr_node_sync.py`
- `tests/test_device_kv_intr_sync.py`
- `docs/DEVICE_LOCAL_HIL_INTR_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-device-local-hil-intr-20260902.json`

## Release boundary

Release after HIL and DEVICE_KV regression validation, current Site orchestration/bootstrap/heartbeat gates, merge, and truthful claim/handoff reconciliation. Public iPhone observation may confirm deployment later but must not retain source ownership.
