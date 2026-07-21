# Ecosystem Chat Build Goal

## End-to-end outcome

A real governed Ecosystem Chat request completes this path:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

The existing portable-node Ecosystem Chat runtime is an active deployment-recovery path for this same vertical slice. It is not a separate replacement gateway.

## Canonical URLs

- Public Ecosystem Chat surface: https://stegverse.org/ecosystem-chat.html
- Usage surface: https://stegverse.org/ecosystem-usage.html
- Comparison surface: https://stegverse.org/ecosystem-comparison.html
- Governed transitions projection: https://stegverse.org/governed-transitions.html
- High-level goal progression: https://stegverse.org/autonomy-roadmap.html
- Prompt-level task tree: https://stegverse.org/autonomy-live.html
- Site repository: https://github.com/StegVerse-Labs/Site
- Authoritative Site mirror handoff: https://github.com/StegVerse-Labs/Site/blob/main/docs/SITE_MIRROR_HANDOFF.md
- Build-goal record: https://github.com/StegVerse-Labs/Site/blob/main/docs/ECOSYSTEM_CHAT_BUILD_GOAL.md
- Active-building record: https://github.com/StegVerse-Labs/Site/blob/main/docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING.md
- Runtime gateway and canonical StegDeploy implementation: https://github.com/StegVerse-org/LLM-adapter
- Persistent deployment recovery issue: https://github.com/StegVerse-org/LLM-adapter/issues/18
- Machine-execution compatibility runtime: https://github.com/StegVerse-org/core-node-runtime-demo
- Machine-execution issue: https://github.com/StegVerse-org/core-node-runtime-demo/issues/5
- Master-Records custody implementation: https://github.com/master-records/core-lite
- Downstream Publisher: https://github.com/GCAT-BCAT-Engine/Publisher
- Downstream admissibility projection: https://github.com/StegVerse-Labs/admissibility-wiki
- Downstream guardian projection: https://github.com/StegVerse-002/stegguardian-wiki

## Completion criteria

- A real provider request and response are observed.
- Provider usage is durably persisted without treating local persistence as custody.
- Provider-usage and transition records are accepted by the established custody path.
- Both custody chains reconstruct with PASS evidence.
- The adapter publishes the first immutable VERIFIED activation receipt with zero blockers and all authority flags false.
- Site imports and validates that receipt, recomputes `ACTIVATION_COMPLETE`, and produces a hash-bound propagation packet.
- Publisher, admissibility-wiki, and stegguardian-wiki record verified downstream ingestion.

## Current required runtime path

https://stegverse.org/ecosystem-chat.html → existing browser classifier → bounded live gateway binding → existing https://github.com/StegVerse-org/LLM-adapter governed gateway, hosted either by the restored existing Render service or the canonical provider-neutral StegDeploy/portable-node runtime → existing provider integration → existing persistence and https://github.com/master-records/core-lite custody/reconstruction → immutable adapter receipt → Site acquisition and validation → downstream consumers.

## Authoritative repositories and owners

- Public request surface and Site activation projection: https://github.com/StegVerse-Labs/Site
- Runtime gateway, canonical StegDeploy runtime, portable-node supervision, and activation evidence: https://github.com/StegVerse-org/LLM-adapter
- Machine-execution compatibility and governed runtime comparison: https://github.com/StegVerse-org/core-node-runtime-demo
- Custody and reconstruction: https://github.com/master-records/core-lite
- Downstream publication projection: https://github.com/GCAT-BCAT-Engine/Publisher
- Downstream admissibility projection: https://github.com/StegVerse-Labs/admissibility-wiki
- Downstream guardian projection: https://github.com/StegVerse-002/stegguardian-wiki

## Goal-monitoring Site pages

- High-level goal progression: https://stegverse.org/autonomy-roadmap.html
- Prompt-level task tree: https://stegverse.org/autonomy-live.html

These pages report evidence state only. They do not grant execution, completion, custody, release, deployment, publication, or heartbeat authority.

## What counts as real progress

Execution, repair of an observed runtime failure, verification, custody, reconstruction, immutable receipt production, Site activation, and verified downstream ingestion.

