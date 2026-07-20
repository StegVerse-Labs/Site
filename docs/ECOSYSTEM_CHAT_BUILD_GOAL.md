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
- The verified blocker is therefore before the FastAPI application: the Render hostname exists at the edge, but no Render server is attached behind it.

## Current blocker

Render returns `x-render-routing: no-server` for every required route. The unresolved boundary is the existing Render control-plane resource: restore or attach the existing `stegverse-ecosystem-chat-gateway` service behind `stegverse-ecosystem-chat-gateway.onrender.com`, with source repository `StegVerse-org/LLM-adapter`, branch `main`, and the existing start command. Provider execution, persistence, custody, reconstruction, immutable VERIFIED receipt, Site activation, and downstream ingestion remain unproven.

## Next executable integration step

In the existing Render control plane, locate the service or hostname record for `stegverse-ecosystem-chat-gateway.onrender.com`. Restore or attach the existing service to `StegVerse-org/LLM-adapter` branch `main`, confirm the start command `python -m llm_adapter.custody_worker && uvicorn llm_adapter.combined_gateway:app --host 0.0.0.0 --port $PORT`, deploy, and rerun the existing verifier. Do not create a replacement gateway unless the existing Render resource is proven unrecoverable and a replacement decision is explicitly approved.

## Manual user action requirement

A Render account owner action is currently required because no connected Render control-plane tool is available in this session. No new deployment, release, custody, execution, publication, or governance authority is granted by this record.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-20
- Diagnostic verifier commit: `5814efd7657a832f55138998b6e3eadad7200d59`
- Validation: `29709832124` SUCCESS
- Architecture Guard: `29709832126` SUCCESS
- Runtime artifact: `8448772066`
- Artifact digest: `sha256:bd129d6e1c46473e56cf40f0b2ab1255cc4912b6fa669299e40aa6ca9fbc1f77`
- Exact edge evidence: `x-render-routing: no-server`
- Merged verifier enhancement: `efb7c4e49a2773c976e4494d5aa84618554a768d`
- Runtime gate delta: the failure is now verified at the Render edge before application execution; no provider or custody gate is upgraded.
