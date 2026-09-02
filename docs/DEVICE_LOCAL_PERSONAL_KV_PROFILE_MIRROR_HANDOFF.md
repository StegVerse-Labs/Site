# Device-Local Personal KV Profile Mirror Handoff

Repository: StegVerse-Labs/Site
Issue: #923
Branch: feat/device-local-personal-profile-923
State: ACTIVE_IMPLEMENTATION
Authority effect: NONE
Activation effect: false
Updated: 2026-09-02

## Purpose

Complete My KV Step 3 against the already-observed current-iPhone device-local DEVICE_KV runtime.

Current observed state:

```text
Step 2: DONE
DEVICE_KV resident installation verification: PASS
Step 3: FAIL_CLOSED
message: Unable to load your current Personal KV profile.
```

The existing browser profile bridge emits `PERSONAL_CONTACT_PROFILE`, but the current device-local service worker and sync client do not admit that record class.

## Canonical path

```text
_Entities/Self/Personal_Contact_Profile.json
```

## Required device-local contract

Read:

```text
record_class=PERSONAL_CONTACT_PROFILE
operation=REQUEST
response schema=stegverse.device-kv.personal-profile-response/v1
state=PROFILE_READ
```

Write:

```text
record_class=PERSONAL_CONTACT_PROFILE
operation=COMMIT_CANDIDATE
candidate_type=PERSONAL_CONTACT_PROFILE_REPLACE
requested_destination=_Entities/Self/Personal_Contact_Profile.json
response schema=stegverse.device-kv.profile-update-response/v1
state=PROFILE_PERSISTED
exact_readback_verified=true
```

All requests remain bound to the registered Node. No profile field may grant authority or contain credential material.

## Initial population

A device-local KV may not yet contain the canonical profile even when installation receipt verification is complete. The existing owner-mediated Files fallback may therefore seed a validated Personal Contact Profile into the same already-admitted DEVICE_KV portable materialization lane.

This is a one-time owner-controlled content admission, not Google Drive provider access. Provider IDs/tokens are not persisted and fresh cloud observation is not claimed.

## Claimed surfaces

- intr-service-worker.js
- stegos-node/device-kv-intr-sync.js
- assets/my-kv-personal-profile-write-bridge.js
- assets/my-kv-personal-profile-file-fallback.js
- my-kv.html
- tests/test_device_kv_intr_sync.py
- tests/test_site_node_continuity.py
- docs/DEVICE_LOCAL_PERSONAL_KV_PROFILE_MIRROR_HANDOFF.md
- data/session-work-claims.d/site-device-local-personal-profile-923-20260902.json

## Completion boundary

Source completion requires exact-head validation and merge.

Runtime completion requires the current iPhone to either:
1. load an existing resident canonical profile automatically, or
2. owner-select the existing canonical profile once, observe device-local admission, then successfully re-read it from the resident KV.

No source merge is runtime proof.


## Source implementation

Implemented on this branch:

- device-local service worker admits `PERSONAL_CONTACT_PROFILE`;
- read requests return only the exact canonical Personal Contact Profile path;
- write candidates require `PERSONAL_CONTACT_PROFILE_REPLACE` and the exact destination;
- profile JSON is fail-closed validated for schema, collections, authority boundary, and secret-like fields;
- writes replace only the canonical profile row in device-local KV and require byte/hash exact readback before `PROFILE_PERSISTED`;
- sync target discovery routes the profile class to the current-iPhone service worker;
- the owner-mediated Files button can seed a validated existing profile through the live profile bridge and immediately re-read it from resident KV;
- My KV and directory pages use the refreshed local sync cache token.

The source work does not prove that the current Google Drive profile has been selected or that the current iPhone has completed resident profile readback.
