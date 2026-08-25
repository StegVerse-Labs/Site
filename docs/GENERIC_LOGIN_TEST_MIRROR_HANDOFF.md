# Generic Login Test Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `feat/generic-login-recovery-links-491`
State: ACCOUNT_LIFECYCLE_SOURCE_COMPLETE_VALIDATION_PENDING

## Goal

Provide one bounded public account lifecycle that proves account creation, verified recovery attributes, login success/failure, post-login account management, password recovery/reset, and automated traversal of the same login submit handler without publishing plaintext accepted credentials.

## Login contract

`generic-login-test.html`

Top banner states:

```text
LOGIN
SUCCESS
FAILED
```

The login form is:

```text
Username
Password
Forgot password?     Create account
Submit
```

Plaintext passwords are never persisted. Created test accounts persist browser-locally as password digests plus verified recovery attributes.

## Successful login contract

On `SUCCESS`, the login card is replaced entirely by an account card:

```text
Successful Login

Email         <verified value or Not set>     Change
Text number   <verified value or Not set>     Change
Password      ••••••••                         Change

Log out
```

Email and Text changes remain on the account card. A proposed new value does not replace the current value until its TEST_ONLY verification challenge succeeds. A future real delivery adapter must preserve this same verify-before-replace transition.

Password `Change` intentionally routes to `forgot-password-test.html?username=<current-user>` and therefore uses the same recovery/reset algorithm as `Forgot password?`; there is no separate password-change authority path.

## Create account contract

`create-account-test.html`

Account creation collects:

```text
username
password
email       optional
text number optional
```

At least one recovery attribute is required. Every supplied recovery attribute must be verified before the account is saved. If both Email and Text are supplied, both are verified sequentially.

Persisted account fields are bounded to:

```text
passwordDigest
email
sms
emailVerified
smsVerified
```

No plaintext password is persisted.

## Forgot password / password change contract

`forgot-password-test.html`

The reset path:

```text
identify username
→ enumerate only verified Email/SMS recovery methods
→ select recovery method
→ issue one-time challenge
→ verify challenge
→ permit new password
→ replace passwordDigest
→ old password fails; new password succeeds
```

When entered from the post-login Password `Change` action, the current username is supplied in the URL and the same recovery page/algorithm is used.

## Delivery boundary

Email/SMS state transitions are implemented, but message delivery remains explicitly `TEST_ONLY`. Until a real email or SMS transport is connected, the challenge is displayed in-page and no claim is made that a message was sent.

Real transport integration must preserve:

```text
verified account recovery attribute
→ actual delivery attempt
→ delivery evidence
→ challenge verification
→ bounded account transition
```

Transport success must never be inferred from challenge generation alone.

## Automated contract

Automation supplies candidate values externally through:

```text
await window.__STEGVERSE_LOGIN_TEST__.submit(username, password)
```

The hook fills the real inputs and invokes `form.requestSubmit()`. It never bypasses the page's credential evaluator.

The automation API also exposes the current view:

```text
window.__STEGVERSE_LOGIN_TEST__.getView()
```

Expected transitions:

```text
initial                    LOGIN_CARD
valid created-account login -> SUCCESS + ACCOUNT_CARD
log out                    LOGIN_CARD
invalid login              FAILED + LOGIN_CARD
```

## Deterministic validation

`scripts/validate_generic_login_test.py` must prove on the exact source:

- all three lifecycle pages exist;
- no visible/copyable accepted credential fixture is published;
- a runtime-only synthetic created account logs in successfully;
- successful login replaces the login card with the account card;
- verified Email and Text values render on the account card;
- Email and Text change actions exist and require new-value verification;
- Password change routes through the same Forgot Password algorithm;
- Forgot Password supports verified EMAIL and SMS selection;
- account creation requires at least one verified recovery attribute and supports both;
- password is cleared after login submission;
- logout returns to the login card;
- invalid credentials produce FAILED;
- no real email/SMS delivery is claimed.

Hosted lane: `.github/workflows/generic-login-test-validation.yml`.

## Publication target

After merge and normal Site publication:

```text
https://stegverse.org/generic-login-test.html
https://stegverse.org/create-account-test.html
https://stegverse.org/forgot-password-test.html
```

Publication must be observed before claiming physical manual lifecycle verification is available.

## Authority boundary

```text
scope: TEST ACCOUNT LIFECYCLE ONLY
production identity authority: NONE
KV authority: NONE
SKAP authority: NONE
TV/TVC authority: NONE
real email authority: NONE
real SMS authority: NONE
production account/session authority: NONE
password plaintext persistence: FALSE
```

This surface proves account/recovery mechanics. It does not yet claim production identity, real communication delivery, KV/SKAP custody, or production authentication authority.
