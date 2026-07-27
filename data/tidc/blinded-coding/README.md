# TIDC Blinded Coding Workflow

## Current state

```text
packet_id: BCP-2026-07-27-01
packet_status: ISSUED_FOR_BLINDED_SECOND_CODING
second_coder_type: blinded AI
return_received: false
comparison_ready: true
release_gate_status: WAITING_FOR_RETURN
```

This directory contains the independent second-coding packet and the governed intake surface for its return. The second coding pass is a reliability probe, not proof that the TIDC hypothesis is correct.

## Files

```text
BCP-2026-07-27-01.md
  Issued evidence-only coding packet.

blinded-coder-return.schema.json
  Machine-readable return contract.

../../../../scripts/validate_tidc_blinded_return.py
  Dependency-free, fail-closed structural validator.

../../../../scripts/compare_tidc_blinded_coding.py
  Descriptive comparison generator that preserves disagreements.
```

## Intake procedure

1. Preserve the coder's returned JSON exactly as received.
2. Store it under a new immutable path such as:

   ```text
   data/tidc/blinded-coding/returns/BCP-2026-07-27-01-return-01.json
   ```

3. Record the receiving date, coder class, model declaration if voluntarily supplied, and SHA-256 digest in a sibling receipt file.
4. Validate the untouched return:

   ```bash
   python scripts/validate_tidc_blinded_return.py \
     data/tidc/blinded-coding/returns/BCP-2026-07-27-01-return-01.json
   ```

5. Do not repair an invalid return silently. Preserve it, publish the validation failure, and request a separately versioned corrected return.
6. Generate descriptive comparison artifacts:

   ```bash
   python scripts/compare_tidc_blinded_coding.py \
     data/tidc/blinded-coding/returns/BCP-2026-07-27-01-return-01.json \
     --json-out data/tidc/blinded-coding/comparisons/BCP-2026-07-27-01-comparison-v0.1.json \
     --md-out docs/TIDC_BLINDED_CODING_COMPARISON_BCP-2026-07-27-01.md
   ```

7. Publish every disagreement and uncertainty. Do not replace the seed coding with the second coding automatically.
8. Create a separate adjudication record for any later codebook revision.

## Comparison fields

The comparison tool measures exact agreement for:

```text
technology_dependency
orientation
problem_origin_type
candidate_generation_date
verification_date
publication_date
acceptance_date
recognition_date
coding_confidence
```

Exact agreement is intentionally strict. Proxy dates, different precision, and distinct null judgments remain visible as disagreements unless a later adjudication policy explicitly defines equivalence.

## Interpretation boundary

```text
single AI second coder != human replication
raw percent agreement != validated reliability
agreement != correctness
disagreement != failure
adjudication != silent overwrite
coding reliability != hypothesis confirmation
```

Chance-corrected measures should not be added opportunistically after seeing the result. The statistic, fields, category treatment, missing-value treatment, and acceptance threshold should be specified before a confirmatory reliability claim.

## Next artifacts after return

```text
returns/BCP-2026-07-27-01-return-01.json
returns/BCP-2026-07-27-01-return-01.receipt.json
comparisons/BCP-2026-07-27-01-comparison-v0.1.json
docs/TIDC_BLINDED_CODING_COMPARISON_BCP-2026-07-27-01.md
data/tidc/blinded-coding/adjudications/BCP-2026-07-27-01-adjudication-v0.1.json
```

The adjudication artifact is created only after the untouched return and descriptive comparison have been preserved.
