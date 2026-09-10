# StegSocials Bounded Group Node/InTr Routing Mirror Handoff

Updated: 2026-09-10

## Goal

- Goal Task ID: `SS-KV-SKAP-SOCIAL-RELEASE-001`
- Canonical handoff: `StegVerse-Labs/StegSocials/docs/STEGSOCIALS_NATIVE_STEGBROWSER_TRANSPORT_MIRROR_HANDOFF.md`
- Parent Site handoff: `docs/STEGSOCIALS_BOUNDED_GROUP_DEVICE_KV_CAS_MIRROR_HANDOFF.md`
- COSV: `60000000102000`
- State: `ACTIVE`
- Current source substate: `REGISTERED_NODE_INTR_TO_EXISTING_MY_KV_DEVICE_KV_WORKER_ROUTING_IMPLEMENTED_VALIDATION_PENDING`

## Implemented route

```text
already-admitted bounded-group CAS request
  -> StegVerseGeneratedInTr.buildIntent("device-kv", ..., "COMMIT_CANDIDATE")
  -> StegVerseHBInTrCarrier.buildBinding(...) [correlation only]
  -> StegVerseGeneratedInTr.buildMaterializationRequest(...)
  -> StegVerseNodeContinuity.queueIntrMaterializationRequest(...)
  -> hash-bound node outbox trigger
  -> existing /assets/my-kv-n-device-kv-receiver.js
     existing scope /assets/my-kv-n-runtime/
  -> bounded social CAS record-class validation
  -> existing DEVICE_KV CAS commit primitive
  -> exact persisted-state readback result
```

No new worker runtime is registered. The existing MyKV #1/#2/#n resident worker now recognizes `STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS` in addition to its existing record classes. The existing worker imports the already-validated bounded-group DEVICE_KV CAS module and delegates only local atomic persistence after Node/outbox/materialization and social-CAS bindings validate.

## Preserved authority boundaries

- InTr remains admission/transition authority. The generated materialization transport is not itself proof that authentic external admission occurred.
- HB remains synchronization/correlation evidence only and explicitly grants no execution/transition authority.
- TV/TVC + SKAP remains credential authority.
- StegBrowser remains bounded ephemeral social-provider execution.
- DEVICE_KV performs local atomic use-state persistence only.
- Site remains a projection/carrier and does not become publication authority.

## Source surfaces

```text
assets/stegsocials-bounded-group-node-intr-bridge.js
assets/my-kv-n-device-kv-receiver.js
assets/stegsocials-bounded-group-device-kv-cas-receiver.js
tests/stegsocials-bounded-group-node-intr-bridge.test.cjs
.github/workflows/stegsocials-post-preparation.yml
docs/STEGSOCIALS_BOUNDED_GROUP_NODE_INTR_ROUTING_README.md
```

## Required deterministic evidence

1. Registered Node is required before routing.
2. Existing GeneratedInTr/HB/Node primitives are reused.
3. Existing `/assets/my-kv-n-device-kv-receiver.js` and `/assets/my-kv-n-runtime/` are reused; no second service-worker runtime is introduced.
4. Bounded social record class, canonical state path, group ID, use index, payload hash, and payload size are exact-bound.
5. Node outbox trigger is hash-bound.
6. HB carrier cannot grant authority.
7. Worker preserves existing three MyKV record classes while adding bounded social CAS.
8. Worker delegates only persistence to the existing CAS receiver.
9. Credential-bearing/provider-authorizing requests fail closed.
10. Publication and terminal StegBrowser destruction predicates remain required.
11. Focused StegSocials workflow, MyKV workflow, Site Bootstrap, Site Handoff, and Ecosystem Heartbeat validation pass.

## Remaining runtime work

1. Exercise this exact merged path on the retained current-iPhone Node and DEVICE_KV.
2. Retain authentic externally admitted InTr transition evidence; do not infer admission from transport construction.
3. Retain exact Node/outbox/materialization identity and pre-state etag.
4. Observe resident CAS commit and independent exact post-state readback.
5. Bind the request to an authentic StegBrowser publication receipt and terminal session-destruction receipt.
6. Execute at least two in-scope posts under one participant-approved bounded group without renewed approval.
7. Exercise stale/replay/widening refusal controls in the authentic path.
8. Persist resulting publication/use-state evidence into Personal-KV and reconstruct in Master Records.
9. Reconcile authentic evidence into the canonical task registry and applicable downstream propagation surfaces.

## Manual work

None.

## Next executable action

Run exact-head validation. Repair deterministic failures without weakening authority separation or stale/replay protections. Merge only after the focused StegSocials, MyKV, Site Bootstrap, Site Handoff, and Ecosystem Heartbeat gates are green, then move directly to authentic current-iPhone route observation.
