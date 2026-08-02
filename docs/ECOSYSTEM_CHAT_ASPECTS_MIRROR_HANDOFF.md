# Ecosystem Chat Governed Aspects Mirror Handoff

## Source of truth

This file is the continuation record for defining every governed aspect of Ecosystem Chat interactions with the same separation applied to contribution value.

Repository-wide activation remains governed by `docs/SITE_MIRROR_HANDOFF.md`. Value-specific continuation remains in `docs/ECOSYSTEM_CHAT_VALUE_MIRROR_HANDOFF.md`. Session consolidation and task claims are canonical in `docs/ECOSYSTEM_CHAT_SESSION_CONSOLIDATION.md` and `data/ecosystem-chat-session-execution-inventory.json`.

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
schemas/ecosystem-chat-governed-aspect-event.schema.json
data/ecosystem-chat-governed-aspect-events.fixture.json
data/ecosystem-chat-governed-aspect-conflicts.fixture.json
scripts/check_ecosystem_chat_governed_aspect_runtime.py
scripts/check_ecosystem_chat_value_integration.py transitive runtime validation binding
data/ecosystem-chat-session-execution-inventory.json
docs/ECOSYSTEM_CHAT_SESSION_CONSOLIDATION.md
scripts/check_ecosystem_chat_session_execution_inventory.py
scripts/write_ecosystem_chat_session_execution_receipt.py
.github/workflows/validate.yml automated inventory validation, receipt generation, artifact upload, and feature-branch receipt persistence
```

## Defined aspects

The registry defines 34 independently governed aspects:

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

## Canonical aspect-event layer

The aspect-event schema and fixtures now define:

```text
stable aspect_event_id
interaction_id
aspect_id
event_type
status and previous_status
subject_refs
actor_ref
timestamp, effective_at, expires_at
confidence and uncertainty
evidence, policy, authority, conflict, and supersession references
human and governed projections
authority_effect
hash field
```

Governed changes require evidence and policy references. `ALLOW`, `DENY`, and `QUARANTINE` effects require authority references. Conflict events cannot resolve to allow.

## Cross-aspect conflicts

Twelve required coupled conflicts are installed and deterministically evaluated:

```text
ownership verified + consent revoked + reuse allowed -> QUARANTINE
high realized value + inadmissible transition + distribution authorized -> DENY
human-only authorship + model generation evidence -> REVIEW_REQUIRED
captured record + derivation asserted -> REVIEW_REQUIRED
public projection + restricted sensitivity + no redaction -> DENY
settled + no settlement receipt -> DENY
active authority + expired delegation -> DENY
high standing + execution permission inferred -> DENY
public novelty + no comparison boundary -> REVIEW_REQUIRED
interaction-only reuse + downstream publication allowed -> DENY
revoked claim + later value advancement -> DENY
successful outcome + externalities unassessed -> REVIEW_REQUIRED
```

No conflict fixture may resolve to `ALLOW`.

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

## Validation chain

```text
scripts/check_ecosystem_chat_application.py
-> scripts/check_ecosystem_chat_value_claims.py
-> scripts/check_ecosystem_chat_value_renderer.py
-> scripts/check_ecosystem_chat_value_integration.py
   -> scripts/check_ecosystem_chat_governed_aspects.py
   -> scripts/check_ecosystem_chat_governed_aspect_runtime.py
   -> scripts/check_ecosystem_chat_session_execution_inventory.py (workflow direct step)
