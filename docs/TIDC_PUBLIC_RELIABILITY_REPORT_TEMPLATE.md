# TIDC Public Reliability Report — Template

```text
posture: RELIABILITY_OUTPUT_NOT_CONFIRMATION
release: TIDC_RELEASE_2_RELIABILITY
report_state: TEMPLATE_ONLY
```

## Report identity

```text
report_id:
first_pass_artifact:
independent_response_artifact:
agreement_output_artifact:
disagreement_ledger_artifact:
codebook_version:
source_packet_version:
generated_at:
```

## Boundary statement

This report evaluates whether independent coders can reproducibly classify the same historical records from the available evidence. It does not test, prove, or confirm the Technology-Induced Discovery Clustering hypothesis.

## Inputs

Describe:

- the governed first-pass snapshot;
- the independent coder response and its attestation;
- source-access limitations;
- records excluded or recommended for splitting;
- codebook version used by each pass;
- any changes made before comparison.

No comparison may be reported where the second pass was not genuinely independent.

## Coverage

```text
candidate_records:
records_coded_first_pass:
records_coded_second_pass:
records_compared:
records_excluded:
fields_compared:
```

## Agreement summary

```text
exact_agreements:
disagreements:
unresolved_disagreements:
percent_agreement:
```

Report field-level values separately. Do not collapse missing, null, and `Unresolved` values into agreement unless both coders used the same value.

## Field-level results

For each field, report:

```text
field:
comparisons:
exact_agreements:
disagreements:
percent_agreement:
interpretive_limitations:
```

## Record-level disagreements

Every disagreement must be listed or linked in machine-readable form with:

```text
record_id
field
first_pass_value
second_pass_value
resolution_status
resolution_rationale
source_locations
codebook_revision_required
```

Resolved disagreements must remain visible in the historical ledger.

## Exclusion and split recommendations

Document every recommendation to:

- exclude a record;
- split an aggregate event;
- change record class;
- downgrade coding confidence;
- retrieve additional evidence before inclusion.

## Codebook revisions

List each versioned revision triggered by the comparison. State whether it changes prior classifications and identify all affected records.

## Source limitations

Identify inaccessible, retrospective, institutional, incomplete, or proxy sources. State which conclusions cannot be reconstructed from the current source packet.

## Gate determination

```text
gate_state: BLOCKED | CONDITIONAL | COMPLETE
requirements_satisfied:
requirements_pending:
release_2_activated: false
```

Release 2 must remain blocked where the independent response, disagreement preservation, source adjudication, or versioned codebook revisions are incomplete.

## Required closing boundary

```text
coding agreement != hypothesis confirmation
reliability report != proof authority
resolved disagreement != erased disagreement
Site publication != validated historical law
```