## What does not count as completion

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, browser code existence, goal-page check marks, task-tree entries, container-image existence, or propagation packets without verified runtime evidence.

Provider-replacement, billing, export, migration-gate, or retirement scaffolding does not advance this declared goal unless it directly enables the current Ecosystem Chat runtime path.

## Heartbeat boundary

GitHub Actions, portable-node process supervision, OCI image publication, and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. Runtime heartbeat architecture was not modified.

## Proven state

- The existing adapter code defines `/health`, `/api/ecosystem-chat`, and transition-status routes.
- The combined gateway preserves provider, persistence, custody, reconstruction, receipt, and authority boundaries.
- The existing Site classifier, fail-closed fallback, gateway binding, activation consumers, and downstream consumers remain installed.
- PR #14 merged the canonical provider-neutral StegDeploy runtime: `Dockerfile`, `compose.stegdeploy.yaml`, `scripts/container-entrypoint.sh`, `scripts/stegdeploy_bootstrap.py`, `.github/workflows/stegdeploy-image.yml`, persistent storage, health verification, image provenance, and a deployment receipt.
- PR #15 merged zero-touch portable-node bootstrap.
- PR #16 merged autonomous portable-node service lifecycle and reconstruction.
- PR #17 merged user-level automatic startup registration across Linux, macOS, and Windows.
- PR #8 was merged as `ce9027d0d3bf79f93b92bc764880a21cd848afda` after full validation and Architecture Guard success.
- Deployed probe run `29706857317` retained artifact `8448172403`; the configured host resolved but all required routes returned HTTP 404.
- `render-production.yaml` was not the consumed default Blueprint path.
- Post-merge probe run `29708519759` retained artifact `8448551905` and confirmed the same HTTP 404 result after the non-consumed production-file repair.
- PR #9 added `renderSubdomainPolicy: enabled` to the consumed `render.yaml` and merged as `1393a06c35a9727b1734a4b7a40ccd62e43e75e5` after validation and Architecture Guard success.
- Immediate and delayed probes continued to return plain-text HTTP 404 at all required routes.
- PR #11 bounded the existing verifier to retain final URLs and a narrow non-secret response-header allowlist.
- Validation run `29709832124` and Architecture Guard run `29709832126` passed.
- Probe artifact `8448772066`, digest `sha256:bd129d6e1c46473e56cf40f0b2ab1255cc4912b6fa669299e40aa6ca9fbc1f77`, retained `server: cloudflare`, `content-type: text/plain; charset=utf-8`, and `x-render-routing: no-server` for health, chat, and transition requests.
- PR #11 merged as `efb7c4e49a2773c976e4494d5aa84618554a768d`.
- The verified hosted blocker is before the FastAPI application: the Render hostname exists at the edge, but no Render server is attached behind it.
- The normal adapter `validate` workflow already executes the live vertical-slice verifier.
- Commit `4c0216bb9cbcfc0912d5f44317cd843738b1247b` writes stable semantic status and retains the current observation directly from that normal validation path.
- Commit `80dbf169faaea7193728efdbe3ff959a50fe56ed` enforces that direct retention contract.
- Commit `042faaaca4d1c1babc8d7d7bc8c8e408356cc337` made the existing portable-node host binding configurable while preserving loopback as the fail-closed default.
- Commit `3f8165686b86419cadfdd093a1e5a3876915801f` corrected the node daemon so authorized provider, custody, host, and port settings are preserved instead of overwritten by defaults.
- Commits `97bef70d3683cfae7029cb9bc368f0b17d955c9c` and `398a4a39523d2a21b2331866593a92c2eba4dc81` added and bound portable-node runtime contract checks to the existing validation path.
- Commits `0eaac3abc6c3691dae73916b1bd6f135e0a9955f`, `ea9efe1c621552f609e1a6d929964135b52476e8`, and `4f2e56913462a74944d67c0e91afb484fe0df643` added overlapping portable-node image packaging after the canonical StegDeploy path already existed. These files are retained but are not designated canonical pending explicit consolidation or removal approval.
- https://github.com/StegVerse-org/core-node-runtime-demo is an existing private governed runtime comparison boundary with Master-Records witness-ready outputs and comparable path reports.
- Commit `9eb2893cffd2fc4e8c7dfc8ae9dfb2b4d96344c2` added a repository-owned StegDeploy runtime intake workflow that pulls the canonical image, launches it fail-closed on a GitHub machine runner, verifies live health, executes the existing core-node comparison pipeline, and persists a hashed compatibility receipt.
- Commit `62b87d6918977f6bcbc909955b4a765460e04238` integrated that intake into the established `.github/workflows/validate.yml` path on `main`.
- Commit `abd8fc8858d3ec46a8d24d5b649ee3cb520c68c4` explicitly bound the existing `push` trigger to `main` without changing runtime steps, permissions, receipt construction, or authority boundaries.
- The expected `receipts/stegdeploy-runtime-intake.latest.json` does not yet exist.
- GitHub currently records no workflow run and no commit status for either `62b87d6918977f6bcbc909955b4a765460e04238` or `abd8fc8858d3ec46a8d24d5b649ee3cb520c68c4`.
- Machine-owned continuation is tracked by https://github.com/StegVerse-org/core-node-runtime-demo/issues/5 and https://github.com/StegVerse-org/LLM-adapter/issues/18.

