# HIL Post-Submit Continuity Mirror Handoff

Updated: 2026-08-15
Repository: `StegVerse-Labs/Site`
Branch: `feat/hil-post-submit-continuity-20260815`
Pull request: `#274`

## Authority and scope

```text
goal_id: HIL-POST-SUBMIT-CONTINUITY-001
originating_session_goal: after successful governed submission, prepend the submission-result packet to the next Site page
canonical_parent_handoff: docs/HIL_SITE_MIRROR_HANDOFF.md
participant_lifecycle_owner: StegVerse-Labs/Site#67
live_receiver_activation_owner: StegVerse-Labs/Site#81
exact_byte_custody_owner: StegVerse-Labs/TVC
standalone_claim_evidence: claims/HIL-POST-SUBMIT-CONTINUITY-001.json
canonical_prework_claim_registry: data/session-work-claims.json#HIL-POST-SUBMIT-CONTINUITY-001
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
```

This handoff is authoritative only for the bounded participant-page continuity tranche. It does not replace `docs/HIL_SITE_MIRROR_HANDOFF.md`, Site #67, Site #81, TVC custody, private review, publication, Master Records, or StegCore lifecycle authority.

## Recovered participant behavior

The participant-facing rule carried from the originating session is now explicit and installed:

```text
unchanged response PDF
-> canonical readiness check
-> governed /api/hil/submissions intake
-> HIL-RECEIVER-RECEIPT-v2
-> advance to hil-accepted.html?submission_id=<id>
-> FIRST PAGE CONTENT: HIL-SUBMISSION-RESULT-PACKET-v1
   - receiver receipt identity
   - independently retrieved exact PDF
   - submitted SHA-256
   - retrieved SHA-256
   - exact-byte PASS/FAIL
   - Primary/prompt provenance identities
   - custody/registry/review/publication state
   - explicit non-authority fields
-> NEXT LIFECYCLE CONTENT below the result packet
```

If the governed receiver is unavailable, the browser may preserve a verified participant-device fallback, but that path is explicitly `LOCAL_FALLBACK_PENDING_RESUBMISSION`, does not claim StegVerse custody, and routes to `hil-receipt.html` instead of the governed result page.

## Drift discovered and corrected

Before this tranche, the public page loaded `assets/hil-direct-upload-v1.js`, whose durable path posted to `/api/hil/upload`. The canonical Site worker does not implement `/api/hil/upload`; it implements:

```text
GET  /api/hil/readiness
POST /api/hil/submissions
GET  /api/hil/submissions/<submission_id>
GET  /api/hil/submissions/<submission_id>/content
```

`data/hil-receiver-config.json` already described `/api/hil/submissions` as canonical. The public client/worker mismatch could therefore drive apparent participant submissions into local fallback rather than governed custody.

The branch now reconciles the public client to the canonical worker contract:

1. require `/api/hil/readiness` state `READY`;
2. require exact v1.1 Primary and Prompt hashes;
3. build `HIL-RESPONSE-PROVENANCE-v1.1`;
4. submit the exact PDF plus provenance to `/api/hil/submissions`;
5. require `HIL-RECEIVER-RECEIPT-v2`;
6. require response hash, Primary hash, Prompt hash, `EXACT_BYTES_PERSISTED`, and `RECORDED`;
7. record successful durable submission locally only as navigation evidence;
8. advance to `hil-accepted.html`;
9. independently request status and exact content from the same-origin governed receiver;
10. recompute SHA-256 before projecting `HIL-SUBMISSION-RESULT-PACKET-v1`.

## Installed files

```text
claims/HIL-POST-SUBMIT-CONTINUITY-001.json
data/session-work-claims.json
assets/hil-direct-upload-v1.js
assets/hil-post-submit-continuity.js
humans-as-interoperability-layer.html
hil-accepted.html
scripts/check_hil_post_submit_continuity.py
scripts/check_hil_v1_upload_surface.py
scripts/check_hil_v1_1_release.py
.github/workflows/hil-post-submit-continuity.yml
docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md
docs/HIL_SITE_MIRROR_HANDOFF.md
```

Existing canonical dependencies inspected and preserved:

```text
src/worker.js
data/hil-receiver-config.json
docs/HIL_RUNTIME_PATH_RECONCILIATION.md
StegVerse-Labs/Site#67
StegVerse-Labs/Site#81
StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md
StegVerse-Labs/StegCore/docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md
```

## Authority invariants

The result packet is evidence projection, not new authority.

