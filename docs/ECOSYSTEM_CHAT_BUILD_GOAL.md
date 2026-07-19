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

Execution, repair, verification, custody, reconstruction, immutable receipt production, Site activation, and verified downstream ingestion.

## What does not count as completion

Documentation, status files, monitors, CI schedules, installed workflows, pending imports, local persistence, or propagation packets without verified runtime evidence.

## Proven state

- Existing Site acquisition, validation, state recomputation, retention, and propagation consumers are implemented.
- Existing adapter stable pending status is the current accepted source evidence.
- Site-local autonomy checks do not complete Ecosystem Chat activation.
- The adapter has removed the incorrect GitHub-derived heartbeat and scheduler-status artifacts.
- Site has been repaired to observe only stable activation status and the immutable VERIFIED receipt; it does not define or modify runtime heartbeat authority.

## Current blocker

The adapter has not yet published an immutable VERIFIED receipt proving real provider use, custody, reconstruction, and zero blockers.

## Next executable integration step

Execute the existing adapter activation-verification path and retain its exact runtime result. Repair only the first observed failing runtime boundary using existing provider, custody, reconstruction, and governance components.

## Manual user action requirement

False.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Site commits: `427f9c6709a7c6a889e07d5a85a1b2226973fd90`, `bbdc5852221bf032a494f20109e70258e4f9f998`
- Advancement: repaired Site’s stale dependency on removed CI-derived heartbeat/scheduler artifacts while preserving the established activation evidence path.
