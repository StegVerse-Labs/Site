# Portable iPhone KV Installation Bridge Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#779`
Branch: `fix/portable-iphone-kv-bridge-779`
State: RELEASED_COMPLETE
Authority effect: NONE
Activation effect: false
Updated: 2026-08-30

## Purpose

Remove the My KV Step 2 browser dead-end when no live resident KV bridge is injected, without pretending that source merge or a public page is a live KV runtime.

The fallback uses the owner's existing canonical KnowledgeVault installation receipt as a portable proof surface on iPhone:

```text
My KV
 -> owner selects _System/installation.receipt.json from Files / cloud provider
 -> browser validates canonical receipt fields fail-closed
 -> provider-specific identifiers are discarded
 -> bounded installation proof is retained in this browser
 -> existing StegVerseKVInstallationBridge contract reports verified binding
```

A separately activated resident `StegVerseKVInstallationBridge` always takes precedence.

## Invariants

1. No provider credential is requested or stored.
2. No Google Drive folder/file ID is persisted by the Site fallback.
3. The selected receipt must claim full recursive template parity = VALIDATED.
4. The receipt must have `authority_effect=NONE` and `activation_effect=false`.
5. The browser fallback does not activate Interlock/InTr, SKAP, provider sessions, or KV mutation authority.
6. Step 5 re-selects/revalidates a receipt instead of treating prior local state as current cloud observation.
7. TV/TVC remains credential authority.
8. No GitHub runtime authority is introduced.

## Claimed surfaces

- `assets/my-kv-portable-installation-bridge.js`
- `my-kv.html`
- `tests/test_site_node_continuity.py`
- `docs/MY_KV_PORTABLE_INSTALLATION_BRIDGE_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-my-kv-portable-installation-bridge-779-20260830.json`

## Current boundary

This lane fixes installation/verification reachability on an iPhone using an already-existing canonical KV receipt. It does not solve direct-source provider ingestion. Email/media direct-source activation remains a separate TV/TVC + SKAP + resident InTr runtime gate.


## 2026-08-31 iPhone settlement and continuity restoration

Public iPhone observation showed Node registration reconstructed correctly while Step 2 remained `Not done`.

Two bounded defects were corrected:

1. the installation receipt picker previously settled only on `change`; iOS Safari can return from the native picker without firing `change` after cancellation;
2. a previously validated bounded installation proof in the same browser was not reconstructed into the registered Node capability chain if Step 2 lacked a Node receipt.

The portable installation bridge now settles through selection, native cancel, focus return, or hidden -> visible return. Cancellation is fail-closed and records no installation state.

The bridge also exposes `existingInstallation()`, derived only from the already-validated privacy-bounded local proof. My KV may use that to restore Step 2 into the existing registered Node continuity chain.

This restoration means only:

```text
a canonical installation receipt was previously validated in this browser
+ the bounded proof still passes local proof validation
+ this browser currently has a registered StegVerse Node
-> restore Step 2 completion receipt to the Node capability chain
```

It does **not** mean the cloud destination was freshly observed. The restored result explicitly carries:

```text
reused_prior_validated_proof = true
current_cloud_observation = false
resident_intr_activation_observed = false
authority_effect = NONE
```

Step 5 remains the fresh owner-selected verification boundary and does not reuse the old proof as current cloud evidence.


## 2026-09-02 device-local canonical receipt admission

The 12:19 -05:00 current-iPhone observation proved that the repaired DEVICE_KV path now reaches the resident device-local KV and returns the bounded `KV_INSTALLATION_NOT_VERIFIED` result. That is authentic evidence that the Node-bound query/return path is functioning; the remaining reason Step 2 is not complete is that the device-local resident KV does not yet contain `_System/installation.receipt.json`.

Issue #908 extends the existing owner-selected receipt fallback rather than creating a second installation mechanism. After the selected receipt passes the existing canonical receipt validation, the bridge now packages that exact canonical receipt as an owner-controlled, credential-free portable DEVICE_KV payload:

```text
directory_id=system
canonical_path=_System
file=installation.receipt.json
credential_requirement=NONE
authority_effect=NONE
```

The request is queued through the registered StegVerse Node, transported through the existing DEVICE_KV materialization lane, and synchronized through the existing device-local InTr receiver. Only after authentic local/network ingress observation is the bounded local proof marked with `device_local_kv_materialization_observed=true`.

This performs a deliberate owner-authorized device-local KV mutation through an already-admitted capability; it grants no new mutation authority, provider authority, credential authority, or cloud-observation claim. Step 5 remains separate.


## 2026-09-02 13:39 -05:00 iOS Files picker settlement repair

Current-iPhone observation showed the canonical `installation.receipt.json` visible in the Files picker, but returning to My KV produced `No installation receipt selected. Nothing changed.`

The receipt picker had an iOS race: the native `cancel`/focus/visibility return signals could settle the promise before Safari finished populating `input.files` and delivering `change`. The bridge now treats native cancel as a return signal instead of an immediate final cancellation, rechecks `input.files`, and uses a 2.5 second bounded settlement window. A real `change` still accepts immediately. If no file appears after the bounded window, cancellation remains fail-closed.

The My KV page now uses a new explicit cache token for the portable installation bridge so Safari cannot continue executing the pre-repair picker logic.


## 2026-09-02 13:44 -05:00 current-iPhone completion

Current-iPhone observation after PR #914 showed Step 2 as `DONE ✓` with the exact message:

```text
KnowledgeVault installation receipt was admitted through DEVICE_KV and verified from the resident device-local KV.
```

This satisfies the remaining runtime predicate for issue #908 and `SITE-DEVICE-LOCAL-INSTALLATION-RECEIPT-908-20260902`:

- the owner selected the current Google Drive KnowledgeVault receipt dated 2026-08-28;
- the iOS picker returned the selected file correctly;
- the canonical receipt passed validation;
- the receipt was materialized into the resident device-local KV through DEVICE_KV;
- a subsequent live installation-status query returned verified state;
- Step 2 was recorded complete in the Node continuity chain.

The older iCloud KnowledgeVault from approximately 2026-05-20 is explicitly **not** treated as equivalent to the current Google Drive installation. It is reserved as a separate non-destructive upgrade/reinstall/migration test candidate.


## Release reconciliation — 2026-09-02

The canonical claim `SITE-MY-KV-PORTABLE-INSTALLATION-BRIDGE-779-20260830` is already `RELEASED_COMPLETE`.

```text
pull_request: #780
release_commit: ead230513bfdb809f05ea2ea0c7d656d49877b7a
archive_eligible: true
```

The owner-selected installation-receipt fallback is released. It does not assert current provider connectivity or current device-local runtime activity.
