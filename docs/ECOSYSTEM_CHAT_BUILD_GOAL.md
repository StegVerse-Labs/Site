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

GitHub Actions and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. Runtime heartbeat architecture was not modified.

## Proven state

- Existing adapter live verifier implements the required request/provider/custody/reconstruction checks.
- Existing Site acquisition, validation, state recomputation, retention, and propagation consumers are implemented.
- Adapter automation contract assertions are aligned with the heartbeat-corrected activation workflow.
- The activation workflow persists both the detailed latest observation and stable semantic status when it executes and either changes.
- The immutable VERIFIED receipt remains separately retained only after zero-blocker verification.
- The adapter repository is public, active, on `main`, and available through an administrative GitHub connection.
- Repeated qualifying adapter commits exist after the workflow repair.
- No post-repair workflow-generated commit or repository-retained `receipts/ecosystem-chat-live-activation.latest.json` is observable.

## Current blocker

The code-level trigger, verifier, contract, and evidence-retention paths are present, but repository-level GitHub Actions execution has not been observed after repeated qualifying pushes.

The connected GitHub application does not expose repository or organization Actions policy settings or workflow dispatch. The prescribed GitHub CLI fallback cannot be used in the current execution environment because `gh` is not installed. Therefore the exact Actions setting or run-level failure cannot currently be inspected or corrected through the available interfaces.

This is not evidence that Actions are disabled and is not a heartbeat failure. The stable adapter status remains `PENDING` with `live_activation_observation_not_yet_recorded`.

## Next executable integration step

Use an authorized interface that exposes GitHub Actions settings or workflow dispatch for `StegVerse-org/LLM-adapter`. Confirm repository and organization Actions execution policy, execute the existing `Ecosystem Chat Live Activation` workflow, and inspect its repository-retained detailed observation. Repair only the first actual gateway, provider, persistence, custody, reconstruction, or receipt blocker.

## Manual user action requirement

No routine Ecosystem Chat action is required. Progress is currently blocked by the absence of an authorized Actions settings/dispatch interface in this session.

## Progress accounting

- Implementation coverage describes code and integrations that exist.
- Runtime gate completion describes current gates passed by real execution.
- Evidence state uses DESIGNED, IMPLEMENTED, INTEGRATED, EXECUTED, VERIFIED, DEPLOYED, LIVE, and PROPAGATED.
- These measures must not be collapsed into one percentage.

## Latest meaningful goal advancement

- Date: 2026-07-19
- Adapter evidence-retention commits: `a5e0b92ac58d924e77e8cc43f2a0d3d2ee8153ae`, `58e61aef236d847885a3eb3750a8b20697120488`
- Adapter contract commit: `06ee40df1370eec398fca29105f0cba8ab0463a9`
- Latest finding: repository history confirms no workflow-generated evidence commit after the qualifying repair commits; connector settings/dispatch are unavailable and the CLI fallback is not installed.
