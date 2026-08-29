# Evaluator Review UI Mirror Handoff

Updated: 2026-08-28

## Source of truth

```text
repository: StegVerse-Labs/Site
issue: #575
branch: feature/evaluator-manifest-review-ui
implementation_state: VALIDATED_MERGED_PUBLICATION_VERIFY_PENDING
claim: SITE-EVALUATOR-MANIFEST-REVIEW-575-20260828
source evaluator contract: StegVerse-org/StegVerse-SDK
current draft: SDK PR #94 / inspection/examples/cross-framework-current-basis-request.draft.json
current draft state: DRAFT_PRE_FREEZE
```

This handoff is the task-specific continuation record. Live repository state and the SDK manifest contract supersede stale conversation claims.

## Architectural boundary

The Site surface is a human review client over the existing evaluator-neutral SDK manifest lane. It does not create a test engine, evaluator-specific route, governance engine, credential authority, signing authority, custody authority, freeze authority, or execution authority.

```text
TV/TVC = credential/secret/token authority
SDK = evaluator-neutral declarative manifest and governed execution contract
Site = public human review/presentation client
Master Records = custody/reconstruction where applicable
GitHub = source/provenance only
```

Consequential actions fail closed unless an authorized `window.StegVerseEvaluatorReviewBridge` is injected by the StegVerse runtime. Public static hosting may render the review projection but cannot manufacture comments, approvals, freezes, executions, or evidence.

## Implemented surfaces

Target files:
- `evaluator-review.html`
- `assets/evaluator-review.js`
- `data/evaluator-review/cross-framework-current-basis-001.json`
- `docs/EVALUATOR_REVIEW_API_CONTRACT.md`
- `tests/evaluator-review-ui.test.cjs`
- `scripts/check_evaluator_review_ui.py`
- `data/tasks/SITE-EVALUATOR-MANIFEST-REVIEW-575.json`

## Required behavior

- plain-language test summary and visual state vector
- generic manifest rendering
- exact draft review hash
- expected-observation vs decision-input separation
- section-scoped discussion presentation
- request-changes / approval actions with exact revision+hash binding
- two-party same-version/hash readiness evaluation
- freeze eligibility gate
- immutable frozen presentation when canonical state says FROZEN
- raw manifest view/copy/export
- evidence/execution/result projections
- revision history and advanced provenance
- mobile-first layout without core horizontal scrolling

## Current truth

```text
SDK PR #94: OPEN / DRAFT
manifest: DRAFT_PRE_FREEZE
external approval: NOT CLAIMED
StegVerse approval: NOT CLAIMED
frozen: NO
executed: NO
results available: NO
public Site route for this UI: NOT YET OBSERVED
```

The fixture may display PENDING/NOT RUN states only. Any computed SHA-256 before freeze is labeled as a review hash, not a frozen hash.

## Completion gates

1. source files implemented;
2. deterministic JS tests pass;
3. static contract checker passes;
4. Site claim/orchestration validation passes;
5. integration merged;
6. public URL publication separately observed;
7. runtime bridge integration remains a separate activation gate if no canonical bridge is presently available.

Do not promote IMPLEMENTED/VALIDATED/MERGED into DEPLOYED/ACTIVATED/OBSERVED without corresponding evidence.


## Implementation checkpoint — 2026-08-28

Implemented on the feature branch:
- generic public review projection loader;
- canonicalized manifest SHA-256 review hash;
- exact-version/hash approval matching;
- change-request blocker handling;
- freeze eligibility gate;
- bridge-only consequential actions;
- mobile-first page with sticky review controls;
- human-readable summary/vector/inputs/criteria/evidence;
- raw manifest copy/export;
- revision/provenance/results projection;
- deterministic Node logic tests and static acceptance checker.

Validation, merge, deployment, activation, and public observation remain distinct later states.


## Exact-head source validation

Validated head before evidence-record update: `6e35e19ed97a99a87cd24b70d15c016195289107`.

```text
Evaluator Review UI Source Validation 33172838593: SUCCESS
Site Bootstrap Validate 33172838696: SUCCESS
Site Handoff Orchestrator 33172838595: SUCCESS
Ecosystem Heartbeat Orchestration 33172838603: SUCCESS
My KV Personal Information regression 33172838598: SUCCESS
```

The evaluator validator performed an anonymous exact-public-SHA fetch. Static UX acceptance, deterministic approval/hash/freeze logic, and authority-boundary checks all passed. GitHub Actions remained source validation only.


## Merge checkpoint

```text
PR: #576
merge commit: cc35fa2083204183a2f7d78f1b692978c9b5a544
merged_at: 2026-08-28T12:53:17Z
final pre-merge head: 3612ce26d1618962f6558bac8b075e951def1b61
Evaluator Review UI Source Validation 33172910874: SUCCESS
Site Bootstrap Validate 33172910999: SUCCESS
Site Handoff Orchestrator 33172910822: SUCCESS
Ecosystem Heartbeat Orchestration 33172910858: SUCCESS
My KV Personal Information regression 33172910875: SUCCESS
```

State is now VALIDATED + MERGED. Public publication/route observation, authorized review-bridge activation, external approval, freeze, execution, replay, reconstruction, and results remain separately unclaimed.


## SDK draft revision reconciliation — 2026-08-28

SDK PR #94 advanced after external evaluator feedback.

```text
SDK PR #94 head: c9b8935309e69d3a6f70e4ad4ef5dd55fb8a9aac
manifest blob: 2dd0468779975d18ad53dfe400e1d2fcf83650c3
vector schema: stegverse.cross-framework-current-basis-vector.v0.2
SDK source validation run 33196691745: SUCCESS
manifest state: DRAFT_PRE_FREEZE
approval: NONE
freeze: NO
execution: NOT RUN
results: NONE
```

Material correction: the primary vector now states CURRENT_POLICY_BASIS_CHANGED rather than combining change with invalidation; invalidation is not asserted as an input conclusion; S1 standing is independently determined; VALID_CONTINUITY_CONTROL and KNOWN_INVALIDATION_CONTROL are explicit, and known invalidation requires frozen invalidation evidence. Site issue #589 owns exact projection synchronization and separate public-route observation. Site #575 remains completed source implementation and is not reopened.
