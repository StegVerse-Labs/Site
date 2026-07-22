# Reciprocal Architectural Evaluation

## Purpose

This contract defines two public test models for comparing StegVerse, TA-14, and other external frameworks without granting any participant inherited parent status.

## Test models

### Model A — neutral public test

Each participating system:

1. declares its own scope and boundary;
2. receives the same normalized input package;
3. operates under criteria published before execution;
4. emits complete machine-readable results;
5. preserves evidence, receipts, refusals, errors, uncertainty, and reconstruction material;
6. permits independent replay and inspection.

### Model B — reciprocal architectural evaluation

Each evaluator independently determines the claimed boundary, functions, dependencies, limitations, and failure conditions of every evaluated framework. Each evaluator then runs the same live test and publishes its determination and execution results on the evaluated framework's page.

No evaluator may overwrite another evaluator's determination. Disagreement is preserved as evidence.

## Required framework page projections

Every framework page MUST expose:

- framework self-declaration;
- StegVerse boundary determination;
- TA-14 boundary determination;
- determinations from any additional evaluator;
- normalized test input reference;
- live execution records;
- evidence and artifact references;
- governed records and receipts;
- replay and reconstruction status;
- disputes and unresolved differences;
- confidence and uncertainty;
- publication timestamp and content hashes.

## Evaluation invariants

```text
comparison != authority
comparison != admissibility
self-declaration != independent validation
evaluator determination != evaluated-framework consent
execution success != architectural completeness
execution failure != universal invalidity
scope overlap != parentage
historical priority != containment
private execution != public verification
page publication != custody
reconstruction PASS != execution authority
```

## Stable identifiers

All records use stable identifiers rather than text matching:

```text
evaluation_id
framework_id
evaluator_id
test_case_id
run_id
event_id
evidence_id
artifact_id
claim_id
dispute_id
receipt_id
```

## Minimum live-test sequence

```text
publish criteria
-> freeze declarations and test package
-> issue shared test_case_id
-> each evaluator maps every framework
-> each system executes the shared input
-> capture canonical event streams
-> publish results on every framework page
-> verify hashes and references
-> replay and reconstruct
-> preserve disagreements
-> issue non-authoritative comparison receipt
```

## Result classes

```text
PASS
PARTIAL
FAIL
ERROR
REFUSE
NOT_TESTED
INCONCLUSIVE
DISPUTED
```

A result MUST include the evidence basis, evaluator identity, confidence, uncertainty, and whether the value is declared, observed, derived, reconstructed, or disputed.

## Publication boundary

The Site is a public projection. It is not the proof authority, custody authority, execution authority, admissibility authority, or release authority. Canonical test records must remain exportable as JSON or JSONL and suitable for custody and reconstruction by the appropriate authoritative repositories.
