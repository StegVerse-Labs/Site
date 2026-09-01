# Portable iPhone KV Installation Bridge Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#779`
Branch: `fix/portable-iphone-kv-bridge-779`
State: ACTIVE_IMPLEMENTATION
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
