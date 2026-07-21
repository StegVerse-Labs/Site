# Ecosystem Chat Build Goal

## End-to-end outcome

A real governed Ecosystem Chat request completes this path:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

The existing portable-node Ecosystem Chat runtime is an active deployment-recovery path for this same vertical slice. It is not a separate replacement gateway.

## Completion criteria

- A real provider request and response are observed.
- Provider usage is durably persisted without treating local persistence as custody.
- Provider-usage and transition records are accepted by the established custody path.
- Both custody chains reconstruct with PASS evidence.
- The adapter publishes the first immutable VERIFIED activation receipt with zero blockers and all authority flags false.
- Site imports and validates that receipt, recomputes `ACTIVATION_COMPLETE`, and produces a hash-bound propagation packet.
- Publisher, admissibility-wiki, and stegguardian-wiki record verified downstream ingestion.

## Current required runtime path

`StegVerse-Labs/Site/ecosystem-chat.html` → existing browser classifier → bounded live gateway binding → existing `StegVerse-org/LLM-adapter` governed gateway, hosted either by the restored Render service or the canonical provider-neutral StegDeploy/portable-node runtime → existing provider integration → existing persistence and Master-Records custody/reconstruction → immutable adapter receipt → Site acquisition and validation → downstream consumers.

## Authoritative repositories and owners

- Public request surface and Site activation projection: `StegVerse-Labs/Site`
- Runtime gateway, canonical StegDeploy runtime, portable-node supervision, and activation evidence: `StegVerse-org/LLM-adapter`
- Custody and reconstruction: existing Master-Records implementation referenced by adapter evidence
- Downstream publication projection: `GCAT-BCAT-Engine/Publisher`
- Downstream admissibility projection: `StegVerse-Labs/admissibility-wiki`
- Downstream guardian projection: `StegVerse-002/stegguardian-wiki`

## Goal-monitoring Site pages

- High-level goal progression: `autonomy-roadmap.html`
- Prompt-level task tree: `autonomy-live.html`

These pages report evidence state only. They do not grant execution, completion, custody, release, deployment, publication, or heartbeat authority.

## What counts as real progress

Execution, repair of an observed runtime failure, verification, custody, reconstruction, immutable receipt production, Site activation, and verified downstream ingestion.

## What does not count as completion

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, browser code existence, goal-page check marks, task-tree entries, container-image existence, or propagation packets without verified runtime evidence.

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

## Current blocker

The configured hosted endpoint still returns `x-render-routing: no-server`, so no application process receives that request. The canonical StegDeploy runtime already supports autonomous build, launch, persistent storage, health verification, and deployment receipts, and the portable-node runtime now preserves authorized host/provider/custody configuration. No currently connected machine-owned executor has yet run the canonical deployment on an authorized host and exposed a live endpoint. Provider execution, persistence, custody, reconstruction, immutable VERIFIED receipt, Site activation, and downstream ingestion remain unproven.

## Next executable integration step

Use the existing machine-owned task `StegVerse-org/LLM-adapter#18` to execute the canonical `python scripts/stegdeploy_bootstrap.py deploy` path on an already-authorized machine runtime or restore the existing Render service. Supply provider and custody environment only through that authorized runtime, point the existing verifier at the resulting endpoint, and allow the normal validation workflow to retain the first exact result automatically. Do not create another deployment package or replacement gateway.

## Manual user action requirement

False. The deployment recovery task is repository-owned. The user is not assigned deployment, credential-copying, workflow-dispatch, image-pull, node-start, or evidence-transcription work.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

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
- Machine-owned deployment task: `https://github.com/StegVerse-org/LLM-adapter/issues/18`
- Runtime gate delta: no provider or custody gate is upgraded; the canonical deployment path is confirmed and the remaining blocker is execution on an authorized machine host.