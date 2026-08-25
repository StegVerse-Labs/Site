# Generic Login / KV Projection Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `feat/generic-login-recovery-links-491`
State: INTR_KV_PROJECTION_SOURCE_COMPLETE_VALIDATION_PENDING

## Goal

Provide a bounded Site surface that follows a Google-style identity-proof model: the Site requests credential verification through InTr and consumes a short-lived assertion instead of retrieving a stored password. Only an admitted identity assertion exposes the KnowledgeVault directory projection. SKAP remains locked behind a separate step-up assertion and a distinct KV→SKAP boundary.

## Authority topology

```text
cloud hosting control plane
  != user identity authority

Browser / Device
  -> Site presentation
  -> InTr identity verification request
  -> identity assertion
  -> KV directory projection
  -> Personal Info transition requests
  -> separate SKAP step-up request
  -> KV -> SKAP InTr boundary
```

Canonical credential topology remains:

```text
Device <-InTr-> KV <-InTr-> SKAP Vault
```

The Site is a presentation/assertion-consumer surface. It is not canonical KV state authority, SKAP custody authority, or cloud credential authority.

## Identity assertion contract

`assets/kv-ui/intr-auth-client.js`

Production contract:

```text
VERIFY_ACCOUNT_LOGIN
-> stegverse.intr.identity-assertion/v1
```

The assertion is audience-bound, short-lived, and must state:

```text
credential_disclosed: false
raw_secret_present: false
authority_effect: ASSERTION_ONLY
```

A real remote InTr verifier is not yet provisioned on this test surface. Default production mode is therefore `NOT_PROVISIONED`, and production authentication fails closed rather than silently adopting test authority.

For deterministic/manual test execution only, `TEST_ONLY_LOCAL_INTR_VERIFIER` verifies browser-local test-account password digests and emits the same assertion shape without returning the stored digest or password to the Site consumer.

## Login / KV projection contract

`generic-login-test.html`

The initial card contains username/password, Forgot Password, and Create Account. The form asks the InTr client for a login assertion. On admitted assertion:

```text
LOGIN_CARD
-> SUCCESS
-> KV_TREE
```

The visible tree currently projects:

```text
Personal Info/
Documents/
Projects/
Research/
Modules/
Shared/
_Vault/SKAP 🔒
```

Unimplemented directories remain disabled rather than implying backing KV state that has not been connected.

## Personal Info contract

Opening `Personal Info/` exposes a bounded editor for:

```text
Name
Email
Text number
Address
```

On this test surface Save produces a secret-free test transition receipt:

```text
schema: stegverse.intr.kv-ui-transition/v1
operation: PERSONAL_INFO_UPDATE
parent_assertion_id: <current admitted identity assertion>
authority_effect: TEST_ONLY_LOCAL_KV_PROJECTION
```

The current browser-local write is not claimed as real KV custody. The production successor must route the same mutation request over InTr into the actual KV and retain the resulting real state-transition receipt.

## SKAP step-up contract

Ordinary account/KV login never unlocks SKAP.

Selecting `_Vault/SKAP` requires a separate validation step and a second assertion:

```text
VERIFY_SKAP_STEP_UP
-> stegverse.intr.step-up-assertion/v1
```

On the test surface, password re-authentication is used only to prove the separate step-up state machine. Production should replace this with the strongest available owner/device proof (for example WebAuthn/passkey-backed verification) without changing the assertion-consumer boundary.

Only after successful step-up does the UI project a SKAP panel. Even then, no stored secret values are returned to the Site. Credential use/disclosure remains separately governed behind the KV→SKAP InTr boundary.

## Account lifecycle

`create-account-test.html` and `forgot-password-test.html` retain the bounded account/recovery lifecycle:

- account creation requires at least one verified Email/Text recovery attribute;
- plaintext passwords are never persisted;
- recovery uses only verified recovery channels;
- password change uses the same Forgot Password algorithm;
- actual email/SMS delivery remains explicitly `TEST_ONLY` until a real transport is attached.

## Cloud-host boundary

Cloud hosting credentialing remains outside user identity/KV/SKAP authority. Infrastructure credentials may authorize deployment/routing of the Site but must never become account, KV, or SKAP credentials, and must never be delivered to browser code.

## Deterministic validation

`scripts/validate_generic_login_test.py` must prove:

- production InTr default is fail-closed `NOT_PROVISIONED`;
- test verifier accepts valid and rejects invalid local test credentials;
- identity assertion contains no raw credential disclosure;
- login assertion replaces the login card with the KV tree projection;
- Personal Info Save produces a transition receipt bound to the identity assertion;
- SKAP remains locked until a separate step-up assertion;
- step-up assertion contains no credential disclosure;
- logout returns to the login card;
- invalid credentials produce FAILED;
- no production InTr runtime, real KV custody, or real SKAP custody is falsely claimed.

Hosted lane: `.github/workflows/generic-login-test-validation.yml`.

## Publication target

After merge and normal Site publication:

```text
https://stegverse.org/generic-login-test.html
https://stegverse.org/create-account-test.html
https://stegverse.org/forgot-password-test.html
```

Publication must be observed before claiming physical manual execution is available.

## Current authority boundary

```text
Site presentation authority: UI ONLY
production identity authority: NOT PROVISIONED
Site credential custody: NONE
real KV authority/custody: NOT CLAIMED
real SKAP authority/custody: NOT CLAIMED
cloud credential authority in browser: NONE
identity assertion consumer: IMPLEMENTED
SKAP step-up assertion consumer: IMPLEMENTED
TEST_ONLY local identity verifier: IMPLEMENTED
```
