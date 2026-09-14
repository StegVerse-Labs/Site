# KV TestFlight Projection Entry Mirror Handoff

Updated: 2026-09-14

Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical issue: `StegVerse-Labs/.github#1299`
COSV: `50000010100000`
Canonical KV producer: `StegVerse-Labs/continuity-vault-kit@47c363611210b7501cbb50abce768cfe0911057f`
Canonical StegOS consumer: `StegVerse-Labs/StegOS@19e2ea02a16bd703767aafcd47e71f5ec5efe3cf`
Original implementation PR: `StegVerse-Labs/Site#1178` merged at `3da593a61a536a625fcea4a26df8d1f491f00b44`
Status: `ACTIVE / AUTHENTIC CURRENT-IPHONE DEVICE-KV RECOVERY REACHED WRITE-ONCE COLLISION / BOUNDED INVALID-RECEIPT REPLACEMENT REPAIR IN VALIDATION`

## Purpose

Bridge the already-running current-iPhone Device -> KV Universal InTr admission path into the merged KV-bound TestFlight projection contract without adding a second InTr service worker, scheduler, KV authority, credential path, browser identity root, or public private-state store.

## Existing runtime reused

This slice reuses the existing Site primitives:

```text
assets/stegverse-node-continuity.js
assets/generated/site-browser-intr-connectors.js
assets/hb-intr-carrier.js
stegos-node/device-kv-intr-sync.js
intr-service-worker.js
assets/my-kv-portable-installation-bridge.js
```

The root-scoped `intr-service-worker.js` already admits `MY_KV_INSTALLATION_STATUS` requests through the current-device Device -> KV InTr path and produces `stegverse.device-kv-intr-materialization-ingress/v1` with `state=INGRESS_ADMITTED`, exact request validation, write-once persistence, exact Node/Interlock/outbox binding, TV/TVC credential authority, and no execution/claim authority.

No new record class or root service worker is introduced. The adapter uses the already-supported installation-status record class but gives the request the exact purpose `CURRENT_IPHONE_TESTFLIGHT_SIGNING`, so the purpose is inside the exact request hash admitted by InTr.

## Current-iPhone observations

The published route was opened on the current iPhone.

Earlier observations established:

1. ChatGPT in-app browser storage produced `Failed to execute 'transaction' on 'IDBDatabase': One of the specified object stores was not found.` This is browser-partition-local and is not promoted as Safari runtime truth.
2. Safari reached the governed projection path and failed closed with `FAIL_CLOSED: resident KV installation not verified`.

On 2026-09-14 the canonical Google Drive KnowledgeVault `_System/installation.receipt.json` was selected through the existing `Admit Existing KV Installation Receipt` control. The same-device Device->KV path then failed closed with the exact authentic result:

```text
DEVICE_KV ingress rejected trigger: HTTP 400: write_once_collision:kv_files
```

This proves the current resident `kv_files` store already contains an entry occupying the canonical `_System/installation.receipt.json` key. Because the immediately preceding installation-status projection was `KV_INSTALLATION_NOT_VERIFIED`, that resident row is not accepted by the current canonical installation validator. The failure is therefore narrower than generic runtime absence: an invalid or stale write-once canonical installation row prevents admission of the validated canonical receipt.

## Recovery implementation

The pre-existing recovery control continues to reuse `StegVerseKVInstallationBridge`, the generated Device->KV InTr connector, Node outbox, HB-derived carrier, and Device-KV sync. No second service worker, scheduler, dispatcher, transport, credential route, or execution plane is introduced.

Branch: `fix/kv-installation-write-once-recovery-20260914`

A bounded extension is loaded on the existing root `intr-service-worker.js` after the retained base worker and before the existing Canonical Work extension:

```text
intr-service-worker-base-v1.js
-> intr-kv-installation-recovery-extension.js
-> intr-canonical-work-extension.js
```

The extension overrides only the existing `persistPortable` function and only for the exact canonical payload `_System/installation.receipt.json`.

Recovery rules:

```text
incoming receipt must satisfy existing canonical installation validator
existing row absent -> normal write-once admission
existing row byte/metadata-equivalent -> idempotent reuse
existing row valid but different -> preserve write_once_collision
existing row invalid + incoming row valid -> replace only that invalid canonical installation row
all other portable payloads -> unchanged retained persistPortable path
```

The replacement records the hash of the displaced invalid resident row. Credential material remains absent, provider authorization remains false, and `authority_effect=NONE`.

Focused regression coverage is in:

```text
tests/kv-testflight-projection-recovery.test.cjs
tests/kv-installation-write-once-recovery.test.cjs
```

## Authority boundary

This repair does not mint InTr admission. It operates inside the existing root-scoped Device-KV InTr runtime and only after the incoming receipt passes the already-existing canonical receipt validator. It does not make Site the KV owner, credential authority, signing authority, WorkerCoordinator, Master Records authority, or TestFlight/runtime truth source.

`HB` remains carrier/observability only. `TV/TVC` remains credential authority. Interlock/InTr remains admission authority. KV remains continuity boundary. Browser capability observation grants no authority.

## Runtime truth

Authentic current-iPhone execution has now reached the Device-KV materialization write-once boundary. No successful replacement, purpose-bound projection, signing, native Build Upload, TestFlight install, retained StegOS runtime, Master Records reconstruction, or global convergence measurement is claimed from this source repair.

The next authentic runtime predicate is:

```text
CANONICAL_KV_INSTALLATION_RECEIPT_RECOVERY_ADMITTED_ON_CURRENT_IPHONE
```

After deployment, the same established iPhone must retry `Admit Existing KV Installation Receipt` using the same canonical `_System/installation.receipt.json`. Only an observed successful Device-KV admission and automatic purpose-bound retry may advance the chain.

## Next

1. Validate and merge the bounded write-once recovery repair.
2. Publish the updated root service worker and recovery extension through the existing Site publication path.
3. Re-open the same published route on the established current iPhone without clearing Safari/site/KV/node continuity.
4. Select the canonical `_System/installation.receipt.json` through the existing recovery control.
5. Require observed bounded replacement/idempotent admission and automatic retry of `CURRENT_IPHONE_TESTFLIGHT_SIGNING`.
6. Continue only from authentic projection/signing/TVC/TestFlight/runtime/Master Records evidence.
7. Return to the existing frozen global runtime measurement only after those prerequisites are actually observed.
