# Account Recovery Test Mirror Handoff

Issue: StegVerse-Labs/Site#491 follow-up
State: SOURCE_IMPLEMENTATION_IN_PROGRESS

## Goal

Replace decorative login options with a bounded account lifecycle test:

create account -> bind recovery attribute -> verify recovery attribute -> login -> forgot password -> recovery challenge -> reset password -> login with new password.

## Recovery attributes

Supported test schema:
- EMAIL
- SMS

An account record may carry one or both, but only a verified attribute is eligible for password recovery.

## Security/test boundary

This is a browser-local lifecycle proof, not production identity authority. Plaintext passwords are never persisted. Account state contains password digest plus normalized recovery metadata and verification state. Recovery codes are short-lived test challenges and are never authority for KV/SKAP/TV/TVC.

Actual email/SMS sending is a separate transport boundary. Until a real delivery transport is attached, the page must label delivery TEST_ONLY and expose the challenge only in the bounded test delivery panel; it must never claim an email or SMS was sent.
