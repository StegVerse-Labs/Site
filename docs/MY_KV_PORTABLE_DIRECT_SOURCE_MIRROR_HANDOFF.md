# Portable Owner-Controlled Direct-Source Staging Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#782`
Branch: `fix/portable-direct-source-782`
State: ACTIVE_IMPLEMENTATION
Authority effect: NONE
Activation effect: false
Updated: 2026-08-30

## Purpose

Remove the My KV directory dead-end when no live SKAP/provider direct-source bridge is injected, while preserving the canonical distinction between local staging and admitted KV persistence.

Portable fallback path:

```text
owner selects files from iPhone Files / device-controlled storage
 -> browser hashes exact bytes
 -> exact bytes staged in browser IndexedDB
 -> canonical DEVICE_SYSTEM -> KV InTr materialization request
 -> existing StegVerse Node outbox
 -> QUEUED_FOR_KV_ADMISSION
 -> resident DEVICE<->KV InTr admission/readback still required
```

A separately activated `StegVerseKVDirectSourceBridge` always takes precedence.

## Invariants

1. Portable fallback is only for owner-controlled file sources with credential requirement NONE.
2. Credentialed providers still require SKAP_VAULT.
3. Staging does not claim canonical KV persistence.
4. Staging does not claim provider-session activation.
5. Exact bytes remain local to the browser until canonical InTr delivery.
6. The existing Node outbox owns durable local transport continuity.
7. No NON-TV/TVC credential or GitHub runtime authority is introduced.
8. UI must clearly distinguish `QUEUED_FOR_KV_ADMISSION` from `KV_LISTED`.

## Claimed surfaces

- `assets/my-kv-portable-direct-source-bridge.js`
- `assets/my-kv-directory.js`
- `my-kv-directory.html`
- `tests/my-kv-directory.test.cjs`
- `scripts/check_my_kv_directory.py`
- `docs/MY_KV_PORTABLE_DIRECT_SOURCE_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-my-kv-portable-direct-source-782-20260830.json`

## Current boundary

This lane gives the current iPhone a lawful local source-staging path. It does not replace live Gmail/Outlook/iCloud provider activation, SKAP, resident KV admission, or private-KV readback.
