# Humans as the Interoperability Layer — Site Mirror Handoff

Updated: 2026-08-15
Repository: `StegVerse-Labs/Site`
Canonical branch: `main`
Current integration branch: `feat/hil-post-submit-continuity-20260815`

## Source-of-truth rule

This document is the canonical participant-facing HIL continuation record in `StegVerse-Labs/Site` and is subordinate to `docs/SITE_MIRROR_HANDOFF.md`.

Read with, in current-authority order:

1. `docs/HIL_RUNTIME_PATH_RECONCILIATION.md`
2. `docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md`
3. `docs/HIL_MIRROR_HANDOFF.md`
4. `docs/HIL_END_TO_END_PROTOCOL.md`
5. `data/hil-experiment.json`
6. `data/hil-receiver-config.json`
7. `src/worker.js`
8. `data/session-work-claims.json`
9. `StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md`
10. `StegVerse-Labs/StegCore/docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md`

Live repository state, active claims, workflow evidence, runtime observations, TVC receipts, and StegCore lifecycle evidence supersede older prose.

The former Cloudflare/D1 GitHub-secret deployment instructions in earlier revisions of this handoff are **historical evidence only**. `docs/HIL_RUNTIME_PATH_RECONCILIATION.md` classifies that path `SUPERSEDED_FOR_ACTIVE_IMPLEMENTATION`. It must not be revived as the canonical HIL runtime path merely because the old attempt is preserved.

## Active goal

```text
goal_id: HIL-LIFECYCLE-ACTIVATION-001
originating_goal: complete a governed HIL participant lifecycle with exact-byte preservation, receipt continuity, private review, separate publication authority, Site projection, Master Record validation/release, and reconstructable evidence
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
participant_surface_authority: StegVerse-Labs/Site
exact_byte_custody_authority: StegVerse-Labs/TVC
cross_repository_lifecycle_validation: StegVerse-Labs/StegCore
```

No Site page, browser script, GitHub-hosted validation workflow, handoff, receipt projection, or result packet may create TV/TVC credential authority, private-review authority, publication authority, release authority, Master Record append authority, wallet authority, or provider authority.

## Current canonical runtime path

```text
participant on stegverse.org
-> same-origin GET /api/hil/readiness
-> same-origin POST /api/hil/submissions
-> Site worker src/worker.js
-> exact PDF + HIL-RESPONSE-PROVENANCE-v1.1
-> HIL-RECEIVER-RECEIPT-v2 only after persistent exact-byte reconstruction verifies
-> same-origin status/content retrieval
-> participant result projection
-> TVC exact-byte/lifecycle verification
-> authenticated private review
-> separately authenticated publication
-> Site lifecycle projection
-> Master Records validation/release under its own authority
-> StegCore cross-repository lifecycle validation
```

Canonical identities:

```text
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt version: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance: HIL-RESPONSE-PROVENANCE-v1.1
Receiver receipt: HIL-RECEIVER-RECEIPT-v2
Registry binding: HIL_REGISTRY
Custody backend: portable-sqlite-chunks-v1
```

`data/hil-receiver-config.json` declares the public receiver base as `https://stegverse.org`, readiness path `/api/hil/readiness`, and submission path `/api/hil/submissions`, with embedded credentials prohibited.

## Post-submit participant behavior — current required contract

Goal/task: `HIL-POST-SUBMIT-CONTINUITY-001`.

Canonical handoff: `docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md`.

Active pre-work claim:

```text
registry: data/session-work-claims.json
claim_id: HIL-POST-SUBMIT-CONTINUITY-001
branch: feat/hil-post-submit-continuity-20260815
state: CLAIMED_FOR_IMPLEMENTATION
created: 2026-08-15T02:22:00-05:00
release: PR #274 merge or explicit supersession after HIL continuity/release/handoff/heartbeat validation
```

The participant behavior is:

```text
successful governed submission
-> receiver receipt proves EXACT_BYTES_PERSISTED + RECORDED
-> navigate to hil-accepted.html?submission_id=<id>
-> FIRST CONTENT: HIL-SUBMISSION-RESULT-PACKET-v1
   -> receipt identity
   -> independently retrieved exact PDF bytes
   -> submitted SHA-256
   -> retrieved SHA-256
   -> exact-byte verification PASS
   -> Primary/prompt provenance identities
   -> current lifecycle state
   -> explicit false authority fields
-> NEXT LIFECYCLE CONTENT below the result packet
```

A receiver failure may preserve a hash-verified participant-device copy as `LOCAL_FALLBACK_PENDING_RESUBMISSION`, but that fallback goes to `hil-receipt.html` and does **not** claim StegVerse custody or successful governed submission.

PR #274 corrects a live source mismatch: the public participant client previously posted to `/api/hil/upload`, while the canonical worker has no such route and instead implements `/api/hil/submissions`. The branch reconciles the public client, worker contract, v1.1 release guard, upload-surface guard, and result page to the same canonical route.

## Existing genuine participant evidence

TVC remains authoritative for exact-byte custody evidence. At least one genuine participant artifact is already recorded outside the later Gmail managed-return path:

```text
submission_id: HIL-20260731-GPT56-001
TVC receipt: HIL-TVC-1442c8407e6de8c6
state: RECONSTRUCTED_HASH_VERIFIED
private_review: pending under TVC #8
publication_authorized: false
release_authorized: false
master_record_created: false
```

Absence of a managed-return email is not evidence that no HIL artifact exists.

