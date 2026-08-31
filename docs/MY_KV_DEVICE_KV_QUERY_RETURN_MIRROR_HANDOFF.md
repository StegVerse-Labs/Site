# My KV DEVICE_KV Query/Return Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#863`
Branch: `feat/my-kv-device-kv-query-863`
State: ACTIVE_IMPLEMENTATION
Updated: 2026-08-31T13:24:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Replace the missing My KV directory/connection-health browser bridges with a canonical DEVICE_KV query/return implementation.

## Upstream

- StegOS #145 / PR #146 / merge `ba1e43dbadaef367c32c7a354fe2857746f6f1cd`
- CVK #164 / PR #165 / merge `f91e465bbf7196557005a8112a6c70c8712f9aaf`
- CVK #166 / PR #167 / merge `70b19663305e63ac6016af9b56848e91aa89b77c`
- .github #676 / PR #677 / merge `677ee5b65f6c8a7d4ced85e66e34850400675282`

## Browser chain

```text
My KV directory/health request
 -> current registered Node state
 -> kv.interlock.request.v1 + selector
 -> generated buildIntent("device-kv", ...)
 -> shared HB buildBinding(...)
 -> generated buildMaterializationRequest(..., {kv_request})
 -> Node outbox
 -> DEVICE_KV sync
 -> admitted resident query
 -> CVK read-only projection
 -> resident HB-derived response signal
 -> /intr/device-kv/result
 -> browser validates exact result/request/node binding
 -> browser recovers exact response bytes from HB-derived carrier
 -> StegVerseKVDirectoryBridge / StegVerseKVConnectionHealthBridge
```

## Runtime target

The fail-closed target gains `result_url`.

- unavailable target: `ingress_url=null`, `result_url=null`
- observed conforming target: exact same origin
  - `/intr/materialization`
  - `/intr/device-kv/result`

Both paths are projected only from authentic HTTPS `/intr/profile` evidence.

## Invariants

- exact current StegOS generated artifact + manifest only;
- query payload hash is canonical `kv_request`;
- authority ref is bound to exact current Node id;
- selector is directory id + exact canonical path only;
- query carries no provider credentials;
- result lookup cannot execute or re-read KV state;
- result response must be recovered from the exact canonical HB-derived carrier signal;
- response/request/materialization/node hashes must match;
- Site stores no private KV directory response as repository or durable public state;
- file bytes are not returned in directory listing;
- missing target/result/bridge fails closed.

## Claimed surfaces

- `assets/generated/site-browser-intr-connectors.js`
- `assets/generated/site-browser-intr-connectors.manifest.json`
- `assets/hb-intr-carrier.js`
- `assets/my-kv-device-kv-query-bridge.js`
- `stegos-node/device-kv-intr-sync.js`
- `stegos-node/device-kv-intr-sync-target.json`
- `scripts/project_device_kv_intr_sync_target.py`
- `my-kv-directory.html`
- `my-kv.html`
- `tests/canonical-generated-intr.test.cjs`
- `tests/test_device_kv_intr_sync.py`
- `tests/test_device_kv_intr_sync_target_projector.py`
- `tests/test_site_hb_intr_carrier_migration.py`
- `tests/my-kv-directory.test.cjs`
- `docs/MY_KV_DEVICE_KV_QUERY_RETURN_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-my-kv-device-kv-query-863-20260831.json`

## Completion boundary

Exact artifact copy, target/result projection, browser query/return bridge, exact HB response recovery, deterministic tests/checkers, exact-head Site validation, merge, claim terminalization. Runtime activation remains separately dependent on an authentically observed public sovereign profiled ingress and a real resident private KV root.
