# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Workspace: `claim/current-iphone-kv-testflight-static-bootstrap-r1`
Status: `ACTIVE / AUTHENTIC G7 FENCE7 / EXACT FROZEN PRODUCT CHAIN MATERIALIZED / LOCAL EXACT-BYTE VERIFIER INSTALLED / PRODUCT PR NOT YET MERGED`

## Authentic allocator evidence

```text
selected_task_id: TASK-2026-0011
claim_registry_generation: 7
claim_observation.state: CLAIM_GRANT_OBSERVED
fencing_token: 7
dependency_surface: site:current-iphone-kv-testflight-static-bootstrap
canonical_allocator_receipt.state: ALLOCATION_COMPLETE
canonical receipt sha256: sha256:3cd0aa9245be0ac5e9b81bc6c5a48aae0edc6f7c95162998e854feea04e75520
node journal sequence: 67
node journal entry sha256: 34d649f1227db25f1a9ddb38fbea709c0fdf4ff5ad0148bb781bbee5c18fb5cf
journal replay: PASS
allocator recovery/export mutation: false
```

TASK-2026-0010 generation-6/fence-6 remains immutable predecessor provenance and is not widened.

## Frozen source identity

Pinned StegOS source commit:

```text
19e2ea02a16bd703767aafcd47e71f5ec5efe3cf
```

The four KV-gating files on the product branch remain byte-identical to that frozen source:

```text
stegos-bootstrap/current-iphone-testflight.html
  c468ceef66a10f1475efc0406c0c9277def004ba
stegos-bootstrap/current-iphone-testflight-bootstrap.js
  e9962ba5589e5f0e3fa2ec32381d65bb41f4f39f
stegos-bootstrap/kv-bound-ephemeral-projection-context.js
  11f69313eae67b9a7f9126f2e1af331331291dec
stegos-bootstrap/kv-projection-file-loader.js
  2682b2f9203770203010146bafcd539313a42948
```

The complete unchanged signing-support chain is now also materialized on this branch with the exact frozen Git blobs. The two large binaries were transferred through the already-authorized StegOS workflow-artifact evidence channel, not by granting Site a StegOS repository credential.

Authentic binary source artifacts:

```text
StegOS artifact 10119511850 -> StegOSMobile-unsigned-device.ipa
StegOS artifact 10120870613 -> stegos_current_iphone_ipa_signer_bg.wasm
```

Destination exact commitments:

```text
StegOSMobile-unsigned-device.ipa
  git blob 3183c95dbcd73ab7d86acad9b68aef41ea1110b0
  sha256 557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35
  bytes 389564

stegos_current_iphone_ipa_signer_bg.wasm
  git blob 74d9ece3a911c20ce9f89e879c91e027fab10c12
  sha256 699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93
  bytes 2277815

stegos_current_iphone_ipa_signer.js
  git blob 4a44ef69ac3e61b9c353d439b4781bec3811f63e
  sha256 17fe61cfdae43cbe5a1d1b211beb39838f58e982efdba90c7156fc36402f3adb
```

Materialization evidence:

```text
7e3937c1863d512d46f831263f77491a3a9389a3  Materialize exact TASK-2026-0011 IPA and WASM binaries
4a47b56c5dc2a7719f4315aac612c15b8600a9ae  Repair exact TASK-2026-0011 signer JS source
83ca0a5e8fcb157a615c84959da998d5440b2db0  Retire completed TASK-2026-0011 exact binary relay
```

The prior private-raw and cross-repository-checkout failures remain useful negative transport evidence, but they are no longer the active predicate. The temporary authenticated relay was retired after materialization.

## Exact local verification workflow

Commit `0aa6d7f912bb2d1b9f4816bbb8688ed72a1c2a21` converted `.github/workflows/task0011-product-source-transport.yml` from the obsolete cross-repository transport attempt into a read-only local exact-byte verifier. It requires `contents: read` only and verifies all frozen Git blob identities plus the IPA/WASM/signer SHA-256 and binary sizes. It does not fetch StegOS, mutate source, push commits, grant runtime authority, or handle credentials.

The previously observed exact-head Site validation run `34613648786` succeeded at head `83ca0a5e8fcb157a615c84959da998d5440b2db0`. Exact-head workflow evidence for the new verifier commit must be observed before this branch is called merge-ready.

## KV gate validation surface

The existing deterministic Site tests assert that the projection path:

- reuses current-device Device-KV InTr admission;
- requires `KV_INSTALLATION_VERIFIED`, resident KV root observation, installation receipt presence, and validated full-template parity;
- collects no user agent or browser/device fingerprint authority;
- keeps browser projection in memory rather than localStorage/sessionStorage/IndexedDB;
- exports only the canonical projection context schema and excludes `kv_lineage_id`;
- preserves TV/TVC credential authority and GitHub runtime authority `NONE`.

Source/test presence is not runtime proof. Current-iPhone signing, TV/TVC Build Upload, TestFlight installation, and retained runtime evidence remain downstream predicates.

## Authority boundary

- WorkerCoordinator/canonical allocator owns claim/fence.
- Interlock/InTr owns governed transition/admission.
- TV/TVC owns Apple credential/provider operations.
- GitHub Actions are validation/evidence transport only.
- HB is observability only.
- No Render or hosted fallback.
- No second user-operated machine.
- No retroactive widening of TASK-2026-0010.

## Current first unresolved predicate

`EXACT_HEAD_LOCAL_CHAIN_VERIFIER_AND_SITE_VALIDATION_PASS_ON_CURRENT_PRODUCT_HEAD`

After that predicate is satisfied:

1. reconcile the product branch against current `main` without changing frozen product bytes;
2. open the product PR from this exact workspace to `main`;
3. merge only after exact-head checks pass and mergeability is proven;
4. observe public publication before claiming Site propagation;
5. on the established current iPhone select the already-produced authentic KV projection JSON and run the same-device TestFlight bootstrap;
6. continue through TV/TVC native Build Upload and retain TestFlight/runtime evidence.

## Manual work

None at this point. Current work is repository-side validation and integration; no iPhone credential entry or second device is required yet.