## Current blocker

The first missing runtime boundary is repository-level Actions execution recognition for the existing `StegVerse-org/core-node-runtime-demo/.github/workflows/validate.yml` path. The canonical intake implementation is integrated on `main`, and the existing trigger is now explicitly bound to `main`, but GitHub has recorded no run or status for either integration commit and no repository-authored compatibility receipt exists.

No duplicate executor, workflow, monitor, scheduler, manual dispatch task, or heartbeat-like automation is justified. The connected environment also lacks a direct workflow-dispatch capability, and no existing run exists to rerun.

The persistent hosted path remains separately blocked because the configured Render endpoint returns `x-render-routing: no-server`. Provider execution, persistence, custody, reconstruction, immutable VERIFIED receipt, Site activation, and downstream ingestion remain unproven.

## Next executable integration step

Continue through the existing repository-owned validation path tracked at https://github.com/StegVerse-org/core-node-runtime-demo/issues/5. The next admissible action is the first GitHub-recognized execution of `.github/workflows/validate.yml`; after a real step-level result exists, repair only its first concrete workflow or runtime failure. Then use https://github.com/StegVerse-org/LLM-adapter/issues/18 to bind the same canonical runtime to an already-authorized persistent host and allow the existing verifier, custody, reconstruction, receipt, Site activation, and downstream paths to proceed.

Do not create another executor, deployment package, gateway, receipt schema, workflow scheduler, or heartbeat mechanism.

## Manual user action requirement

False. Both tasks remain repository-owned. The user is not assigned workflow dispatch, credential copying, image pull, node start, deployment, health testing, receipt construction, or evidence transcription.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.
- This cycle does not increase runtime completion because no workflow execution or receipt was observed.

## Latest meaningful goal advancement

- Date: 2026-07-21
- Canonical provider-neutral runtime: merged PR #14
- Zero-touch bootstrap: merged PR #15
- Autonomous node lifecycle: merged PR #16
- Automatic user-level startup: merged PR #17
- Portable-node binding repair: `042faaaca4d1c1babc8d7d7bc8c8e408356cc337`
- Authorized environment preservation: `3f8165686b86419cadfdd093a1e5a3876915801f`
- Portable-node runtime tests: `97bef70d3683cfae7029cb9bc368f0b17d955c9c`
- Existing-validation contract binding: `398a4a39523d2a21b2331866593a92c2eba4dc81`
- Core-node machine executor: `9eb2893cffd2fc4e8c7dfc8ae9dfb2b4d96344c2`
- Established-workflow integration: `62b87d6918977f6bcbc909955b4a765460e04238`
- Explicit main-branch trigger binding: `abd8fc8858d3ec46a8d24d5b649ee3cb520c68c4`
- Machine-execution task: https://github.com/StegVerse-org/core-node-runtime-demo/issues/5
- Persistent deployment task: https://github.com/StegVerse-org/LLM-adapter/issues/18
- Latest Site goal-record advancement: this commit records the bounded trigger repair and the remaining repository-level non-execution boundary; runtime gate delta remains zero.
