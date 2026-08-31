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