```text
receiver_custody_evidence: true only after exact-byte retrieval/hash verification
private_review_authorized: false
publication_authorized: false
release_authorized: false
master_record_append_authorized: false
execution_authorized: false
```

The public JavaScript contains no `GITHUB_TOKEN`, no Authorization header, and no embedded provider secret. TV/TVC remains the credential authority. GitHub-hosted checkout/orchestration credentials are validation transport only and do not enter the participant runtime path.

## Validation

Local/static validation surfaces:

```text
python scripts/check_hil_post_submit_continuity.py
python scripts/check_hil_v1_upload_surface.py
python scripts/check_hil_v1_1_release.py
python scripts/check_session_work_claims.py
```

Hosted validation already observed:

```text
HIL Post-Submit Continuity
  run: 31872177965
  result: SUCCESS

Check HIL v1 Upload Surface
  run: 31872177971
  result: SUCCESS
  note: repaired a pre-existing v1.0-only guard that was already failing on main

Check HIL v1.1 Release
  run: 31872177977
  result: SUCCESS
  note: repaired a stale /api/hil/upload expectation to the canonical /api/hil/submissions path
```

The Site Handoff Orchestrator correctly rejected earlier heads because the standalone claim file was not present in the canonical `data/session-work-claims.json` pre-work registry. `HIL-POST-SUBMIT-CONTINUITY-001` is now installed there with an exclusive dependency surface and branch binding. Final handoff-orchestrator and ecosystem-heartbeat validation are required before merge.

The dedicated checker fails closed unless all of these remain true:

- public page uses the governed submit client;
- legacy `/api/hil/upload` is absent from the canonical client;
- readiness and submission routes match the canonical worker;
- v1.1 provenance and receipt contracts are enforced;
- durable success advances to `hil-accepted.html`;
- local fallback remains distinct and routes to `hil-receipt.html`;
- result-packet section occurs before next-lifecycle content;
- accepted-page status and content are fetched from `/api/hil/submissions/...`;
- exact retrieved bytes are hashed and compared;
- result packet grants no review/publication/release/Master Record/execution authority;
- no GitHub token/runtime credential path is introduced.

## Claims and collision state

```text
HIL-POST-SUBMIT-CONTINUITY-001
  state: CLAIMED_FOR_IMPLEMENTATION
  branch: feat/hil-post-submit-continuity-20260815
  owner: this bounded branch
  canonical registry: data/session-work-claims.json
  release: PR #274 merge or explicit supersession after final validation

Site #67
  state: CLAIMED_FOR_INTEGRATION
  scope: participant lifecycle projection/private-review/publication continuation
  collision: do not duplicate

Site #81
  scope: live hosted receiver activation/readiness
  collision: do not claim deployment from source changes

TVC #8
  scope: exact-byte custody/reconstruction/private review
  collision: Site projection cannot become custody/review authority
```

## Completion state

Required bounded deliverables: 8.

```text
1 canonical pre-work claim: COMPLETE
2 canonical public submit route: COMPLETE_SOURCE
3 v1.1 provenance-bound submission: COMPLETE_SOURCE
4 governed-success redirect: COMPLETE_SOURCE
5 prepended result page: COMPLETE_SOURCE
6 exact-byte re-verification on result page: COMPLETE_SOURCE
7 fail-closed validators/workflow: COMPLETE_VALIDATED
8 final handoff/heartbeat validation + merge + claim release: PENDING
```

Developed source/validation/claim/handoff surfaces: 9/9 required logical surfaces complete.
Validation groups: 3/5 required hosted groups PASS; handoff orchestration and heartbeat orchestration pending revalidation after canonical claim registration.
Integration predicates: 7/8 complete; merge/claim release remains.
Goal activation for this bounded source tranche: 7/8 before merge/claim release.

## Archive / release condition

This bounded session responsibility may be transferred only after:

1. final `HIL Post-Submit Continuity`, v1 upload-surface, and v1.1 release validation remain green;
2. Site Handoff Orchestrator accepts the canonical branch claim;
3. Ecosystem Heartbeat Orchestration accepts the branch/claim/handoff state, or an exact independently owned blocker is durably recorded;
4. PR #274 is merged or explicitly superseded;
5. the canonical claim is released;
6. Site #67/#81 and TVC #8 retain their unresolved lifecycle/runtime ownership;
7. no statement equates this source integration with live HIL product activation.

Live HIL activation remains a separate product-level condition and is not granted by this handoff.
