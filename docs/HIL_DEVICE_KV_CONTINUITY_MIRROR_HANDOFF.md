# HIL Device/KV Continuity Mirror Handoff

Updated: 2026-09-11
Issue: `StegVerse-Labs/Site#1272`
Parent Goal Task ID: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Parent COSV: `50000000102000`
KV Dependency Goal Task ID: `STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001`
KV Dependency COSV: `50000000102000`
Node continuity dependency: `StegVerse-Labs/StegOS#347`
Inherited Node owner: `StegVerse-Labs/StegOS#23`
Repository: `StegVerse-Labs/Site`
State: `DEPENDENCY_IDENTIFIED / SOURCE_WIRING_NOT_ADMISSIBLE_YET`

## Physical observation

Current-iPhone browser observations establish that browser storage is partitioned by browser/app container:

- Safari retains HIL continuity material and reaches a fail-closed continuity result;
- ChatGPT in-app browser reaches generic `READY_FOR_USER_ACTION`;
- Opera reaches generic `READY_FOR_USER_ACTION`.

Therefore browser `localStorage`, IndexedDB, and service-worker state may remain a local cache but cannot be the canonical device continuity authority. The user must not be required to remember which browser carried a prior HIL phase.

## Deeper prerequisite discovered

Source inspection of `assets/stegverse-node-continuity-impl.js` shows the current Site Node registration is also browser-container-local:

- Node state is stored in IndexedDB database `stegos-node-v1`;
- `registerDevice()` creates a fresh 32-byte random value with `crypto.getRandomValues`;
- the random value is hashed into `device_binding_sha256`;
- `node_id` and `interlock_id` are deterministically derived from that browser-local device binding;
- the registration projection and Receipt #1 are then written only to the same browser IndexedDB.

Therefore different browsers on one physical iPhone can legitimately materialize different Site Node identities. The existing DEVICE_KV browser bridge requires `StegVerseNodeContinuity.status()` and binds each request to that Node identity before any KV read/write is admitted.

This creates a circular dependency if HIL attempts to use KV directly:

```text
recover HIL from canonical KV
-> requires retained Node identity
-> current retained Node identity is browser-local
-> new browser cannot prove it is the same retained Node
```

A HIL-specific workaround must not mint or substitute a different Node merely to reach the prior KV state.

## Canonical Node dependency owner

An organization issue search found `StegVerse-Labs/StegOS#23` as the inherited Node genesis/continuity owner, but its current evidence covers same-Node reload/offline continuity and does not expose browser-independent recovery of the retained Node identity across separate browser/app containers.

`StegVerse-Labs/StegOS#347` now owns the missing capability: recover the same retained Node ID / continuity root / Interlock identity on the same physical device without depending on the originating browser container, while preserving Receipt #1/genesis lineage and existing authority boundaries.

Site issue `#1272` is the downstream HIL consumer integration point and must remain open until `StegOS#347` or an equivalent canonical capability is available.

## Correct dependency order

The admissible architecture is:

```text
StegOS#347 browser-independent device Node continuity/recovery
-> STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001 / Interlock/InTr continuity
-> HIL continuity capsule
-> current browser cache rehydration
-> existing HIL stage continuation
```

HIL may consume those layers but must not own or duplicate them.

## Existing authority preserved

The intended KV transport remains the already-canonical Device -> KV -> SKAP -> KV -> Device lane owned by `STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001`. It does not create a second KV, provider adapter, runtime lease plane, WorkerCoordinator, InTr, SKAP writer, credential authority, or hosted fallback.

```text
WorkerCoordinator -> claim/fence
Canonical Runtime Lane -> bounded event lifecycle
Interlock/InTr -> transition admission
TV/TVC -> credential authority
TVC -> sole SKAP ciphertext custody writer
retained StegOS Node -> identity/genesis/continuity
GitHub/CI/HB -> validation/evidence/observation only
```

## Future HIL continuity capsule contract

Once browser-independent Node continuity is available, the Site HIL consumer may define `stegverse.hil.device-continuity-capsule/v1` as a non-secret, exact-hash-bound continuity object. A capsule may describe the latest admissible HIL stage but grants no authority.

Required bindings include:

- exact HIL task `SHWP-HIL-SOVEREIGN-RECEIVER-001`;
- resident request `RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002`;
- retained G25 claim `SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25`;
- fence `25`;
- retained device-level StegOS Node identity;
- canonical stage (`LOCAL_READY`, `ESRL_LEASE_OPEN`, `PACKET_STAGED`, or `RECEIVER_CUSTODY`);
- exact hashes for any included local-ready result, ESRL lease, staged packet, and custody receipt;
- exact staged response bytes only when needed for reconstruction and always bound to their SHA-256;
- `credential_material_present=false`;
- `provider_operation_authorized=false`;
- `authority_effect=NONE_CONTINUITY_ONLY`.

The browser context identifier is provenance only and must not be a recovery selector or authority binding.

## Future resume semantics

`hil-resume.html` may use a valid browser-local cache for speed. When browser-independent Node continuity and canonical DEVICE_KV recovery are available, absent/incomplete/contradictory local HIL state should trigger device-level continuity recovery rather than a new browser-local lineage.

Successful recovery must:

1. recover and validate the retained device-level Node identity without relying on the prior browser container;
2. return a HIL capsule bound to that retained Node and exact HIL lineage;
3. verify canonical response transport/readback and exact capsule hash;
4. validate every stage object before any local cache write;
5. repopulate only the current browser cache from the exact validated capsule;
6. continue through the existing HIL stage-specific pages without minting another claim/fence.

If device-level Node/KV continuity is unavailable, the router must eventually fail closed as `DEVICE_KV_CONTINUITY_UNAVAILABLE`; it must not silently establish a replacement HIL lineage because a new browser lacks cached state.

## Why HIL source wiring stops here

Wiring a HIL -> KV bridge now would preserve a hidden dependency on browser-local Node IndexedDB and would not satisfy the physical-device continuity requirement. No HIL runtime source is changed on this branch. This handoff is the anti-collision record that prevents a later session from building that circular workaround.

## Runtime boundary

`STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001` has source integration complete but authentic runtime completion remains false. Source/CI cannot establish that Safari, ChatGPT browser, Opera, or any other browser already share HIL state.

Authentic cross-browser completion ultimately requires an observed governed operation where one browser writes exact Node-bound HIL continuity into the canonical device/KV path and another browser on the same iPhone recovers the same retained Node plus exact HIL capsule/readback without minting replacement identity or authority.

No HIL parent COSV transition, receiver custody, restart proof, or TVC lifecycle handoff is authorized by this investigation.

## Manual work

None. Do not ask the user to choose, remember, or revisit the browser that carried prior HIL state while this dependency remains unresolved.
