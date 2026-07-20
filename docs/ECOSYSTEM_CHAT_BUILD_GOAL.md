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
- The consumed `render.yaml` retained the existing free plan, provider-disabled posture, non-durable storage, and external Master-Records settings, but omitted an explicit public subdomain policy.
- PR #9 added only `renderSubdomainPolicy: enabled` to that existing service.
- Validation run `29708558752` and Architecture Guard run `29708558778` passed.
- PR #9 was merged as `1393a06c35a9727b1734a4b7a40ccd62e43e75e5` through the existing repository path.
- Immediate post-merge probe run `29708684759` retained artifact `8448582241` and still observed plain-text HTTP 404 at `/health`, `/api/ecosystem-chat`, and `/api/transitions/{id}`.
- The existing validation job was rerun directly after the deployment window without another repository change.
- Delayed attempt 2 retained artifact `8448604301`, digest `sha256:80a9b91723eeed13712d71ab75163c93c039e36f1f2b1ba50ca834c97e2de404`, and again observed plain-text HTTP 404 at all three required routes at `2026-07-20T00:00:03Z`.
- The delayed result confirms a persistent Render service-binding problem rather than DNS failure, transient transport failure, or an observation taken before deployment had time to complete.

## Current blocker

The repository-side route implementation and consumed Blueprint have been inspected and repaired, but the live hostname still serves plain-text HTTP 404 for every required route after a delayed verifier rerun. The unresolved boundary is the existing Render control-plane binding: which Render service owns `stegverse-ecosystem-chat-gateway.onrender.com`, which repository and branch it follows, and whether it is actually managed from this Blueprint. Provider execution, persistence, custody, reconstruction, immutable VERIFIED receipt, Site activation, and downstream ingestion remain unproven.

## Next executable integration step

Inspect the existing Render service-to-repository, branch, and Blueprint binding for `stegverse-ecosystem-chat-gateway.onrender.com`. Bind that existing service to `StegVerse-org/LLM-adapter` main and the consumed `render.yaml` if it is currently detached or pointed elsewhere, then rerun the same verifier. Do not create a replacement gateway unless the existing Render service cannot be recovered through its current control plane.

## Manual user action requirement

False for routine repository work. The current blocker requires access to the existing Render control plane; no new deployment, release, custody, execution, publication, or governance authority is granted by this record.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Initial merged integration: `ce9027d0d3bf79f93b92bc764880a21cd848afda`
- Post-merge deployed probe run: `29708519759`
- Post-merge deployed receipt artifact: `8448551905`
- Consumed Blueprint repair: `3a885095fd3f695da3c852ced0543969de295493`
- Repair validation: `29708558752` SUCCESS
- Repair Architecture Guard: `29708558778` SUCCESS
- Merged repair: `1393a06c35a9727b1734a4b7a40ccd62e43e75e5`
- Immediate post-merge probe run: `29708684759`
- Immediate post-merge probe artifact: `8448582241`
- Delayed verifier rerun job: `88249881505`
- Delayed verifier artifact: `8448604301`
- Delayed observed result: unchanged HTTP 404 at health, chat, and transition routes
- Runtime gate delta: the persistent live failure is now classified at the existing Render control-plane service binding; no provider or custody gate is upgraded.