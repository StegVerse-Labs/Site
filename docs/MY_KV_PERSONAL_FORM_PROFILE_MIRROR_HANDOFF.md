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
