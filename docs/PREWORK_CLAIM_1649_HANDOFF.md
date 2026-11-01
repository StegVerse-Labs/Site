# Pre-work claim for Site PR #1649: handoff

Status: PROPOSED. The claim/registry lane must approve this claim before it is merged. RATIFY-OR-REVERT stays with that lane. This follows the Site#1634 precedent (`docs/PREWORK_CLAIMS_1622_1623_1628_HANDOFF.md`).

## Why this claim exists

`scripts/site_handoff_orchestrator.py` requires a pull request branch to resolve to exactly one active pre-work claim that names an in-repository handoff. Site#1649 (docs only, for StegVerse-Labs/.github#3398) fails that gate on `main`, which has no claim for its branch. The six-field record is at Site#1649 comment 6509637187.

| PR | Branch | Claim fragment |
|---|---|---|
| #1649 (assessment-path entry and downloadable-PDF procedure) | `p1/round18-assessment-path-and-pdf-procedure` | `data/session-work-claims.d/site-assessment-path-pdf-procedure-3398-20261029.json` |

The claim PR itself passes the same gate through its own claim, `data/session-work-claims.d/site-prework-claim-1649-20261029.json` (branch `p1/round18-prework-claim-1649`).

## Admission boundary

- The claims were prepared by P1. They are not self-admitted, and P1 does not merge the claim PR. P4 reviews it against the Site#1634 precedent and merges it.
- Each claim uses its own task id and dependency surface key, and names only the paths its PR changes. Neither claim grants publication authority, publishes anything, or changes the coordination state of REAL-GOVERNANCE-ASSESSMENT-SAMPLE-001, which stays PROPOSED.
- No credential, token, workflow, dependency, dispatch or schedule is added.

SKAP Vault invariant (existing source, quoted, not restated as new): "SKAP Vault inside KV is the only PII and credential store for every user, the ecosystem's own included; the ecosystem holds none (HST citation pending P1 #163). (`docs/FEDERATION_DIRECTORY.md:3`)"

## Remaining work

- Claim/registry lane: approve or revert this PR.
- After merge: bring main into the Site#1649 branch with a normal merge, re-run its exact-head CI with 0 skipped, then P4 gives the CONFIRM on Site#1649 and on StegVerse-org/.github#166.
- Release each claim when Site#1649 is merged or closed.
