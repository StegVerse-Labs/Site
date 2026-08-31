# Site DEVICE_KV HB-Derived Carrier Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#800`
Branch: `feat/device-kv-hb-carrier-800`
State: ACTIVE_IMPLEMENTATION
Updated: 2026-08-31T08:04:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Migrate the Site portable DEVICE_KV Universal InTr packet to the canonical HB-derived carrier profile without changing Interlock/InTr authority semantics.

## Runtime contract

Upstream runtime profile:
`StegVerse-Labs/.github#619`
`stegverse.intr.hb-derived-carrier-profile/v1`

Packet path:

```text
canonical HB32 anchor + Date.now()
 -> independently derived HB reference
packet_id
 -> SHA-256 first 32 bits modulo 16
 -> H1 phase slot
packet_id + payload_hash + HB reference + phase channel
 -> stegverse.intr.hb-derived-carrier-binding/v1
 -> canonical binding SHA-256
 -> materialization request
 -> Node outbox
 -> DEVICE_KV sync
 -> profiled ingress validates binding
 -> ingress receipt returns carrier evidence
```

## Authority invariant

A valid carrier binding proves only deterministic carrier consistency. It does not grant or imply:
- InTr/Interlock admission;
- execution;
- credential use;
- routing;
- transition;
- receiving;
- provider access;
- KV persistence/readback;
- trusted semantic admission;
- claim/fence/lease;
- consequence authority.

## Claimed surfaces

- `assets/my-kv-portable-direct-source-bridge.js`
- `stegos-node/device-kv-intr-sync.js`
- `scripts/check_device_kv_intr_sync.py`
- `scripts/project_device_kv_intr_sync_target.py`
- `tests/test_device_kv_intr_sync_target_projector.py`
- `tests/test_device_kv_intr_sync.py`
- `docs/DEVICE_KV_HB_DERIVED_CARRIER_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-device-kv-hb-carrier-800-20260831.json`

## Completion boundary

Source completion requires exact deterministic JS/Python contract alignment, receipt validation, exact-head Site validation and merge. Public/live carrier propagation remains separate runtime evidence.
