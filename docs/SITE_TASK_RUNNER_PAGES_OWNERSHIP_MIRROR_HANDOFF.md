# Site Task Runner Pages Ownership Mirror Handoff

Issue: #578
Claim: SITE-TASK-RUNNER-PAGES-578-20260828
State: IMPLEMENTED_VALIDATED_MERGED / LIVE_DEPLOYMENT_OBSERVATION_PENDING

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


## Validation and merge evidence

- validated implementation head: `7176dd8c1fb72a32c917c353a30a473cb7bb8a67`
- Ecosystem Heartbeat Orchestration `33174011052`: PASS
- Site Handoff Orchestrator `33174011070`: PASS
- Site Bootstrap Validate `33174011054`: PASS
- PR: #580
- merge: `a22065b4514a13a4e6cc5c7764d10504f666c3d6`
- claim release commit: `7e49f8416dd033c284942ad6a7025bd0b9655803`

Source ownership is repaired. Live completion still requires observing a subsequent main transition and confirming Site Task Runner does not create a `github-pages` deployment record.
