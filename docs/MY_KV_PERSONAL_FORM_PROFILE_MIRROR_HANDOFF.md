# My KV Personal Form Profile Mirror Handoff

Repository: StegVerse-Labs/Site
Updated: 2026-09-02
State: SOURCE_IMPLEMENTED_RUNTIME_VALIDATION_REQUIRED
Authority effect: NONE
Activation effect: false

## Goal

Make repeated personal/business filing information enterable once from My KV on the current device and persist it to the user's Personal KnowledgeVault.

Canonical KV record:
`_Entities/Self/Personal_Form_Profile.json`

Canonical schema owner:
`StegVerse-Labs/continuity-vault-kit/schemas/personal-form-profile.schema.json`

## Implemented source

- My KV Step 3 now includes Reusable Form Information.
- TVC Unique ID and SSN/ITIN may be entered as private KV facts.
- default organizer, registered agent, effective-on-filing preference, and accounting-year close month are supported.
- a SKAP e-signature reference may be stored; reusable signature material itself is prohibited from ordinary KV.
- device-local DEVICE_KV admits `PERSONAL_FORM_PROFILE` read/write.
- writes are exact-path replacement candidates with exact-readback requirement.
- current-device sync routes `PERSONAL_FORM_PROFILE` to the resident device-local receiver.
- browser bridge fails closed when the resident receiver is unavailable.

## SKAP boundary

The profile may contain only:
`skap://signing/<profile-id>`

It may never contain reusable signature image/key material and may never set automatic signature application.

A signing profile reference is not signing authorization.

## Runtime completion

Requires current-iPhone observation of:
1. Personal Form Profile save;
2. exact readback receipt;
3. later profile load;
4. SKAP Vault signing profile setup through an authentic SKAP runtime, separately.

Source merge/availability is not runtime proof.


## 2026-09-02 canonical HB runtime consolidation

This lane is now a consumer of the shared StegVerse-Labs HB Runtime Presence / Resident Observability Contract rather than an independent runtime-signal implementation.

Shared owner:
- `StegVerse-Labs/.github/docs/HB_RUNTIME_PRESENCE_RESIDENT_OBSERVABILITY_MIRROR_HANDOFF.md`
- `StegVerse-Labs/.github/management/HB_RUNTIME_PRESENCE_RESIDENT_OBSERVABILITY_CONTRACT.json`
- `StegVerse-Labs/.github/heartbeat_runtime/runtime_presence_projection.py`
- `StegVerse-Labs/.github/scripts/project_hb_runtime_presence.py`
- canonical merge: `6358375c81fedb579cb6fcac59946268ea485ebb`

Site binding:
- `data/my-kv-runtime-observability-binding.json`

Shared-consumer registry:
- `StegVerse-Labs/.github/control/runtime-observability-consumers/site-my-kv-personal-form-profile.json`

No new heartbeat, scheduler, worker coordinator, carrier, or runtime authority was introduced.

Current runtime predicates remain distinct:
- Personal Form Profile write consumed;
- exact DEVICE_KV readback verified;
- later Personal Form Profile read observed;
- SKAP signing-profile custody observed.

The existing current-iPhone service worker already emits HB-bound DEVICE_KV InTr ingress evidence and the profile update/read response classes. Therefore the missing signal is not a new source mechanism; it is authentic current-device execution evidence.

The e-signature source boundary remains `skap://signing/<profile-id>` reference-only in KV. TVC's current credential-model semantic-expansion freeze prevents creating a generalized signing-key/signature manager from this Site lane. Authentic signing-profile custody must be admitted by TV/TVC through the existing SKAP/InTr architecture.

Source tests installed:
- `tests/my-kv-personal-form-profile.test.cjs`
- `tests/test_my_kv_personal_form_profile_source.py`

No hosted workflow run was exposed for these latest source commits at inspection time; runtime completion is not claimed.

## 2026-09-02 post-consolidation integration closure

Additional source integration completed after the shared runtime contract merge:

- the connected owner KnowledgeVault now contains exact `_Entities/Self/Personal_Form_Profile.json`;
- continuity-vault-kit bounded Google Drive materialization scope now includes that path;
- the canonical `.github` Personal Profile DEVICE_KV extension now handles both `PERSONAL_CONTACT_PROFILE` and `PERSONAL_FORM_PROFILE` rather than introducing a second DEVICE_KV runtime;
- Site read responses now include the persisted profile hash;
- the My KV form bridge exposes detailed readback evidence;
- one Save action now requires `PROFILE_PERSISTED`, exact readback, an immediate subsequent `PROFILE_READ` with the same profile hash, and appends non-personal Node continuity receipts for write/read evidence.

No authentic current-iPhone execution has yet produced those receipts in this session. Source support is developed; runtime observation remains open.

Automatic writeback from a temporary read-only Google Drive provider materialization to the cloud provider is not claimed. Current provider binding is `READ_ONLY_MATERIALIZATION`. Any provider write capability is a separate governed operation and must not be inferred from device-local KV persistence.

Public deployment of the latest Site source was not independently observed in this pass.


## Current-iPhone direct UI observation — 2026-09-02 19:05 CDT

Owner-provided current-iPhone screenshot directly observed:

```text
Reusable form information loaded from Personal KV.
```

This success string is emitted only after the browser Personal Form Profile bridge returns a successful `PROFILE_READ` result and the profile passes client validation. It is therefore legitimate UI/runtime observation of the form-profile read path on the current device.

It is not yet retained reconstruction evidence because the screenshot does not expose the response receipt hash/profile hash/Node evidence chain. The predicate is therefore split:

```text
PERSONAL_FORM_PROFILE_READ_UI_OBSERVED = true
PERSONAL_FORM_PROFILE_READ_RETAINED_RECEIPT_PROVEN = false
PERSONAL_FORM_PROFILE_WRITE_CONSUMED = false
PERSONAL_FORM_PROFILE_EXACT_READBACK_VERIFIED = false
```

No write/save runtime is inferred from the read observation.
