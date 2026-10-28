# TIDC coordinator push trigger, main only: handoff

Status: PROPOSED. The TIDC lane may ratify or revert this change.

## Problem

`.github/workflows/tidc-task-coordinator.yml` ran on push to any branch whose
change touched its `paths`. On a PR branch it then committed
`chore(tidc): advance repository-native task state [skip ci]` and pushed it to
that branch, for example a338709 on #1622. A `[skip ci]` commit at a PR's head
leaves that head with no exact-head CI.

## Change

The push trigger is restricted to `branches: [main]`. The step that commits and
runs `git push origin "HEAD:${GITHUB_REF_NAME}"` also gets
`if: github.ref == 'refs/heads/main'`. Without that, a `workflow_dispatch` run
with a PR branch as its ref would still commit `[skip ci]` to that branch.
Nothing else in the workflow changes: its paths, other steps, permissions,
`workflow_dispatch` trigger and writeback logic are the same.
`control/workflow-surface-registry.json` re-pins the file's sha256 and records
the narrowed trigger and gated step. Its `classification` stays
`KEEP_EXISTING_SURFACE_UNCHANGED`: the registry and its test accept only that
value and `KEEP_STABLE_DISPATCHER` for surfaces, and the dispatcher label does
not apply.

## Remaining work

- TIDC lane: ratify or revert.
- PR branches that change TIDC inputs no longer get a coordinator writeback. The
  coordinator runs after merge to main, or by `workflow_dispatch`. A dispatch on a
  non-main ref still runs the queue advancer and coordinator and uploads the run
  artifact, but skips the commit and push.
- Release this branch's claim when the PR merges or closes.

## Boundaries

- No new trigger, dispatch, schedule, dependency, credential or secret.
- The writeback logic, owned by TIDC-COORDINATOR-WRITEBACK-RETRY-20260829
  (`site:tidc-coordinator-writeback`), is not changed.

## Merge overlap

This branch and `claude/prework-claims-1622-1623-1628` (#1634) both append rows to
`data/cosv/task-vector-index.json` and `data/cosv/active-claim-projections.json`.
They also raise the same four coverage counts. Whichever PR merges second needs
main merged in: keep both sets of rows, and add the two count increases together.
