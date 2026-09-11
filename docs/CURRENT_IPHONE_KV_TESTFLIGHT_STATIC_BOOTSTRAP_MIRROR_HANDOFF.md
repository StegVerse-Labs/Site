# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Workspace: `claim/current-iphone-kv-testflight-static-bootstrap-r1`
Status: `ACTIVE / AUTHENTIC G7 FENCE7 / KV-GATED SOURCE PROJECTION IN PROGRESS`

## Authentic allocator evidence

The current-iPhone v2 allocator export proves:

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

## Exact KV-gated source

Pinned StegOS source commit:

```text
19e2ea02a16bd703767aafcd47e71f5ec5efe3cf
```

Exact projected source identities:

```text
mobile/web-bootstrap/current-iphone-testflight.html
  git blob c468ceef66a10f1475efc0406c0c9277def004ba
  -> stegos-bootstrap/current-iphone-testflight.html

mobile/web-bootstrap/current-iphone-testflight-bootstrap.js
  git blob e9962ba5589e5f0e3fa2ec32381d65bb41f4f39f
  -> stegos-bootstrap/current-iphone-testflight-bootstrap.js

mobile/web-bootstrap/kv-bound-ephemeral-projection-context.js
  git blob 11f69313eae67b9a7f9126f2e1af331331291dec
  -> stegos-bootstrap/kv-bound-ephemeral-projection-context.js

mobile/web-bootstrap/kv-projection-file-loader.js
  git blob 2682b2f9203770203010146bafcd539313a42948
  -> stegos-bootstrap/kv-projection-file-loader.js
```

The entry requires the user-selected purpose-bound KV projection JSON before signing materialization. The file loader reads at most 32 KiB in memory and validates the projection; the page does not persist the projection.

## Static predecessor material

The KV-gated bootstrap imports the existing unchanged current-iPhone signing chain. Those bytes are not yet present on the Site product branch and must be materialized exactly before this branch can be merged or presented as runnable:

```text
stegos-bootstrap/current-iphone-unsigned-ipa-materializer.js
stegos-bootstrap/StegOSMobile-unsigned-device.ipa
stegos-bootstrap/StegOSMobile-unsigned-device-manifest.json
stegos-bootstrap/StegOSMobile.signing-requirements.json
stegos-bootstrap/current-iphone-wasm-materializer.js
stegos-bootstrap/stegos_current_iphone_ipa_signer.js
stegos-bootstrap/stegos_current_iphone_ipa_signer_bg.wasm
stegos-bootstrap/current-iphone-wasm-signing-engine.js
stegos-bootstrap/current-iphone-ipa-signing-executor.js
stegos-bootstrap/current-iphone-tvc-provider-client.js
stegos-bootstrap/current-iphone-testflight-signing-action.js
contracts/current-iphone-ipa-signing-executor.v1.json
```

Required exact binary commitments remain:

```text
StegOSMobile-unsigned-device.ipa
sha256 557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35

stegos_current_iphone_ipa_signer_bg.wasm
sha256 699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93
```

The shared static source may be transported as exact-byte support material, but that transport must not reinterpret, renew, or widen TASK-2026-0010 authority. TASK-2026-0011 G7/fence7 is the active product execution fence.

## Authority boundary

- WorkerCoordinator/canonical allocator owns claim/fence.
- Interlock/InTr owns governed transition/admission.
- TV/TVC owns Apple credential/provider operations.
- GitHub Actions, if used, are exact source/evidence transport and validation only.
- HB is observability only.
- No Render or hosted fallback.
- No second user-operated machine.

## Current first unresolved predicate

`EXACT_STATIC_SIGNING_CHAIN_MATERIALIZED_AND_VERIFIED_ON_TASK_2026_0011_PRODUCT_BRANCH`

After that predicate is satisfied:

1. validate exact byte identities for the complete product chain;
2. validate the KV gate against positive and fail-closed projection fixtures;
3. open the product PR from this exact workspace to `main`;
4. merge only after exact-head checks pass and public publication is observed;
5. on the established current iPhone select the already-produced authentic KV projection JSON and run the same-device TestFlight bootstrap;
6. continue to TV/TVC native Build Upload and retained TestFlight/runtime evidence.

## Manual work

None while exact static predecessor material is being materialized and validated.
