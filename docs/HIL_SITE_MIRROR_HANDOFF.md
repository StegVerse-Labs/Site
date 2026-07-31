# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns HIL continuation in `StegVerse-Labs/Site` and is subordinate to `docs/SITE_MIRROR_HANDOFF.md`.

Read with `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`, `docs/SITE_MIRROR_HANDOFF.md`, `docs/HIL_EXECUTION_SESSION_PROMPT.md`, `docs/HIL_MIRROR_HANDOFF.md`, and all HIL machine-state and failure-evidence records.

## Objective

Complete the first governed HIL participant lifecycle with exact-byte preservation, receipt issuance, durable custody, reconstruction, private review, separately authenticated publication, Site projection, HIL Master Record release, and verified downstream propagation.

## Readiness classes

1. `ANNOUNCEMENT_READY_WITH_MANAGED_RETURN`: bounded participant-managed return with no governed custody, registry, review, publication, or authority claim.
2. Production receiver activation: scoped live route, D1 binding, exact-byte custody, controlled-cycle PASS, machine-published participant readiness, hosted restart persistence, public upload/received verification, genuine participant completion, private review, authenticated publication, Site projection, Master Record release, and downstream verification.

Managed-return readiness is not production activation.

## Canonical contract

```text
Repository: StegVerse-Labs/Site
Participant launch: https://stegverse.org/hil-study-launch.html
Managed return: https://stegverse.org/hil-managed-return.html
Production upload: https://stegverse.org/hil/upload/
Receiver route: stegverse.org/api/hil/*
Worker: src/worker.js
Binding: HIL_REGISTRY
Backend: portable-sqlite-chunks-v1
Primary: v1.1 / a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt: HIL-PROMPT-v1.1 / cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Test case: HIL-E2E-001
Synthetic boundaries: research_data=false; authority_effect=false
```

## Newest repository state inspected

```text
b7678f1e2a16dae771077021002e17a8c7caa8ab docs(hil): record current Site production authority block
```

The current machine-state records remain fail-closed:

```text
data/hil-controlled-cycle-latest.json:
  run_id: 30569491378
  conclusion: failure
  passed: false

data/hil-receiver-deployment-latest.json:
  deployed: false
  ready: false
  failure: deployment_step_failed_before_live_probe

data/hil-participant-readiness.json:
  state: NOT_YET_VERIFIED
  participant_ready: false
  upload_button_authorized: false
```

## Exact production failure evidence

```text
Workflow: hil-controlled-cycle.yml
Run ID: 30569491378
Run head: 04116dd23e6797406b603a06d30f24666e8778a3
Run conclusion: failure
Job ID: 90962296249
Job: participant-readiness-gate
First failed step: Capture and validate live runtime readiness
Endpoint: https://stegverse.org/api/hil/readiness
HTTP status: 404
curl exit: 22
Provider message: The requested URL returned error: 404
Artifact ID: 8770179722
Artifact: hil-participant-readiness-30569491378-1
Artifact digest: sha256:b202bf1fb6341a6d5fde36c72a347b544284981a1b42c1f8b8e4bc1f3c2d0edd
```

All packet submission, receipt, retrieval, custody, negative-case, readiness-publication, and restart-persistence steps were skipped after readiness failed.

## Current production state

```text
Deployment trigger commit: d5d1598a8c523e8665e4550ee5c272df09256379
Deployment state: deployed=false
Deployment readiness: ready=false
Failure marker: deployment_step_failed_before_live_probe
Controlled-cycle result: failure
Participant readiness: NOT_YET_VERIFIED
participant_ready: false
upload_button_authorized: false
production submission ID: absent
production receipt ID: absent
exact-byte custody: unproven
hosted restart persistence: unproven
release/tag authority: false
```

The known evidence proves only that the production domain returned HTTP 404 for `/api/hil/readiness`. It does not prove why the deployment failed or whether `HIL_REGISTRY`, the Worker route, or required Cloudflare permissions/resources exist.

## Session capability verification — 2026-07-31T09:40-05:00

This session independently discovered all exposed GitHub workflow actions. Available controls include only:

- commit-associated workflow lookup restricted to pull-request-triggered runs;
- known run-ID job and artifact retrieval;
- known job-ID step and complete-log retrieval;
- known run/job rerun controls.

