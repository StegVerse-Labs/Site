# Site HB Carrier Channel Reconciliation Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#814`
Branch: `fix/site-hb-carrier-channel-814`
State: ACTIVE_IMPLEMENTATION
Updated: 2026-08-31T09:52:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Align the shared Site HB-derived InTr carrier binding with the canonical exact-byte carrier in `StegVerse-Labs/.github/heartbeat_runtime/intr_derived_carrier.py`.

## Canonical channel rule

```text
payload_hash = sha256:<64 hex>
slot = int(first 64 bits of payload SHA-256, 16) mod 16
channel = HB:H1:P<slot>
```

This replaces the prior browser-only `SHA256(packet_id)` slot rule. `packet_id` remains part of the immutable carrier binding identity, but does not select the channel.

## Claimed surfaces

- `assets/hb-intr-carrier.js`
- `scripts/project_device_kv_intr_sync_target.py`
- `scripts/project_sv002_intr_sync_target.py`
- `scripts/check_device_kv_intr_sync.py`
- `tests/test_device_kv_intr_sync.py`
- `tests/test_device_kv_intr_sync_target_projector.py`
- `tests/test_sv002_intr_sync_target_projector.py`
- `docs/SHARED_HB_INTR_CARRIER_CLIENT_MIRROR_HANDOFF.md`
- `docs/SITE_HB_CARRIER_CHANNEL_RECONCILIATION_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-hb-carrier-channel-814-20260831.json`

## Completion boundary

Exact browser/runtime channel equivalence, profile expectation updates, exact-head validation, merge, and claim terminalization.
