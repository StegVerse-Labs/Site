# Site Task Runner Pages Ownership Mirror Handoff

Issue: #578
Claim: SITE-TASK-RUNNER-PAGES-578-20260828
State: IMPLEMENTED / VALIDATION_PENDING

## Defect

Site Task Runner currently declares the `github-pages` environment and invokes the Pages deployment actions. A later Task Runner validation failure therefore creates a newer failed `github-pages` deployment record even when the canonical Pages publisher successfully deployed the same source.

## Required invariant

```text
pages-build-deployment -> sole github-pages publisher
Site Task Runner       -> validation / observation / orchestration only
```

Task Runner must not create or update the `github-pages` deployment environment.

Public-route validation remains required and should observe `https://stegverse.org/` after the canonical Pages publisher runs.

Authority effect: NONE.


## Implemented

- removed `environment: github-pages` from Site Task Runner;
- removed `pages: write` and `id-token: write` from Site Task Runner;
- removed `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`;
- public verification remains against `https://stegverse.org/`;
- terminal receipt records `STEGVERSE_PAGES_DEPLOYMENT_RESULT: NOT_OWNED_BY_TASK_RUNNER`;
- terminal completion no longer depends on a Task Runner-owned Pages deployment;
- orchestration validator now fails if any Pages deployment ownership returns to Site Task Runner.

Expected live result:

```text
native pages-build-deployment: updates github-pages environment
Site Task Runner: never creates a github-pages deployment record
Task Runner failure: may make Task Runner red, but must not make github-pages environment red
```
