# Generic Login / KV Projection Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `feat/generic-login-recovery-links-491`
State: INTR_KV_PROJECTION_WITH_LOGIN_AUDIT_VALIDATION_PENDING

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
  -> Account Info login audit projection
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

## Account Info login-audit contract

The Account Info screen includes an append-only Login History. Every form submission records:

```text
LOGIN_ATTEMPT
-> LOGIN_SUCCESS
```

or:

```text
LOGIN_ATTEMPT
-> LOGIN_FAILED
```

Each audit record uses:

```text
schema: stegverse.intr.login-audit-event/v1
transport_protocol: InTr
account_ref_sha256: sha256:<deterministic account reference>
prior_login_event_hash: <previous event hash or null>
login_event_hash: sha256:<canonical event hash>
secret_plaintext_present: false
credential_material_recorded: false
authority_effect: AUDIT_ONLY
```

`login_event_hash` is designed as the exact searchable/correlation handle for reviewing other evidence tied to that login. Successful records also retain the non-secret `assertion_id` and `assurance_level` when available. Failed records do not invent an assertion.

The audit history must never store the submitted username or password inside an event. The account is correlated through `account_ref_sha256`; each event is chained through `prior_login_event_hash` so missing/reordered/tampered records are detectable by validation.

This browser-local history is still TEST_ONLY projection state. The production successor should append the same event schema through InTr into canonical KV/account audit custody while preserving hash/search semantics.

## Personal Info contract

Opening `Personal Info/` exposes a bounded editor for Name, Email, Text number, and Address. On this test surface Save produces a secret-free test transition receipt bound to the current admitted identity assertion. The current browser-local write is not claimed as real KV custody.

## SKAP step-up contract

Ordinary account/KV login never unlocks SKAP. Selecting `_Vault/SKAP` requires a separate validation step and a second `stegverse.intr.step-up-assertion/v1`. On the test surface, password re-authentication proves the separate state machine only. Production should replace this with the strongest available owner/device proof without changing the assertion-consumer boundary.

## Account lifecycle

`create-account-test.html` and `forgot-password-test.html` retain the bounded account/recovery lifecycle:

- account creation requires at least one verified Email/Text recovery attribute;
- plaintext passwords are never persisted;
- recovery uses only verified recovery channels;
- password change uses the same Forgot Password algorithm;
- actual email/SMS delivery remains explicitly `TEST_ONLY` until a real transport is attached.

## Deterministic validation

`scripts/validate_generic_login_test.py` must prove:

- production InTr default is fail-closed `NOT_PROVISIONED`;
- test verifier accepts valid and rejects invalid local test credentials;
- identity assertion contains no raw credential disclosure;
- successful login appends exact `LOGIN_ATTEMPT -> LOGIN_SUCCESS`;
- subsequent invalid login appends exact `LOGIN_ATTEMPT -> LOGIN_FAILED`;
- all four event hashes recompute from canonical non-secret event bodies;
- every prior-event hash links correctly;
- one deterministic account search hash correlates all records;
- raw username/password are absent from audit records;
- success audit binds assertion ID/assurance and failure does not invent assertion evidence;
- Personal Info Save produces a transition receipt bound to the identity assertion;
- SKAP remains locked until a separate step-up assertion;
- logout returns to the login card;
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
login audit authority: AUDIT_ONLY / TEST_ONLY LOCAL PROJECTION
real KV authority/custody: NOT CLAIMED
real SKAP authority/custody: NOT CLAIMED
cloud credential authority in browser: NONE
identity assertion consumer: IMPLEMENTED
searchable login-event hash chain: IMPLEMENTED / VALIDATION PENDING
SKAP step-up assertion consumer: IMPLEMENTED
TEST_ONLY local identity verifier: IMPLEMENTED
```
