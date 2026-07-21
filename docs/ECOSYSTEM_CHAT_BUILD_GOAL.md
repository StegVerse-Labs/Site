# Ecosystem Chat Build Goal

## End-to-end outcome

A real governed Ecosystem Chat request completes this path:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

The existing portable-node Ecosystem Chat runtime is the active StegVerse-owned execution path for this vertical slice. It is not a separate replacement gateway and it does not depend on Render.

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
- Latest StegVerse local-node cycle: https://github.com/StegVerse-Labs/Site/blob/main/docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_STEGVERSE_LOCAL_NODE_DISCOVERY.md
- Runtime gateway and canonical StegDeploy implementation: https://github.com/StegVerse-org/LLM-adapter
- StegVerse node advertisement PR: https://github.com/StegVerse-org/LLM-adapter/pull/24
- Site verified local-node binding PR: https://github.com/StegVerse-Labs/Site/pull/29
- Corrected active-path issue: https://github.com/StegVerse-Labs/Site/issues/24
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

https://stegverse.org/ecosystem-chat.html → existing browser classifier → verified loopback StegVerse-node discovery → health-bound node advertisement → existing https://github.com/StegVerse-org/LLM-adapter governed gateway running through canonical StegDeploy/portable-node lifecycle → existing provider integration → existing persistence and https://github.com/master-records/core-lite custody/reconstruction → immutable adapter receipt → Site acquisition and validation → downstream consumers.

No external hosting platform is authoritative in this path.

## Authoritative repositories and owners

- Public request surface and Site activation projection: https://github.com/StegVerse-Labs/Site
- Runtime gateway, canonical StegDeploy runtime, portable-node supervision, node advertisement, and activation evidence: https://github.com/StegVerse-org/LLM-adapter
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

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, browser code existence, node-advertisement code existence, goal-page check marks, task-tree entries, container-image existence, pull-request readiness, or propagation packets without verified runtime evidence.

Provider-replacement, billing, export, migration-gate, or retirement scaffolding does not advance this declared goal unless it directly enables the current Ecosystem Chat runtime path.

## Heartbeat boundary

GitHub Actions, portable-node process supervision, OCI image publication, endpoint discovery, and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. Runtime heartbeat architecture was not modified.

## Proven state