```

Repository automation in `.github/workflows/validate.yml` now:

```text
runs canonical application validation
validates the session execution inventory
writes evidence/ecosystem-chat/session-execution-receipt.json
uploads the receipt with the Site validation artifact
persists the receipt on feature/ecosystem-node-dual-view when the workflow succeeds
```

## Session consolidation and claims

Canonical inventory:

```text
data/ecosystem-chat-session-execution-inventory.json
```

Canonical consolidation record:

```text
docs/ECOSYSTEM_CHAT_SESSION_CONSOLIDATION.md
```

The inventory preserves the original value-lever discussion, all adjacent goals, exact owners, file locations, completion and validation states, collision boundaries, claim expiration/release conditions, blockers, cross-repository dependencies, and next executable actions.

## Verification posture

```text
Human-readable aspect model: IMPLEMENTED
Machine-readable registry: IMPLEMENTED
Registry validator: IMPLEMENTED AND TRANSITIVELY BOUND
Required aspect count: 34
Default missing-evidence posture: UNRESOLVED
Canonical aspect-event schema: IMPLEMENTED
Aspect event fixture stream: IMPLEMENTED
Cross-aspect conflict fixture set: IMPLEMENTED (12 cases)
Cross-aspect conflict validator: IMPLEMENTED AND TRANSITIVELY BOUND
Session execution inventory: IMPLEMENTED
Inventory validator: IMPLEMENTED AND WORKFLOW-BOUND
Receipt writer: IMPLEMENTED AND WORKFLOW-BOUND
Workflow execution of latest changes: NOT YET OBSERVED
Aspect renderer: NOT YET IMPLEMENTED
Gateway-origin aspect events: NOT YET IMPLEMENTED
Custody and reconstruction: NOT YET IMPLEMENTED
Authority effect: NONE
```

## Next Site work

Destination `StegVerse-Labs/Site`:

```text
Implement assets/ecosystem-chat-aspect-matrix.js.
Implement scripts/check_ecosystem_chat_aspect_matrix.py.
Render the 34-aspect matrix inside Ecosystem Node with human, governed, and split projections.
Allow selection of a message, claim, decision, artifact, or execution event to reveal attached aspect records.
Add raw JSON/JSONL aspect export without creating independent authority state.
Add role-based and locale-aware aspect disclosure.
Add deterministic browser behavior tests.
Observe the workflow run created by the latest push and inspect jobs, logs, artifacts, and generated session execution receipt.
```

## Upstream destinations

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical aspect events before rendering.
Bind aspect records to stable event_id, transition_id, claim_id, artifact_id, and execution_id values.
Sign and hash aspect events.
Evaluate cross-aspect conflicts before commit.
Emit refusal, quarantine, override, revocation, recovery, and correction events where required.
Release condition: publish a commit-pinned contract and signed sample stream accepted by Site import validation.
```

Destination `master-records/orchestration`:

```text
Custody aspect events, policies, evidence, conflicts, decisions, and receipts.
Reconstruct each aspect independently and as a coupled interaction state.
Verify that no aspect silently granted another.
Return authenticated reconstruction and disclosure receipts.
Release condition: consume the commit-pinned canonical package and return RECORDED plus reconstruction PASS receipts.
```

## Downstream destinations after verified Site activation

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

Propagation remains blocked until Site activation and authenticated custody/reconstruction receipts exist and match a hash-bound outbound manifest.

## Release posture

```text
Aspect definition layer: COMPLETE FOR INITIAL 34-ASPECT MODEL
Machine-readable registry: COMPLETE
Canonical static aspect-event and conflict layer: IMPLEMENTED
Static validation binding: COMPLETE
Session consolidation automation: INSTALLED; HOSTED EXECUTION NOT YET OBSERVED
Aspect matrix renderer: PENDING
Gateway integration: PENDING
Custody/reconstruction: PENDING
CI observation: PENDING
Deployment observation: PENDING
Release/tag readiness: NOT YET REACHED
```

## Archive posture

```text
MERGED INTO: StegVerse-Labs/Site/docs/ECOSYSTEM_CHAT_SESSION_CONSOLIDATION.md
MACHINE STATE: StegVerse-Labs/Site/data/ecosystem-chat-session-execution-inventory.json
```

This session's unique requirements are durably transferred. Archival still depends on successful inventory validation and a generated inspectable receipt proving that no task is unassigned and every unresolved dependency has an owner and release condition.
