# Evaluator Review API Contract

## Purpose

The evaluator review page is a non-authorizing client over the published StegVerse SDK evaluator-manifest lane. It may render public review data without credentials. Any consequential state transition requires the canonical runtime to inject `window.StegVerseEvaluatorReviewBridge`.

## Read model

The bridge MAY implement:

```js
await StegVerseEvaluatorReviewBridge.loadReview({ testId, source })
```

Return shape:

```json
{
  "review_schema": "stegverse.evaluator-review.v1",
  "test": { "id": "...", "title": "...", "version": 4, "state": "DRAFT" },
  "manifest": {},
  "approvals": [],
  "comments": [],
  "evidence": [],
  "executions": {},
  "results": null,
  "history": []
}
```

A static same-origin JSON projection may be used for PUBLIC READ. Static projection is evidence presentation only and grants no write authority.

## Consequential operations

The bridge MAY implement:

```js
comment({ testId, section, category, body, revision, manifestHash })
requestChanges({ testId, reason, section, revision, manifestHash })
approve({ testId, revision, manifestHash, attestation: "TEST_SPECIFICATION_ONLY" })
freeze({ testId, revision, manifestHash })
```

Every operation must return a canonical updated review model or a fail-closed error.

### Required invariants

- approval binds reviewer identity + exact revision + exact manifest SHA-256 + timestamp;
- evaluator identity is never a governance decision input;
- expected observation is never a governance decision input;
- any manifest mutation invalidates approvals for freeze readiness;
- freeze is unavailable unless all required approvals match the current revision/hash, no blocking change request remains, and canonical validation is PASS;
- frozen artifact is immutable for execution; amendment creates a new draft/version;
- Site never generates canonical freeze receipts, execution receipts, custody receipts, replay evidence, or reconstruction evidence;
- TV/TVC remains the only credential/secret/token authority;
- replay/reconstruction never re-executes the original consequence.

## Access modes

```text
PUBLIC_READ
INVITED_REVIEWER
AUTHENTICATED_APPROVER
```

The bridge, not static Site JavaScript, decides authenticated role and permitted actions. Missing bridge capability must be rendered as unavailable rather than simulated.

## Hashing

The client computes a deterministic review SHA-256 over canonicalized JSON for comparison and approval confirmation. A hash is labeled FROZEN only when the canonical review model reports state `FROZEN` and supplies the canonical frozen hash.