- The existing adapter code defines `/health`, `/api/ecosystem-chat`, and transition-status routes.
- The combined gateway preserves provider, persistence, custody, reconstruction, receipt, and authority boundaries.
- The existing Site classifier, fail-closed fallback, activation consumers, and downstream consumers remain installed.
- PR #14 merged the canonical provider-neutral StegDeploy runtime: `Dockerfile`, `compose.stegdeploy.yaml`, `scripts/container-entrypoint.sh`, `scripts/stegdeploy_bootstrap.py`, `.github/workflows/stegdeploy-image.yml`, persistent storage, health verification, image provenance, and a deployment receipt.
- PR #15 merged zero-touch portable-node bootstrap.
- PR #16 merged autonomous portable-node service lifecycle and reconstruction.
- PR #17 merged user-level automatic startup registration across Linux, macOS, and Windows.
- PR #19 merged autonomous runtime hardening.
- PR #20 merged singleton ownership and stale-lock repair.
- PR #8 was merged as `ce9027d0d3bf79f93b92bc764880a21cd848afda` after full validation and Architecture Guard success.
- Deployed probe run `29706857317` retained artifact `8448172403`; the configured historical Render host resolved but all required routes returned HTTP 404.
- `render-production.yaml` was not the consumed default Blueprint path.
- Post-merge probe run `29708519759` retained artifact `8448551905` and confirmed the same HTTP 404 result after the non-consumed production-file repair.
- PR #9 added `renderSubdomainPolicy: enabled` to the consumed `render.yaml` and merged as `1393a06c35a9727b1734a4b7a40ccd62e43e75e5` after validation and Architecture Guard success.
- Immediate and delayed probes continued to return plain-text HTTP 404 at all required routes.
- PR #11 bounded the existing verifier to retain final URLs and a narrow non-secret response-header allowlist.
- Validation run `29709832124` and Architecture Guard run `29709832126` passed.
- Probe artifact `8448772066`, digest `sha256:bd129d6e1c46473e56cf40f0b2ab1255cc4912b6fa669299e40aa6ca9fbc1f77`, retained `server: cloudflare`, `content-type: text/plain; charset=utf-8`, and `x-render-routing: no-server` for health, chat, and transition requests.
- PR #11 merged as `efb7c4e49a2773c976e4494d5aa84618554a768d`.
- The normal adapter `validate` workflow already executes the live vertical-slice verifier.
- Commit `4c0216bb9cbcfc0912d5f44317cd843738b1247b` writes stable semantic status and retains the current observation directly from that normal validation path.
- Commit `80dbf169faaea7193728efdbe3ff959a50fe56ed` enforces that direct retention contract.
- Commit `042faaaca4d1c1babc8d7d7bc8c8e408356cc337` made the portable-node host binding configurable while preserving loopback as the fail-closed default.
- Commit `3f8165686b86419cadfdd093a1e5a3876915801f` corrected the node daemon so authorized provider, custody, host, and port settings are preserved instead of overwritten by defaults.
- Commits `97bef70d3683cfae7029cb9bc368f0b17d955c9c` and `398a4a39523d2a21b2331866593a92c2eba4dc81` added and bound portable-node runtime contract checks to the existing validation path.
- Commits `0eaac3abc6c3691dae73916b1bd6f135e0a9955f`, `ea9efe1c621552f609e1a6d929964135b52476e8`, and `4f2e56913462a74944d67c0e91afb484fe0df643` added overlapping portable-node image packaging after the canonical StegDeploy path already existed. These files are retained but are not designated canonical pending explicit consolidation or removal approval.
- https://github.com/StegVerse-org/core-node-runtime-demo is an existing private governed runtime comparison boundary with Master-Records witness-ready outputs and comparable path reports.
- Commit `9eb2893cffd2fc4e8c7dfc8ae9dfb2b4d96344c2` added a repository-owned StegDeploy runtime intake workflow that pulls the canonical image, launches it fail-closed on a GitHub machine runner, verifies live health, executes the existing core-node comparison pipeline, and persists a hashed compatibility receipt.
- Commit `62b87d6918977f6bcbc909955b4a765460e04238` integrated that intake into the established `.github/workflows/validate.yml` path on `main`.
- Commit `abd8fc8858d3ec46a8d24d5b649ee3cb520c68c4` explicitly bound the existing `push` trigger to `main` without changing runtime steps, permissions, receipt construction, or authority boundaries.
- The expected `receipts/stegdeploy-runtime-intake.latest.json` does not yet exist.
- The available commit-workflow lookup is limited to pull-request-triggered runs; its empty result does not prove that no push-triggered run occurred.
- No step-level push-run logs were available through the connected path, and empty commit-status results are not equivalent to absence of GitHub Actions check runs.
- Machine-owned continuation is tracked by https://github.com/StegVerse-org/core-node-runtime-demo/issues/5 and https://github.com/StegVerse-org/LLM-adapter/issues/18.
- An adjacent persistent-host search evaluated `StegVerse-002/micro-node-runtime`, `StegVerse-Labs/media-runtime`, `StegVerse-org/HPS-runtime`, and `StegVerse-Labs/broadcast-runtime`; no already-authorized persistent host, self-hosted runner, deployment agent, or public-service contract was found.
- `StegVerse-002/micro-node-runtime` remains reusable as a deterministic governance, receipt, return-path, and reconstruction pattern, but it explicitly does not claim external deployment or host authority.
- PR https://github.com/StegVerse-org/LLM-adapter/pull/23 remains retained, non-canonical, unmerged, and unapplied. It must not be merged or removed without the applicable authority and removal decisions.
- Adapter PR https://github.com/StegVerse-org/LLM-adapter/pull/24 implements `stegverse.node.endpoint-advertisement.v1`, health binding, canonical SHA-256, non-authority fields, and Site CORS support.
- Site PR https://github.com/StegVerse-Labs/Site/pull/29 removes the hard-coded Render endpoint and implements verified loopback StegVerse-node discovery.
- Adapter Architecture Guard run `29856876975` passed.
- Adapter validation run `29856876922` is executing at the latest observation.
- Site validation run `29856890380` stopped before application validation because the pre-existing workflow inventory reported five operational workflows while its expected set contained three.

## Current blocker

The source-level StegVerse-owned discovery path is IMPLEMENTED on adapter PR #24 and Site PR #29 but is not yet merged or exercised by a live portable node.

The first current validation boundary is completion of adapter run `29856876922`. The Site aggregate is independently blocked before application validation by the existing workflow-inventory mismatch involving `autonomy-telemetry.yml` and `sync-executive-rhetoric-ledger.yml`; this cycle did not remove, disable, rename, or reclassify those workflows.

Provider execution, persistence, custody, reconstruction, immutable VERIFIED receipt, Site activation, and downstream ingestion remain unproven.

## Next executable integration step

Complete adapter PR https://github.com/StegVerse-org/LLM-adapter/pull/24 validation and repair only a concrete failure if one appears. Validate the focused Site local-node contract on https://github.com/StegVerse-Labs/Site/pull/29 without changing unrelated workflow architecture. Then merge the bounded adapter and Site integrations, launch the existing zero-touch portable node, and execute one real Site request through the verified loopback endpoint.

