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

These existing pages are reused and now read the Ecosystem Chat goal state from `data/autonomy/roadmap-status.json` and `data/autonomy/live-status.json`. Green checks require completed or integrated evidence states; red Xs identify unpassed runtime gates. The pages do not grant execution, completion, custody, release, or heartbeat authority.

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
- Both monitoring pages now use explicit status marks and bounded responsive card layouts.
- Adapter evidence retention, immutable receipt retention, Site activation consumers, and downstream consumers remain implemented.

## Current blocker

The browser-to-gateway binding is IMPLEMENTED and INTEGRATED in repository state but has not yet been EXECUTED or VERIFIED from a deployed public Site origin. No real browser request, provider response, usage persistence, custody, reconstruction, or receipt evidence was produced during this cycle.

The goal and prompt-level monitoring pages accurately expose this boundary but do not advance the runtime gate by themselves.

## Next executable integration step

Execute one non-restricted request through the deployed `ecosystem-chat.html` surface. Inspect the returned gateway receipt line for provider use, local persistence, provider-usage custody and reconstruction, and transition custody and reconstruction. Repair only the first concrete failure. If the public Site has not deployed the binding, use the existing Site deployment path rather than creating another chat surface or gateway.

## Manual user action requirement

False for routine application use. A platform-owner action is required only if the existing Site deployment or GitHub Actions policy cannot be operated through connected tooling.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes gates passed by a current real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Goal-page integration: `7c1020e4f83c2ba43a4e1a17c288ea25e905ab9a`
- Prompt-tree integration: `b56bd49a6adf8b5053282ffb158ce5882c18dbd8`
- Goal data update: `310d0873143faceae61fc35fafd06bb89a232353`
- Prompt-tree data update: `2371b90b0f00c161b382fd8a852da03ba542cb7b`
- Advancement: reused the existing monitoring pages, rebound them to the current Ecosystem Chat vertical slice, and repaired narrow-screen card containment without creating replacement pages or changing the declared goal.
