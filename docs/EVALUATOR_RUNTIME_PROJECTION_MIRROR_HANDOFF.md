# Evaluator Runtime Projection Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`
Issue: `#660`
Replacement PR: `#708`
Credential authority: `TV/TVC`
Authority effect: `NONE`
Activation effect: `false`

## Source of truth

This file is the bounded continuation source for `SITE-EVALUATOR-RUNTIME-PROJECTION-660`. It is subordinate to the root `SITE_MIRROR_HANDOFF.md` and the broader evaluator transport contract in `docs/EVALUATOR_REVIEW_INTR_CONNECTOR_MIRROR_HANDOFF.md`.

The former implementation PR #661 passed its exact historical validation head but diverged from current `main` by more than one hundred commits. It must not be merged over newer evaluator/SV002 connector behavior. PR #708 rematerializes only this bounded capability on current main.

## Goal

The Site evaluator page must discover a consequential evaluator InTr connector only from a fresh, independently projected shared-Gateway observation, while remaining blocked by default and preserving every newer request-class route already present in the shared connector.

```text
canonical instruction/source
-> replaceable Site projection
-> blocked runtime-projection record
-> fresh TVC Gateway observation when one actually exists
-> strict Site validation
-> Interlock Connector discovery
-> evaluator READ_REVIEW via InTr
```

Site does not invent a production hostname, acquire credentials, grant authority, mint receipts, or establish runtime readiness.

## Upstream observer

Canonical upstream source is now complete:

```text
repository: StegVerse-Labs/TVC
issue: #250 CLOSED_COMPLETE
PR: #251
validated head: 8e7285545a66708725d3ae8711be2daaa0ae3b0c
validation run: 33297615527 SUCCESS
merge: cceb5ef3ea79cd02cc040dd1a1655527d93ee466
post-merge handoff reconciliation: PR #261 / dd60726eea29a261b1a570173fa20f94097430f9
```

That is source capability only. No public evaluator route is inferred from the merge.

## Current Site implementation

```text
assets/evaluator-intr-connector.js
  -> preserves current injected EVALUATOR_REVIEW endpoint support
  -> preserves current SV002_PUBLIC_OBSERVE / sv002_observe_endpoint routing
  -> loads data/evaluator-review/runtime-projection.json for evaluator discovery
  -> validates schema, freshness, SHA-256 bindings, HTTPS paths, same origin, receiver READY, TV/TVC, Gateway NONE
  -> keeps SV002-only injected connector available when evaluator projection is blocked

assets/evaluator-review.js
  -> awaits StegVerseInterlockConnectorReady before deciding whether READ_REVIEW uses InTr or static public fallback

data/evaluator-review/runtime-projection.json
  -> BLOCKED by default
  -> endpoint/readiness null
  -> active=false
  -> no fabricated observation timestamps/digests

tests/evaluator-intr-runtime-projection.test.cjs
  -> valid fresh projection -> READY
  -> blocked/stale/tampered/cross-origin projection -> NOT_PROVISIONED
  -> explicit regression proof that SV002-only routing survives evaluator projection reconciliation

scripts/check_evaluator_review_ui.py
  -> requires projection, discovery promise, digest/freshness boundary tokens and SV002 preservation
```

## Collision boundary

The current shared connector already serves more than the evaluator lane. Therefore this implementation MUST preserve:

```text
request_class=SV002_PUBLIC_OBSERVE
sv002_observe_endpoint
fail-closed request-class endpoint selection
current InTr headers and payload hashing
```

The stale #661 connector patch did not contain the later SV002 behavior and is superseded. PR #708 reconciles the two instead of reverting current main.

## Validation gate

Required exact-head Site evidence before merge:

```text
Evaluator Review UI Source Validation: PASS
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
```

Earlier #708 head `337288a7049a902bd960674151ae49763f3d4162` passed all four, but further acceptance edits require a new exact-head PASS before merge.

## Runtime boundary

Still NOT OBSERVED and not satisfied by source/CI/merge:

```text
public production Gateway/WebPKI evaluator route
public evaluator readiness runtime_receiver_ready=true
fresh TVC route observation from that public runtime
Site VERIFIED/active runtime projection derived from that observation
public deployed Site -> Gateway -> InTr evaluator round trip
resident sovereign production activation
review/freeze/execute authority
```

No second user-operated machine is required by this source path. Authentic runtime evidence remains owned by the existing sovereign runtime/shared-Gateway lifecycle.

## Completion accounting

```text
current-main source rematerialization: IN_PROGRESS_PR_708
known scoped scaffolding/stubs: 0
TVC observer source: COMPLETE_MERGED_VALIDATED
Site runtime projection source: IMPLEMENTED_PENDING_FINAL_EXACT_HEAD_VALIDATION
public evaluator route: NOT_OBSERVED
runtime activation: NOT_CLAIMED
```
