# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Source workspace: `claim/current-iphone-kv-testflight-static-bootstrap-r1`
Publication-proof workspace: `reconcile/task0011-postmerge-publication`
Status: `ACTIVE / AUTHENTIC G7 FENCE7 / EXACT PRODUCT MERGED / PUBLIC EXACT PUBLICATION PROVEN / CURRENT-IPHONE TESTFLIGHT RUNTIME PENDING`

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

## Frozen source and product identity

Pinned StegOS source commit:

```text
19e2ea02a16bd703767aafcd47e71f5ec5efe3cf
```

Exact product commitments:

```text
current-iphone-testflight.html
  blob c468ceef66a10f1475efc0406c0c9277def004ba
current-iphone-testflight-bootstrap.js
  blob e9962ba5589e5f0e3fa2ec32381d65bb41f4f39f
kv-bound-ephemeral-projection-context.js
  blob 11f69313eae67b9a7f9126f2e1af331331291dec
kv-projection-file-loader.js
  blob 2682b2f9203770203010146bafcd539313a42948
stegos_current_iphone_ipa_signer.js
  blob 4a44ef69ac3e61b9c353d439b4781bec3811f63e
  sha256 17fe61cfdae43cbe5a1d1b211beb39838f58e982efdba90c7156fc36402f3adb
StegOSMobile-unsigned-device.ipa
  blob 3183c95dbcd73ab7d86acad9b68aef41ea1110b0
  sha256 557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35
  bytes 389564
stegos_current_iphone_ipa_signer_bg.wasm
  blob 74d9ece3a911c20ce9f89e879c91e027fab10c12
  sha256 699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93
  bytes 2277815
```

The IPA and WASM were recovered through authentic StegOS workflow artifacts `10119511850` and `10120870613`. No Site credential was granted cross-repository StegOS read authority.

## Validation and merge evidence

Commit `0aa6d7f912bb2d1b9f4816bbb8688ed72a1c2a21` retired the obsolete cross-repository transport attempt and installed the read-only local exact-byte verifier.

```text
Site Bootstrap Validate run 34615091923: SUCCESS
TASK-0011 Exact Product Source Verification run 34615092070: SUCCESS
```

PR validation then exposed and repaired coordination drift: the product branch was explicitly claimed, and stale completed allocator ownership was terminalized using PR #1230 plus authentic generation-7/fence-7 evidence. Exact PR head `e92e739d622b7756bf59a82d22919a089fffeeef` passed Bootstrap Validate, Ecosystem Heartbeat, Site Handoff Orchestrator, and Persistent Card UX.

Site PR `#1236` was squash-merged:

```text
merge commit 841ab0298741fd5152c9cf88211468c3b86093d3
merged_at 2026-09-11T15:24:11Z
post-merge main Site Bootstrap Validate run 34615914477: SUCCESS
```

## Public exact publication evidence

Publication-proof commit:

```text
6202ffb8f7b777fc9275c4a8548f41b2c703c1ad
```

Credential-free run `34616154322` fetched the live `https://stegverse.org/stegos-bootstrap/` assets and succeeded. The job log proves the live public bytes match all frozen identities above, including exact IPA/WASM SHA-256, byte counts, and Git blobs.

```text
TASK0011_PUBLIC_SITE_PUBLICATION=PASS
TASK0011_PUBLICATION_AUTHORITY_EFFECT=NONE
TASK0011_RUNTIME_PROOF_EFFECT=NONE
```

Public propagation is therefore proven. Publication is not signing, TestFlight, or runtime proof.

## KV gate validation surface

The deterministic Site path requires the authentic purpose-bound projection before signing materialization and retains these boundaries:

- current-device Device→KV InTr admission is reused;
- `KV_INSTALLATION_VERIFIED`, resident KV root observation, installation receipt presence, and full-template parity are required;
- browser projection remains ephemeral/in-memory;
- user-agent/browser fingerprint data is not elevated to authority;
- TV/TVC remains Apple credential/provider authority;
- GitHub runtime authority remains `NONE`;
- HB remains observability only;
- no second user-operated machine and no hosted fallback.

## Current first unresolved predicate

`TESTFLIGHT_CURRENT_IPHONE_RUNTIME_OBSERVED`

Public entrypoint:

```text
https://stegverse.org/stegos-bootstrap/current-iphone-testflight.html
```

The established current iPhone must select one already-produced authentic `CURRENT_IPHONE_TESTFLIGHT_SIGNING` KV projection JSON. The page must admit that exact projection before the unsigned IPA and WASM signer materialize. TV/TVC then owns Apple provisioning/provider operations. Preserve the complete displayed result or fail-closed message and subsequent Build Upload/TestFlight/runtime evidence.

## README state

`README.md` was reviewed against the completed source/publication milestone. Its existing public-mirror and authority boundary remains correct and does not imply that Site publication grants receipt, credential, allocator, signing, execution, or runtime authority. No semantic README rewrite is required for this milestone.

## Manual work

On the established current iPhone, open `https://stegverse.org/stegos-bootstrap/current-iphone-testflight.html`, tap the KV projection file selector, select one of the already-produced authentic `CURRENT_IPHONE_TESTFLIGHT_SIGNING` JSON files, and tap `Prepare Signed TestFlight IPA`. Preserve the complete displayed result or exact fail-closed message. Do not clear Safari/site/KV/node continuity state and do not switch to a second device.
