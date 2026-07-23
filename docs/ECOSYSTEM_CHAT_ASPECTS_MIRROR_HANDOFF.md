# Ecosystem Chat Governed Aspects Mirror Handoff

## Source of truth

This file is the continuation record for defining every governed aspect of Ecosystem Chat interactions with the same separation applied to contribution value.

Repository-wide activation remains governed by `docs/SITE_MIRROR_HANDOFF.md`. Value-specific continuation remains in `docs/ECOSYSTEM_CHAT_VALUE_MIRROR_HANDOFF.md`.

## Goal

```text
Define every material aspect of a governed interaction separately,
prevent one aspect from silently granting another,
preserve evidence, uncertainty, disagreement, and lifecycle state,
and provide machine-readable contracts that can become canonical events,
validators, renderers, custody records, reconstruction checks,
and downstream projection receipts.
```

## Implemented

```text
docs/ECOSYSTEM_CHAT_GOVERNED_ASPECT_MODEL.md
data/ecosystem-chat-governed-aspects.registry.json
scripts/check_ecosystem_chat_governed_aspects.py
scripts/check_ecosystem_chat_value_integration.py transitive registry validation binding
```

## Defined aspects

The initial registry defines 34 independently governed aspects:

```text
identity and participation
source and provenance
ownership and control
consent and permission
privacy and sensitivity
contribution
causal influence
attribution
authorship
originality and novelty
scarcity and substitutability
labor and effort
compute and infrastructure
outcome and utility
realized value
cost and externalities
risk and harm
admissibility
authority and delegation
standing and capability
reward and incentive
distribution and allocation
settlement
jurisdiction and legal posture
temporal state and decay
dispute and competing claims
fraud, gaming, and manipulation
collective and network contribution
derivation and transformation
disclosure and projection
custody and reconstruction
confidence and uncertainty
recovery and correction
public claim and communication
```

Each registry entry contains:

```text
stable aspect id
aspect family
governing question
facts the aspect does not prove
required evidence/reference classes
allowed status values
```

## Global invariants

```text
no aspect silently grants another
missing evidence resolves to UNRESOLVED
authoritative changes are governed events
human-facing simplification does not remove distinctions
browser state grants no authority, custody, payment, or settlement
competing determinations remain visible
history is append-only under governed correction or supersession
sensitivity is not an automatic value multiplier
success does not erase invalid consent or externalized harm
downstream projection requires purpose, permission, redaction, and minimum disclosure
```

## Validation posture

```text
Human-readable aspect model: IMPLEMENTED
Machine-readable registry: IMPLEMENTED
Registry validator: IMPLEMENTED
Required aspect count: 34
Default missing-evidence posture: UNRESOLVED
Transitive canonical application validation binding: IMPLEMENTED
Aspect event schema: NOT YET IMPLEMENTED
Aspect renderer: NOT YET IMPLEMENTED
Cross-aspect conflict fixtures: NOT YET IMPLEMENTED
Gateway-origin aspect events: NOT YET IMPLEMENTED
Custody and reconstruction: NOT YET IMPLEMENTED
Authority effect: NONE
```

## Next Site work

Destination `StegVerse-Labs/Site`:

```text
Create a canonical governed aspect-event schema.
Create fixtures representing one interaction across all applicable aspects.
Create cross-aspect conflict fixtures and fail-closed validators.
Render an aspect matrix inside Ecosystem Node with human, governed, and split projections.
Allow selection of a message, claim, decision, artifact, or execution event to reveal all attached aspect records.
Add raw JSON/JSONL aspect export without creating an independent authoritative record.
Add role-based and locale-aware aspect disclosure.
Add static and executable browser behavior tests.
Observe the complete validation chain in CI and on deployed preview.
```

## Required cross-aspect conflicts

The next validation layer must reject or quarantine at least these combinations:

```text
ownership verified + consent revoked + reuse allowed
high realized value + inadmissible transition + distribution authorized
authorship human-only + model generation evidence present
captured record + derivation method asserted
public projection allowed + restricted sensitivity + no redaction
settled + no settlement receipt
authority active + delegation expired
standing high + execution permission inferred
novelty publicly established + no comparison boundary
interaction-only reuse + downstream publication allowed
revoked claim + later stage advancement
successful outcome + externalized harm omitted
```

## Upstream destinations

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical aspect events before rendering.
Bind aspect records to stable event_id, transition_id, claim_id, artifact_id, and execution_id values.
Sign and hash aspect events.
Evaluate cross-aspect conflicts before commit.
Emit refusal, quarantine, override, revocation, recovery, and correction events where required.
```

Destination `master-records/orchestration`:

```text
Custody aspect events, policies, evidence, conflicts, decisions, and receipts.
Reconstruct each aspect independently and as a coupled interaction state.
Verify that no aspect silently granted another.
Return authenticated reconstruction and disclosure receipts.
```

## Downstream destinations after verified Site activation

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Release posture

```text
Aspect definition layer: COMPLETE FOR INITIAL 34-ASPECT MODEL
Machine-readable registry: COMPLETE
Static validation binding: COMPLETE
Canonical runtime implementation: PENDING
CI observation: PENDING
Deployment observation: PENDING
Release/tag readiness: NOT YET REACHED
```
