# Site Atomic Claim/COSV Terminalization Mirror Handoff

Updated: 2026-09-20
Repository: `StegVerse-Labs/Site`

## Defect

Current Site terminalization allows `data/cosv/task-vector-index.json` as auxiliary release bookkeeping but does not allow `data/cosv/active-claim-projections.json`. Once an indexed claim becomes terminal, the validator therefore sees a stale active projection and fails deterministically. Global COSV tests also hard-code the current active projection count, forcing unrelated source edits whenever a claim enters or leaves the active denominator.

## Repair

1. Permit the existing active-claim projection bundle as terminalization auxiliary bookkeeping.
2. Make COSV tests compare the index and projection bundle dynamically rather than hard-coding the global active-claim count.
3. Remove the stale `SITE-HIL-PAYLOAD-CONTINUITY-OUTBOX-1425` active projection created by its already-merged release.
4. Preserve zero unindexed active claims and all existing authority boundaries.

## Reusable signature

`CLAIM_TERMINALIZATION_COSV_PROJECTION_SKEW`

Recognize when a terminal claim remains in an active projection or a repository-wide count assertion fails only because the active denominator changed. Remediation is projection/index reconciliation plus dynamic parity validation; do not reopen the completed implementation and do not classify the implementation itself as runtime-incomplete.
