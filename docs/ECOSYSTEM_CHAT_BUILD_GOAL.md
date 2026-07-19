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

## What counts as real progress

Execution, repair of an observed runtime failure, verification, custody, reconstruction, immutable receipt production, Site activation, and verified downstream ingestion.

## What does not count as completion

Documentation, status files, handoffs, monitors, CI schedules, installed workflows, pending imports, local persistence, browser code existence, or propagation packets without verified runtime evidence.

## Heartbeat boundary

GitHub Actions and Site evidence-retention workflows do not define the StegVerse runtime heartbeat. Runtime heartbeat architecture was not modified.

## Proven state

- The existing adapter gateway exposes the governed Ecosystem Chat endpoint, requires transition identity, applies bounded provider and rate policies, persists lifecycle state, and reports custody and reconstruction posture.
- The production blueprint allows the canonical StegVerse Site origins through CORS and configures the existing provider, durable storage, and Master-Records connection.
- The existing Site classifier and fail-closed local fallback remain installed.
- A bounded additive Site binding now supplies transition identity and submits non-restricted requests to the existing governed gateway.
- Restricted requests remain local and require separate review. Provider output is not authority.
- The binding is loaded through the existing Ecosystem Chat page loader.
- JavaScript syntax validation for the binding passed with `node --check`.
- Adapter evidence retention, immutable receipt retention, Site activation consumers, and downstream consumers remain implemented.

## Current blocker

The browser-to-gateway binding is IMPLEMENTED and INTEGRATED in repository state but has not yet been EXECUTED or VERIFIED from the deployed public Site. No real browser request, provider response, usage persistence, custody, reconstruction, or receipt evidence was produced during this cycle.

The separate adapter live-activation workflow also has not produced a repository-retained detailed observation, and the available GitHub interfaces still do not expose Actions settings or dispatch.

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
- Site live-binding commit: `4b1cf2472a510d64c3803d42cf85451594198fce`
- Site loader integration commit: `b6f087d6f0c79edc660e53eb1b726bf0519ea01c`
- Advancement: reused the existing Site classifier and adapter gateway to connect the public Ecosystem Chat form to the governed provider, custody, and reconstruction path while retaining restricted-request refusal and local fail-closed fallback.
