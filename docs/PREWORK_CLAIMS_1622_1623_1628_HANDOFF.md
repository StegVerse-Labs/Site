# Pre-work claims for Site PRs #1622, #1623 and #1628: handoff

Status: PROPOSED. The claim/registry lane must approve these claims before they
are merged. RATIFY-OR-REVERT stays with that lane.

## Why these claims exist

`scripts/site_handoff_orchestrator.py` requires a pull request branch to resolve to
exactly one active pre-work claim that names an in-repository handoff. Three open
Site PRs fail that gate because main has no claim for their branches:

| PR | Branch | Claim fragment |
|---|---|---|
| #1622 (Site#1509 D-P9) | `claude/1509-dp9-claim-release-writer` | `data/session-work-claims.d/site-1509-dp9-claim-release-writer-20261028.json` |
| #1623 (Site#1509 D-P8) | `claude/1509-dp8-owner-flagged-dependency-removal` | `data/session-work-claims.d/site-1509-dp8-owner-flagged-dependency-removal-20261028.json` |
| #1628 (enterprise-host eradication) | `repair/enterprise-host-eradication-site-20261022` | `data/session-work-claims.d/site-enterprise-host-steggate-fallback-retirement-20261028.json` |

The six-field record for the failure is at #1628 comment 6474081827.

## Admission boundary

- The claims were prepared by a coordinator worker. They are not self-admitted.
- PRs #1622 and #1623 state that their admission waits on the #1615 request and on
  StegVerse-org/.github#167 r9. Whether merging these claims supersedes, or waits for,
  that path is the claim/registry lane's decision.
- Each claim uses its own task id and dependency surface key, so it does not collide
  with the existing active claims SITE-WORKSPACE-INTEROPERABILITY-20260831 and
  ENTERPRISE-HOST-PROVIDER-ERADICATION-SITE-001-20260919. Each claim names only the
  paths its PR changes.
- No credential, token, workflow, dependency, dispatch or schedule is added.

## Remaining work

- Claim/registry lane: approve or revert this PR.
- After merge: bring main into each of the three PR branches so the orchestrator
  sees the claim, then re-run CI on each PR's head.
- Release each claim when its PR is merged or closed, using the terminalization
  path (`scripts/release_merged_session_claims.py` once #1622 lands).
