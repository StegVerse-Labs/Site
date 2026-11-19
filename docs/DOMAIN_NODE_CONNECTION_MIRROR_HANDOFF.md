# Domain Node Connection — Mirror Handoff

Status: ACTIVE — implementation in PR #1713, claimed under
`data/session-work-claims.d/SITE-DOMAIN-NODE-CONNECTION-20261119.json`.

## Determination

The StegOS node connection is applied to the domain, not to individual
pages. Every served page of stegverse.org carries the continuity entry
`/assets/stegverse-node-continuity.js`, so no page stands outside the
node apparatus. (Principal determination, 2026-11-19, after a seven-context
browser census showed node establishment varying by browser container on
the pages that carried the connection, and no connection at all on the
pages that did not.)

## What PR #1713 changes

- Commit 1 (`1fa705b643531002343efead66c30a18946ea5ab`): the continuity
  entry inserted into 281 served pages (306 served pages total; 25 already
  wired, untouched; no page double-wired; byte-exactness proven by
  inverse transform).
- Commit 2 (`78cd452333b92f73f119155cc72d7b99d283eed2`): the entry admitted
  by name in the three page-contract validators whose closed script
  inventories it flipped (stegfin phone projection with SKAP, stegos iPod
  bootstrap projection, LLM browser conformance page). Each admission is
  minimal and negative-proven: an unadmitted script still fails all three.
- Commit 3 (this claim): registers the pre-work claim for this branch and
  this handoff. The dispatcher group `validate-physical-economics-report-ui.validate`
  fail-closes any pull request whose head branch resolves to no active
  pre-work claim; this branch had none. The claim is the cure — the check
  itself is unchanged.

## Evidence

- Full local validator sweep (393 scripts, HEAD vs amended tree):
  zero pass-to-fail flips after commit 2.
- `validate-physical-economics-report-ui.validate` on head `78cd4523…`:
  step 2 failed in CI with the branch-claim predicate; reproduced locally
  under the CI environment on both the base tree and the merge tree, and
  cured by this claim (see the claim fragment and the PR record).

## Remainders (untouched by this work)

Node identity derivation, the resident-health classifier, the repair
flow, and the node-status display box are not modified. No apparatus
JavaScript changed. This claim releases when PR #1713 merges and the
domain connection is verified on the live site; terminalize it with the
PR #1713 merge commit as release evidence.
