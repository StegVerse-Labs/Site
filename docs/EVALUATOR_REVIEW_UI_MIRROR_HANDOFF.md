# Evaluator Review UI Mirror Handoff

Updated: 2026-08-28

## Source of truth

```text
repository: StegVerse-Labs/Site
issue: #575
branch: feature/evaluator-manifest-review-ui
implementation_state: COMPLETE_VALIDATED_MERGED_PUBLICLY_OBSERVED
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
public Site route for this UI: OBSERVED
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


## Projection sync merge checkpoint — PR #590

```text
issue: Site #589
PR: #590
final pre-merge head: b92b2700742f4b12bca4eb3e95454cf46bb6c406
merge: dd7e6d5685abea6c87429e90e36b1069bd9c9b9d
Evaluator Review UI Source Validation 33222852501: SUCCESS
Site Bootstrap Validate 33222852459: SUCCESS
Site Handoff Orchestrator 33222852526: SUCCESS
Ecosystem Heartbeat Orchestration 33222852590: SUCCESS
My KV Personal Information regression 33222852475: SUCCESS
```

The first PR #590 validation attempt failed only because the new session-work claim omitted required `handoff_revision`. That fail-closed orchestration defect was corrected on head `b92b2700742f4b12bca4eb3e95454cf46bb6c406`; the replacement exact-head validation set passed and the projection sync merged. Current Site projection is now bound to SDK PR #94 v0.2/source blob `2dd0468779975d18ad53dfe400e1d2fcf83650c3`.

Current state: VALIDATED + MERGED + PUBLICLY OBSERVED; authorized review bridge activation NOT CLAIMED; external approval NONE; frozen NO; executed NO; replay/reconstruction/results NONE.


## Public observation verifier implementation

Issue #589 now has a bounded anonymous verifier:

```text
script: scripts/check_evaluator_review_public.py
workflow: .github/workflows/evaluator-review-public-verification.yml
html: https://stegverse.org/evaluator-review.html
projection: https://stegverse.org/data/evaluator-review/cross-framework-current-basis-001.json
authentication: NONE
review action: NONE
authority effect: NONE
activation effect: false
```

The verifier checks HTTP publication separately from source merge. It requires the exact SDK v0.2 source head/blob, DRAFT_PRE_FREEZE, CURRENT_POLICY_BASIS_CHANGED, both controls, no approvals, no freeze, no execution, and no results. It cannot comment, approve, freeze, execute, or activate the review bridge.

State: PUBLICLY_OBSERVED / #589 COMPLETE.


## Public v0.2 observation — COMPLETE

The final Site #589 publication gate is now satisfied by anonymous HTTP observation against the custom domain.

```text
implementation PR: #598
merge: 1d1e5f0535db5a967fc75f8acd92fb2e0a0d0165

pull-request public verifier:
  run: 33228784079
  job: 99037615775
  artifact: 9707771388
  digest: sha256:1943c10453bde430f66e3738730bff240b35d750783aafafb7141834d0b177d5
  result: PASS

main public verifier:
  run: 33228826510
  job: 99037735109
  artifact: 9707785332
  digest: sha256:27a64910d7a137313cc790c6a4df69ae6977b1a3ccaaad6d96cf18c3ae470354
  result: PASS

observed:
  https://stegverse.org/evaluator-review.html
  https://stegverse.org/data/evaluator-review/cross-framework-current-basis-001.json

observed projection:
  SDK head: c9b8935309e69d3a6f70e4ad4ef5dd55fb8a9aac
  source blob: 2dd0468779975d18ad53dfe400e1d2fcf83650c3
  state: DRAFT_PRE_FREEZE
  approval: false
  frozen: false
  execution: NOT_RUN
  results: absent
  authority effect: NONE
  activation effect: false
