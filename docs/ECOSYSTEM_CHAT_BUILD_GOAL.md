# Ecosystem Chat Build Goal

## End-to-end outcome

A real governed Ecosystem Chat request completes the path:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

Portable-node expansion is out of scope until this first hosted vertical slice is executed and verified.

## Completion criteria

- A real provider request and response are observed.
- Provider usage is durably persisted without treating local persistence as custody.
- Provider-usage and transition records are accepted by the established custody path.
- Both custody chains reconstruct with PASS evidence.
- The adapter publishes the first immutable VERIFIED activation receipt with zero blockers and all authority flags false.
- Site imports and validates that receipt, recomputes `ACTIVATION_COMPLETE`, and produces a hash-bound propagation packet.
- Publisher, admissibility-wiki, and stegguardian-wiki record verified downstream ingestion.

## Current required runtime path

`StegVerse-org/LLM-adapter` governed gateway → existing provider integration → existing persistence and Master-Records custody/reconstruction → immutable adapter receipt → `StegVerse-Labs/Site` acquisition and validation → downstream consumers.

## Authoritative repositories and owners

- Runtime gateway and activation evidence: `StegVerse-org/LLM-adapter`
- Site activation projection: `StegVerse-Labs/Site`
- Custody and reconstruction: existing Master-Records implementation referenced by adapter evidence
- Downstream publication projection: `GCAT-BCAT-Engine/Publisher`
- Downstream admissibility projection: `StegVerse-Labs/admissibility-wiki`
- Downstream guardian projection: `StegVerse-002/stegguardian-wiki`

## What counts as real progress

Execution, repair of an observed runtime failure, verification, custody, reconstruction, immutable receipt production, Site activation, and verified downstream ingestion.

## What does not count as completion

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, or propagation packets without verified runtime evidence.

## Heartbeat boundary

GitHub Actions and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. The adapter and Site do not require CI-derived heartbeat or scheduler-status artifacts. Runtime heartbeat architecture was not modified.

## Proven state

- Existing adapter live verifier implements the required request/provider/custody/reconstruction checks.
- Existing Site acquisition, validation, state recomputation, retention, and propagation consumers are implemented.
- Adapter automation contract assertions are aligned with the heartbeat-corrected activation workflow.
- The existing activation workflow now persists both the detailed latest live observation and stable semantic status to the adapter repository when they change.
- The immutable VERIFIED receipt remains separately retained only after zero-blocker verification.
- Site handoff no longer reports removed CI artifacts as heartbeat blockers.
- Existing adapter stable pending status remains the current accepted runtime source until the next detailed observation is produced.
- Site-local autonomy checks do not complete Ecosystem Chat activation.

## Current blocker

The repaired activation workflow has not yet produced the next repository-retained `receipts/ecosystem-chat-live-activation.latest.json` observation. Therefore the first actual gateway, provider, persistence, custody, reconstruction, or receipt failure is still not observable.

The stable adapter status remains `PENDING` with `live_activation_observation_not_yet_recorded` until that execution occurs.

## Next executable integration step

Execute the existing adapter live-activation workflow after commits `58e61aef236d847885a3eb3750a8b20697120488` and `06ee40df1370eec398fca29105f0cba8ab0463a9`. Inspect the repository-retained detailed observation and repair only its first reported runtime blocker using existing components.

## Manual user action requirement

False.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes current gates passed by real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.

These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Adapter evidence-retention commits: `a5e0b92ac58d924e77e8cc43f2a0d3d2ee8153ae`, `58e61aef236d847885a3eb3750a8b20697120488`
- Adapter contract commit: `06ee40df1370eec398fca29105f0cba8ab0463a9`
- Advancement: repaired the existing live-activation workflow so its already-generated detailed pending or verified observation is durably retained in repository state, eliminating dependence on expiring workflow artifacts for the first actual runtime blocker.
