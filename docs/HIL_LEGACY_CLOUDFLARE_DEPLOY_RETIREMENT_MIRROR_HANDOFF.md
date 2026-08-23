# HIL Legacy Cloudflare Deploy Retirement Mirror Handoff

Updated: 2026-08-23
Repository: `StegVerse-Labs/Site`
Issue: `#476`
Claim: `SITE-HIL-LEGACY-CLOUDFLARE-DEPLOY-RETIREMENT-476-20260823`
Branch: `claim/site-hil-legacy-cloudflare-deploy-retirement-476`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Physically retire the superseded HIL Cloudflare/D1 GitHub-secret deployment workflow while preserving its historical failure evidence and leaving the provider-neutral active HIL runtime path untouched.

## Canonical authority

Read in this order:

1. `docs/HIL_RUNTIME_PATH_RECONCILIATION.md`
2. `docs/HIL_SITE_MIRROR_HANDOFF.md`
3. `docs/HIL_MIRROR_HANDOFF.md`

The canonical runtime-path reconciliation classifies the Cloudflare deployment attempt as:

```text
claim state: SUPERSEDED_FOR_ACTIVE_IMPLEMENTATION
completion state: FAILED_BEFORE_PROVIDER_INVOCATION
preservation state: RETAIN_HISTORICAL_EVIDENCE
retry authority: NOT_GRANTED_BY_THIS_RECORD
```

The Site HIL handoff further states:

```text
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
old Cloudflare/D1 GitHub-secret deployment attempt: historical evidence only
no historical GitHub-secret path may be revived as HIL production authority
```

## Historical evidence retained

The prior failed deployment remains durably documented in HIL handoffs:

```text
workflow: HIL Cloudflare Receiver Deploy
run: 30573565667
job: 90976121829
result: FAILURE before provider invocation
first failed step: Validate deployment credentials
CLOUDFLARE_API_TOKEN: empty
CLOUDFLARE_ACCOUNT_ID: empty
HIL_REGISTRY_DATABASE_ID: empty
Wrangler/provider invocation: never occurred
production receiver proven: false
```

Deleting the stale workflow does not delete that history.

## Active runtime path preserved

Active HIL implementation remains separately owned:

```text
Site #81: provider-neutral connected hosted runtime/readiness/receiver observation
Site #67: lifecycle projection
StegVerse-Labs/TVC #8: exact-byte custody and authenticated private review
StegVerse-Labs/StegCore #41: cross-repository lifecycle consistency/next-action coordination
master-records/orchestration: independent candidate validation/release predicates
```

This retirement does not modify any of those implementations or authority domains.

## Current stale-carrier hazard

`.github/workflows/hil-cloudflare-deploy.yml` still exists on `main` despite the superseding decision. It still:

- triggers on `main` source changes and manual dispatch;
- requests generic `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and `HIL_REGISTRY_DATABASE_ID` GitHub secrets;
- performs direct Wrangler deployment when credentials exist;
- writes deployment observations back to `main` with `contents: write`;
- uploads 30-day deployment artifacts.

Because retry authority is explicitly not granted and the active path is provider-neutral, retaining this carrier can revive an obsolete production path contrary to canonical governance.

## Repair boundary

- delete `.github/workflows/hil-cloudflare-deploy.yml`;
- retain canonical HIL handoffs and historical failed-run evidence unchanged;
- do not add a replacement GitHub deployment workflow;
- do not add or rename Cloudflare/D1 secrets;
- do not touch Site #81 runtime implementation, Site #67 projection, TVC custody/private review, StegCore coordination, participant pages/assets, or active upload-owned paths;
- no Render;
- no NON-TV/TVC credential;
- no GitHub-token production/runtime authority;
- no activation effect.

## Completion gate

Release requires the legacy workflow to be absent from the exact PR head, Site pre-work claim validation to pass, Site Handoff Orchestrator and Site Bootstrap to pass, integration to merge, and durable release evidence to be recorded here and in the claim fragment. Workflow removal is not HIL activation.
