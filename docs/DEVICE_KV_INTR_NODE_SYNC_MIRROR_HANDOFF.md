# DEVICE_KV Node Outbox InTr Sync Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#794`
Branch: `feat/device-kv-intr-sync-794`
State: SOURCE_MERGED_VALIDATED / RUNTIME_INGRESS_OBSERVATION_OPEN
Updated: 2026-08-31
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Add the missing browser egress for canonical DEVICE_SYSTEM -> KV Universal InTr materializations already stored in the registered StegVerse Node outbox.

## Existing canonical owners

- Node continuity/outbox: `assets/stegverse-node-continuity.js`
- profiled sovereign ingress: `StegVerse-Labs/.github/workers/universal_intr_profiled_ingress.py`
- resident DEVICE_KV consumer: `StegVerse-Labs/.github/scripts/consume_device_kv_intr_materialization_request.py`
- CVK portable staging: `StegVerse-Labs/continuity-vault-kit/runtime/portable_direct_source_ingress.py`

This lane creates no second transport/runtime owner.

## Exact admitted class

```text
destination={"boundary":"KV","subsystem":"KnowledgeVault:Interlock"}
downstream_owner_ref=StegVerse-Labs/continuity-vault-kit#79
transport_origin=STEGOS_NODE_OUTBOX
ingress_receipt_schema=stegverse.device-kv-intr-materialization-ingress/v1
```

## Required behavior

1. My KV directory loads canonical Node continuity before portable source bridge.
2. New portable materialization is queued locally first.
3. DEVICE_KV sync selects only its exact destination/owner class.
4. Full outbox entry hash and materialization request binding are revalidated.
5. Trigger contains the exact outbox entry and grants no authority.
6. Only a conforming credentialless HTTPS `/intr/materialization` target may be called.
7. Only exact `INGRESS_ADMITTED` receipt advances network-delivery observation.
8. Runtime execution, KV staging, trusted semantic admission, and provider state remain separate.
9. Pending packets retry only by exact packet identity.

## Claimed surfaces

- `stegos-node/device-kv-intr-sync.js`
- `stegos-node/device-kv-intr-sync-target.json`
- `my-kv-directory.html`
- `assets/my-kv-portable-direct-source-bridge.js`
- `scripts/check_device_kv_intr_sync.py`
- `tests/test_device_kv_intr_sync.py`
- `docs/DEVICE_KV_INTR_NODE_SYNC_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-device-kv-intr-sync-794-20260831.json`

## Completion boundary

Source completion requires exact-head Site validation and merge. Live delivery requires an authentic runtime projection that changes the target from AWAITING to a currently observed conforming sovereign ingress URL; source must not fabricate that route.


## Release reconciliation — 2026-08-31

Machine claim:
`SITE-DEVICE-KV-INTR-SYNC-794-20260831` = `RELEASED_COMPLETE`.

Source evidence:
- issue #794
- implementation PR #795
- release commit `3e2dbd71e503bb5fd59d6d6b154ff7ac899b22ee`

Repository-local source implementation and validation are complete. The live delivery boundary remains open:
```text
PUBLIC_SOVEREIGN_INTR_PROFILE_OBSERVED: false
TARGET_STATE: AWAITING_SOVEREIGN_INTR_INGRESS
INGRESS_URL: null
DEVICE_KV_NETWORK_DELIVERY_OBSERVED: false
RUNTIME_MATERIALIZATION_OBSERVED: false
```

No source/CI/merge/deployment state substitutes for an authentic HTTPS runtime observation.


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


## 2026-09-02 My KV Step 2 device-local installation-status repair

The public iPhone runtime exposed a concrete post-merge gap: the DEVICE_KV browser bridge emits `MY_KV_INSTALLATION_STATUS`, but the root-scoped device-local InTr service worker admitted only directory and connection-health query classes. That caused Step 2 to fall into the generic unavailable/fallback path before a canonical installation projection could return.

The device-local runtime now admits exactly one additional read-only record class:

```text
MY_KV_INSTALLATION_STATUS
selector.receipt_path = _System/installation.receipt.json
```

It returns `stegverse.kv.installation-status-projection/v1` and preserves the existing fail-closed distinction:

- missing/invalid canonical receipt -> `KV_INSTALLATION_NOT_VERIFIED`;
- canonical schema/source/tree/destination/parity/authority/source-census validation PASS -> `KV_INSTALLATION_VERIFIED`;
- `current_cloud_provider_observation=false` in both cases;
- no provider credentials, execution authority, claim/fence, or cloud verification are created.

The response binds `receipt_path` and the exact selector while setting directory selectors to null, matching the existing browser validation contract. This repair is source/runtime-capability work only; an authentic current-iPhone re-observation remains required before the active claim can terminalize.


## 2026-09-02 installation-status local-target routing repair

Post-merge inspection found a second exact routing defect. The root-scoped service worker now accepts `MY_KV_INSTALLATION_STATUS`, but `stegos-node/device-kv-intr-sync.js` still classified only directory and connection-health reads as eligible for device-local target discovery. Installation-status queries therefore bypassed the repaired iPhone service worker and fell back to the static remote target.

The local target allowlist now contains exactly:

```text
MY_KV_DIRECTORY_PROJECTION
MY_KV_CONNECTION_HEALTH
MY_KV_INSTALLATION_STATUS
```

This keeps the device-local route bounded to the three explicitly implemented read classes. Other record classes continue to use the remote-target path and fail closed when unavailable. No authority or credential semantics change.


## 2026-09-02 installation-status local-ingress receipt repair

A third exact device-local incompatibility was identified after the routing repair. The query bridge accepted `local_ingress_observed=true` for directory and connection-health reads, but installation-status still required `network_delivery_observed=true`. The iPhone service-worker path intentionally records device-local ingress as local, not network, so a valid installation response would still fail before result retrieval.

The query-return bridge now treats the three explicitly supported device-local read classes equivalently for ingress observation:

```text
MY_KV_DIRECTORY_PROJECTION
MY_KV_CONNECTION_HEALTH
MY_KV_INSTALLATION_STATUS
```

A remote delivery may still satisfy `network_delivery_observed=true`; the device-local service-worker path may satisfy `local_ingress_observed=true`. This only changes evidence classification for the already-admitted read path and does not weaken result, Node, materialization, request-hash, HB-carrier, credential, or authority validation.


## 2026-09-02 current service-worker controller refresh repair

The device-local query contract now depends on the new installation-status class being present in the active root-scoped service worker. A browser can still have an older controller active while a newly deployed worker is installing or waiting. Reading `/intr/profile` immediately in that state can observe the stale controller and incorrectly fall back to the remote target even though the corrected worker is already deployed.

Before reading the local profile, the sync client now performs a bounded service-worker update check and waits for controller handoff when an installing/waiting worker exists. The wait is bounded and non-authorizing; failure to obtain the updated controller still falls back through the existing fail-closed target logic.

This prevents a single stale service-worker controller from masking the already-deployed device-local installation-status capability. It does not assert public runtime activation or bypass exact profile validation.
