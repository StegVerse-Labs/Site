# HIL TV/TVC Authority Mirror Handoff

Updated: 2026-07-31
Repository: `StegVerse-Labs/Site`

## Decision

Site and its deployment runtime may not store, resolve, receive, log, export, or use GitHub credentials or equivalent provider authority for HIL submission processing.

All protected values and execution authority belong exclusively to `StegVerse-Labs/TV` and `StegVerse-Labs/TVC`.

## Implemented Site boundary

`api/hil/upload.js` now:

1. validates the participant PDF and required confirmations;
2. calculates the PDF SHA-256;
3. creates a five-minute, single-submission capability request containing only non-secret metadata;
4. binds the request to `StegVerse-Labs/Site` and `hil-direct-ingress-worker.yml`;
5. forwards the PDF and capability request to `https://tvc.stegverse.org/api/hil/ingress`;
6. never reads `HIL_GITHUB_TOKEN`, `GITHUB_TOKEN`, or any equivalent credential;
7. returns the TVC receipt to the participant-facing receipt flow.

## Concurrent-submission boundary

Each participant receives unique submission, receipt, nonce, source-branch, issue, workflow-run, review-branch, PR, and artifact identities. Site does not serialize unrelated submissions.

## Remaining activation dependency

The TVC ingress must be deployed at `tvc.stegverse.org/api/hil/ingress` with its protected authority resolved only inside TV/TVC. Until that route is live, Site must fail closed and must not fall back to a Site, Vercel, browser, or participant credential.

## Non-claims

This handoff does not claim that the TVC route is deployed, that a protected value exists, or that an end-to-end participant upload has passed.

## Archive readiness

The secret-governance correction is repository-resident. Future continuation must read this file with `docs/HIL_SITE_MIRROR_HANDOFF.md`, `StegVerse-Labs/TV/docs/TV_MIRROR_HANDOFF.md`, and `StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md`.
