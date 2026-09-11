# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Source workspace: `claim/current-iphone-kv-testflight-static-bootstrap-r1`
Recovery workspace: `fix/task0011-same-device-kv-recovery-r1`
Status: `ACTIVE / AUTHENTIC G7 FENCE7 / EXACT PRODUCT MERGED / PUBLIC EXACT PUBLICATION PROVEN / SAME-DEVICE KV RECOVERY IN VALIDATION`

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

The frozen TASK-0011 product remains unchanged. Its public exact publication is already proven through Site PR #1236 merge commit `841ab0298741fd5152c9cf88211468c3b86093d3`, post-merge validation run `34615914477`, and credential-free public proof run `34616154322`.

Frozen identities retained:

```text
current-iphone-testflight.html blob c468ceef66a10f1475efc0406c0c9277def004ba
current-iphone-testflight-bootstrap.js blob e9962ba5589e5f0e3fa2ec32381d65bb41f4f39f
kv-bound-ephemeral-projection-context.js blob 11f69313eae67b9a7f9126f2e1af331331291dec
kv-projection-file-loader.js blob 2682b2f9203770203010146bafcd539313a42948
StegOSMobile-unsigned-device.ipa sha256 557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35 bytes 389564
stegos_current_iphone_ipa_signer_bg.wasm sha256 699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93 bytes 2277815
```

## User-observed recovery condition

On 2026-09-11 the established current-iPhone operator reported that the correct projection file was not available and the candidate files on hand all produced `FAIL_CLOSED` at the frozen bootstrap.

This is not treated as a reason to synthesize projection commitments or weaken the gate. The frozen validator requires the exact purpose `CURRENT_IPHONE_TESTFLIGHT_SIGNING`, `entry_state=ADMITTED`, `browser_capability_state=OBSERVED_COMPATIBLE`, exact persistence/authority effects, and three `sha256:` commitments. Older exports, allocator receipts, installation receipts, or differently shaped JSON are not valid substitutes.

## Same-device recovery implementation

Branch `fix/task0011-same-device-kv-recovery-r1` introduces only a wrapper surface:

```text
task0011-same-device-kv-recovery.html
```

The wrapper leaves every frozen `stegos-bootstrap/` byte untouched. It reuses the existing Site projection stack:

```text
StegVerseNodeContinuity
StegVerseGeneratedInTr
StegVerseHBInTrCarrier
StegVerseDeviceKVInTrSync
StegVerseKVTestFlightProjectionEntry
StegVerseKVTestFlightProjectionExport
StegVerseKVInstallationBridge
```

Normal path:

```text
owner tap
-> current-device Device→KV InTr purpose-bound request
-> authentic InTr ingress validation
-> KV_INSTALLATION_VERIFIED required
-> current browser capability observation
-> exact projection derived in memory
-> frozen executeStaticCurrentIphoneTestflightBootstrap({projectionContext})
-> TV/TVC-owned signing/provider path
```

No saved projection file is required for the normal path. The exact projection can still be optionally saved after successful materialization for evidence/reuse.

If the resident KV installation itself is not verified, the wrapper exposes the existing bounded `Admit Existing KV Installation Receipt` recovery control. It still requires the canonical `_System/installation.receipt.json`; it does not invent or reconstruct that receipt.

Focused regression test:

```text
tests/task0011-same-device-kv-recovery.test.cjs
```

The test asserts direct in-memory projection handoff, frozen-bootstrap reuse, canonical installation-recovery reuse, and absence of localStorage/sessionStorage/IndexedDB/GitHub-token/hosted-fallback dependencies on the wrapper.

## Authority boundary

- Interlock/InTr remains governed transition/admission authority.
- KV remains the private continuity boundary.
- TV/TVC remains Apple credential/provider/signing authority.
- WorkerCoordinator/canonical allocator remains claim/fence authority.
- Site remains a public projection/rendezvous surface only.
- GitHub Actions remain validation/evidence transport only.
- HB remains carrier/observability only.
- No projection commitment is synthesized.
- `KV_INSTALLATION_VERIFIED` is not bypassed.
- No second user-operated machine is introduced.

## README state

`README.md` was reviewed for this recovery slice. Its public-mirror and authority-boundary language remains correct; this wrapper is an operational same-device rendezvous and does not change Site authority semantics. No repository-wide semantic rewrite is required.

## Current first unresolved predicate

`SAME_DEVICE_KV_RECOVERY_EXACT_HEAD_VALIDATION_AND_MERGE`

After that predicate:

1. prove public publication of `task0011-same-device-kv-recovery.html`;
2. open it on the established current iPhone;
3. tap `Use This iPhone's KV and Prepare IPA`;
4. preserve the exact successful result or exact fail-closed message;
5. if and only if the error is `resident KV installation not verified`, use the existing installation-receipt recovery control if the canonical `_System/installation.receipt.json` is available;
6. continue TV/TVC Build Upload/TestFlight/runtime evidence only after authentic signing succeeds.

## Manual work

None until exact-head validation, merge, and public publication of the recovery wrapper are proven.
