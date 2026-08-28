# Site Task Runner Pages Ownership Mirror Handoff

Issue: #578
Claim: SITE-TASK-RUNNER-PAGES-578-20260828
State: CLAIM_PENDING_ADMISSION

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
