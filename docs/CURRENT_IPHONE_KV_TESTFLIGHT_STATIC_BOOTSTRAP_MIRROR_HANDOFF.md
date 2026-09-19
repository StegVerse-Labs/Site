# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Status: `LEGACY IMPLEMENTATION LABELS / DEVICE-BOUND CONTINUATION SUPERSEDED / AUTHENTIC G7 FENCE7 RETAINED / PROVIDER-NEUTRAL ANY-DEVICE REBIND REQUIRED`

## Mandatory supersession notice

This file name and historical symbols contain `CURRENT_IPHONE` and `same-device` because that was the implementation path used to produce earlier evidence. Those strings are now `NON_NORMATIVE_LEGACY_LABELS_ONLY`.

They MUST NOT be interpreted as:

- a requirement to use one particular iPhone;
- a requirement to preserve Safari, IndexedDB, service-worker, or browser-local node state;
- a requirement not to switch devices;
- a requirement that MyKV be local to iOS;
- a requirement that Google Drive access flow through iOS Files;
- a continuity identity;
- a runtime-completion identity.

Canonical architecture is defined by `StegVerse-Labs/.github/control/device-replaceability-invariant.json` and `StegVerse-Labs/.github/docs/DEVICE_REPLACEABILITY_INVARIANT_MIRROR_HANDOFF.md`.

## Canonical replacement semantics

```text
ANY AUTHORIZED USER DEVICE
-> provider-neutral MyKV/KV resolution from configured provider(s)
-> canonical continuity reconstruction from KV + retained receipts
-> WorkerCoordinator claim/fence where required
-> Interlock/InTr governed admission
-> bounded ephemeral execution/signing with no device-unique continuity
-> TV/TVC provider and credential execution
-> exact receipts
-> Master Records reconstruction
```

The user device is an interchangeable access/transport endpoint. Google Drive, iCloud, or another configured provider remains the KV storage provider independently of which device is used.

Replacing the device MUST NOT invalidate already-authentic TASK-2026-0011 G7/fence7 evidence and MUST NOT require replay of already-authentic transitions solely because the device changed.

## Retained authentic evidence

The following evidence remains valid historical provenance:

```text
selected_task_id: TASK-2026-0011
claim_registry_generation: 7
claim_observation.state: CLAIM_GRANT_OBSERVED
fencing_token: 7
canonical_allocator_receipt.state: ALLOCATION_COMPLETE
node journal sequence: 67
journal replay: PASS
```

Earlier observations were made on an iPhone and may retain device-specific labels. Those labels identify where the observation happened; they do not bind future continuation to that device.

The most recent observed legacy-path failure was:

```text
current_iphone_testflight_bootstrap:current_iphone_signing:Load failed
```

That observation proves a failure inside the legacy device-local signing path. It does not justify another iPhone-specific repair and does not make iOS the required execution substrate.

## Existing source artifacts

Existing source files and symbols such as:

```text
current-iphone-testflight-bootstrap.js
current-iphone-testflight-signing-action.js
CURRENT_IPHONE_TESTFLIGHT_SIGNING
task0011-same-device-kv-recovery.html
```

may remain temporarily for compatibility and provenance. Their names are implementation labels only. Any future mutation to this Goal must preserve the global replaceable-device invariant and must not reintroduce device-bound continuity.

## Authority boundary

- WorkerCoordinator/canonical allocator: claim/fence authority.
- Interlock/InTr: governed transition/admission authority.
- KV/MyKV: provider-neutral continuity boundary.
- SKAP + TV/TVC: credential/provider authority.
- Master Records: observed-reality/reconstruction authority.
- Site: projection/rendezvous only.
- User device: no continuity, credential, transition, or reconstruction authority.

## Current first unresolved predicate

The old predicate name:

```text
TESTFLIGHT_CURRENT_IPHONE_RUNTIME_OBSERVED
```

is superseded by:

```text
TESTFLIGHT_AUTHORIZED_USER_DEVICE_RUNTIME_OBSERVED
```

The old name may appear in immutable evidence and historical records only.

## Current implementation requirement

Do not ask the user to preserve or continue on one particular iPhone. Do not ask the user to keep Safari/IndexedDB/service-worker state as canonical continuity.

The next source-side work is to rebind TASK-2026-0011 to provider-neutral MyKV/KV reconstruction and an interchangeable authorized-device endpoint. No device-local retry is required before that architectural rebind.

## Manual work

None.
