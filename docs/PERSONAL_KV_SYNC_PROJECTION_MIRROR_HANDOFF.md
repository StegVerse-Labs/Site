# Personal KV Sync Projection Mirror Handoff

Repository: `StegVerse-Labs/Site`
State: ACTIVE_IMPLEMENTATION
Branch: `fix/personal-kv-sync-projection-20260902`
Updated: 2026-09-02
Authority effect: NONE
Activation effect: false

## Observed contradiction

The current iPhone can complete an exact Personal KV write/readback flow and show a successful Personal KV save while the StegOS Node panel still renders:

```text
Last Personal KV Sync: Not yet observed
```

Source inspection identifies the projection gap: the Node page reads metadata key `personal-kv-sync`, but the shared Node continuity API has no writer for that key. Personal KV flows append capability receipts but never update the dedicated non-personal sync marker.

## Goal

Write a privacy-bounded Personal KV sync observation only after an exact DEVICE_KV result is successfully validated.

The marker may contain:

- Node ID;
- operation: read or write;
- profile class;
- resulting state;
- response receipt/hash reference;
- exact-readback flag;
- timestamp;
- authority/credential boundary.

It must contain no Personal KV values, profile fields, credentials, provider identifiers, or authority grants.

## Claimed paths

- `assets/stegverse-node-continuity.js`
- `my-kv.html`
- `assets/my-kv-personal-profile-write-bridge.js`
- `tests/test_site_node_continuity.py`
- `tests/test_my_kv_personal_form_profile_source.py`
- `tests/my-kv-personal-info.test.cjs`
- `docs/PERSONAL_KV_SYNC_PROJECTION_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-personal-kv-sync-projection-20260902.json`

## Release boundary

Release after focused Personal KV/Node continuity tests and current Site orchestration/bootstrap/heartbeat gates pass, merge, and truthful reconciliation. Public re-observation may confirm deployment but must not retain source ownership.
