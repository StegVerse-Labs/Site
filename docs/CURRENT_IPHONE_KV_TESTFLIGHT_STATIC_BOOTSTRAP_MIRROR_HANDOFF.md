# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Workspace: `claim/current-iphone-kv-testflight-static-bootstrap-r1`
Status: `ACTIVE / AUTHENTIC G7 FENCE7 / KV-GATED SOURCE PROJECTION PARTIAL / STATIC SUPPORT TRANSPORT REPAIR REQUIRED`

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

## Exact KV-gated source already materialized

Pinned StegOS source commit:

```text
19e2ea02a16bd703767aafcd47e71f5ec5efe3cf
```

The TASK-2026-0011 product branch already contains byte-identical copies of all four new KV-gating files, with Git blob identities equal to the pinned StegOS source:

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

## Static predecessor support material

The exact pinned StegOS successor manifest proves the KV-gated bootstrap also depends on the unchanged current-iPhone signing chain. Those support bytes are not yet present on this Site product branch:

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

Required exact binary commitments:

```text
StegOSMobile-unsigned-device.ipa
sha256 557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35
bytes 389564
git blob 3183c95dbcd73ab7d86acad9b68aef41ea1110b0

stegos_current_iphone_ipa_signer_bg.wasm
sha256 699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93
bytes 2277815
git blob 74d9ece3a911c20ce9f89e879c91e027fab10c12
```

The authentic source artifacts were independently recovered from StegOS workflow artifacts `10119511850` and `10120870613`; their bytes/hashes match the frozen successor manifest. This proves source availability but does not by itself materialize those bytes into Site.

## Transport investigation and repair state

Transport run `34558913408` failed before materialization because the runner attempted unauthenticated `raw.githubusercontent.com` access to the non-public StegOS source and received HTTP 404.

Commit `541823fec8c5b40201e98dfb767697e68cb79763` repaired the transport workflow to use a pinned second `actions/checkout` and added the workflow path to its own push trigger. Exact-head Site validation started successfully, but transport run `34611288342` failed at the second checkout: the Site-scoped `GITHUB_TOKEN` has no cross-repository read authority for `StegVerse-Labs/StegOS` and GitHub returned `Repository not found`. No product bytes were committed by either failed transport run.

That failure is a transport-permission condition, not a source or architecture failure. GitHub Actions must remain validation/evidence transport only and must not be granted runtime or credential authority merely to bypass this condition. The next continuation should use an existing authorized cross-repository evidence channel or connector-mediated exact-byte transfer, preserving all pinned Git blob/SHA-256 commitments. Do not expose a StegOS private-repository token in Site and do not substitute hosted/runtime fallback.

A connector-side attempt to reference StegOS binary blob `3183c95dbcd73ab7d86acad9b68aef41ea1110b0` directly in a Site Git tree was correctly rejected because Git blob objects are repository-scoped. This confirms that exact binary bytes must actually be transferred into the Site repository object database rather than merely cross-referenced.

## Authority boundary

- WorkerCoordinator/canonical allocator owns claim/fence.
- Interlock/InTr owns governed transition/admission.
- TV/TVC owns Apple credential/provider operations.
- GitHub Actions are exact source/evidence transport and validation only.
- HB is observability only.
- No Render or hosted fallback.
- No second user-operated machine.
- No retroactive widening of TASK-2026-0010.

## Current first unresolved predicate

`EXACT_STATIC_SIGNING_CHAIN_MATERIALIZED_AND_VERIFIED_ON_TASK_2026_0011_PRODUCT_BRANCH`

After that predicate is satisfied:

1. validate exact byte identities for the complete product chain;
2. validate the KV gate against positive and fail-closed projection fixtures;
3. update repository README/handoff with the exact validated source/transport evidence;
4. open the product PR from this exact workspace to `main`;
5. merge only after exact-head checks pass and public publication is observed;
6. on the established current iPhone select the already-produced authentic KV projection JSON and run the same-device TestFlight bootstrap;
7. continue to TV/TVC native Build Upload and retained TestFlight/runtime evidence.

## Coordination note

An accidental empty `noop` file was briefly created on `StegVerse-Labs/.github` main during connector write-capability discovery and immediately deleted. Commits `4a956862fc061e2ae5178c7a35997ebe91c046cf` and `9d27831384028f9a5de375702f96f05e98a56a4f` record the create/revert pair; there is no net tree change and neither commit is runtime, validation, or task evidence.

## Manual work

None. The unresolved condition is repository-to-repository exact-byte transport and must be solved without requiring a second user-operated machine or exposing private repository credentials.
