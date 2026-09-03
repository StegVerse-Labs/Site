# Device-Local Personal KV Profile Mirror Handoff

Repository: StegVerse-Labs/Site
Issue: #923
Branch: main
State: RELEASED_COMPLETE / PERSONAL_CONTACT_PROFILE_RUNTIME_COMPLETE
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


## Runtime observation — 2026-09-02 17:06 CDT

Authentic current-iPhone observation advanced the lane beyond the Files-picker boundary:

```text
owner selection: reached
profile file validation: passed far enough to invoke DEVICE_KV
DEVICE_KV ingress: DENIED
HTTP status: 400
exact denial predicate: not surfaced by current client
PROFILE_PERSISTED: NOT OBSERVED
PROFILE_READ: NOT OBSERVED
```

This is not a generic HB/runtime-presence failure. The current request reached the DEVICE_KV ingress transition and was denied there. The exact missing runtime predicate is therefore **successful Interlock/InTr admission of the Node-bound PERSONAL_CONTACT_PROFILE materialization request**.

The shared `stegos-node/device-kv-intr-sync.js` already receives the service-worker JSON denial body, but previously discarded its `reason` and exposed only HTTP 400. That prevented the authentic runtime observation from identifying the failed admission invariant. The shared transport now surfaces the exact receiver denial reason. This is reusable DEVICE_KV observability work, not a session-local signal mechanism.

The Personal Profile bridge also consumes the existing shared HB-derived response-carrier contract on successful result delivery; HB supplies reference/freshness/carrier proof only and does not override the denied ingress.

Next runtime attempt must preserve the exact denial reason if admission still fails. No source/CI/merge outcome may be counted as satisfying `PROFILE_PERSISTED` or `PROFILE_READ`.


## Current-iPhone observation and legacy-profile compatibility repair — 2026-09-02 19:05 CDT

Direct owner-provided current-iPhone screenshots establish two distinct UI observations:

```text
KnowledgeVault installation verified from the current resident KV root over DEVICE_KV.
No receipt selection was required.

Reusable form information loaded from Personal KV.
```

The same current page still showed:

```text
Unable to load your current Personal KV profile.
Live editing remains locked; owner-mediated Files fallback is available.
```

These observations must not be collapsed. They show that installation-status DEVICE_KV and the new Personal Form Profile read path reached their success UI states, while the Personal Contact Profile path still failed.

Live connected-KV inspection identified the exact compatibility defect rather than a missing DEVICE_KV implementation:

`KnowledgeVault/_Entities/Self/Personal_Contact_Profile.json` is an older sparse-but-valid v1 shape containing only:
- schema;
- email_addresses=[];
- authority_effect=NONE.

The current Site DEVICE_KV validator required the later optional/default fields `phone_numbers` and `postal_addresses` to be physically present, so the older installed canonical file failed before browser editing could unlock.

Repair on current `main`:
- `intr-service-worker.js` now normalizes omitted optional v1 fields to canonical defaults before validation/read response;
- sparse reads remain read-only compatibility normalization and expose `legacy_shape_normalized=true`;
- writes canonicalize the full current shape before exact-readback persistence;
- `assets/my-kv-personal-info.js` performs the same client-side normalization before validation;
- regression coverage added to `tests/my-kv-personal-info.test.cjs`.

This is a compatibility repair, not a schema-version invention and not provider mutation authority. The existing Google Drive file is not rewritten merely by loading it. A later owner save through DEVICE_KV will persist the current full shape in the device-local KV path; durable provider writeback remains separately governed.

The screenshot success message for Reusable Form Information is direct current-device UI observation of the form-profile read success path, but durable reconstruction still requires the retained DEVICE_KV/Node receipt hash chain. No receipt hash is inferred from the screenshot alone.


## Source-ownership/runtime-validation split — 2026-09-02

The Personal KV source implementation is already merged, and current-device observation has established that the reusable form-profile read path reaches its success UI while the Personal Contact Profile path has an identified compatibility/runtime-validation remainder.

The remaining write/exact-readback/subsequent-read predicates are now retained as **non-owning runtime validation**. They no longer reserve `intr-service-worker.js` or the shared DEVICE_KV transport files against unrelated canonical profile integration.

This is not a completion claim for the missing Personal Contact Profile write/readback predicates. It is an ownership correction: pending runtime validation may remain open without turning into a permanent source lock or requiring another device.


## Current-iPhone Personal Contact Profile runtime completion — 2026-09-02 20:53 CDT

Authentic current-iPhone owner observation now satisfies the Personal Contact Profile runtime boundary.

Observed sequence:

```text
owner-mediated Files picker opened
-> current KnowledgeVault _Entities/Self/Personal_Contact_Profile.json selected
-> file accepted by Site
-> profileBridge.saveProfile()
-> registered Node-bound DEVICE_KV write path
-> PROFILE_PERSISTED
-> exact_readback_verified=true required by bridge
-> profileBridge.loadProfile()
-> PROFILE_READ
-> resident profile client validation
-> editing enabled
```

Exact success UI observed:

```text
Personal KV profile was admitted through DEVICE_KV and verified from the resident device-local KV.
```

This success string is emitted only after the write promise resolves, the immediate resident re-read resolves, the returned profile validates, fallback mode is disabled, and live editing is enabled. Therefore this current-device observation legitimately establishes the Step-3 Personal Contact Profile completion predicate.

Established now:

```text
PERSONAL_CONTACT_PROFILE_OWNER_SELECTION_OBSERVED = true
PERSONAL_CONTACT_PROFILE_WRITE_CONSUMED = true
PERSONAL_CONTACT_PROFILE_EXACT_READBACK_VERIFIED = true
PERSONAL_CONTACT_PROFILE_READ_OBSERVED = true
PERSONAL_CONTACT_PROFILE_EDITING_ENABLED = true
STEP_3_PERSONAL_CONTACT_PROFILE = DONE
```

This does not by itself complete the separate Personal Form Profile write/exact-readback/SKAP predicates tracked in `docs/MY_KV_PERSONAL_FORM_PROFILE_MIRROR_HANDOFF.md`.

Issue #923 may be terminalized for its original Personal Contact Profile read/write objective. No provider writeback, cloud mutation, credential authority, or broader runtime activation is inferred.


## Claim terminalization — 2026-09-03

Claim `SITE-DEVICE-LOCAL-PERSONAL-PROFILE-923-20260902` is now terminalized as `RELEASED_COMPLETE`.

The original #923 Personal Contact Profile objective was already satisfied by the canonical current-iPhone observation recorded above:

```text
owner selection observed
DEVICE_KV write consumed
PROFILE_PERSISTED
exact_readback_verified=true
subsequent PROFILE_READ
resident validation passed
editing enabled
```

The separate Personal Form Profile lane remains non-owning continuation work under `docs/MY_KV_PERSONAL_FORM_PROFILE_MIRROR_HANDOFF.md`; it does not retain #923 source ownership or reopen the completed Personal Contact Profile path.
