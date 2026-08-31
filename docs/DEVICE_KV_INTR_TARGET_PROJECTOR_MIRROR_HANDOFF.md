# DEVICE_KV InTr Runtime Target Projector Mirror Handoff

Updated: 2026-08-31
Repository: `StegVerse-Labs/Site`
Issue: `#797`
Branch: `feat/device-kv-intr-target-projector-797`
State: ACTIVE_IMPLEMENTATION
Credential authority: TV/TVC
Authority effect: NONE

## Purpose

Promote `stegos-node/device-kv-intr-sync-target.json` only from independently captured runtime evidence that a credentialless HTTPS sovereign `/intr/profile` is live and explicitly supports `KV:KnowledgeVaultInterlock`.

The merged/default target remains fail closed:

```text
state: AWAITING_SOVEREIGN_INTR_INGRESS
ingress_url: null
runtime_ingress_observed: false
```

Source, CI, a configured hostname, or the existence of profiled-ingress code is not runtime observation.

## Accepted evidence

Input schema: `stegverse.universal-intr-ingress-observation/v1`.

Required predicates:
- HTTPS `/intr/profile` observed;
- HTTP 200;
- no credential used;
- exact canonical profile hash;
- durable evidence reference;
- TV/TVC credential authority;
- no GitHub-token runtime authority;
- no execution authority;
- event-triggered;
- no always-on application receiver;
- `STEGOS_NODE_OUTBOX` supported;
- `KV:KnowledgeVaultInterlock` included in profiles;
- TLS observed.

## Projection

Only after all predicates pass may the projector emit:
`CONFORMING_SOVEREIGN_INTR_INGRESS`
with the exact same-origin `/intr/materialization` URL.

It explicitly leaves:
- runtime materialization observation false;
- canonical KV staging/readback false;
- trusted semantic admission false;
- provider/SKAP activation false.

## Claimed surfaces

- `scripts/project_device_kv_intr_sync_target.py`
- `tests/test_device_kv_intr_sync_target_projector.py`
- `docs/DEVICE_KV_INTR_TARGET_PROJECTOR_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-device-kv-intr-target-projector-797-20260831.json`

## Completion boundary

Source completion requires exact-head validation and merge. Target activation requires authentic runtime observation evidence and separate projection execution.
