# Generic Login Test Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `feat/generic-login-verification-491`
State: SOURCE_IMPLEMENTED_VALIDATION_PENDING

## Goal

Provide one bounded public test page that a person can use to observe an explicit login state transition and that automation can drive through the same submit handler.

## Test fixture

```text
username: test
password: stegverse
```

These values are intentionally non-secret test fixtures. They grant no identity, session, KV, SKAP, TV/TVC, release, publication, provider, or runtime authority.

## Page contract

`generic-login-test.html`

Top banner states:

```text
LOGIN
SUCCESS
FAILED
```

The credential form is centered in the page. The fixture values are displayed below with copy controls.

Manual valid submission:

```text
test / stegverse -> SUCCESS
```

Manual invalid submission:

```text
any mismatch -> FAILED
```

The password field is cleared after every submission.

## Automated contract

Automation uses the identical `form` submit event handler:

```text
/generic-login-test.html?auto=success -> fills valid fixture -> form.requestSubmit() -> SUCCESS
/generic-login-test.html?auto=failure -> fills invalid fixture -> form.requestSubmit() -> FAILED
```

The page also exposes the non-authorizing test hook:

```text
window.__STEGVERSE_LOGIN_TEST__.getState()
window.__STEGVERSE_LOGIN_TEST__.submit(username, password)
```

The hook calls the same `form.requestSubmit()` path and does not bypass credential evaluation.

## Deterministic validation

`scripts/validate_generic_login_test.py` executes the actual inline page JavaScript with Node under a minimal browser shim and requires:

- initial `LOGIN`;
- manual valid -> `SUCCESS`;
- manual invalid -> `FAILED`;
- `?auto=success` -> `SUCCESS`;
- `?auto=failure` -> `FAILED`;
- password cleared after submission;
- same submit handler for manual and automated paths;
- no localStorage, sessionStorage, cookie, network request, or TVC credential behavior.

Hosted lane: `.github/workflows/generic-login-test-validation.yml`.

## Publication target

After merge and normal Site publication, expected public path:

```text
https://stegverse.org/generic-login-test.html
```

Publication must be observed before claiming physical manual verification is available.

## Authority boundary

```text
authentication authority: NONE_TEST_FIXTURE_ONLY
credential custody: NONE
KV authority: NONE
SKAP authority: NONE
TV/TVC authority: NONE
network/provider authentication: NONE
real session minted: FALSE
```

This page proves UI/login-path mechanics only. It does not prove a real account, SKAP credential, or production authentication boundary.
