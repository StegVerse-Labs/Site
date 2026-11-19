# Site CI Standing-Red Cure Mirror Handoff

Updated: 2026-11-18
Repository: `StegVerse-Labs/Site`
Coordination task: `BUILD-Q-51`
Native Goal Task ID: `UNVERIFIED_NOT_REGISTERED_IN_GENERATION_326`
Canonical parent context only: `STEGVERSE-CANONICAL-WORK-COORDINATION-001`
Parent COSV: `10100000100000`
Status: `ACTIVE_SOURCE_CURE / PROTECTED_INTEGRATION_PENDING`
Pull request: `#1709`
Candidate head before this handoff refresh: `948d9163ca5caf96226be23835c20499c0464458`

## Authority and scope

This handoff is the canonical repository continuation record for BUILD-Q-51. BUILD-Q-51 is a coordination queue identity, not a Task Registry Goal Task ID. Task Registry generation 326 contains no BUILD-Q-51 record; this file does not mint one and does not grant WorkerCoordinator claim/fence, protected integration, deployment, release, or propagation authority.

The bounded source task is to remove the Site repository's standing-red CI state without suppressing a real regression:

1. state the exact log cause for each of the eight known failures;
2. remove unsupported Python 3.9 dispatcher cells and declare the supported Python floor;
3. carry an active exact-branch Site pre-work claim for the cure PR;
4. obtain a full PR check-set readback;
5. merge only when the repository's ordinary integration authority allows it, then verify the post-merge board.

## Exact failure evidence

Source head inspected: PR #1708 head `abf91c5605736bfa3b4b6a781947358c3673bbb1`.

Five stable-dispatcher jobs fail at the setup step before their catalog group runs:

| Check | Run / job | Exact cause |
| --- | --- | --- |
| `check-tidc-research.verify-publication-python3.9` | `44456636643 / 135333197031` | `actions/setup-python`: version 3.9 x64 not found for Ubuntu 26.04 |
| `check-tidc-session-consolidation.validate-python3.9` | `44456636643 / 135333192383` | same setup-python refusal |
| `validate-review-authority-projection.validate-python3.9` | `44456636643 / 135333196955` | same setup-python refusal |
| `check-steglearn-landing.verify-python3.9` | `44456636643 / 135333192978` | same setup-python refusal |
| `check-ecosystem-node-gateway-binding.verify-python3.9` | `44456636643 / 135333192424` | same setup-python refusal |

Python 3.9 reached end of life in October 2025. The supported Site validation floor is Python 3.11; Python 3.12 remains covered where catalog entries declare it.

Three orchestration checks fail on one predicate:

| Check | Run / job | Exact cause |
| --- | --- | --- |
| `validate` | `44456636691 / 135333127963` | PR branch did not resolve to exactly one active pre-work claim |
| `validate-heartbeat-contract` | `44456636661 / 135333127216` | same branch-claim refusal |
| `reconcile` | `44456942081 / 135334147688` | same branch-claim refusal |

The exact log text names branch `8374-static-pages-2026-11-18`; terminalization-only maintenance was also rejected because that PR was not claim-registry-only.

## Source cure

- Remove exactly the five catalog groups whose `runner.python_version` is `3.9`.
- Preserve their 3.11/3.12 counterparts and pinned step bodies.
- Declare Python 3.11 as the Site CI validation floor in `.github/workflows/validation-dispatcher.yml` and `README.md`.
- Carry `data/session-work-claims.d/build-q51-site-ci-standing-red-20261118.json` in the cure branch so orchestration resolves one active exact-branch claim.

## Validation

Required before source disposition:

- `python3 tools/tasks/run_catalog.py verify` returns ALLOW;
- matrix generation contains zero Python 3.9 cells and retains the expected 3.11/3.12 cells;
- session-work-claim validation passes;
- Site handoff orchestration resolves this branch's claim;
- full PR check set has no standing failure attributable to the eight named checks.

## Remaining work

- Open the cure PR and read every check conclusion.
- Repair any new concrete CI defect rather than suppressing it.
- Obtain authorized merge and read the post-merge check board.
- Register or reconcile the native Goal Task ID/COSV through the existing Task Registry owner; do not infer it from BUILD-Q-51.

## Continuation

Next session starts from the BUILD-Q-51 source comment on `StegVerse-Labs/.github#3471`, this handoff, and the cure PR. Preserve exact-head checks and do not claim integration, deployment, or completion before evidence.

## PR #1709 bootstrap follow-up

The first PR-head bootstrap run proved that the exact branch claim is now accepted, then exposed the next independent invariant: every effective active claim task must have a non-authorizing repository-local COSV projection. BUILD-Q-51 is not admitted to the native Task Registry; this patch does not pretend otherwise. It adds only the Site-local active-claim projection required by the existing validator:

- `data/cosv/active-claim-projections.json`: BUILD-Q-51 / CLAIMED_FOR_IMPLEMENTATION / `20010000100000`.
- `data/cosv/task-vector-index.json`: `EXTERNAL_PROJECTION_ACTIVE_CLAIM_SOURCE` binding to this claim and handoff.
- Coverage moves from 67 to 68 effective active claims/task IDs, 60 to 61 active-claim source vectors, and remains zero unindexed active task IDs.

This is an authority-neutral bookkeeping repair. Native Goal Task ID and COSV admission remain with the existing Registry owner. Protected integration, merge, deployment, release, activation, and propagation remain outside this claim.
