# Site Chain Status

## Assumption

This document records a Site-facing status surface for the chain path involving `master-records/core-lite` and `StegVerse-Labs/Standing-Proof-Engine`.

It does not update Site mirror activation state, Publisher closure state, or paper mirror standing.

## Done Criteria

This status surface is complete when it records source repo, verification repo, payload location, expected fixture, verification command, boundary, and next follow-up.

## Source Repo

```text
master-records/core-lite
```

## Verification Repo

```text
StegVerse-Labs/Standing-Proof-Engine
```

## Source Payload Candidate

```text
master-records/core-lite samples/spe_mapped_receipt_chain_001.json
```

## SPE-Side Fixture

```text
StegVerse-Labs/Standing-Proof-Engine samples/external_master_records_receipt_chain_001.json
```

## SPE-Side Expected Fixture

```text
StegVerse-Labs/Standing-Proof-Engine expected_results/external_master_records_receipt_chain_001.expected.json
```

## Verification Command

```bash
python -m spe.verify_expected_result expected_results/external_master_records_receipt_chain_001.expected.json
```

Expected result:

```text
SPE RESULT: PASS
CHAIN_BOUND
```

## Boundary

This page records status only. It does not claim adoption, endorsement, Site mirror activation, Publisher closure, or consequence-binding standing from Site placement.

Future live emissions from `master-records/core-lite` must be imported again and checked by SPE before public status is advanced.

## Next Follow-Up

```text
1. Observe or record workflow evidence for the relevant repositories.
2. Re-run SPE-side verification against the imported payload.
3. Update Publisher and wiki surfaces only after the verification boundary is preserved.
```
