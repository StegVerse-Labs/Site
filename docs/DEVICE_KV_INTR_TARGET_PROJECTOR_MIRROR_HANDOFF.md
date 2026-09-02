# DEVICE_KV InTr Runtime Target Projector Mirror Handoff

Updated: 2026-08-31
Repository: `StegVerse-Labs/Site`
Issue: `#797`
Branch: `feat/device-kv-intr-target-projector-797`
State: SOURCE_MERGED_VALIDATED / RUNTIME_INGRESS_OBSERVATION_OPEN
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


## Release reconciliation — 2026-08-31

Machine claim:
`SITE-DEVICE-KV-INTR-TARGET-PROJECTOR-797-20260831` = `RELEASED_COMPLETE`.

Source evidence:
- issue #797
- implementation PR #798
- release commit `81df29e4d79360ac5a5baf264b74a0f97c3ee172`

The projector is implemented, validated, merged, and released. It has **not** been executed against authentic conforming public runtime evidence. The canonical target therefore remains:
```text
state: AWAITING_SOVEREIGN_INTR_INGRESS
ingress_url: null
runtime_ingress_observed: false
```

Activation requires an independently captured credentialless HTTPS `/intr/profile` observation satisfying every projector predicate. No hostname configuration, repository source, CI result, or deployment declaration is sufficient.


## 2026-08-31 device-local sovereign InTr runtime correction

The previous checked-in `AWAITING_SOVEREIGN_INTR_INGRESS` target remains a fail-closed remote fallback, but it is no longer the primary runtime-discovery mechanism.

The current-user iPhone already satisfies the physical/runtime requirements needed for the DEVICE_KV transport edge through a root-scoped StegVerse service worker:

```text
registered StegVerse Node on current iPhone
-> /intr-service-worker.js, scope /
-> GET /intr/profile
-> ACTIVE_SOVEREIGN_INTR_INGRESS
-> runtime_surface=CURRENT_USER_IPHONE_SERVICE_WORKER
-> runtime_owner=REGISTERED_STEGVERSE_NODE
-> profile KV:KnowledgeVaultInterlock
-> POST /intr/materialization
-> write-once IndexedDB DEVICE_KV materialization
-> POST /intr/device-kv/result
-> HB-derived exact response recovery evidence
```

`stegos-node/device-kv-intr-sync.js` now attempts this live same-origin observation first. It returns `CONFORMING_SOVEREIGN_INTR_INGRESS` only after the service worker is registered/ready and an actual `/intr/profile` response satisfies every transport, TLS, profile, credential-authority, and non-execution predicate.

Only if that authentic device-local observation fails does discovery fall back to the static `device-kv-intr-sync-target.json`, whose null `AWAITING_SOVEREIGN_INTR_INGRESS` state remains unchanged.

This corrects the earlier remote-only assumption. "Sovereign ingress" describes the admitted StegVerse Node/runtime boundary, not a requirement for a second machine or an always-on remote server.

Authority remains:

```text
credential authority: TV/TVC
transport execution authority: NONE
GitHub token runtime authority: NONE
HB carrier authority: NONE
second user device required: false
external non-StegVerse machine required: false
```

The local runtime does not advertise SKAP_VAULT custody yet; that profile remains a separate downstream integration and cannot be inferred from DEVICE_KV activation.


## DEVICE_LOCAL_SOVEREIGN_INTR_RUNTIME_CURRENT_SERVICE_WORKER_REFRESH — 2026-09-02

The active Site claim now owns a fully reconciled current-iPhone DEVICE_KV read path. The prior device-local correction section described the architecture but did not yet include the installation-status compatibility repairs that were subsequently merged.

Current merged sequence:

```text
PR #900 -> root-scoped service worker admits MY_KV_INSTALLATION_STATUS
PR #901 -> device-kv-intr-sync routes MY_KV_INSTALLATION_STATUS through device-local target discovery
PR #902 -> query bridge accepts authentic local_ingress_observed evidence for installation status
PR #903 -> device-kv-intr-sync performs bounded registration.update() and controller handoff before /intr/profile
```

Exact supported device-local read classes are now:

```text
MY_KV_DIRECTORY_PROJECTION
MY_KV_CONNECTION_HEALTH
MY_KV_INSTALLATION_STATUS
```

The remaining activation predicate is runtime-only and must be observed on the current registered iPhone:

```text
GET /intr/profile
state=ACTIVE_SOVEREIGN_INTR_INGRESS
runtime_surface=CURRENT_USER_IPHONE_SERVICE_WORKER
runtime_owner=REGISTERED_STEGVERSE_NODE
profiles includes KV:KnowledgeVaultInterlock
device_local_query_record_classes exactly matches the three-class allowlist
credential_authority=TV/TVC
execution_authority=NONE
authority_effect=NONE_DISCOVERY_EVIDENCE_ONLY
```

For My KV Step 2, that profile observation must be followed by an authentic Node-bound `MY_KV_INSTALLATION_STATUS` materialization and exact HB-derived result recovery. A valid device-local result may establish the bounded resident installation projection; it does not establish fresh cloud-provider observation or Step 5 verification.

No additional Site source implementation is currently identified for this Step 2 path. The active claim remains open only because the current-device runtime evidence has not yet been captured.


## 2026-09-02 current-iPhone observation regression repair

The 11:44 -05:00 current-iPhone observation reached the deployed Step 2 page but still returned the generic automatic DEVICE_KV unavailable state. Inspection of current `main` found a concrete regression: `assets/my-kv-device-kv-query-bridge.js` had reverted its local-ingress eligibility expression to directory + health only, excluding `MY_KV_INSTALLATION_STATUS`, despite the service worker and sync target already advertising the three-class local capability.

The browser pages also retained the pre-repair query-bridge cache token, so Safari could continue executing an older bridge asset even after source correction.

This repair:
- restores `MY_KV_INSTALLATION_STATUS` to device-local result eligibility;
- adds a fresh version token to both the DEVICE_KV sync client and query bridge on My KV pages;
- preserves the separate network-delivery path;
- surfaces the exact fail-closed Step 2 error reason after the generic product-safe prefix so a subsequent current-device observation identifies the next failing predicate without requiring developer tools.

No file picker is opened automatically, no runtime observation is inferred from source, and no credential/authority semantics change.
