# BUILD-Q-51 — Site CI standing-red cure

## Authority and scope

Queue assignment: `StegVerse-Labs/.github#3471`, comment `7000632566`;
pairing: `#3472`, comment `7000638068`. Seat: CODEX (ChatGPT participant,
Work surface, Codex environment), verified from the current lane registry.
The universal prompt and Lane Session Prompt plus amendments were fetched and
verified against their filed SHA-256 values before use. This is a bounded source
repair assigned explicitly by the owner. BUILD-Q-51 is a queue identifier;
native Task Registry Goal ID and COSV binding remain UNBOUND, not invented or
borrowed from the retired Site COSV adoption task. No runtime authority is granted.

## Log-derived causes

The coordinator's PR #1707/#1708 standing-red baseline is accepted. These are
the actual failures, not inferred Python syntax failures:

| Check | Job | Cause |
| --- | --- | --- |
| check-tidc-research.verify-publication-python3.9 | 135333197031 | setup-python: Python 3.9 x64 not found for Ubuntu 26.04; no validator ran |
| check-tidc-session-consolidation.validate-python3.9 | 135333192383 | same setup-python failure |
| validate-review-authority-projection.validate-python3.9 | 135333196955 | same setup-python failure |
| check-steglearn-landing.verify-python3.9 | 135333192978 | same setup-python failure |
| check-ecosystem-node-gateway-binding.verify-python3.9 | 135333192424 | same setup-python failure |
| validate | 135333127963 | branch `8374-static-pages-2026-11-18` has no exactly-one active pre-work claim; not a claim-registry-only terminalization |
| validate-heartbeat-contract | 135333127216 | same missing active branch claim |
| reconcile | 135333127749; latest 135334147688 | same missing active branch claim |

Job URLs are `https://github.com/StegVerse-Labs/Site/actions/runs/44456636643/job/JOB`
for the five Python legs; validate run `44456636691`, heartbeat run
`44456636661`, reconcile runs `44456636692` and `44456942081`.
Full per-check cause filing: `.github#3471`, comment `7000733233`.

## Repair and acceptance

The supported Python minimum is 3.11. Retire only the five executable 3.9 catalog
cells; retain their existing 3.11 and 3.12 validators, and preserve historical
folded workflows and step bodies as provenance. Catalog edits select the ten
remaining affected legs so green evidence executes their validators.
Keep all three claim/orchestration gates intact. Register this repair's exact
branch before opening the PR, retain its claim through merge-event validation,
then release it through the existing registry-only terminalization path.

Acceptance remains pending: merge the repair PR through ordinary protections,
read every check page at the exact head and merge, and file counts, conclusions,
run URLs and any remainder on #3471/#3472. No green/merge/runtime assertion is
made by this initial handoff. If integration cannot proceed, file the exact
six-field failed predicate and actionable receiving owner.

## Continuation

Branch: `fix/build-q51-site-ci-standing-red`. Claim:
`CODEX-BUILD-Q51-SITE-CI-20261119`. README and this handoff are maintained with
the source change. Close using CHECKED OUT / DISCHARGED / EVIDENCE / REMAINDER.
