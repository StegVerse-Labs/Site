# HIL Device/KV Continuity Mirror Handoff

Updated: 2026-09-11
Issue: `#1272`
Parent Goal Task ID: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Parent COSV: `50000000102000`
Dependency Goal Task ID: `STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001`
Dependency COSV: `50000000102000`
Repository: `StegVerse-Labs/Site`

## Physical observation

Current-iPhone browser observations establish that browser storage is partitioned by browser/app container:

- Safari retains HIL continuity material and reaches a fail-closed continuity result;
- ChatGPT in-app browser reaches generic `READY_FOR_USER_ACTION`;
- Opera reaches generic `READY_FOR_USER_ACTION`.

Therefore browser `localStorage`, IndexedDB, and service-worker state may remain a local cache but cannot be the canonical device continuity authority. The user must not be required to remember which browser carried a prior HIL phase.

## Existing owner reused

This work consumes the already-canonical Device -> KV -> SKAP -> KV -> Device lane owned by `STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001`. It does not create a second KV, provider adapter, runtime lease plane, WorkerCoordinator, InTr, SKAP writer, credential authority, or hosted fallback.

Existing authority remains:

```text
WorkerCoordinator -> claim/fence
Canonical Runtime Lane -> bounded event lifecycle
Interlock/InTr -> transition admission
TV/TVC -> credential authority
TVC -> sole SKAP ciphertext custody writer
retained StegOS Node -> identity/genesis/continuity
GitHub/CI/HB -> validation/evidence/observation only
```

## Source contract

The Site HIL consumer will define `stegverse.hil.device-continuity-capsule/v1` as a non-secret, exact-hash-bound continuity object. A capsule may describe the latest admissible HIL stage but grants no authority.

Required bindings include:

- exact HIL task `SHWP-HIL-SOVEREIGN-RECEIVER-001`;
- resident request `RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002`;
- retained G25 claim `SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25`;
- fence `25`;
- retained StegOS Node identity;
- canonical stage (`LOCAL_READY`, `ESRL_LEASE_OPEN`, `PACKET_STAGED`, or `RECEIVER_CUSTODY`);
- exact hashes for any included local-ready result, ESRL lease, staged packet, and custody receipt;
- exact staged response bytes only when needed for reconstruction and always bound to their SHA-256;
- `credential_material_present=false`;
- `provider_operation_authorized=false`;
- `authority_effect=NONE_CONTINUITY_ONLY`.

The browser context identifier is provenance only and must not be a recovery selector or authority binding.

## Resume semantics

`hil-resume.html` may use a valid browser-local cache for speed. If local continuity is absent, incomplete, contradictory, or belongs to another browser container, the canonical next action is DEVICE_KV recovery through the existing governed transport.

Successful DEVICE_KV recovery must:

1. return a capsule bound to the current retained Node and exact HIL lineage;
2. verify canonical response transport/readback and exact capsule hash;
3. validate every stage object before any local cache write;
4. repopulate only the current browser cache from the exact validated capsule;
5. continue through the existing HIL stage-specific pages without minting another claim/fence.

If DEVICE_KV continuity is unavailable, the router must fail closed as `DEVICE_KV_CONTINUITY_UNAVAILABLE`. It must not silently establish a fresh browser-local HIL lineage merely because a different browser container lacks cached state.

## Runtime boundary

`STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001` currently has source integration complete but authentic runtime completion remains false. Therefore this source integration cannot be presented as proof that Safari, ChatGPT browser, Opera, or any other browser already share HIL state.

Authentic cross-browser completion requires an observed governed Device/KV operation with exact KV readback that stores and later recovers the same HIL continuity capsule from a different browser container on the same iPhone.

No HIL parent COSV transition, receiver custody, restart proof, or TVC lifecycle handoff is authorized by source integration alone.

## Manual work

None during source integration. Do not ask the user to choose or remember a prior browser while this dependency remains unresolved.
