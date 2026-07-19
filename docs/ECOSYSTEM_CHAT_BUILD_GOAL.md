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

These existing pages are reused and read the Ecosystem Chat goal state from `data/autonomy/roadmap-status.json` and `data/autonomy/live-status.json`. Green checks require completed or integrated evidence states; red Xs identify unpassed runtime gates. The pages do not grant execution, completion, custody, release, or heartbeat authority.

## What counts as real progress

Execution, repair of an observed runtime failure, verification, custody, reconstruction, immutable receipt production, Site activation, and verified downstream ingestion.

## What does not count as completion

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, browser code existence, goal-page check marks, task-tree entries, or propagation packets without verified runtime evidence.

## Heartbeat boundary

GitHub Actions and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. Runtime heartbeat architecture was not modified.

## Proven state

- The existing adapter gateway code defines `/health`, `/api/ecosystem-chat`, and transition-status routes and preserves the established provider, persistence, custody, reconstruction, receipt, and authority boundaries.
- The production blueprint configures the combined gateway application, durable storage, provider integration, Master-Records connection, CORS, and `/health` health check.
- The existing Site classifier, fail-closed local fallback, and bounded gateway binding remain installed.
- Adapter evidence retention, immutable receipt retention, Site activation consumers, and downstream consumers remain implemented.
- Draft PR `StegVerse-org/LLM-adapter#8` passes the installed validation suite and Architecture Guard.
- The no-manual-task, capability-manifest, live-activation-contract, and iOS workflow-parity blockers were repaired without removing existing runtime architecture.
- Validation run `29706109903` and Architecture Guard run `29706109924` completed successfully.
- An observable deployed probe was added to the existing PR validation path at adapter commits `025ca539f1d110675572d9e924a009a836d8f898` and `8bf65c85acb7c76b3cc98b219e59530fb4baae6d`.
- Validation run `29706857317` executed the real deployed verifier and uploaded artifact `8448172403`.
- The retained receipt proves the configured host resolves and responds, but `/health`, `/api/ecosystem-chat`, and `/api/transitions/{id}` each returned HTTP 404.
- The receipt remains `PENDING`; all authority and repository-mutation flags remain false.
- The existing production blueprint was bounded on the probe branch at adapter commit `33d652229a80246ab0b0384409b13b2c6c285a11` with `renderSubdomainPolicy: enabled` for the already-intended public gateway URL.

## Current blocker

The deployed `onrender.com` gateway hostname is reachable but serves 404 for every required gateway route. Repository code and the production blueprint define those routes, so the current boundary is deployment/service exposure rather than DNS, transport, provider logic, or Master-Records logic. The bounded Render subdomain-policy repair is validated only on the probe branch and is not yet deployed.

## Next executable integration step

Complete validation for adapter commit `33d652229a80246ab0b0384409b13b2c6c285a11`, integrate the bounded production-blueprint repair through the established repository path, allow the existing `checksPass` deployment policy to operate, then rerun the same deployed verifier. Repair only the first remaining concrete runtime blocker.

## Manual user action requirement

False for routine repository work. The remaining deployment action must use the already-established Render Blueprint and `checksPass` authority; no new deployment, release, custody, execution, or governance authority is being granted.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Draft execution probe: `StegVerse-org/LLM-adapter#8`
- Green validation run: `29706109903`
- Green Architecture Guard run: `29706109924`
- Observable deployed-probe commits: `025ca539f1d110675572d9e924a009a836d8f898`, `8bf65c85acb7c76b3cc98b219e59530fb4baae6d`
- Deployed-probe validation run: `29706857317`
- Deployed receipt artifact: `8448172403`
- Exact runtime failure: HTTP 404 at health, chat, and transition routes
- Bounded Render exposure repair: `33d652229a80246ab0b0384409b13b2c6c285a11`
- Runtime gate delta: the real deployed path is now EXECUTED and its first concrete failure is retained; provider, custody, reconstruction, receipt verification, Site activation, and propagation remain unproven.
