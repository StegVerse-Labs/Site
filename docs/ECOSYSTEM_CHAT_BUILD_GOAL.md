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

- The existing adapter gateway exposes the governed Ecosystem Chat endpoint, requires transition identity, applies bounded provider and rate policies, persists lifecycle state, and reports custody and reconstruction posture.
- The production blueprint allows the canonical StegVerse Site origins through CORS and configures the existing provider, durable storage, and Master-Records connection.
- The existing Site classifier and fail-closed local fallback remain installed.
- A bounded additive Site binding supplies transition identity and submits non-restricted requests to the existing governed gateway.
- Restricted requests remain local and require separate review. Provider output is not authority.
- The binding is loaded through the existing Ecosystem Chat page loader.
- The existing roadmap and live-tree pages are rebound to the current Ecosystem Chat goal rather than duplicated.
- Adapter evidence retention, immutable receipt retention, Site activation consumers, and downstream consumers remain implemented.
- Draft PR `StegVerse-org/LLM-adapter#8` produced observable validation runs through the existing pull-request trigger.
- The stale no-manual-task checker was repaired at adapter commit `beab2903df8468925006a2b5b4d84215be368340`; its validation step now passes.
- The stale capability-manifest verifier was repaired at adapter commit `3f35b6b0e645f631af837a191f3e2152815a3480`; manifest verification and all earlier provider, usage, and Master-Records custody tests now pass.
- The overbroad live-activation contract assertion was bounded at adapter commit `fcb1b7d8b6bafa7991ad1ce53917a66cec9ee006` so YAML comments are ignored only by the generic heartbeat-term scan while explicit prohibited monitor phrases remain checked against the complete workflow.

## Current blocker

A new validation run for adapter commit `fcb1b7d8b6bafa7991ad1ce53917a66cec9ee006` has not yet been observed. The contract repair is committed, but no live provider response, runtime custody/reconstruction evidence, immutable VERIFIED receipt, Site activation, or downstream ingestion is yet retained.

## Next executable integration step

Observe the validation run produced by adapter commit `fcb1b7d8b6bafa7991ad1ce53917a66cec9ee006`. If validation passes, inspect the existing live-activation execution and repair only its first concrete runtime blocker. If another validation assertion fails, repair only that exact assertion without altering heartbeat architecture.

## Manual user action requirement

False for routine application use. Draft PR execution and repository validation are being operated through connected tooling.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Draft execution probe: `StegVerse-org/LLM-adapter#8`
- No-manual-task repair: `beab2903df8468925006a2b5b4d84215be368340`
- Capability-manifest compatibility repair: `3f35b6b0e645f631af837a191f3e2152815a3480`
- Live-activation contract repair: `fcb1b7d8b6bafa7991ad1ce53917a66cec9ee006`
- Runtime gate delta: none yet; the exact blocking assertion was repaired without deleting the retained comment or weakening the heartbeat boundary.
