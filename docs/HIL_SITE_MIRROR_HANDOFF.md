# Humans as the Interoperability Layer — Site Mirror Handoff

Updated: 2026-08-15
Repository: `StegVerse-Labs/Site`
Canonical branch: `main`

## Source-of-truth rule

This is the canonical participant-facing HIL continuation record in `StegVerse-Labs/Site`, subordinate to `docs/SITE_MIRROR_HANDOFF.md`.

Current authority order:

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

Live repository state, claims, receipts, workflow evidence, runtime observations, TVC evidence, and StegCore lifecycle state supersede older prose.

The old Cloudflare/D1 GitHub-secret deployment attempt is historical evidence only. `docs/HIL_RUNTIME_PATH_RECONCILIATION.md` supersedes it for active implementation. No historical GitHub-secret path may be revived as HIL production authority.

## Active product goal

```text
goal_id: HIL-LIFECYCLE-ACTIVATION-001
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
participant_surface_authority: StegVerse-Labs/Site
exact_byte_custody_authority: StegVerse-Labs/TVC
cross_repository_lifecycle_validation: StegVerse-Labs/StegCore
```

No Site page, browser code, GitHub-hosted workflow, result packet, handoff, or projection may mint private-review, publication, release, Master Record, provider, wallet, or credential authority.

## Canonical runtime path

```text
participant on stegverse.org
-> same-origin GET /api/hil/readiness
-> same-origin POST /api/hil/submissions
-> src/worker.js
-> exact response PDF + HIL-RESPONSE-PROVENANCE-v1.1
-> persistent custody + post-persistence exact-byte reconstruction
-> HIL-RECEIVER-RECEIPT-v2
-> same-origin status/content retrieval
-> HIL-SUBMISSION-RESULT-PACKET-v1 projected first on hil-accepted.html
-> TVC lifecycle/private-review verification
-> separate publication authority
-> Site lifecycle projection
-> Master Records validation/release under its own authority
-> StegCore lifecycle verification
```

Canonical identities:

```text
Primary: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance: HIL-RESPONSE-PROVENANCE-v1.1
Receiver receipt: HIL-RECEIVER-RECEIPT-v2
Registry: HIL_REGISTRY
Custody backend: portable-sqlite-chunks-v1
```

## Post-submit continuity — COMPLETE / MERGED

`HIL-POST-SUBMIT-CONTINUITY-001` is complete for its bounded source/integration scope.

```text
PR: #274
merge: e5c4e70ccf341768940dbcedbf3171e921e28344
claim: RELEASED / MERGED_INTO_CANONICAL_WORKSTREAM
handoff: docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md
```

The repaired participant path is:

```text
governed submission succeeds
-> receipt proves EXACT_BYTES_PERSISTED + RECORDED
-> hil-accepted.html?submission_id=<id>
-> FIRST CONTENT: HIL-SUBMISSION-RESULT-PACKET-v1
   -> receipt identity
   -> independently retrieved exact PDF
   -> submitted/retrieved SHA-256
   -> exact-byte PASS
   -> provenance/lifecycle state
   -> explicit false authority fields
-> NEXT LIFECYCLE CONTENT below it
```

The prior public client used `/api/hil/upload`, a route not implemented by the canonical worker. PR #274 aligned the public client with `/api/hil/readiness` and `/api/hil/submissions`. Receiver failure remains a clearly non-custodial participant-device fallback (`LOCAL_FALLBACK_PENDING_RESUBMISSION`) routed to `hil-receipt.html`.

Final source/integration evidence:

```text
HIL Post-Submit Continuity run 31872738022: SUCCESS
Check HIL v1 Upload Surface run 31872738030: SUCCESS
Check HIL v1.1 Release run 31872738020: SUCCESS
Site Handoff Orchestrator run 31872738026: SUCCESS
Ecosystem Heartbeat Orchestration run 31872738024: SUCCESS
Cloudflare Workers build ec0dd15a-f6cc-4637-9bea-9a2f79ac8c1e: SUCCESS
PR #274 merge e5c4e70ccf341768940dbcedbf3171e921e28344
```

## Genuine participant evidence already preserved

TVC remains authoritative for exact-byte custody evidence. At least one genuine participant artifact predates the repaired public path:

```text
submission_id: HIL-20260731-GPT56-001
TVC receipt: HIL-TVC-1442c8407e6de8c6
state: RECONSTRUCTED_HASH_VERIFIED
private_review: pending under TVC #8
publication_authorized: false
release_authorized: false
master_record_created: false
```

That artifact came through a connected-file path, not the later managed-return email route.

## Current owners / collision boundaries

```text
StegVerse-Labs/Site#81
  owner: live same-origin receiver/readiness/runtime activation and observation

StegVerse-Labs/Site#67
  owner: participant lifecycle projection/integration

StegVerse-Labs/TVC#8
  owner: exact-byte lifecycle + authenticated private review

StegVerse-Labs/StegCore#41
  owner: cross-repository lifecycle consistency and next-action coordination

master-records/orchestration
  owner: candidate validation/release under independent predicates
```

The machine-owned pre-work admission gate remains `SITE-PREWORK-CLAIM-GATE-MACHINE-001` in `data/session-work-claims.json`. The completed HIL post-submit claim is retained there as released provenance and no longer blocks new nonconflicting work.

## Product activation denominator

Full HIL lifecycle activation requires 8 gates:

```text
1 canonical v1.1 source + post-submit integration
2 live governed same-origin receiver readiness
3 authentic governed participant submission + exact-byte receipt on current path
4 authenticated private review
5 separately authenticated publication
6 validated Site lifecycle projection
7 Master Record validation/release under independent authority
8 StegCore/downstream lifecycle verification
```

Current source-of-truth state before direct live re-observation:

```text
1 source/integration: COMPLETE
2 live readiness after merge: MUST BE DIRECTLY REOBSERVED
3 historical genuine custody: COMPLETE for HIL-20260731-GPT56-001; current repaired public path submission not yet observed
4 private review: PENDING TVC #8
5 publication: PENDING separate authority
6 lifecycle projection: PENDING Site #67
7 Master Record: PENDING independent authority
8 downstream lifecycle verification: PENDING
```

Do not infer product activation from source merge or hosted CI. The next executable Site action is direct runtime observation under Site #81 against the current main deployment. It must emit an inspectable READY/RETRY/REVIEW_REQUIRED/FAILED receipt and preserve TV/TVC-only authority.

## Session consolidation

The previously chat-only post-submit requirement is now fully durable and merged. The session no longer owns unique source implementation for this requirement. Remaining value is distinct activation/reconciliation support across Site #81, Site #67, TVC #8, StegCore #41, heartbeat/runtime owners, and the separately active StegFin goal.