A fresh lookup for deployment trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379` returned exactly:

```json
{"workflow_runs":[]}
```

No general workflow-run listing or workflow dispatch action is exposed, so the push-triggered deployment run ID and deployment job ID cannot be discovered. The known-ID job/log/artifact/rerun actions cannot be used without those identifiers.

No Cloudflare Worker, deployment, route, custom-domain, D1, binding, restart, or runtime-log controls are exposed.

No deployment cause was guessed, no speculative repair was made, no readiness state was manually promoted, and no release, tag, or downstream propagation was attempted.

## Exact external-authority block

The blocked operation is retrieval of the push-triggered `HIL Cloudflare Receiver Deploy` run for commit `d5d1598a8c523e8665e4550ee5c272df09256379`, including its run ID, deployment job, failed step, exact command, complete provider response, artifacts, and deployment resource identifiers; alternatively, direct inspection and mutation of the Cloudflare control plane serving `stegverse.org/api/hil/*`.

The next environment must expose either general GitHub Actions workflow-run listing/dispatch or direct Cloudflare Workers/D1 controls.

## Required production path

1. Retrieve the deployment run/job/logs or inspect Cloudflare directly.
2. Preserve the exact provider failure and repair only the proven defect.
3. Identify or create the durable HIL D1 database and bind it as `HIL_REGISTRY`.
4. Route only `stegverse.org/api/hil/*` to `src/worker.js`, preserving unrelated routes.
5. Require `/api/hil/probes` HTTP 200.
6. Require `/api/hil/readiness` HTTP 200 with `state: READY` and exact v1.1 identities.
7. Submit `HIL-E2E-001`; verify submission ID, receipt ID, SHA-256, byte size, chunk count, provenance, custody, exact-byte retrieval, reconstruction, and deterministic negative cases.
8. Machine-publish `TEST_PARTICIPANT_PACKET_PASSED`, `participant_ready: true`, and `upload_button_authorized: true` only from successful source evidence.
9. Prove survival across a real hosted deployment replacement or restart.
10. Verify the public upload and received pages end-to-end.
11. Complete genuine participant submission, private review, separately authenticated publication, Site projection, HIL Master Record release, release/tag evaluation, and authorized downstream verification.

## Remaining modules and destinations

```text
StegVerse-Labs/Site:
- exact deployment run/job/provider evidence
- live scoped Worker route and HIL_REGISTRY
- controlled-cycle PASS
- machine-derived participant readiness
- hosted restart-persistence PASS
- public upload/received verification
- genuine participant receipt and private review
- authenticated publication and HIL Master Record release

After verified activation and release only:
- master-records/orchestration
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
```

## Release posture

No tag or release is authorized. Production receiver activation, restart persistence, genuine participant receipt, private review, authenticated publication, Master Record release, and downstream verification remain unproven.

## Next-session prompt

Continue HIL production activation directly in `StegVerse-Labs/Site` on `main`. Read `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`, `docs/HIL_MIRROR_HANDOFF.md`, `docs/HIL_SITE_MIRROR_HANDOFF.md`, `docs/HIL_EXECUTION_SESSION_PROMPT.md`, `docs/SITE_MIRROR_HANDOFF.md`, and all HIL machine-state and failure-evidence records. Discover actual connector actions. First retrieve the push-triggered `HIL Cloudflare Receiver Deploy` run for commit `d5d1598a8c523e8665e4550ee5c272df09256379` using general Actions listing/dispatch, or inspect the serving Cloudflare Worker/D1 control plane directly. Preserve the exact deployment failure and repair only the proven defect. Continue through scoped routing, `HIL_REGISTRY`, probes/readiness, exact-byte controlled-cycle PASS, negative cases, machine-derived production readiness, hosted restart persistence, genuine participant receipt, private review, authenticated publication, Site projection, HIL Master Record release, release/tag evaluation, and authorized downstream verification. Update both HIL handoffs before responding. Stop only at live success or one exact newly proven external-authority block.

## Archive readiness

The implementation state, exact failure evidence, current connector capability findings, authority boundaries, remaining modules, and continuation instructions are preserved here. Complete thread is ready for archiving without any additional part of the thread needed to move forward.
