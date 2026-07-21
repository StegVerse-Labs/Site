# Ecosystem Chat Active Building Cycle — Render Alignment Build

Date: 2026-07-21

## Active goal

Complete the hosted Ecosystem Chat vertical slice:

`request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation`

## Required capability

Make the existing consumed Render Blueprint capable of hosting the already-built canonical gateway with durable storage, private Master-Records custody, provider configuration through an external secret boundary, and the existing verifier path.

## Existing candidates evaluated

### Canonical StegDeploy runtime

Repository: https://github.com/StegVerse-org/LLM-adapter

Paths:

- `Dockerfile`
- `compose.stegdeploy.yaml`
- `scripts/container-entrypoint.sh`
- `scripts/stegdeploy_bootstrap.py`
- `.github/workflows/stegdeploy-image.yml`

Decision: directly reusable and retained unchanged.

### Existing production Render contract

Path: `render-production.yaml`

Current behavior: defines the existing gateway plus private Master-Records custody, durable disks, `/var/data` database paths, provider fields supplied through `sync: false`, generated internal auth/receipt keys, and `/health` verification.

Decision: directly reusable as the source contract.

### Consumed Render Blueprint

Path: `render.yaml`

Current behavior: defines the known public service identity but remains on the free fail-closed profile with `/tmp` databases, no persistent disk, provider disabled, and Master-Records bound to `127.0.0.1:9`.

Decision: bounded modification candidate.

### New hosting adapter or new host architecture

Decision: rejected because it would duplicate the canonical runtime and existing Render contracts.

## Work performed

- Added default-branch contract tests for the existing production Blueprint and fail-closed consumed Blueprint at commit `10f1a7809a2aa111edf619c63cd8526bee13a6ab`.
- Created branch `reuse/render-production-alignment`.
- Aligned branch `render.yaml` with the retained `render-production.yaml` contract at commit `b6c7ab2aaf8abe2d4ea991b54e21be809d2d6776`.
- Preserved the existing service name and health path.
- Added private Master-Records custody service binding.
- Added durable 1 GB disks for custody and gateway data.
- Moved transition, usage-session, external-review, and custody databases to `/var/data`.
- Preserved external mutation disabled by default.
- Required provider endpoint, host allowlist, token, name, and model through Render `sync: false` fields; no provider secret was embedded.
- Opened draft PR https://github.com/StegVerse-org/LLM-adapter/pull/23.

## Components reused

- Existing public Render service identity.
- Existing `render-production.yaml` contract.
- Existing combined gateway.
- Existing custody worker.
- Existing Master-Records service implementation.
- Existing provider integration.
- Existing health route.
- Existing verifier, immutable receipt, Site acquisition, activation-state computation, and downstream consumers.

## Components modified

- Branch-only `StegVerse-org/LLM-adapter/render.yaml`.
- Render Blueprint contract tests.

## New components

No new gateway, deployment architecture, provider adapter, custody service, receipt schema, monitor, scheduler, or heartbeat component was created.

A test file and draft integration branch were added because they directly secure and verify the bounded reuse of the existing deployment contract.

## Runtime tests actually executed

No GitHub Actions result or local test execution was observed during this cycle.

Source inspection confirmed the branch Blueprint contains the required durability, custody binding, secret-boundary, and health-route fields. This is IMPLEMENTED on the branch, not EXECUTED or DEPLOYED.

## Observed results

- Production-capable consumed Blueprint: IMPLEMENTED on draft branch.
- Deployment alignment PR: OPEN / DRAFT / UNMERGED.
- Provider-side Render application: NOT EXECUTED.
- Persistent public gateway: NOT DEPLOYED.
- Real provider response: UNPROVEN.
- Provider usage persistence: UNPROVEN.
- Custody and reconstruction: UNPROVEN.
- Immutable VERIFIED receipt: UNPROVEN.
- Site activation: UNPROVEN.
- Downstream ingestion: UNPROVEN.

## Exact failures and blockers

- Draft PR reports no completed validation evidence in the connected path.
- Merge and Blueprint application may create paid Render services and persistent disks.
- Provider and Master-Records secret authority is not granted by the code or PR.
- The current public hostname remains attached to no server until an authorized provider-side deployment occurs.

## Durable evidence

- Safe default-branch contract test commit: https://github.com/StegVerse-org/LLM-adapter/commit/10f1a7809a2aa111edf619c63cd8526bee13a6ab
- Branch alignment commit: https://github.com/StegVerse-org/LLM-adapter/commit/b6c7ab2aaf8abe2d4ea991b54e21be809d2d6776
- Draft PR: https://github.com/StegVerse-org/LLM-adapter/pull/23
- Deployment owner: https://github.com/StegVerse-org/LLM-adapter/issues/18
- Authority decision: https://github.com/StegVerse-Labs/Site/issues/24

## Removals proposed but not performed

None.

No existing Blueprint, gateway, runtime, provider integration, custody path, receipt path, Site consumer, downstream consumer, or heartbeat component was deleted, disabled, renamed, superseded, or replaced.

## Goal delta

The exact production-capable consumed Render Blueprint now exists on a reversible draft branch. Before this cycle, the production contract existed only in a non-consumed file.

No runtime gate is advanced because the PR is unmerged and no provider-side deployment occurred.

## Reuse delta

The retained `render-production.yaml`, canonical gateway, Master-Records service, provider integration, verifier, receipts, and Site consumers eliminated the need for a new host architecture or deployment adapter.

## Non-progress

- Contract tests and a draft PR do not prove deployment.
- Blueprint source does not prove provider execution, persistence, custody, reconstruction, activation, or propagation.
- The marker file added during branch initialization does not advance a runtime gate.

## Next executable step

Validate draft PR #23. After explicit authorization for potential paid Render services, merge and apply the existing Blueprint, supply provider configuration through Render's secret boundary, observe `/health`, execute one governed request, and repair only the first concrete runtime failure.

## Manual user action requirement

No routine file editing, deployment commands, receipt construction, or evidence copying is assigned to the user. Provider-side deployment and potential paid-resource authority remain explicit approval boundaries.