## Active ownership and collision boundaries

```text
HIL-POST-SUBMIT-CONTINUITY-001
  owner: PR #274 bounded Site integration branch
  role: CLAIMED_FOR_IMPLEMENTATION

StegVerse-Labs/Site#67
  owner: participant lifecycle projection
  state: CLAIMED_FOR_INTEGRATION
  do not duplicate private-review/publication/lifecycle projection work

StegVerse-Labs/Site#81
  owner: live hosted receiver/readiness/runtime activation
  do not infer deployment from source merge

StegVerse-Labs/TVC#8
  owner: exact-byte lifecycle + authenticated private-review contract
  do not fabricate review decision

StegVerse-Labs/StegCore#41
  owner: cross-repository lifecycle consistency and next-action coordination

master-records/orchestration
  owner: candidate validation/custody under independent predicates
```

The machine-owned Site pre-work admission gate remains `SITE-PREWORK-CLAIM-GATE-MACHINE-001` in `data/session-work-claims.json`. Pull-request work must resolve to exactly one active pre-work claim. A standalone claim file is not sufficient admission evidence.

## Historical runtime path — preserved but superseded

The following evidence remains valid historical provenance and must not be deleted:

```text
Cloudflare deployment run: 30573565667
result: failed before provider invocation
historical cause: required Actions values empty
Wrangler invoked: false
Cloudflare invoked: false
public probes/readiness at that time: GitHub Pages 404
```

Preserved evidence includes:

```text
data/hil-cloudflare-deployment-investigation-d5d1598a.json
data/hil-cloudflare-deployment-failure-evidence-30573565667.json
evidence/hil-cloudflare-deployment-d5d1598a8c52/job-90976121829-credential-gate-failure.log
data/hil-receiver-deployment-latest.json
```

These records explain a past failed path. They are **not** the current next-action contract. The current provider-neutral runtime decision is `docs/HIL_RUNTIME_PATH_RECONCILIATION.md`.

## Validation state for PR #274

Observed successful validation on the branch:

```text
HIL Post-Submit Continuity
  run 31872177965: SUCCESS

Check HIL v1 Upload Surface
  run 31872177971: SUCCESS after stale v1.0-only guard was reconciled to canonical v1.1

Check HIL v1.1 Release
  run 31872177977: SUCCESS after stale /api/hil/upload expectation was reconciled to /api/hil/submissions
```

The Site Handoff Orchestrator correctly rejected an earlier head because the branch had no active claim in `data/session-work-claims.json`. The claim has now been installed in that canonical registry. Final handoff/heartbeat revalidation is required before merge.

Validation commands:

```text
python scripts/check_hil_post_submit_continuity.py
python scripts/check_hil_v1_upload_surface.py
python scripts/check_hil_v1_1_release.py
python scripts/check_session_work_claims.py
python scripts/site_handoff_orchestrator.py
```

Hosted validation is source/integration evidence only. It grants no production runtime authority.

## Activation denominator

Full HIL lifecycle activation remains separate from this bounded UI/source repair.

Required product gates:

```text
1 canonical v1.1 experiment identity/source
2 live governed same-origin receiver readiness
3 authentic participant governed submission + exact-byte receipt
4 authenticated private review
5 separately authenticated publication
6 validated Site lifecycle projection
7 Master Record validation/release under independent authority
8 StegCore/downstream lifecycle verification
```

Current directly supported state:

```text
1 canonical source: COMPLETE
2 live current receiver readiness after current source: NOT YET REOBSERVED
3 genuine historical participant exact-byte custody: COMPLETE for HIL-20260731-GPT56-001; new canonical public-path submission not yet observed
4 authenticated private review: PENDING TVC #8
5 publication: PENDING separate authority
6 lifecycle projection: PENDING Site #67
7 Master Record release: PENDING independent authority
8 downstream/cross-repository verification: PENDING
```

Do not report HIL fully activated from PR #274 or any GitHub-hosted workflow.

## Exact next executable work

```text
PR #274 / HIL-POST-SUBMIT-CONTINUITY-001
- require final Site Handoff Orchestrator PASS with the canonical registry claim
- require final Ecosystem Heartbeat Orchestration PASS or preserve an exact independently owned blocker
- merge only after collision-safe validation
- release the bounded claim after merge

Site #81
- directly observe the current deployed same-origin /api/hil/readiness and /api/hil/submissions runtime after canonical source reaches main
- produce RETRY / REVIEW_REQUIRED / FAILED / CLAIMED / SUPERSEDED / COMPLETE evidence; no vague external task

Site #67 + TVC #8
- continue authentic lifecycle review/projection from real receipts without creating publication/release authority
```

## Session consolidation / archive conditions

The post-submit behavior that existed only in current conversation is now durable in:

```text
docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md
claims/HIL-POST-SUBMIT-CONTINUITY-001.json
data/session-work-claims.json
PR #274
```

This session is **not archive-ready while PR #274 remains unmerged or its active claim remains unreleased**. Product-level HIL activation also remains incomplete and must continue through Site #81, Site #67, TVC #8, StegCore #41, and Master Records without relying on chat memory.

Developed-file completion for bounded post-submit tranche: 9/9 required source/validator/claim/handoff surfaces installed.
Validation completion: 3/5 required hosted validation groups observed PASS; handoff and heartbeat revalidation pending.
Integration completion: 7/8 bounded predicates implemented; merge pending.
Goal activation for bounded tranche: 7/8 before merge/claim release.