```

Site #589 is COMPLETE_VALIDATED_MERGED_PUBLICLY_OBSERVED.

This closes publication observation only. It does not activate `StegVerseEvaluatorReviewBridge`, create approval/freeze authority, execute the test, produce results, or establish replay/reconstruction evidence.


## Frozen v0.4 projection synchronization — 2026-08-30

Issue: #695.

The public evaluator-review source was stale at the previously observed v0.2 draft while the SDK comparison lane had already advanced through the externally approved and owner-frozen v0.4 identity. This synchronization updates the presentation layer only; it does not execute the test or create runtime authority.

Authoritative projection:

```text
vector schema: stegverse.cross-framework-current-basis-vector.v0.4
SDK exact source commit: 5a21fc6bdf4a94cfd6c4a4f369a1ba8b86721909
Git blob SHA-1: 59d818a15fc7be732c97dae7d2174d8cfe9a7bab
raw manifest SHA-256: 07a08496c21b31f70f6f45ef731aa5f6b2522a6fc8f67f2d0a4c2b6fceda7a3f
external exact-revision approval: APPROVED_FOR_HASH_FREEZE
StegVerse owner freeze: FROZEN
effective freeze source: separate hash-bound attestation
embedded DRAFT_PRE_FREEZE: preserved snapshot content
common execution window: OPEN
StegVerse authentic execution: NOT_RUN
results/custody/replay/reconstruction: PENDING
```

The UI now reads `manifest.input.comparison_input` before the legacy `input_data` shape and renders the v0.4 successor determination together with the neutral S1 observed inputs. The public verifier now requires the exact v0.4 frozen identity, post-observation receipt semantics, no pre-asserted architecture-native currentness, and an unexecuted/no-results state until authentic resident evidence is available.

The Site remains a non-authorizing read/presentation surface. Publication of FROZEN/OPEN state is not execution.


## Frozen v0.4 public observation completion — 2026-08-30

Site #695 is complete.

```text
implementation PR: #700
merge: 8a13182c7630eab1efa613cde45229b4de27a975
Evaluator Review UI Source Validation: 33294500131 SUCCESS
Site Handoff Orchestrator: 33294500130 SUCCESS
Ecosystem Heartbeat: 33294500135 SUCCESS
Evaluator Review Public Verification source mode: 33294500155 SUCCESS
Site Bootstrap: 33294500132 SUCCESS

post-merge public verifier:
  run: 33294523117
  attempt: 2
  job: 99211964506
  result: PASS

observed state:
  vector: stegverse.cross-framework-current-basis-vector.v0.4
  frozen manifest SHA-256: 07a08496c21b31f70f6f45ef731aa5f6b2522a6fc8f67f2d0a4c2b6fceda7a3f
  frozen manifest Git blob: 59d818a15fc7be732c97dae7d2174d8cfe9a7bab
  effective state: FROZEN
  embedded snapshot label: DRAFT_PRE_FREEZE
  execution window: OPEN
  authentic execution: NOT_RUN
  results: absent
  authority effect: NONE
```

The first post-merge attempt ran before publication propagation and correctly failed against the stale v0.2 projection. Attempt 2 observed the exact v0.4 projection and passed. This closes Site synchronization/publication only. Runtime execution, S1 observation, the post-observation transition receipt, Master Records custody, replay, reconstruction, and result publication remain owned by the sovereign experiment execution lane.


## Exact v0.4 StegVerse result projection — 2026-08-31

Issue: #785.

The exact frozen v0.4 manifest has now completed one independent StegVerse SDK-style execution. Site is updated only as a verifier/presentation entry point; it does not rerun or reinterpret the canonical evaluator.

```text
manifest SHA-256: 07a08496c21b31f70f6f45ef731aa5f6b2522a6fc8f67f2d0a4c2b6fceda7a3f
StegVerse execution: COMPLETE
StegVerse result: DENY
reason: execution.authority_stale
S1 observed: true
manifest receipt: MR-C554125F385C65B7AA8303C10F076AD471CF864CF1DB2CC472FF771D8260F796
transition receipt hash: 91410d8539e8225a6de77e6f299afafb5d813572c4fc2292a351ca56c0bc7c18
Master Records custody: RECORDED
replay: RECORDED
reconstruction: RECORDED
counterpart result: NOT_RUN
comparison: AWAITING_COUNTERPART
```

The Site comparison table now exposes the observed StegVerse semantics and leaves every counterpart cell PENDING until an independently produced counterpart result is supplied. This preserves the frozen experiment's cross-architecture isolation rule.
