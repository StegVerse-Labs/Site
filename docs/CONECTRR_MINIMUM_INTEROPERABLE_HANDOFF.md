# Conectrr Minimum Interoperable Handoff

## Purpose

This contract defines the smallest structured context that an intent-first discovery system must preserve so a downstream governance system can independently understand, evaluate, reconstruct, and build upon a recommendation without transferring consent, authority, admissibility, commitment, or execution responsibility upstream.

The target is not the largest useful record. The target is the smallest interoperable handoff.

## Architectural rule

A valid handoff must avoid both failure directions:

1. **Overreach** — the discovery layer decides or implies a later-stage governance or execution outcome.
2. **Under-specification** — the discovery layer omits enough context that a downstream system cannot reconstruct why the recommendation was made.

Both are contract failures.

## Required fields

```json
{
  "handoff_id": "stable identifier",
  "schema": "stegverse.conectrr.minimum-handoff.v0.1",
  "source": {
    "system": "Conectrr",
    "recorded_at": "RFC3339 timestamp",
    "source_record_refs": []
  },
  "intent": {
    "summary": "human-readable declared intent",
    "criteria": [],
    "constraints": []
  },
  "recommendation": {
    "summary": "recommended opportunity or next coordination target",
    "reasoning": [],
    "evidence_refs": [],
    "alternatives_considered": [],
    "confidence": null,
    "uncertainties": []
  },
  "unresolved_dependencies": [],
  "boundary": {
    "consent_established": false,
    "authority_established": false,
    "admissibility_determined": false,
    "commitment_created": false,
    "execution_authorized": false,
    "recommendation_only": true
  }
}
```

## Field minimization rule

A field belongs in the handoff only when removing it would prevent a downstream evaluator from doing at least one of the following:

- understand the declared intent;
- identify why the recommendation was surfaced;
- inspect the evidence or source references;
- identify uncertainty or unresolved dependency;
- distinguish recommendation from consent, authority, admissibility, commitment, or execution;
- independently decide what must happen next.

Fields that merely duplicate later-stage governance state do not belong in the discovery handoff.

## Downstream obligations

The downstream governance layer must determine independently:

- whether the recommendation is legible;
- whether the reasoning is reconstructable;
- whether evidence is sufficient for review;
- which dependencies remain unresolved;
- whether identity, consent, authority, policy standing, and admissibility can be established;
- whether commitment or execution must be allowed, denied, or deferred.

The downstream layer must not treat the recommendation itself as evidence that any later-stage condition has been satisfied.

## Pass conditions

A fixture passes when:

- all required fields are present;
- the record is reconstructable without private text-matching assumptions;
- every later-stage authority flag is false;
- `recommendation_only` is true;
- at least one reason or evidence reference explains why the recommendation was surfaced;
- unresolved dependencies are explicit rather than silently assumed;
- no field claims approval, consent, commitment, admissibility, or execution.

## Failure classes

```text
OVERREACH_AUTHORITY
OVERREACH_CONSENT
OVERREACH_ADMISSIBILITY
OVERREACH_COMMITMENT
OVERREACH_EXECUTION
UNDER_SPECIFIED_INTENT
UNDER_SPECIFIED_REASONING
UNDER_SPECIFIED_EVIDENCE
UNDER_SPECIFIED_UNCERTAINTY
UNRESOLVED_DEPENDENCY_HIDDEN
UNSTABLE_HANDOFF_ID
```

## Authority boundary

```text
recommendation != consent
recommendation != authority
recommendation != admissibility
recommendation != commitment
recommendation != execution
reconstructability != approval
explainability != standing
handoff completeness != downstream acceptance
```

## Production next step

Conectrr should emit this structure directly from its discovery layer. StegVerse should ingest the record, preserve the source fields unchanged, issue an independent evaluation event, and prove that the later decision can disagree with the recommendation without mutating the original handoff.
