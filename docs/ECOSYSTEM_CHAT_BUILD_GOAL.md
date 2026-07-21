# Ecosystem Chat Build Goal

## End-to-end outcome

A real governed Ecosystem Chat request completes this path:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

Portable-node expansion remains out of scope until this hosted vertical slice is executed and verified.

## Completion criteria

- A real provider request and response are observed.
- Provider usage is durably persisted without treating local persistence as custody.
- Provider-usage and transition records are accepted by the established custody path.
- Both custody chains reconstruct with PASS evidence.
- The adapter publishes the first immutable VERIFIED activation receipt with zero blockers and all authority flags false.
- Site imports and validates that receipt, recomputes `ACTIVATION_COMPLETE`, and produces a hash-bound propagation packet.
- Publisher, admissibility-wiki, and stegguardian-wiki record verified downstream ingestion.

## Current required runtime path

`StegVerse-Labs/Site/ecosystem-chat.html` → existing browser classifier → bounded live gateway binding → `StegVerse-org/LLM-adapter` governed gateway → existing provider integration → existing persistence and Master-Records custody/reconstruction → immutable adapter receipt → Site acquisition and validation → downstream consumers.

## Authoritative repositories and owners

- Public request surface and Site activation projection: `StegVerse-Labs/Site`
- Runtime gateway and activation evidence: `StegVerse-org/LLM-adapter`
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

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, browser code existence, goal-page check marks, task-tree entries, or propagation packets without verified runtime evidence.

## Heartbeat boundary

GitHub Actions and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. Runtime heartbeat architecture was not modified.

## Proven state

- The existing adapter code defines `/health`, `/api/ecosystem-chat`, and transition-status routes.
- The combined gateway preserves provider, persistence, custody, reconstruction, receipt, and authority boundaries.
- The existing Site classifier, fail-closed fallback, gateway binding, activation consumers, and downstream consumers remain installed.
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
- The verified runtime blocker is before the FastAPI application: the Render hostname exists at the edge, but no Render server is attached behind it.
- The normal adapter `validate` workflow already executes the live vertical-slice verifier.
- Commit `4c0216bb9cbcfc0912d5f44317cd843738b1247b` now writes stable semantic status and retains the current observation directly from that normal validation path.
- Commit `80dbf169faaea7193728efdbe3ff959a50fe56ed` enforces that direct retention contract, removing dependency on a second workflow for durable activation evidence.

## Current blocker

The configured hostname `stegverse-ecosystem-chat-gateway.onrender.com` still returns `x-render-routing: no-server`, so no application process receives the request. The consumed `render.yaml` also remains a fail-closed non-production profile with provider execution disabled, non-durable `/tmp` storage, and no reachable Master-Records service. Provider execution, persistence, custody, reconstruction, immutable VERIFIED receipt, Site activation, and downstream ingestion therefore remain unproven.

## Next executable integration step

Use an already-authorized deployment control plane or existing sovereign node runtime to attach the current `StegVerse-org/LLM-adapter` application and the existing production configuration to a live endpoint, then allow the normal validation workflow to retain the first exact result automatically. Do not create a replacement gateway or remove the existing Render configuration without the required options and removal review.

## Manual user action requirement

False. The remaining boundary is machine-owned deployment capability: no connected tool in the current run can mutate the existing Render control plane, and no already-authorized alternative live host was found. The user is not assigned a deployment, credential-copying, workflow-dispatch, or evidence-transcription task.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-20
- Validation-owned evidence retention: `4c0216bb9cbcfc0912d5f44317cd843738b1247b`
- Retention contract enforcement: `80dbf169faaea7193728efdbe3ff959a50fe56ed`
- Prior diagnostic validation: `29709832124` SUCCESS
- Prior Architecture Guard: `29709832126` SUCCESS
- Prior runtime artifact: `8448772066`
- Prior artifact digest: `sha256:bd129d6e1c46473e56cf40f0b2ab1255cc4912b6fa669299e40aa6ca9fbc1f77`
- Exact deployed edge evidence: `x-render-routing: no-server`
- Runtime gate delta: no provider or custody gate is upgraded; a normal validation run can now retain current evidence without depending on a secondary workflow.
