# Generic Login Test Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `feat/generic-login-recovery-links-491`
State: SOURCE_HARDENED_VALIDATION_PENDING

## Goal

Provide one bounded public test page that a person can use to observe an explicit login state transition and that automation can drive through the same submit handler, without publishing the plaintext accepted fixture on the page.

## Manual operator fixture

The accepted manual fixture is supplied out-of-band to the test operator. The published page contains only SHA-256 digests of the accepted username/password values; it does not display them, include copy controls, or auto-fill them from query parameters.

These fixture values grant no identity, session, KV, SKAP, TV/TVC, release, publication, provider, or runtime authority.

## Page contract

`generic-login-test.html`

Top banner states:

```text
LOGIN
SUCCESS
FAILED
```

The centered form order is:

```text
Username
Password
Forgot password?     Create account
Submit
```

`Forgot password?` and `Create account` are bounded, non-authorizing option links for this verification surface. They do not recover or create a real account and do not alter login status.

The password field is cleared after every submission.

## Automated contract

Automation supplies candidate values externally through:

```text
await window.__STEGVERSE_LOGIN_TEST__.submit(username, password)
```

The hook fills the same username/password inputs and invokes `form.requestSubmit()`. It does not bypass the form submit handler or credential evaluation.

The previous `?auto=success` / `?auto=failure` auto-fill shortcuts are removed so the published page does not contain or reconstruct the accepted plaintext fixture.

## Deterministic validation

`scripts/validate_generic_login_test.py` executes the page's actual inline JavaScript with Node under a minimal browser shim. CI substitutes a fresh runtime-only synthetic credential digest pair into the extracted script, then requires:

- initial `LOGIN`;
- externally supplied valid candidate -> `SUCCESS`;
- externally supplied invalid candidate -> `FAILED`;
- both paths traverse the same form submit handler;
- password cleared after submission;
- Forgot password/Create account option events are reachable without changing login authority;
- no visible fixture block/copy controls;
- no query-string credential auto-fill shortcut;
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
forgot-password authority: NONE
create-account authority: NONE
```

This page proves UI/login-path mechanics only. It does not prove a real account, SKAP credential, or production authentication boundary.
