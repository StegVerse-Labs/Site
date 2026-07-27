# TIDC Blinded Coding Adjudication Protocol

## Status

```text
posture: RESEARCH_NOTE
stage: PRE-ADJUDICATION_PROTOCOL
packet: BCP-2026-07-27-01
second_coder_type: blinded AI
human_replication: not established
authority_effect: NONE
```

## Purpose

This protocol governs what happens after a blinded coding return is received, validated, receipted, and compared with the seed coding. It prevents disagreements from being silently collapsed into the seed ledger.

## Required artifact chain

```text
issued packet
-> untouched coder return
-> structural validation
-> integrity receipt
-> descriptive comparison
-> disagreement ledger
-> source expansion where required
-> adjudication record
-> codebook revision, event revision, or retained disagreement
```

No stage may be skipped merely because the two coders agree.

## Non-negotiable boundaries

- A blinded AI second coder is not a human replication.
- Raw agreement is descriptive and is not proof of reliability.
- Agreement does not convert a weakly sourced field into a verified field.
- Disagreement does not automatically make either coder wrong.
- The seed ledger may not be silently overwritten.
- The blinded return may not be repaired, reordered, paraphrased, or normalized in place.
- Adjudication must cite the evidence used to resolve or retain each difference.

## Disagreement classes

Each field-level difference must be assigned one of these classes:

```text
DEFINITIONAL
SOURCE_INSUFFICIENCY
DATE_PROXY
AGGREGATE_EVENT
DEPENDENCY_JUDGMENT
ORIENTATION_JUDGMENT
PROBLEM_ORIGIN_JUDGMENT
CONFIDENCE_JUDGMENT
CODER_ERROR
SEED_ERROR
UNRESOLVED
```

## Allowed dispositions

```text
RETAIN_SEED
ADOPT_BLIND
RECODE_BOTH
SPLIT_EVENT
EXPAND_SOURCE_THEN_REVIEW
REVISE_CODEBOOK_THEN_RECODE
RETAIN_EXPLICIT_DISAGREEMENT
DEFER
```

Every disposition must include:

- packet ID;
- blind event ID and canonical event ID;
- disputed field;
- seed value;
- blinded value;
- disagreement class;
- evidence references;
- adjudicator rationale;
- resulting value, when applicable;
- whether the codebook changed;
- whether the historical event record changed;
- whether the public page or registry must be updated.

## Fail-closed adjudication rule

A field remains unresolved when the available evidence cannot support one value over another. Unresolved fields must not be forced into agreement for the purpose of improving reliability statistics.

```text
insufficient evidence
-> retain disagreement
-> expand sources
-> repeat review
```

## Release-gate interpretation

The first blinded AI pass may test whether the packet and codebook produce stable classifications. It cannot independently satisfy a human inter-rater reliability claim.

Release 2 may advance from `PENDING` to `ACTIVE` only when:

1. the untouched return is repository-preserved;
2. structural validation passes;
3. an integrity receipt is published;
4. all field-level agreements and disagreements are published;
5. every disagreement has an adjudication status;
6. codebook revisions are versioned rather than silently applied;
7. the public posture remains non-confirmatory.

Release 2 may be marked `COMPLETE` only after at least one additional independent coding pass under a declared replication posture. A human pass is preferred before any claim about inter-rater reliability.

## Adjudication record template

```json
{
  "schema": "stegverse.site.tidc.adjudication_record.v0.1",
  "packet_id": "BCP-2026-07-27-01",
  "blind_event_id": "BCP-E01",
  "event_id": "COMP-001",
  "field": "technology_dependency",
  "seed_value": "Necessary",
  "blind_value": "Material",
  "disagreement_class": "DEPENDENCY_JUDGMENT",
  "evidence_refs": [],
  "disposition": "EXPAND_SOURCE_THEN_REVIEW",
  "resulting_value": null,
  "rationale": "",
  "codebook_changed": false,
  "event_record_changed": false,
  "public_surface_update_required": false,
  "status": "PENDING"
}
```

## Governance boundary

```text
validation != adjudication
receipt != reliability
agreement != truth
disagreement != failure
AI second coding != human replication
Site publication != proof authority
```
