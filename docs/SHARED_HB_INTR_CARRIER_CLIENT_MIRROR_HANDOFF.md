# Shared Site HB-Derived InTr Carrier Client Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#803`
Branch: `refactor/shared-hb-intr-carrier-803`
State: ACTIVE_IMPLEMENTATION
Updated: 2026-08-31T08:15:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Extract the merged DEVICE_KV HB-derived carrier implementation into one reusable browser client so every Site InTr lane can consume the same canonical runtime carrier contract without copy/paste drift.

## Canonical upstream contract

`StegVerse-Labs/.github#619` / PR #620
`stegverse.intr.hb-derived-carrier-profile/v1`
`stegverse.intr.hb-derived-carrier-binding/v1`

## Shared browser contract

`assets/hb-intr-carrier.js` must provide:

- canonical HB32 anchor;
- 10 ms / 100 Hz OSCILLATOR_ONLY derivation;
- reversible HB Base36 identifier;
- deterministic 16-slot H1 channel selection from SHA-256(packet_id);
- canonical JSON SHA-256 binding;
- packet/payload binding;
- all carrier authority implications false;
- no network fetch;
- no credentials;
- no runtime/route/admission authority.

## First migrated consumer

`assets/my-kv-portable-direct-source-bridge.js` uses the shared module for DEVICE_KV materializations.

## Claimed surfaces

- `assets/hb-intr-carrier.js`
- `assets/my-kv-portable-direct-source-bridge.js`
- `my-kv-directory.html`
- `tests/test_device_kv_intr_sync.py`
- `scripts/check_device_kv_intr_sync.py`
- `docs/SHARED_HB_INTR_CARRIER_CLIENT_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-shared-hb-intr-carrier-803-20260831.json`

## Completion boundary

Source completion requires exact contract-preserving refactor, validation, and merge. No live carrier propagation, route activation, or downstream admission state is inferred from refactoring.
