# Device-Local HIL InTr Mirror Handoff

Repository: `StegVerse-Labs/Site`
State: RELEASED
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


## Release reconciliation — 2026-09-02

PR #941 merged as `20b7603be8e88dd714fa4cef3337552704f9e4e8`.

Validated exact head after the initial syntax defect was corrected:

- Site Bootstrap Validate `33706014809` — SUCCESS
- Site Handoff Orchestrator `33706014823` — SUCCESS
- Ecosystem Heartbeat Orchestration `33706014808` — SUCCESS
- StegOS Node Public Observation source validation `33706014813` — SUCCESS

The registered-iPhone root InTr service worker now advertises both:

```text
KV:KnowledgeVaultInterlock
HIL:Ingress
```

The HIL Node sync client checks the authenticated same-device profile first and uses the static HIL target only as external fallback.

Same-device HIL admission is now explicitly:

```text
local_ingress_observed=true
network_delivery_observed=false
runtime_materialization_observed=false
receiver_receipt_observed=false
tvc_receipt_observed=false
```

This closes the second-device/external-ingress implementation gap without fabricating downstream HIL completion.
