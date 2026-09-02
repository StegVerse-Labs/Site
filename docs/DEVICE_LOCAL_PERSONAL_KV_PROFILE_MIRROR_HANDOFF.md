# Device-Local Personal KV Profile Mirror Handoff

Repository: StegVerse-Labs/Site
Issue: #923
Branch: main
State: SOURCE_MERGED_RUNTIME_VALIDATION_REQUIRED
Authority effect: NONE
Activation effect: false
Updated: 2026-09-02 14:41 CDT

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

## Source merge reconciliation — 2026-09-02 14:41 CDT

Canonical source implementation is merged through PR #925 at:

```text
a8fa5c49f029431074425c688120c36c0500983c
```

The source lane is complete and exact-head validation passed. Issue #923 and claim `SITE-DEVICE-LOCAL-PERSONAL-PROFILE-923-20260902` remain open solely because runtime completion has not yet been demonstrated on the current registered iPhone.

Required next runtime action is an explicit current-iPhone My KV refresh/reopen. If no resident profile is already present, the owner may explicitly choose `Open existing profile from Files` and select the current Google Drive `KnowledgeVault/_Entities/Self/Personal_Contact_Profile.json`. The legacy iCloud KnowledgeVault is outside this production lane and must not be selected here.

A successful runtime completion requires resident DEVICE_KV admission plus exact readback and subsequent `PROFILE_READ`. Source merge, hosted validation, or Files visibility alone do not satisfy this boundary.

## Current-iPhone runtime defect — 2026-09-02 15:57 CDT

Observed owner-mediated Files picker behavior after PR #925: the canonical 114-byte `Personal_Contact_Profile.json` was visible in the current Google Drive `_Entities/Self` directory but rendered disabled/gray and could not be selected.

Root cause: the Personal Profile fallback picker admitted only `.json,application/json`, while the installed canonical profile is preserved by the KnowledgeVault installation lane as unconverted `text/plain`. iOS Files therefore treated the valid canonical file as outside the picker MIME filter.

Repair: align the Personal Profile picker with the already-working installation-receipt picker and admit `application/json,.json,text/plain`. JSON/schema/secret-boundary validation still occurs after owner selection, so broadening the Files MIME eligibility does not weaken content admission.

This repair is source-only until the current iPhone can select the 114-byte canonical profile and complete DEVICE_KV write + exact readback + `PROFILE_READ`.

## 2026-09-02 reusable form-profile extension

A second device-local record class, `PERSONAL_FORM_PROFILE`, is now source-implemented for `_Entities/Self/Personal_Form_Profile.json`.

My KV now exposes reusable private filing information separately from the existing Personal Contact Profile. The browser bridge, device-local service worker, and sync routing support read/write with exact-readback requirements. The profile may reference a SKAP signing profile but may not contain reusable signing material or automatic signature authority.

Canonical continuation: `docs/MY_KV_PERSONAL_FORM_PROFILE_MIRROR_HANDOFF.md`.

Runtime completion still requires authentic current-iPhone save/readback observation; source mutation is not runtime proof.


## Canonical HB / InTr runtime consolidation — 2026-09-02 16:59 CDT

This lane is a consumer of the shared HB/InTr runtime-observability substrate; it does not own a separate heartbeat, runtime-presence service, dispatcher, WorkerCoordinator, or receipt authority.

Canonical upstream contracts:
- `StegVerse-Labs/.github/docs/HB_DERIVED_INTR_CARRIER_MIRROR_HANDOFF.md`
- `StegVerse-Labs/.github/docs/DEVICE_KV_INTR_SOVEREIGN_OBSERVATION_MIRROR_HANDOFF.md`
- Site shared browser carrier: `assets/hb-intr-carrier.js`
- Site DEVICE_KV transport: `stegos-node/device-kv-intr-sync.js`

The exact unresolved runtime predicate for My KV Step 3 is:

```text
current registered iPhone
-> owner selects canonical Personal_Contact_Profile.json
-> registered Node-bound PERSONAL_CONTACT_PROFILE COMMIT_CANDIDATE admitted
-> resident device-local DEVICE_KV receiver consumes request
-> PROFILE_PERSISTED with exact_readback_verified=true
-> HB-derived response carrier recovered and independently validated
-> subsequent PERSONAL_CONTACT_PROFILE REQUEST consumed
-> PROFILE_READ returned on validated HB-derived carrier
-> UI editing enabled
```

HB supplies deterministic reference/freshness/carrier evidence only. Interlock/InTr supplies admissible movement. Neither HB nor the carrier grants write, credential, route, admission, execution, or transition authority.

The Personal Profile bridge now consumes the same canonical HB-derived result proof already used by the general My KV query bridge: exact response packet recovery, payload hash, receipt binding, carrier authority-effect check, and HB reference/channel observation. No session-local signal format is introduced.

The current iOS Files blocker is separately repaired by removing OS MIME classification as a pre-selection gate. Selection is not admission: JSON/schema/secret checks and DEVICE_KV exact-readback remain mandatory. The fallback asset is cache-busted so Safari cannot retain the prior picker policy.

Runtime completion remains NOT OBSERVED until the current iPhone supplies the machine-produced result above. Source, merge, CI, deployment, HB progression, and handoff state do not satisfy it.
