# My KV Multi-Email Personal Information Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#558`  
Claim: `SITE-MY-KV-MULTI-EMAIL-558-20260828`  
Branch: `claim/site-my-kv-multi-email-558`  
State: CLAIM_ADMITTED / IMPLEMENTATION_ACTIVE  
Authority effect: NONE  
Activation effect: false

## Purpose

Project the canonical KnowledgeVault multi-email personal-information model into a bounded Site / My KV interaction surface.

Canonical upstream authority remains:

- `StegVerse-Labs/continuity-vault-kit/KV_EMAIL_INGRESS_MIRROR_HANDOFF.md`
- `schemas/kv-personal-contact-profile.schema.json`
- `runtime/personal_contact_profile.py`
- `runtime/email_continuity.py`

Site does not redefine the profile schema, mailbox mapping authority, provider registry, SKAP credential custody, Interlock admission, or email-ingress governance.

## Required UX

```text
My KV
 -> Personal Information
 -> Email Addresses
 -> + Add email
 -> label / optional primary
 -> optional Connect this email
 -> canonical KV mapping bridge
 -> Complete setup in SKAP Vault
 -> provider session verification
 -> governed ingress
```

## Invariants

1. More than one email address is allowed.
2. Duplicate addresses are rejected case-insensitively.
3. At most one address may be primary.
4. Primary status is preference/display metadata only.
5. Adding an address does not grant mailbox access.
6. Each address independently opts into email continuity.
7. Raw passwords, tokens, app passwords, refresh tokens, or provider secrets are never accepted by this Site surface.
8. `Connect this email` must fail closed when the canonical KV mapping bridge is absent.
9. Site may display canonical mapping state returned by the bridge but may not fabricate mapped/session state.
10. SKAP Vault is the credential destination after successful mapping.
11. Site source readiness does not imply provider activation or email monitoring.

## Planned files

- `my-kv.html`
- `assets/my-kv-personal-info.js`
- `tests/my-kv-personal-info.test.cjs`
- `scripts/check_my_kv_personal_info.py`
- `docs/MY_KV_MULTI_EMAIL_MIRROR_HANDOFF.md`
- `SITE_MIRROR_HANDOFF.md`

## Current boundary

The connected KnowledgeVault profile template is already installed and parity-validated upstream. This Site lane owns only the user-facing projection and canonical-bridge handoff semantics.

## Completion gates

- claim/orchestration validation PASS;
- deterministic profile/UI contract tests PASS;
- static Site checker PASS;
- no secret-bearing input fields or persistence;
- absent KV bridge fails closed without changing connection state;
- successful synthetic bridge mapping shows `MAPPED_CREDENTIAL_REQUIRED` and SKAP completion guidance;
- Site mirror handoff reconciled;
- PR merged.

Live mailbox/provider/SKAP execution remains a separate owner-authorized activation boundary.
