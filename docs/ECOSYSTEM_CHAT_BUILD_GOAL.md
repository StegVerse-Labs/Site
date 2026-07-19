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

GitHub Actions and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. The adapter and Site no longer require CI-derived heartbeat or scheduler-status artifacts. Runtime heartbeat architecture was not modified.

## Proven state

- Existing adapter live verifier implements the required request/provider/custody/reconstruction checks.
- Existing Site acquisition, validation, state recomputation, retention, and propagation consumers are implemented.
- Adapter automation contract assertions are aligned with the heartbeat-corrected activation workflow at commit `7c26041eeeb7f165583308efaedd59e1d17a8c92`.
- Site handoff no longer reports removed CI artifacts as heartbeat blockers.
- Existing adapter stable pending status is the current accepted source evidence.
- Site-local autonomy checks do not complete Ecosystem Chat activation.

## Current blocker

A current live activation execution after the contract repair has not yet been observed and retained. The stable adapter status therefore remains `PENDING` with `live_activation_observation_not_yet_recorded`.

## Next executable integration step

Allow the existing adapter validation and live-activation workflows to execute from commit `7c26041eeeb7f165583308efaedd59e1d17a8c92`. Inspect the resulting live observation and repair only the first actual gateway, provider, persistence, custody, reconstruction, or receipt failure using existing components.

## Manual user action requirement

False.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes current gates passed by real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.

These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Adapter commit: `7c26041eeeb7f165583308efaedd59e1d17a8c92`
- Site handoff commit: `95be2549e7576d742fe0c687da44e3b5ba33b400`
- Advancement: aligned the existing adapter automation contract with the current heartbeat-corrected workflow and corrected the authoritative Site handoff without introducing a new heartbeat, monitor, scheduler, service, or runtime subsystem.
