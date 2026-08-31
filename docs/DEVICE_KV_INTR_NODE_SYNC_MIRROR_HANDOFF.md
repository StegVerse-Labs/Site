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