Do not create another executor, deployment package, external host adapter, gateway, receipt schema, workflow scheduler, or heartbeat mechanism.

## Manual user action requirement

No routine manual repository or evidence task is assigned to the user. No Render setup, endpoint copying, browser credential entry, workflow dispatch, receipt construction, or evidence transcription is required.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.
- This cycle advances StegVerse-owned endpoint discovery from missing to IMPLEMENTED on two bounded PRs.
- Runtime gate completion remains unchanged because no live portable node or provider request was executed.

## Latest meaningful goal advancement

- Date: 2026-07-21
- Canonical provider-neutral runtime: merged PR #14
- Zero-touch bootstrap: merged PR #15
- Autonomous node lifecycle: merged PR #16
- Automatic user-level startup: merged PR #17
- Runtime hardening: merged PR #19
- Singleton ownership and stale-lock repair: merged PR #20
- Portable-node binding repair: `042faaaca4d1c1babc8d7d7bc8c8e408356cc337`
- Authorized environment preservation: `3f8165686b86419cadfdd093a1e5a3876915801f`
- Portable-node runtime tests: `97bef70d3683cfae7029cb9bc368f0b17d955c9c`
- Existing-validation contract binding: `398a4a39523d2a21b2331866593a92c2eba4dc81`
- Core-node machine executor: `9eb2893cffd2fc4e8c7dfc8ae9dfb2b4d96344c2`
- Established-workflow integration: `62b87d6918977f6bcbc909955b4a765460e04238`
- Explicit main-branch trigger binding: `abd8fc8858d3ec46a8d24d5b649ee3cb520c68c4`
- StegVerse node advertisement PR: https://github.com/StegVerse-org/LLM-adapter/pull/24
- Site verified local-node binding PR: https://github.com/StegVerse-Labs/Site/pull/29
- Adapter Architecture Guard: https://github.com/StegVerse-org/LLM-adapter/actions/runs/29856876975
- Adapter validation: https://github.com/StegVerse-org/LLM-adapter/actions/runs/29856876922
- Site validation: https://github.com/StegVerse-Labs/Site/actions/runs/29856890380
- Active-building cycle: https://github.com/StegVerse-Labs/Site/blob/main/docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_STEGVERSE_LOCAL_NODE_DISCOVERY.md
- Corrected active-path issue: https://github.com/StegVerse-Labs/Site/issues/24
- Runtime gate delta remains zero.

---

## Current authoritative machine-execution update — 2026-07-21

This section supersedes only the earlier statements that the core-node machine result and compatibility receipt were unobserved.

- Current cycle record: https://github.com/StegVerse-Labs/Site/blob/agent/ecosystem-chat-machine-execution-state/docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_MACHINE_EXECUTION.md
- Core-node PR #6 merged as `d8a4f82bfaa596b26463d3ea2ff11fd923477b08`.
- Core-node PR #8 merged as `6f40cb7110823c48527efadd90c13d87b5cf2455`.
- Machine-execution run `29853848999` passed the existing pipeline, canonical source checkout, canonical Dockerfile build, fail-closed gateway start, live `/health`, compatibility enforcement, and evidence upload.
- Canonical authoritative-source runtime compatibility is VERIFIED.
- Published GHCR package compatibility remains BLOCKED / UNPROVEN.
- Persistent public deployment is NOT DEPLOYED and the public gateway is NOT LIVE.
- Real provider response, usage persistence, custody, reconstruction, immutable activation receipt, Site activation, and downstream ingestion remain UNPROVEN.

### Current blocker

No already-authorized persistent host is connected to the existing canonical StegDeploy runtime. The existing Render alignment remains a candidate subject to the recorded platform-owner decision. Package publication or access also remains unresolved, but it no longer blocks machine verification of the authoritative source runtime.

### Next executable integration step

Run the verified existing canonical runtime on an already-authorized persistent host, execute one governed request, and pass the result through the existing adapter verifier. Repair only the first concrete provider, persistence, custody, reconstruction, or receipt failure.

### Manual user action requirement

False for routine repository work. A platform-owner decision remains required before applying hosted infrastructure that may incur charges or enabling real provider and custody configuration.

### Latest meaningful goal advancement

- Date: 2026-07-21
- Machine-execution merge: `6f40cb7110823c48527efadd90c13d87b5cf2455`
- Verified machine run: `29853848999`
- Runtime gate delta: machine execution and fail-closed health advanced to VERIFIED; all later end-to-end gates remain unproven.
