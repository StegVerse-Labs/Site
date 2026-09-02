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
- `StegVerse-Labs/.github/org-kernel/runtime_observability.py`

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
